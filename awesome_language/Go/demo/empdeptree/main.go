package main

import (
	"encoding/json"
	"fmt"
	"log"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func main() {
	// --- 初始化数据库 (使用内存SQLite做演示) ---
	db, err := gorm.Open(sqlite.Open("file::memory:?cache=shared"), &gorm.Config{})
	if err != nil {
		log.Fatalf("failed to connect database: %v", err)
	}

	// --- 自动迁移表结构 ---
	err = db.AutoMigrate(&Department{}, &Employee{}, &EmployeeDepartment{})
	if err != nil {
		log.Fatalf("failed to migrate database: %v", err)
	}

	// --- 填充示例数据 ---
	seedData(db)

	// --- 使用服务 ---
	service := NewDepartmentService(db)

	fmt.Println("=========================================================")
	fmt.Println("需求1: 获取包含员工的完整组织架构树")
	fmt.Println("=========================================================")
	fullTree, err := service.GetOrganizationTree()
	if err != nil {
		log.Fatalf("Error getting organization tree: %v", err)
	}
	printJSON(fullTree)

	fmt.Println("\n=========================================================")
	fmt.Println("需求2: 只获取部门层级树")
	fmt.Println("=========================================================")
	deptTree, err := service.GetDepartmentTree()
	if err != nil {
		log.Fatalf("Error getting department tree: %v", err)
	}
	printJSON(deptTree)
}

// printJSON 格式化打印JSON
func printJSON(v interface{}) {
	b, err := json.MarshalIndent(v, "", "  ")
	if err != nil {
		fmt.Println("Error marshalling to JSON:", err)
		return
	}
	fmt.Println(string(b))
}

// seedData 填充测试数据
func seedData(db *gorm.DB) {
	// 部门 (Departments)
	// 注意 ParentID 的处理
	pID1, pID10, pID11, _, _ := uint(1), uint(10), uint(11), uint(12), uint(20)
	departments := []Department{
		{ID: 1, Name: "总公司", ParentID: nil, Sort: 0},
		{ID: 10, Name: "研发部", ParentID: &pID1, Sort: 0},
		{ID: 11, Name: "产品部", ParentID: &pID1, Sort: 1},
		{ID: 12, Name: "市场部", ParentID: &pID1, Sort: 2},
		{ID: 20, Name: "后端开发组", ParentID: &pID10, Sort: 0},
		{ID: 21, Name: "前端开发组", ParentID: &pID10, Sort: 1},
		{ID: 30, Name: "产品设计组", ParentID: &pID11, Sort: 0},
	}
	db.Create(&departments)

	// 员工 (Employees)
	employees := []Employee{
		{ID: 101, Uin: "ceo001", Name: "张总"},
		{ID: 102, Uin: "rd_leader", Name: "李主管"},
		{ID: 103, Uin: "backend01", Name: "王工程师"},
		{ID: 104, Uin: "backend02", Name: "赵工程师"},
		{ID: 105, Uin: "frontend01", Name: "孙工程师"},
		{ID: 106, Uin: "pm01", Name: "周经理"},
	}
	db.Create(&employees)

	// 关系 (Relations)
	// 注意：李主管同时属于研发部和后端开发组
	relations := []EmployeeDepartment{
		{EmployeeID: 101, DepartmentID: 1},  // 张总在总公司 (非叶子节点)
		{EmployeeID: 102, DepartmentID: 10}, // 李主管在研发部 (非叶子节点)
		{EmployeeID: 102, DepartmentID: 20}, // 李主管也在后端开发组
		{EmployeeID: 103, DepartmentID: 20}, // 王工程师在后端开发组
		{EmployeeID: 104, DepartmentID: 20}, // 赵工程师在后端开发组
		{EmployeeID: 105, DepartmentID: 21}, // 孙工程师在前端开发组
		{EmployeeID: 106, DepartmentID: 11}, // 周经理在产品部 (非叶子节点)
		{EmployeeID: 106, DepartmentID: 30}, // 周经理也在产品设计组
	}
	db.Create(&relations)
}
