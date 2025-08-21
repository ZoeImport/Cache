package main

import (
	"crypto/tls"
	"crypto/x509"
	_ "embed"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"

	"C"
)

//go:embed certs/ca.crt
var caCert []byte

//go:embed certs/go-server.crt
var clientCert []byte

//go:embed certs/go-server.key
var clientKey []byte

// export MakeSecureRequest 是提供给 Python 调用的函数
//
//export MakeSecureRequest
func MakeSecureRequest(url *C.char) *C.char {
	// 1. 从嵌入数据中加载证书和密钥
	cert, err := tls.X509KeyPair(clientCert, clientKey)
	if err != nil {
		return C.CString(fmt.Sprintf("Failed to load client cert: %v", err))
	}

	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		return C.CString("Failed to append CA cert")
	}

	// 2. 配置 TLS 客户端
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}

	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
		},
	}

	// 3. 发起安全的 HTTPS 请求
	resp, err := client.Get(C.GoString(url))
	if err != nil {
		return C.CString(fmt.Sprintf("Request failed: %v", err))
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return C.CString("Failed to read response body")
	}

	return C.CString(string(body))
}

// ... (将 go_client_lib/client_lib.go 中的所有代码复制到这里，包括 MakeSecureRequest 函数)

// 导入动态库
// 这是一个 Go 程序，但为了调用 CGO 封装的函数，我们需要加载库
// extern void MakeSecureRequest(char*);

// 导入动态库，这里假设在 main 函数中通过 ctypes 直接调用，而非在 Go 内部调用
// 因此，这里不需要额外的 Cgo 导入，直接在 main 函数中运行即可

// startGoServer 启动 Go 服务端
func startGoServer(caCertPath, serverCertPath, serverKeyPath string, listenAddr string) {
	// 1. 加载服务器的证书和私钥
	cert, err := tls.LoadX509KeyPair(serverCertPath, serverKeyPath)
	if err != nil {
		log.Fatalf("Failed to load server key pair: %v", err)
	}

	// 2. 加载 CA 证书，用于验证客户端
	caCert, err := os.ReadFile(caCertPath)
	if err != nil {
		log.Fatalf("Failed to read CA cert: %v", err)
	}
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		log.Fatalf("Failed to append CA cert")
	}

	// 3. 配置 TLS 服务端
	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caCertPool,
		ClientAuth:   tls.RequireAndVerifyClientCert,
	}

	server := &http.Server{
		Addr:      listenAddr,
		TLSConfig: tlsConfig,
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			log.Println("Go service received a request from Python service.")
			io.WriteString(w, "Hello from Go service!")
		}),
	}

	log.Printf("Go service listening on %s...", listenAddr)
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("Failed to start Go server: %v", err)
	}
}

// clientRequestToPython 使用 Go 内部客户端向 Python 服务发起请求
func clientRequestToPython() {
	// 假设 Python 服务在 8001 端口
	url := "https://localhost:8001"

	// 从 go_client_lib/client_lib.go 获取 MakeSecureRequest 的逻辑
	// 为了简化，我们直接在这里重新实现客户端逻辑，而不是调用动态库
	// 实际项目中，此部分会由 Python 通过 ctypes 调用

	// 加载客户端证书和私钥
	clientCert, err := tls.LoadX509KeyPair("certs/go-server.crt", "certs/go-server.key")
	if err != nil {
		log.Fatalf("Failed to load client cert: %v", err)
	}

	// 加载 CA 证书
	caCert, err := os.ReadFile("certs/ca.crt")
	if err != nil {
		log.Fatalf("Failed to read CA cert: %v", err)
	}
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		log.Fatalf("Failed to append CA cert")
	}

	tlsConfig := &tls.Config{
		Certificates: []tls.Certificate{clientCert},
		RootCAs:      caCertPool,
	}

	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
		},
	}

	log.Printf("Go service making a request to Python service...")
	resp, err := client.Get(url)
	if err != nil {
		log.Fatalf("Request to Python service failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	log.Printf("Go service received response from Python: %s", body)
}

// This function handles loading the TLS credentials for both client and server roles.
func loadTLSCredentials(caCertPath, serviceCertPath, serviceKeyPath string) (*tls.Config, *tls.Config, error) {
	// 1. Load the service's certificate and key.
	cert, err := tls.LoadX509KeyPair(serviceCertPath, serviceKeyPath)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to load key pair: %v", err)
	}

	// 2. Load the CA certificate to trust others.
	caCert, err := os.ReadFile(caCertPath)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to read CA certificate: %v", err)
	}
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		return nil, nil, fmt.Errorf("failed to append CA certificate to pool")
	}

	// 3. Create the TLS config for the server role.
	serverTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		//ClientCAs:    caCertPool,
		//ClientAuth:   tls.RequireAndVerifyClientCert,
	}

	// 4. Create the TLS config for the client role.
	clientTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}

	return serverTLSConfig, clientTLSConfig, nil
}

var ch chan struct{}

// startServer launches the service in server mode.
func startServer(serviceName, listenAddr string, tlsConfig *tls.Config) {
	server := &http.Server{
		Addr:      listenAddr,
		TLSConfig: tlsConfig,
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			log.Printf("%s server: Received a request from client.", serviceName)
			io.WriteString(w, "Hello from the Go server!")
			ch <- struct{}{}
		}),
	}

	log.Printf("Starting %s server on %s...", serviceName, listenAddr)
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("Failed to start %s server: %v", serviceName, err)
	}
}

// makeRequest acts as the service's client, making an outbound request.
func makeRequest(clientName, targetURL string, tlsConfig *tls.Config) {
	client := &http.Client{
		Transport: &http.Transport{
			TLSClientConfig: tlsConfig,
		},
	}

	log.Printf("%s client: Making a request to %s...", clientName, targetURL)
	resp, err := client.Get(targetURL)
	if err != nil {
		log.Fatalf("❌ %s client: Request failed: %v", clientName, err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("❌ %s client: Failed to read response body: %v", clientName, err)
	}
	log.Printf("✅ %s client: Received response from %s: %s", clientName, targetURL, body)
}

func main() {
	ch = make(chan struct{}, 1)
	// Configure and start the Go service as a server.
	goServerTLSConfig, goClientTLSConfig, err := loadTLSCredentials(
		"certs/ca.crt",
		"certs/go-server.crt",
		"certs/go-server.key",
	)
	if err != nil {
		log.Fatalf("Failed to load Go service TLS credentials: %v", err)
	}
	go startServer("Go Service", ":8000", goServerTLSConfig)

	// Wait for the Go server to start.
	<-ch

	// Now, the Go service acts as a client and makes a request to the Python service.
	// The Python service is expected to be running on port 8001.
	makeRequest("Go Service", "https://localhost:8001", goClientTLSConfig)

	// Keep the main function alive to serve requests from Python.
	select {}
}
