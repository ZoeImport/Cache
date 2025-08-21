package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"fmt"
	"log"
	"math/big"
	"os"
	"time"
)

// -------------------- 1. 生成 CA 根证书 --------------------
func generateCA() (*rsa.PrivateKey, *x509.Certificate) {
	// 生成 CA 的 RSA 私钥
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		log.Fatalf("无法生成 CA 私钥: %v", err)
	}

	// 定义 CA 证书模板
	template := x509.Certificate{
		SerialNumber: big.NewInt(1),
		Subject: pkix.Name{
			Organization: []string{"My Company CA"},
			CommonName:   "My Company Root CA",
		},
		NotBefore:             time.Now(),
		NotAfter:              time.Now().Add(365 * 24 * time.Hour), // 证书有效期一年
		KeyUsage:              x509.KeyUsageCertSign | x509.KeyUsageCRLSign,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
		IsCA:                  true, // 标记为 CA 证书
	}

	// 使用私钥自签名，生成根证书
	derBytes, err := x509.CreateCertificate(rand.Reader, &template, &template, &privateKey.PublicKey, privateKey)
	if err != nil {
		log.Fatalf("无法创建 CA 证书: %v", err)
	}

	cert, err := x509.ParseCertificate(derBytes)
	if err != nil {
		log.Fatalf("无法解析 CA 证书: %v", err)
	}

	fmt.Println("成功生成 CA 根证书。")
	return privateKey, cert
}

// -------------------- 2. 生成服务器证书 --------------------
func generateServerCert(caKey *rsa.PrivateKey, caCert *x509.Certificate) (*rsa.PrivateKey, *x509.Certificate) {
	// 服务器生成自己的私钥
	privateKey, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		log.Fatalf("无法生成服务器私钥: %v", err)
	}

	// 定义服务器证书模板
	template := x509.Certificate{
		SerialNumber: big.NewInt(2),
		Subject: pkix.Name{
			Organization: []string{"My Company"},
			CommonName:   "localhost", // 服务器域名
		},
		NotBefore:   time.Now(),
		NotAfter:    time.Now().Add(30 * 24 * time.Hour), // 证书有效期一个月
		KeyUsage:    x509.KeyUsageDigitalSignature | x509.KeyUsageKeyEncipherment,
		ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		DNSNames:    []string{"localhost"},
	}

	// 使用 CA 的私钥为服务器证书签名
	derBytes, err := x509.CreateCertificate(rand.Reader, &template, caCert, &privateKey.PublicKey, caKey)
	if err != nil {
		log.Fatalf("无法创建服务器证书: %v", err)
	}

	cert, err := x509.ParseCertificate(derBytes)
	if err != nil {
		log.Fatalf("无法解析服务器证书: %v", err)
	}

	fmt.Println("成功生成服务器证书，由 CA 签名。")
	return privateKey, cert
}

// -------------------- 3. 客户端验证证书 --------------------
func verifyCert(caCert *x509.Certificate, serverCert *x509.Certificate) {
	// 创建证书池，将 CA 根证书加入其中
	certPool := x509.NewCertPool()
	certPool.AddCert(caCert)

	// 验证服务器证书
	opts := x509.VerifyOptions{
		Roots:         certPool,
		Intermediates: x509.NewCertPool(),
	}

	_, err := serverCert.Verify(opts)
	if err != nil {
		fmt.Printf("❌ 证书验证失败: %v\n", err)
		return
	}

	fmt.Println("✅ 证书验证成功！服务器证书由受信任的 CA 签发。")
}

// -------------------- 辅助函数：将证书和私钥保存到文件 --------------------
func saveToFile(filename string, pemType string, data []byte) {
	file, err := os.Create(filename)
	if err != nil {
		log.Fatalf("无法创建文件 %s: %v", filename, err)
	}
	defer file.Close()
	err = pem.Encode(file, &pem.Block{Type: pemType, Bytes: data})
	if err != nil {
		log.Fatalf("无法写入 PEM 数据: %v", err)
	}
	fmt.Printf("证书/私钥已保存到 %s\n", filename)
}

func main() {
	// 1. CA 自我签发根证书
	caKey, caCert := generateCA()
	caCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: caCert.Raw})
	caKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(caKey)})
	saveToFile("ca.crt", "CERTIFICATE", caCertPEM)
	saveToFile("ca.key", "RSA PRIVATE KEY", caKeyPEM)

	// 2. 服务器生成证书请求并由 CA 签发
	serverKey, serverCert := generateServerCert(caKey, caCert)
	serverCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: serverCert.Raw})
	serverKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(serverKey)})
	saveToFile("server.crt", "CERTIFICATE", serverCertPEM)
	saveToFile("server.key", "RSA PRIVATE KEY", serverKeyPEM)

	// 3. 客户端验证服务器证书
	fmt.Println("\n--- 客户端验证服务器证书 ---")
	verifyCert(caCert, serverCert)

	// 模拟一个伪造的证书，看是否能通过验证
	fmt.Println("\n--- 模拟伪造证书 ---")
	forgedCAKey, _ := rsa.GenerateKey(rand.Reader, 2048)
	_, forgedServerCert := generateServerCert(forgedCAKey, caCert) // 使用错误的私钥签名
	verifyCert(caCert, forgedServerCert)
}
