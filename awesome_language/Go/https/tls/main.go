package tls

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"fmt"
	"io"
	"log"
	"math/big"
	"net/http"
	"time"
)

// genCertAndKey 生成证书和私钥，并返回 PEM 格式数据
func genCertAndKey(isCA bool, commonName string, parentCert *x509.Certificate, parentKey *rsa.PrivateKey) ([]byte, []byte, error) {
	// 1. 生成 RSA 私钥
	key, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		return nil, nil, fmt.Errorf("生成私钥失败: %v", err)
	}

	// 2. 创建证书模板
	template := x509.Certificate{
		SerialNumber: big.NewInt(time.Now().Unix()),
		Subject: pkix.Name{
			CommonName: commonName,
		},
		NotBefore:             time.Now(),
		NotAfter:              time.Now().Add(365 * 24 * time.Hour), // 有效期一年
		KeyUsage:              x509.KeyUsageDigitalSignature | x509.KeyUsageKeyEncipherment,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth, x509.ExtKeyUsageClientAuth},
		BasicConstraintsValid: true,
	}

	if isCA {
		template.IsCA = true
		template.KeyUsage |= x509.KeyUsageCertSign
	} else {
		//为非 CA 证书添加 SAN 字段
		template.DNSNames = []string{commonName}
	}

	// 3. 签名证书
	var certBytes []byte
	if isCA {
		// 自签名
		certBytes, err = x509.CreateCertificate(rand.Reader, &template, &template, &key.PublicKey, key)
	} else {
		// 由父级 CA 签名
		certBytes, err = x509.CreateCertificate(rand.Reader, &template, parentCert, &key.PublicKey, parentKey)
	}
	if err != nil {
		return nil, nil, fmt.Errorf("创建证书失败: %v", err)
	}

	// 4. 将证书和私钥编码为 PEM 格式
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certBytes})
	keyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(key)})

	return certPEM, keyPEM, nil
}

func HttpTls() {
	// 1. 生成 CA 证书和私钥
	caCertPEM, caKeyPEM, err := genCertAndKey(true, "MyCA", nil, nil)
	if err != nil {
		log.Fatalf("生成 CA 证书失败: %v", err)
	}

	// 2. 生成服务端证书和私钥（由 CA 签名）
	//parse from caCertPEM, caKeyPEM
	caCert, _ := pem.Decode(caCertPEM)
	caCertificate, _ := x509.ParseCertificate(caCert.Bytes)
	caKey, _ := pem.Decode(caKeyPEM)
	caPrivateKey, _ := x509.ParsePKCS1PrivateKey(caKey.Bytes)

	//sign it for server cert/priKey
	serverCertPEM, serverKeyPEM, err := genCertAndKey(false, "localhost", caCertificate, caPrivateKey)
	if err != nil {
		log.Fatalf("生成服务端证书失败: %v", err)
	}

	// 3. 生成客户端证书和私钥（由 CA 签名）
	clientCertPEM, clientKeyPEM, err := genCertAndKey(false, "client", caCertificate, caPrivateKey)
	if err != nil {
		log.Fatalf("生成客户端证书失败: %v", err)
	}

	log.Println("所有证书和私钥已生成。")

	// 4. 配置并启动服务端
	go func() {
		defer func() {
			if err := recover(); err != nil {
				log.Fatalf("recover: %v", err)
			}
		}()
		// 从 PEM 数据解析证书和私钥
		cert, err := tls.X509KeyPair(serverCertPEM, serverKeyPEM)
		if err != nil {
			log.Fatalf("服务端证书解析失败: %v", err)
		}

		// 创建一个证书池，包含 CA 根证书
		clientCertPool := x509.NewCertPool()
		clientCertPool.AppendCertsFromPEM(caCertPEM)

		// 配置 TLS，要求客户端提供证书，并由 CA 验证
		server := &http.Server{
			Addr: ":8443",
			TLSConfig: &tls.Config{
				Certificates: []tls.Certificate{cert},
				ClientCAs:    clientCertPool,
				ClientAuth:   tls.RequireAndVerifyClientCert,
			},
			Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				fmt.Fprintln(w, "Hello, secure world!")
			}),
		}

		log.Println("服务端启动，监听 :8443...")
		if err := server.ListenAndServeTLS("", ""); err != nil {
			log.Fatalf("服务端启动失败: %v", err)
		}
	}()

	// 5. 配置并启动客户端，稍后发起请求
	time.Sleep(1 * time.Second) // 等待服务端启动

	// 从 PEM 数据解析客户端证书和私钥
	clientCert, err := tls.X509KeyPair(clientCertPEM, clientKeyPEM)
	if err != nil {
		log.Fatalf("客户端证书解析失败: %v", err)
	}

	// 创建一个证书池，包含 CA 根证书
	serverCertPool := x509.NewCertPool()
	serverCertPool.AppendCertsFromPEM(caCertPEM)

	// 配置 TLS，信任 CA 证书，并提供客户端自己的证书
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{clientCert},
		RootCAs:      serverCertPool,
	}

	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
		},
	}

	log.Println("客户端发起请求...")
	resp, err := client.Get("https://localhost:8443")
	if err != nil {
		log.Fatalf("客户端请求失败: %v", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("读取响应失败: %v", err)
	}

	log.Printf("响应状态码: %d\n", resp.StatusCode)
	log.Printf("响应内容: %s\n", body)
}

