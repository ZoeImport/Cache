package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

type BaseResponse struct {
	Code int    `json:"code"`
	Env  string `json:"env"`
}
type ResourceType string // 假设 ResourceType 是 string
type KnownowForest struct {
	// 这里只需要 ID 和 Name 字段来接收 JSON
	ID   uint   `json:"ID"`   // 知识库 ID
	Name string `json:"name"` // 知识库名称
	// 忽略其他字段
}

type FileItem struct {
	// ID is forest file id
	ID uint `json:"id"`
	// Name is forest file name
	Name string `json:"name"`
	// PublicUrl is forest file public url
	PublicUrl string `json:"public_url"`
	// FileID is not forest file id, it's core_upload_files' id
	FileID uint `json:"file_id"`
	// ForestID is forest id
	ForestID uint `json:"forest_id"`
}

//type Forest struct {
//	KnownowForest // 匿名嵌套，JSON 字段会被提升到 Forest 级别
//	// 注意：您的 JSON 中 file_list 在 meta 下，而非 forest 下，
//	// 因此我们不能直接在 Forest 中定义 Files []*FileItem。
//	// 我们需要一个辅助结构体来处理嵌套。
//}

type ResourceMeta struct {
	Forest   KnownowForest `json:"forest"`
	FileList []*FileItem   `json:"file_list"` // 直接映射 file_list 数组
}

type Resource struct {
	// ID 资源 id
	ID uint `json:"id"`
	//Meta 资源元数据
	Meta ResourceMeta `json:"meta"` // 将 Meta 从 map[string]interface{} 改为具体结构体
	// ResourceType 资源类型
	ResourceType ResourceType `json:"resource_type"`
}

type GetResourceURLListEmbedResponse struct {
	Data []*Resource `json:"data"`
}

type GetOriginResourceResponse struct {
	BaseResponse                                 // 匿名嵌套
	Response     GetResourceURLListEmbedResponse `json:"Response"`
}

// --- 核心下载逻辑 ---

// downloadFile 保持不变，用于从 URL 下载文件到本地
func downloadFile(url string, filePath string) error {
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Errorf("error fetching URL %s: %w", url, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("bad status code for URL %s: %s", url, resp.Status)
	}

	out, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("error creating file %s: %w", filePath, err)
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return fmt.Errorf("error copying data to file %s: %w", filePath, err)
	}

	fmt.Printf("✅ Successfully downloaded: %s\n", filePath)
	return nil
}

// processJSONStruct 使用结构体进行 JSON 序列化并执行下载任务
func processJSONStruct(resp *GetOriginResourceResponse, baseDir string) error {

	// 1. 遍历 Data 列表 (即不同的 resource/forest)
	for _, resource := range resp.Response.Data {
		// 提取 Forest 信息
		forest := resource.Meta.Forest

		// 提取 FileItem 列表
		fileList := resource.Meta.FileList

		// 构造知识库目录名: forest_id + forest_name
		forestDirName := fmt.Sprintf("%d_%s", forest.ID, forest.Name)
		fullForestDirPath := filepath.Join(baseDir, forestDirName)

		// 创建知识库目录
		if err := os.MkdirAll(fullForestDirPath, 0755); err != nil {
			return fmt.Errorf("error creating forest directory %s: %w", fullForestDirPath, err)
		}

		fmt.Printf("📁 Processing Forest: %s\n", fullForestDirPath)

		// 3. 遍历 FileItem 列表 (已通过结构体映射完成)
		for _, fileItem := range fileList {

			// 构造文件名： file_id + file_name
			// 注意：您要求的文件 ID 是 file_list 中 item 的 ID (FileItem.ID)
			targetFileName := fmt.Sprintf("%d_%s", fileItem.ID, fileItem.Name)
			fullFilePath := filepath.Join(fullForestDirPath, targetFileName)

			// 4. 调用下载函数
			if err := downloadFile(fileItem.PublicUrl, fullFilePath); err != nil {
				// 记录错误但不中断后续文件的下载
				fmt.Printf("❌ Download failed for %s: %v\n", fileItem.PublicUrl, err)
			}
		}
	}
	return nil
}

// RequestBody 结构体用于序列化 POST 请求体
type RequestBody struct {
	Cmd     string `json:"cmd"`
	Env     string `json:"env"`
	Request struct {
		ResourceIDs  []int  `json:"resource_ids"`
		ResourceType string `json:"resource_type"`
	} `json:"request"`
	Version string `json:"version"`
}

const (
	route = "/v9/xxxxx.xxxx"
)

var (
	originUrl = "http://x.x.x.x:x"

	targetPath = fmt.Sprintf("/tmp/forest_download_struct_%v", time.Now().Unix())

	// 2. 构造请求体数据 (对应 --data-raw)
	requestData = RequestBody{
		Request: struct {
			ResourceIDs  []int  `json:"resource_ids"`
			ResourceType string `json:"resource_type"`
		}{
			ResourceIDs:  []int{930},
			ResourceType: "forest",
		},
	}

	authKey = "xxxx"
)

func main() {
	jsonBody, err := json.Marshal(requestData)
	if err != nil {
		fmt.Printf("Error marshalling request body: %v\n", err)
		return
	}
	bodyReader := bytes.NewBuffer(jsonBody)

	req, err := http.NewRequest(http.MethodPost, originUrl+route, bodyReader)
	if err != nil {
		fmt.Printf("Error creating request: %v\n", err)
		return
	}

	req.Header.Set("Authorization", authKey)
	req.Header.Set("Content-Type", "application/json")

	fmt.Printf("🚀 Sending POST request to %s with body: %s\n", originUrl+route, jsonBody)

	resp, err := (&http.Client{
		Timeout: 10 * time.Second,
	}).Do(req)
	if err != nil {
		fmt.Printf("Error sending request: %v\n", err)
		return
	}
	defer resp.Body.Close()

	fmt.Printf("✅ Received response. Status: %s\n", resp.Status)

	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Printf("Error reading response body: %v\n", err)
		return
	}

	fmt.Println("--- Response Body ---")
	fmt.Println(string(responseBody))
	fmt.Println("---------------------")

	var apiResponse GetOriginResourceResponse
	if err := json.Unmarshal(responseBody, &apiResponse); err != nil {
		fmt.Printf("Error unmarshalling response: %v\n", err)
		return
	}
	fmt.Printf("Response Code: %d\n", apiResponse.Code)

	if err = processJSONStruct(&apiResponse, targetPath); err != nil {
		fmt.Printf("Error processing response: %v\n", err)
	}
}
