package license

import (
	"context"
	"crypto"
	"crypto/hmac"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"encoding/pem"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/google/uuid"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

// Content defines the license data structure
type Content struct {
	ClusterID string    `json:"cluster_id"`
	Expiry    time.Time `json:"expiry"`
	Seed      string    `json:"seed"` // Used to generate the HMAC key
}

// DailyLog defines a single daily log entry
type DailyLog struct {
	Date         string `json:"date"`
	PreviousHash string `json:"previous_hash"`
	CurrentHash  string `json:"current_hash"`
}

const (
	privateKeyFile = "private.pem"
	publicKeyFile  = "public.pem"
	licenseFile    = "license.dat"
	logFile        = "license_log.dat"
)

// GenerateKeys generates public and private key files
func GenerateKeys() error {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return fmt.Errorf("failed to generate private key: %w", err)
	}

	privatePEM := pem.EncodeToMemory(&pem.Block{
		Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(privateKey),
	})
	if err := os.WriteFile(privateKeyFile, privatePEM, 0600); err != nil {
		return fmt.Errorf("failed to write private key file: %w", err)
	}

	publicPEM := pem.EncodeToMemory(&pem.Block{
		Type: "RSA PUBLIC KEY", Bytes: x509.MarshalPKCS1PublicKey(&privateKey.PublicKey),
	})
	if err := os.WriteFile(publicKeyFile, publicPEM, 0644); err != nil {
		return fmt.Errorf("failed to write public key file: %w", err)
	}

	fmt.Println("Keys generated successfully.")
	return nil
}

// GenerateLicense creates a signed license and saves it to a file
func GenerateLicense(clusterID string, expirationTime time.Time) error {
	privateKeyPEM, err := os.ReadFile(privateKeyFile)
	if err != nil {
		return fmt.Errorf("failed to read private key file: %w", err)
	}
	privateKey, err := parsePrivateKey(string(privateKeyPEM))
	if err != nil {
		return err
	}

	licenseData := Content{
		ClusterID: clusterID, Expiry: expirationTime, Seed: uuid.New().String(), // Generate a unique seed for this license
	}
	jsonData, err := json.Marshal(licenseData)
	if err != nil {
		return err
	}

	hashed := sha256.Sum256(jsonData)
	signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, hashed[:])
	if err != nil {
		return err
	}

	encodedSignature := base64.StdEncoding.EncodeToString(signature)
	encodedData := base64.StdEncoding.EncodeToString(jsonData)
	licenseString := fmt.Sprintf("%s.%s", encodedSignature, encodedData)

	if err := os.WriteFile(licenseFile, []byte(licenseString), 0644); err != nil {
		return fmt.Errorf("failed to write license file: %w", err)
	}

	fmt.Println("License generated and saved to 'license.dat'.")
	return nil
}

// VerifyLicense verifies the license validity, including the HMAC hash chain
func VerifyLicense(clusterID string) (bool, error) {
	licenseString, err := os.ReadFile(licenseFile)
	if err != nil {
		return false, fmt.Errorf("failed to read license file: %w", err)
	}
	parts := strings.Split(string(licenseString), ".")
	if len(parts) != 2 {
		return false, fmt.Errorf("invalid license format")
	}
	signature, err := base64.StdEncoding.DecodeString(parts[0])
	if err != nil {
		return false, err
	}
	jsonData, err := base64.StdEncoding.DecodeString(parts[1])
	if err != nil {
		return false, err
	}

	publicKeyPEM, err := os.ReadFile(publicKeyFile)
	if err != nil {
		return false, fmt.Errorf("failed to read public key file: %w", err)
	}
	publicKey, err := parsePublicKey(string(publicKeyPEM))
	if err != nil {
		return false, err
	}

	hashed := sha256.Sum256(jsonData)
	if err := rsa.VerifyPKCS1v15(publicKey, crypto.SHA256, hashed[:], signature); err != nil {
		return false, fmt.Errorf("signature verification failed: %w", err)
	}

	var licenseData Content
	if err := json.Unmarshal(jsonData, &licenseData); err != nil {
		return false, err
	}

	if licenseData.ClusterID != clusterID {
		return false, fmt.Errorf("cluster ID mismatch: expected %s, got %s", licenseData.ClusterID, clusterID)
	}

	if time.Now().After(licenseData.Expiry) {
		return false, fmt.Errorf("license expired")
	}

	// Verify and log the daily hash chain
	if err := verifyAndLogDaily(licenseData); err != nil {
		return false, fmt.Errorf("daily log verification failed: %w", err)
	}

	return true, nil
}

