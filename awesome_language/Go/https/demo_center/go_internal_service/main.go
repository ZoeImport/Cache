package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"log"
	"net/http"
	"os"
)

func main() {
	certPath := "../certs/go-internal.crt"
	keyPath := "../certs/go-internal.key"
	caCertPath := "../certs/ca.crt"

	cert, err := tls.LoadX509KeyPair(certPath, keyPath)
	if err != nil {
		log.Fatalf("无法加载服务证书: %v", err)
	}

	caCert, err := os.ReadFile(caCertPath)
	if err != nil {
		log.Fatalf("无法加载 CA 证书: %v", err)
	}
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		log.Fatalf("无法将 CA 证书添加到证书池")
	}

	serverTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caCertPool,
		ClientAuth:   tls.RequireAndVerifyClientCert,
	}

	server := &http.Server{
		Addr:      ":8000",
		TLSConfig: serverTLSConfig,
		Handler: http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			log.Println("Go 内部服务：收到来自认证中心的请求。")
			fmt.Fprintf(w, "Hello from the Go internal service!")
		}),
	}

	log.Println("Go 内部服务正在监听 :8000...")
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("无法启动 Go 内部服务: %v", err)
	}
}
