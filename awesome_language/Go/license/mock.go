package license

import (
	"crypto"
	"crypto/hmac"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"time"
)

// VerifyLicenseHour verifies the license validity, including the HMAC hash chain
func VerifyLicenseHour(clusterID string) (bool, error) {
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
	if err := verifyAndLogHourly(licenseData); err != nil {
		return false, fmt.Errorf("log verification failed: %w", err)
	}
	return true, nil
}

// verifyAndLogHourly verifies the HMAC hash chain and logs a new entry, based on minutes
func verifyAndLogHourly(licenseData Content) error {
	content, err := os.ReadFile(logFile)
	if err != nil && !os.IsNotExist(err) {
		return err
	}

	key := sha256.Sum256([]byte(licenseData.ClusterID + licenseData.Seed))
	// 修改为分钟格式
	currentDate := time.Now().Format("2006-01-02 15:04")
	var logs []DailyLog
	if len(content) > 0 {
		if err := json.Unmarshal(content, &logs); err != nil {
			return fmt.Errorf("invalid log file content: %w", err)
		}
	}
	previousHash := hex.EncodeToString(key[:])
	if len(logs) > 0 {
		lastLog := logs[len(logs)-1]
		lastDate, _ := time.Parse("2006-01-02 15:04", lastLog.Date)
		if time.Now().Before(lastDate) {
			return fmt.Errorf("system time has been tampered with")
		}
		if lastLog.Date == currentDate {
			return nil
		}
		for _, logEntry := range logs {
			mac := hmac.New(sha256.New, key[:])
			mac.Write([]byte(logEntry.Date + previousHash))
			expectedHash := hex.EncodeToString(mac.Sum(nil))
			if expectedHash != logEntry.CurrentHash {
				return fmt.Errorf("hash chain integrity compromised at date: %s", logEntry.Date)
			}
			previousHash = logEntry.CurrentHash
		}
		mac := hmac.New(sha256.New, key[:])
		mac.Write([]byte(currentDate + previousHash))
		newLog := DailyLog{
			Date:         currentDate,
			PreviousHash: previousHash,
			CurrentHash:  hex.EncodeToString(mac.Sum(nil)),
		}
		logs = append(logs, newLog)
	} else {
		mac := hmac.New(sha256.New, key[:])
		mac.Write([]byte(currentDate + previousHash))
		logs = append(logs, DailyLog{
			Date:         currentDate,
			PreviousHash: previousHash,
			CurrentHash:  hex.EncodeToString(mac.Sum(nil)),
		})
	}
	newContent, err := json.MarshalIndent(logs, "", "  ")
	if err != nil {
		return fmt.Errorf("failed to marshal logs: %w", err)
	}
	return os.WriteFile(logFile, newContent, 0644)
}