// verifyAndLogDaily verifies the HMAC hash chain and logs a new entry
func verifyAndLogDaily(licenseData Content) error {
	content, err := os.ReadFile(logFile)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	// Generate the HMAC key from the license data
	key := sha256.Sum256([]byte(licenseData.ClusterID + licenseData.Seed))

	currentDate := time.Now().Format("2006-01-02")
	var logs []DailyLog
	if len(content) > 0 {
		if err := json.Unmarshal(content, &logs); err != nil {
			return fmt.Errorf("invalid log file content: %w", err)
		}
	}

	previousHash := hex.EncodeToString(key[:])

	if len(logs) > 0 {
		lastLog := logs[len(logs)-1]

		lastDate, _ := time.Parse("2006-01-02", lastLog.Date)
		if time.Now().Before(lastDate) {
			return fmt.Errorf("system time has been tampered with")
		}

		if lastLog.Date == currentDate {
			return nil
		}

		// Verify the existing chain
		for _, logEntry := range logs {
			mac := hmac.New(sha256.New, key[:])
			mac.Write([]byte(logEntry.Date + previousHash))
			expectedHash := hex.EncodeToString(mac.Sum(nil))

			if expectedHash != logEntry.CurrentHash {
				return fmt.Errorf("hash chain integrity compromised at date: %s", logEntry.Date)
			}
			previousHash = logEntry.CurrentHash
		}

		// Append new log entry
		mac := hmac.New(sha256.New, key[:])
		mac.Write([]byte(currentDate + previousHash))
		newLog := DailyLog{
			Date: currentDate, PreviousHash: previousHash, CurrentHash: hex.EncodeToString(mac.Sum(nil)),
		}
		logs = append(logs, newLog)
	} else {
		// First log entry
		mac := hmac.New(sha256.New, key[:])
		mac.Write([]byte(currentDate + previousHash))
		logs = append(logs, DailyLog{
			Date: currentDate, PreviousHash: previousHash, CurrentHash: hex.EncodeToString(mac.Sum(nil)),
		})
	}

	newContent, err := json.MarshalIndent(logs, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal logs: %w", err)
	}
	return os.WriteFile(logFile, newContent, 0644)
}

// --- Utility functions ---
func parsePrivateKey(pemStr string) (*rsa.PrivateKey, error) {
	block, _ := pem.Decode([]byte(pemStr))
	if block == nil {
		return nil, fmt.Errorf("failed to parse PEM block containing the key")
	}
	key, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		return nil, fmt.Errorf("failed to parse DER encoded private key: %w", err)
	}
	return key, nil
}

func parsePublicKey(pemStr string) (*rsa.PublicKey, error) {
	block, _ := pem.Decode([]byte(pemStr))
	if block == nil {
		return nil, fmt.Errorf("failed to parse PEM block containing the key")
	}
	pub, err := x509.ParsePKCS1PublicKey(block.Bytes)
	if err != nil {
		return nil, err
	}
	return pub, nil
}

// GetClusterID fetches the cluster UID using client-go
func GetClusterID(ctx context.Context) (string, error) {
	config, err := rest.InClusterConfig()
	if err != nil {
		return "", fmt.Errorf("failed to create in-cluster config: %w", err)
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return "", fmt.Errorf("failed to create Kubernetes clientset: %w", err)
	}

	namespace, err := clientset.CoreV1().Namespaces().Get(ctx, "kube-system", metav1.GetOptions{})
	if err != nil {
		return "", fmt.Errorf("failed to get kube-system namespace: %w", err)
	}

	return string(namespace.ObjectMeta.UID), nil
}

//
//func main() {
//	// --- License Generation (Run this only on the license server) ---
//	fmt.Println("--- Running License Generation ---")
//	if err := GenerateKeys(); err != nil {
//		log.Fatalf("Error generating keys: %v", err)
//	}
//
//	//clusterID, err := GetClusterID(context.Background())
//	//if err != nil {
//	//	log.Fatalf("Error getting cluster ID: %v", err)
//	//}
//
//	clusterID := "3e3e6f57-2150-4d00-9f8b-7dd1c1262668"
//
//	if err := GenerateLicense(clusterID, time.Now().Add(time.Hour*24*365)); err != nil {
//		log.Fatalf("Error generating license: %v", err)
//	}
//	fmt.Println("-------------------------------------")
//
//	// --- License Verification (Run this on the customer's machine inside a Pod) ---
//	fmt.Println("--- Running License Verification ---")
//	// The program would automatically get the ClusterID here
//
//	currentClusterID := "sample-cluster-uid-12345"
//
//	// Simulate daily checks
//	for i := 0; i < 3; i++ {
//		fmt.Printf("Verifying license on day %d...\n", i+1)
//		isValid, err := VerifyLicense(currentClusterID)
//		if err != nil {
//			log.Fatalf("License validation failed: %v", err)
//		}
//		if !isValid {
//			log.Fatalf("License is invalid.")
//		}
//		fmt.Printf("License is valid.\n")
//		// Simulate time passing to trigger a new daily log entry
//		time.Sleep(1 * time.Second)
//	}
//}
