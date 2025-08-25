package main

import (
	"context"
	"crypto"
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
	"os/exec"
	"strings"
	"time"

	"github.com/google/uuid"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

// LicenseContent 定义License数据结构
type LicenseContent struct {
	MachineID string    `json:"machine_id"`
	Expiry    time.Time `json:"expiry"`
	UUID      string    `json:"uuid"` // 用于哈希链的唯一ID
}

// DailyLog 定义每日打卡记录
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

// GetClusterID 使用 client-go 库获取集群的唯一 UID
func GetClusterID(ctx context.Context) (string, error) {
	// 创建一个 in-cluster 配置，它会自动使用 Pod 挂载的 Service Account Token
	config, err := rest.InClusterConfig()
	if err != nil {
		return "", fmt.Errorf("failed to create in-cluster config: %w", err)
	}

	// 创建客户端集
	clientSet, err := kubernetes.NewForConfig(config)
	if err != nil {
		return "", fmt.Errorf("failed to create Kubernetes clientSet: %w", err)
	}

	// 使用 clientSet 获取 kube-system 命名空间
	namespace, err := clientSet.CoreV1().Namespaces().Get(ctx, "kube-system", metav1.GetOptions{})
	if err != nil {
		return "", fmt.Errorf("failed to get kube-system namespace: %w", err)
	}

	// 返回命名空间的 UID
	return string(namespace.ObjectMeta.UID), nil
}

// GenerateKeys 生成公私钥文件
func GenerateKeys() error {
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return fmt.Errorf("failed to generate private key: %w", err)
	}

	// 保存私钥
	privatePEM := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(privateKey),
	})
	if err := os.WriteFile(privateKeyFile, privatePEM, 0600); err != nil {
		return fmt.Errorf("failed to write private key file: %w", err)
	}

	// 保存公钥
	publicPEM := pem.EncodeToMemory(&pem.Block{
		Type:  "RSA PUBLIC KEY",
		Bytes: x509.MarshalPKCS1PublicKey(&privateKey.PublicKey),
	})
	if err := os.WriteFile(publicKeyFile, publicPEM, 0644); err != nil {
		return fmt.Errorf("failed to write public key file: %w", err)
	}

	fmt.Println("Keys generated successfully.")
	return nil
}

// GenerateLicense 根据机器唯一标识生成加密的License并保存到文件
func GenerateLicense(machineID string, expirationTime time.Time) error {
	privateKeyPEM, err := os.ReadFile(privateKeyFile)
	if err != nil {
		return fmt.Errorf("failed to read private key file: %w", err)
	}
	privateKey, err := parsePrivateKey(string(privateKeyPEM))
	if err != nil {
		return err
	}

	licenseData := LicenseContent{
		MachineID: machineID,
		Expiry:    expirationTime,
		UUID:      uuid.New().String(),
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

// VerifyLicense 校验License的有效性
func VerifyLicense() (bool, error) {
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

	var licenseData LicenseContent
	if err := json.Unmarshal(jsonData, &licenseData); err != nil {
		return false, err
	}

	currentMachineID, err := getMachineIDInLinux()
	if err != nil {
		return false, fmt.Errorf("failed to get current machine id: %w", err)
	}

	if licenseData.MachineID != currentMachineID {
		return false, fmt.Errorf("machine ID mismatch: expected %s, got %s", licenseData.MachineID, currentMachineID)
	}

	if time.Now().After(licenseData.Expiry) {
		return false, fmt.Errorf("license expired")
	}

	if err := verifyAndLogDaily(licenseData.UUID); err != nil {
		return false, fmt.Errorf("daily log verification failed: %w", err)
	}

	return true, nil
}

// verifyAndLogDaily 每日哈希链验证和记录
func verifyAndLogDaily(licenseUUID string) error {
	content, err := os.ReadFile(logFile)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	currentDate := time.Now().Format("2006-01-02")
	var logs []DailyLog
	if len(content) > 0 {
		if err := json.Unmarshal(content, &logs); err != nil {
			return fmt.Errorf("invalid log file content: %w", err)
		}
	}

	if len(logs) > 0 {
		lastLog := logs[len(logs)-1]

		lastDate, _ := time.Parse("2006-01-02", lastLog.Date)
		if time.Now().Before(lastDate) {
			return fmt.Errorf("system time has been tampered with")
		}

		if lastLog.Date == currentDate {
			return nil
		}

		previousHash := licenseUUID
		for _, log := range logs {
			expectedHash := sha256.Sum256([]byte(log.Date + previousHash))
			if hex.EncodeToString(expectedHash[:]) != log.CurrentHash {
				return fmt.Errorf("hash chain integrity compromised at date: %s", log.Date)
			}
			previousHash = log.CurrentHash
		}

		sum256 := sha256.Sum256([]byte(currentDate + previousHash))
		newLog := DailyLog{
			Date:         currentDate,
			PreviousHash: previousHash,
			CurrentHash:  hex.EncodeToString(sum256[:]),
		}
		logs = append(logs, newLog)
	} else {
		firstHash := sha256.Sum256([]byte(currentDate + licenseUUID))
		logs = append(logs, DailyLog{
			Date:         currentDate,
			PreviousHash: licenseUUID,
			CurrentHash:  hex.EncodeToString(firstHash[:]),
		})
	}

	newContent, _ := json.MarshalIndent(logs, "", "  ")
	return os.WriteFile(logFile, newContent, 0644)
}

// parsePrivateKey 从 PEM 格式解析私钥
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

// parsePublicKey 从 PEM 格式解析公钥
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

// getMachineIDInLinux 使用 dmidecode 获取 CPU 和主板序列号
func getMachineIDInLinux() (string, error) {
	cmd := exec.Command("sudo", "dmidecode", "-t", "processor")
	out, err := cmd.Output()
	if err != nil {
		return "", fmt.Errorf("failed to run dmidecode -t processor: %w", err)
	}
	cpuID := parseDmiOutput(string(out), "ID:")
	cmd = exec.Command("sudo", "dmidecode", "-t", "baseboard")
	out, err = cmd.Output()
	if err != nil {
		return "", fmt.Errorf("failed to run dmidecode -t baseboard: %w", err)
	}
	boardID := parseDmiOutput(string(out), "Serial Number:")

	if cpuID == "" || boardID == "" {
		return "", fmt.Errorf("failed to extract hardware IDs from dmidecode output")
	}

	return fmt.Sprintf("%s-%s", cpuID, boardID), nil
}

// parseDmiOutput 解析 dmidecode 的输出，提取指定关键词后的值
func parseDmiOutput(output, key string) string {
	lines := strings.Split(output, "\n")
	for _, line := range lines {
		if strings.Contains(line, key) {
			value := strings.TrimSpace(strings.Split(line, key)[1])
			return strings.ReplaceAll(value, " ", "")
		}
	}
	return ""
}

func main() {
	// 在客户部署环境，只需运行 VerifyLicense：
	fmt.Println("\n--- Verifying License for the first time ---")
	valid, err := VerifyLicense()
	if err != nil {
		fmt.Println("License validation failed:", err)
	} else {
		fmt.Println("License is valid:", valid)
	}

	// 模拟第二天运行，进行每日打卡校验
	fmt.Println("\n--- Simulating verification on a new day ---")
	time.Sleep(2 * time.Second) // 模拟时间流逝
	valid, err = VerifyLicense()
	if err != nil {
		fmt.Println("License validation failed:", err)
	} else {
		fmt.Println("License is valid:", valid)
	}
}
