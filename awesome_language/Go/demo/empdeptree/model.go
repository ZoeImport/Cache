package main

import (
	"time"

	"gorm.io/gorm"
)

// Department 部门表模型
// 使用字段/逻辑外键，不设置物理外键
type Department struct {
	ID        uint `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Name      string         `gorm:"unique;not null;size:100"`
	ParentID  *uint          // 使用指针类型以允许根部门的 ParentID 为 NULL
	Sort      int            `gorm:"not null;default:0;comment:同级排序，数值越小越靠前"`
}

func (Department) TableName() string {
	return "departments"
}

// Employee 员工表模型
type Employee struct {
	ID        uint `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Uin       string         `gorm:"unique;not null;size:50"`
	Name      string         `gorm:"not null;size:100"`
}

func (Employee) TableName() string {
	return "employees"
}

// EmployeeDepartment 员工部门关系表（多对多）
type EmployeeDepartment struct {
	EmployeeID   uint `gorm:"primaryKey"`
	DepartmentID uint `gorm:"primaryKey"`
}

func (EmployeeDepartment) TableName() string {
	return "employee_departments"
}
