package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
)

func loadTLSCredentials(caCertPath, serviceCertPath, serviceKeyPath string) (*tls.Config, *tls.Config, error) {
	cert, err := tls.LoadX509KeyPair(serviceCertPath, serviceKeyPath)
	if err != nil {
		return nil, nil, fmt.Errorf("无法加载服务证书密钥对: %v", err)
	}

	caCert, err := os.ReadFile(caCertPath)
	if err != nil {
		return nil, nil, fmt.Errorf("无法加载 CA 证书: %v", err)
	}
	caCertPool := x509.NewCertPool()
	if ok := caCertPool.AppendCertsFromPEM(caCert); !ok {
		return nil, nil, fmt.Errorf("无法将 CA 证书添加到证书池")
	}

	serverTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		ClientCAs:    caCertPool,
		ClientAuth:   tls.RequireAndVerifyClientCert,
	}

	clientTLSConfig := &tls.Config{
		Certificates: []tls.Certificate{cert},
		RootCAs:      caCertPool,
	}

	return serverTLSConfig, clientTLSConfig, nil
}

func main() {
	proxyServerTLSConfig, proxyClientTLSConfig, err := loadTLSCredentials("../certs/ca.crt", "../certs/auth-proxy.crt", "../certs/auth-proxy.key")
	if err != nil {
		log.Fatalf("无法加载代理证书: %v", err)
	}
   	
	goServiceURL, _ := url.Parse("https://localhost:8000")
	goProxy := httputil.NewSingleHostReverseProxy(goServiceURL)
	goProxy.Transport = &http.Transport{
		TLSClientConfig: proxyClientTLSConfig,
	}

	pyServiceURL, _ := url.Parse("https://localhost:8001")
	pyProxy := httputil.NewSingleHostReverseProxy(pyServiceURL)
	pyProxy.Transport = &http.Transport{
		TLSClientConfig: proxyClientTLSConfig,
	}

	router := http.NewServeMux()
	router.HandleFunc("/go", func(w http.ResponseWriter, r *http.Request) {
		log.Println("代理服务器: 正在转发请求到 Go 服务...")
		goProxy.ServeHTTP(w, r)
	})
	router.HandleFunc("/py", func(w http.ResponseWriter, r *http.Request) {
		log.Println("代理服务器: 正在转发请求到 Python 服务...")
		pyProxy.ServeHTTP(w, r)
	})

	server := &http.Server{
		Addr:      ":8080",
		TLSConfig: proxyServerTLSConfig,
		Handler:   router,
	}

	log.Println("认证中心（代理）正在监听 :8080，等待客户端请求...")
	if err := server.ListenAndServeTLS("", ""); err != nil {
		log.Fatalf("无法启动认证中心: %v", err)
	}
}
