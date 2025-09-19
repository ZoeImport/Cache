package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/PuerkitoBio/goquery"
	"golang.org/x/time/rate"
)

const (
	targetURL     = "https://www.gutenberg.org/ebooks/66166.txt.utf-8"
	outputFile    = "collected_content.txt"
	maxTotalChars = 1000000         // 目标50万字
	concurrency   = 3               // 并发数
	requestDelay  = 1 * time.Second // 请求间隔
)

func main() {
	fmt.Println("开始爬取公开领域文学作品...")

	// 创建输出文件
	file, err := os.Create(outputFile)
	if err != nil {
		fmt.Printf("创建文件失败: %v\n", err)
		return
	}
	defer file.Close()

	writer := bufio.NewWriter(file)
	defer writer.Flush()

	// 限流器
	limiter := rate.NewLimiter(rate.Every(requestDelay), 1)

	// 使用waitgroup管理并发
	var wg sync.WaitGroup
	var mu sync.Mutex
	var totalChars int

	// 爬取主URL内容
	fmt.Printf("爬取主内容: %s\n", targetURL)

	if err := limiter.Wait(context.Background()); err != nil {
		fmt.Printf("限流等待错误: %v\n", err)
		return
	}

	content, err := fetchContent(targetURL)
	if err != nil {
		fmt.Printf("爬取失败: %v\n", err)
		return
	}

	// 写入内容
	mu.Lock()
	if _, err := writer.WriteString(content + "\n\n"); err != nil {
		fmt.Printf("写入失败: %v\n", err)
		mu.Unlock()
		return
	}
	totalChars += len(content)
	mu.Unlock()

	fmt.Printf("已获取 %d 字符，总共 %d 字符\n", len(content), totalChars)

	// 如果需要更多内容，可以爬取相关链接
	if totalChars < maxTotalChars {
		fmt.Println("获取更多相关内容...")
		relatedLinks := findRelatedLiteratureLinks()

		for _, link := range relatedLinks {
			if totalChars >= maxTotalChars {
				break
			}

			wg.Add(1)
			go func(link string) {
				defer wg.Done()

				if err := limiter.Wait(context.Background()); err != nil {
					fmt.Printf("限流错误: %v\n", err)
					return
				}

				content, err := fetchContent(link)
				if err != nil {
					fmt.Printf("爬取 %s 失败: %v\n", link, err)
					return
				}

				mu.Lock()
				if totalChars+len(content) <= maxTotalChars {
					if _, err := writer.WriteString(content + "\n\n"); err != nil {
						fmt.Printf("写入失败: %v\n", err)
					} else {
						totalChars += len(content)
						fmt.Printf("从 %s 获取 %d 字符，总共 %d 字符\n", domainFromURL(link), len(content), totalChars)
					}
				}
				mu.Unlock()
			}(link)
		}

		wg.Wait()
	}

	fmt.Printf("爬取完成！总共获取 %d 字符，已保存到 %s\n", totalChars, outputFile)

	// 验证文件内容
	if err := verifyContent(outputFile); err != nil {
		fmt.Printf("内容验证失败: %v\n", err)
	} else {
		fmt.Println("内容验证通过！")
	}
}

// fetchContent 获取URL的文本内容
func fetchContent(urlStr string) (string, error) {
	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	resp, err := client.Get(urlStr)
	if err != nil {
		return "", fmt.Errorf("HTTP请求失败: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("HTTP状态码错误: %d", resp.StatusCode)
	}

	// 读取内容
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", fmt.Errorf("读取响应失败: %v", err)
	}

	// 简单的文本提取（避免HTML标签）
	content := extractTextFromHTML(string(body))
	if content == "" {
		content = string(body) // 如果是纯文本文件直接使用
	}

	// 清理内容
	content = cleanContent(content)

	return content, nil
}

// extractTextFromHTML 从HTML中提取文本内容
func extractTextFromHTML(htmlContent string) string {
	doc, err := goquery.NewDocumentFromReader(strings.NewReader(htmlContent))
	if err != nil {
		// 如果不是HTML，返回原内容
		return htmlContent
	}

	// 移除脚本和样式
	doc.Find("script, style").Each(func(i int, s *goquery.Selection) {
		s.Remove()
	})

	// 获取文本内容
	text := doc.Text()
	return strings.TrimSpace(text)
}

// cleanContent 清理内容
func cleanContent(content string) string {
	// 移除多余的空格和换行
	content = strings.ReplaceAll(content, "\r", "")
	content = strings.ReplaceAll(content, "  ", " ")

	// 分割成行并清理
	lines := strings.Split(content, "\n")
	var cleanedLines []string

	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line != "" && len(line) > 10 { // 过滤过短的行
			cleanedLines = append(cleanedLines, line)
		}
	}

	return strings.Join(cleanedLines, "\n")
}

// findRelatedLiteratureLinks 返回一些公开领域文学作品的URL
func findRelatedLiteratureLinks() []string {
	return []string{
		// 鲁迅作品（公开领域）
		"https://www.gutenberg.org/ebooks/66166.txt.utf-8", // 呐喊
		"https://www.gutenberg.org/ebooks/66167.txt.utf-8", // 彷徨
		"https://www.gutenberg.org/ebooks/66168.txt.utf-8", // 朝花夕拾

		// 古典文学
		"https://www.gutenberg.org/ebooks/23950.txt.utf-8", // 红楼梦片段
		"https://www.gutenberg.org/ebooks/23953.txt.utf-8", // 水浒传片段
		"https://www.gutenberg.org/ebooks/23954.txt.utf-8", // 西游记片段
		"https://www.gutenberg.org/ebooks/23955.txt.utf-8", // 三国演义片段

		// 现代文学
		"https://www.gutenberg.org/ebooks/36166.txt.utf-8", // 骆驼祥子片段
		"https://www.gutenberg.org/ebooks/36167.txt.utf-8", // 茶馆片段

		// 更多中文公开领域资源
		"https://www.gutenberg.org/ebooks/50316.txt.utf-8", // 古文观止
		"https://www.gutenberg.org/ebooks/50317.txt.utf-8", // 唐诗三百首
		"https://www.gutenberg.org/ebooks/50318.txt.utf-8", // 宋词三百首
	}
}

// domainFromURL 从URL提取域名
func domainFromURL(urlStr string) string {
	u, err := url.Parse(urlStr)
	if err != nil {
		return "unknown"
	}
	return u.Hostname()
}

// verifyContent 验证内容文件
func verifyContent(filename string) error {
	file, err := os.Open(filename)
	if err != nil {
		return err
	}
	defer file.Close()

	info, err := file.Stat()
	if err != nil {
		return err
	}

	if info.Size() == 0 {
		return fmt.Errorf("文件为空")
	}

	// 检查文件大小
	if info.Size() < 100000 { // 至少100KB
		return fmt.Errorf("文件大小不足")
	}

	fmt.Printf("文件大小: %.2f MB\n", float64(info.Size())/1024/1024)
	return nil
}

// 简单的敏感词检查（确保内容安全）
func containsSensitiveContent(text string) bool {
	sensitiveWords := []string{
		// 这里可以添加需要过滤的词汇
	}

	lowerText := strings.ToLower(text)
	for _, word := range sensitiveWords {
		if strings.Contains(lowerText, word) {
			return true
		}
	}
	return false
}
