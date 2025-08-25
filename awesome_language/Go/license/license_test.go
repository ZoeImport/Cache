package main

import (
	"context"
	"fmt"
	"testing"
	"time"
)

func TestGenerateMachineLicense(t *testing.T) {
	// 在开发/生成环境：
	fmt.Println("--- Generating Keys and License ---")
	if err := GenerateKeys(); err != nil {
		fmt.Println("Error generating keys:", err)
		return
	}

	machineID, err := getMachineIDInLinux()
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

func TestGenerateClusterLicense(t *testing.T) {
	// 在开发/生成环境：
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

	if err := GenerateLicense(clusterID, time.Now().Add(time.Hour*24*365)); err != nil { // 1年有效期
		fmt.Println("Error generating license:", err)
		return
	}

	// ----------------------------------------------------
}
