package main

import (
	"context"
	"fmt"
	"os"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
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

func main() {
	clusterID, err := GetClusterID(context.TODO())
	if err != nil {
		// 打印错误信息
		fmt.Fprintf(os.Stderr, "Error getting cluster ID: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Cluster UID: %s\n", clusterID)
}
