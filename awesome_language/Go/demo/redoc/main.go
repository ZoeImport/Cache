package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	// 引入 docs 包，注意下划线，用于导入自动生成的文档信息
	_ "main/docs"
)

// --- Swagger 顶层注释 (用于 swag init) ---

// @title Go 嵌套 API 文档示例 (ReDoc 集成)
// @version 1.0
// @description 这是一个使用 Gin 和 Swaggo 生成的 Go 接口文档示例，并使用 ReDoc 展示。
// @host localhost:8080
// @BasePath /api/v1
// @schemes http

// --- 复杂嵌套结构体定义 ---

// Detail 是嵌套在 Response 结构体中的详细数据
type Detail struct {
	// 字段ID
	ID int `json:"id" example:"100"`
	// 字段名称
	Name string `json:"name" example:"Nested Item"`
}

// UserResponse 是接口返回的主体结构
type UserResponse struct {
	// 状态码
	Code int `json:"code" example:"200"`
	// 消息提示
	Message string `json:"message" example:"Success"`
	// 嵌套的详细数据，此处即是您提到的复杂嵌套类型
	Data Detail `json:"data"`
}

// @Summary 获取用户详细信息
// @Description 根据用户 ID 获取用户详细信息，包含复杂嵌套结构。
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "用户 ID"
// @Success 200 {object} UserResponse "成功响应，包含嵌套数据"
// @Failure 400 {object} map[string]string "请求参数错误"
// @Router /users/{id} [get]
func GetUserByID(c *gin.Context) {
	// 模拟返回一个包含嵌套结构的 JSON 响应
	response := UserResponse{
		Code:    200,
		Message: "User detail retrieved successfully",
		Data: Detail{
			ID:   123,
			Name: "Alice Smith",
		},
	}
	c.JSON(http.StatusOK, response)
}

// HandleReDoc 处理器：用于读取 redoc_template.html 并动态替换 JSON 路径后返回
func HandleReDoc(model string) gin.HandlerFunc {
	return func(c *gin.Context) {
		// 1. 读取 HTML 模板文件
		content, err := os.ReadFile("./redoc_template.html")
		if err != nil {
			c.String(http.StatusInternalServerError, "Error loading ReDoc template: "+err.Error())
			return
		}
		fmt.Println("=====================", string(content))

		// 2. 动态计算 JSON URL
		// 假设 ReDoc 页面路由是 /model.redoc
		// 假设 Swagger JSON 路由是 /model.docs/doc.json
		// c.FullPath() 获取路由模板，例如 /api/v1/users/redoc
		// 注意：这里需要根据实际注册的路由来计算，我们假设注册路径是 /redoc

		// 简化的路径计算：直接拼接 BasePath + JSON 文件的标准路径
		// 在 Gin 中，我们直接使用绝对路径：/api/v1/model.docs/doc.json
		// 为了兼容性，我们直接从 c.Request.URL.Path 推导

		// 假设 ReDoc 路由注册在 /api/v1/redoc
		jsonURL := "/api/v1/" + model + ".docs/doc.json"

		// 3. 替换 HTML 模板中的占位符
		htmlContent := strings.Replace(string(content), "__JSON_URL__", jsonURL, 1)

		// 4. 返回 ReDoc 页面
		c.Data(http.StatusOK, "text/html; charset=utf-8", []byte(htmlContent))
	}
}

func main() {
	r := gin.Default()

	// 定义模块名称
	const modelName = "users"

	// 注册 API 路由
	v1 := r.Group("/api/v1")
	{
		v1.GET("/users/:id", GetUserByID)

		// --- 文档路由注册 ---

		// 1. 暴露 Swagger JSON 文件：这是 ReDoc 页面请求的数据源
		// 路径：/api/v1/users.docs/doc.json
		v1.GET("/"+modelName+".docs/*any", ginSwagger.WrapHandler(swaggerFiles.Handler, ginSwagger.InstanceName(modelName)))

		// 2. 暴露 ReDoc 界面：当访问 /api/v1/users.redoc 时，返回 ReDoc HTML
		v1.GET("/"+modelName+".redoc", HandleReDoc(modelName))
	}

	// 启动服务
	// ReDoc 文档入口：http://localhost:8080/api/v1/users.redoc
	r.Run(":8080")
}