// loadTLSCredentialsFromPEM 封装了从 PEM 数据加载证书和 TLS 配置的逻辑
func loadTLSCredentialsFromPEM(certPEM, keyPEM, caCertPEM []byte) (*tls.Config, *tls.Config, error) {
	// 1. 加载本服务的证书和私钥
	cert, err := tls.X509KeyPair(certPEM, keyPEM)
	if err != nil {
		return nil, nil, fmt.Errorf("无法加载证书密钥对: %v", err)
	}

	// 2. 加载 CA 根证书，用于验证对方身份
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCertPEM); !ok {
		return nil, nil, fmt.Errorf("无法将 CA 证书添加到证书池")
	}

	// 3. 构建服务端的 tls.Config
	serverTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caCertPool,
		ClientAuth:   tls.RequireAndVerifyClientCert,
	}

	// 4. 构建客户端的 tls.Config
	clientTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}

	return serverTLSConfig, clientTLSConfig, nil
}

// startServer 启动一个服务端
func startServer(serverName, listenAddr string, serverTLSConfig *tls.Config) {
	server := &http.Server{
		Addr:      listenAddr,
		TLSConfig: serverTLSConfig,
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			fmt.Fprintf(w, "Hello from %s!", serverName)
			log.Printf("来自 %s 的请求已处理", serverName)
		}),
	}

	log.Printf("%s 正在监听 %s...", serverName, listenAddr)
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("无法启动 %s: %v", serverName, err)
	}
}

// makeRequest 发起一个客户端请求
func makeRequest(clientName, url string, clientTLSConfig *tls.Config) {
	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: clientTLSConfig,
		},
	}

	log.Printf("%s 正在向 %s 发起请求...", clientName, url)
	resp, err := client.Get(url)
	if err != nil {
		log.Printf("❌ %s 请求失败: %v", clientName, err)
		return
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	log.Printf("✅ %s 收到来自 %s 的响应: %s", clientName, url, body)
}

func MutiTls() {
	// 1. 动态生成 CA 证书
	caCertPEM, caKeyPEM, err := genCertAndKey(true, "MyCA", nil, nil)
	if err != nil {
		log.Fatalf("无法生成 CA 证书: %v", err)
	}
	caCert, _ := pem.Decode(caCertPEM)
	caCertificate, _ := x509.ParseCertificate(caCert.Bytes)
	caKey, _ := pem.Decode(caKeyPEM)
	caPrivateKey, _ := x509.ParsePKCS1PrivateKey(caKey.Bytes)

	// 2. 动态生成 Service-A 的证书
	serviceACertPEM, serviceAKeyPEM, err := genCertAndKey(false, "service-a", caCertificate, caPrivateKey)
	if err != nil {
		log.Fatalf("无法生成 Service-A 证书: %v", err)
	}

	// 3. 动态生成 Service-B 的证书
	serviceBCertPEM, serviceBKeyPEM, err := genCertAndKey(false, "service-b", caCertificate, caPrivateKey)
	if err != nil {
		log.Fatalf("无法生成 Service-B 证书: %v", err)
	}
	log.Println("所有证书和私钥已在内存中动态生成。")

	// 4. 加载 Service-A 的证书配置
	serviceAServerTlsConfig, serviceAClientTLSConfig, err := loadTLSCredentialsFromPEM(serviceACertPEM, serviceAKeyPEM, caCertPEM)
	if err != nil {
		log.Fatalf("无法加载 Service-A 证书配置: %v", err)
	}

	// 5. 加载 Service-B 的证书配置
	serviceBServerTLSConfig, serviceBClientTLSConfig, err := loadTLSCredentialsFromPEM(serviceBCertPEM, serviceBKeyPEM, caCertPEM)
	if err != nil {
		log.Fatalf("无法加载 Service-B 证书配置: %v", err)
	}
	log.Println("TLS 配置已加载。")

	// 6. 启动 Service-A 和 Service-B
	go startServer("Service-A", ":8001", serviceAServerTlsConfig)
	go startServer("Service-B", ":8002", serviceBServerTLSConfig)

	// 延时等待服务启动
	time.Sleep(2 * time.Second)

	// 7. 模拟 Service-A 调用 Service-B
	makeRequest("Service-A", "https://localhost:8002", serviceAClientTLSConfig)

	// 8. 模拟 Service-B 调用 Service-A
	makeRequest("Service-B", "https://localhost:8001", serviceBClientTLSConfig)

	// 阻止主 goroutine 退出
	select {}
}
