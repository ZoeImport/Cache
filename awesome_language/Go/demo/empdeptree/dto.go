package main

// EmployeeInfo 用于在树中展示的员工信息
type EmployeeInfo struct {
	Uin  string `json:"uin"`
	Name string `json:"name"`
}

// DepartmentNode 树形结构的节点
type DepartmentNode struct {
	ID        uint              `json:"id"`
	Name      string            `json:"name"`
	ParentID  *uint             `json:"-"` // 内部组装使用, JSON中忽略
	Sort      int               `json:"sort"`
	Children  []*DepartmentNode `json:"children,omitempty"` // omitempty: 如果为空则在JSON中忽略
	Employees []*EmployeeInfo   `json:"employees,omitempty"`
}
