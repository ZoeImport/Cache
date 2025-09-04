package license

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"testing"
	"time"
)

func TestGenerateMachineLicense(t *testing.T) {
	fmt.Println("--- Generating Keys and License ---")
	if err := GenerateKeys(); err != nil {
		fmt.Println("Error generating keys:", err)
		return
	}

	machineID, err := GetClusterID(context.Background())
	if err != nil {
		fmt.Println("Error getting machine ID:", err)
		return
	}
	fmt.Println("Current Machine ID:", machineID)

	if err := GenerateLicense(machineID, time.Now().Add(time.Hour*24*365)); err != nil { // 1年有效期
		fmt.Println("Error generating license:", err)
		return
	}

	// ----------------------------------------------------
}

func TestVerifyLicense(t *testing.T) {
	// 在客户部署环境，只需运行 VerifyLicense：
	fmt.Println("\n--- Verifying License for the first time ---")
	clusterID, err2 := GetClusterID(context.Background())
	if err2 != nil {
		t.Fatal(err2)
	}
	valid, err := VerifyLicense(clusterID)
	if err != nil {
		fmt.Println("License validation failed:", err)
	} else {
		fmt.Println("License is valid:", valid)
	}

	// 模拟第二天运行，进行每日打卡校验
	fmt.Println("\n--- Simulating verification on a new day ---")
	time.Sleep(2 * time.Second) // 模拟时间流逝
	valid, err = VerifyLicense(clusterID)
	if err != nil {
		fmt.Println("License validation failed:", err)
	} else {
		fmt.Println("License is valid:", valid)
	}
}

func TestGenerateClusterLicense(t *testing.T) {
	fmt.Println("--- Generating Keys and License ---")
	if err := GenerateKeys(); err != nil {
		fmt.Println("Error generating keys:", err)
		return
	}

	clusterID, err := GetClusterID(context.Background())
	if err != nil {
		fmt.Println("Error getting machine ID:", err)
		return
	}
	fmt.Println("Current Cluster ID:", clusterID)

	if err := GenerateLicense(clusterID, time.Now().Add(time.Hour*24*7)); err != nil { // 1年有效期
		fmt.Println("Error generating license:", err)
		return
	}

	// ----------------------------------------------------
}

func TestMockHashChain(t *testing.T) {
	log.SetFlags(log.Lshortfile | log.LstdFlags)
	os.Remove(logFile) // 每次运行前清空日志文件
	if err := GenerateKeys(); err != nil {
		log.Fatalf("Error generating keys: %v", err)
	}
	clusterID := "sample-cluster-uid-12345"
	if err := GenerateLicense(clusterID, time.Now().Add(time.Hour*24*365)); err != nil {
		log.Fatalf("Error generating license: %v", err)
	}

	// --- 模拟正常打卡 3 次 ---
	for i := 0; i < 3; i++ {
		fmt.Printf("Verifying license on minute %d...\n", i+1)
		_, err := VerifyLicenseHour(clusterID)
		if err != nil {
			log.Fatalf("License validation failed: %v", err)
		}
		fmt.Printf("License is valid.\n")
		time.Sleep(1 * time.Minute) // 模拟时间流逝
	}

	// --- 尝试篡改第 2 条记录 ---
	fmt.Println("\n--- 开始篡改日志文件 ---")
	logContent, _ := os.ReadFile(logFile)
	var logs []DailyLog
	json.Unmarshal(logContent, &logs)
	logs[1].Date = "2025-08-25 15:00" // 篡改日期
	newContent, _ := json.MarshalIndent(logs, "", "  ")
	os.WriteFile(logFile, newContent, 0644)
	fmt.Println("日志文件已被篡改！")

	// --- 再次校验，哈希链应被破坏 ---
	fmt.Println("\n--- 再次验证许可证，预期失败 ---")
	_, err := VerifyLicenseHour(clusterID)
	if err != nil {
		fmt.Printf("许可证验证失败，错误信息为：%v\n", err)
	}
}
