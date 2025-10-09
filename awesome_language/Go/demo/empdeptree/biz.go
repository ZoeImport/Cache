package main

import (
	"sort"

	"gorm.io/gorm"
)

// DepartmentService 负责处理部门和组织架构的业务逻辑
type DepartmentService struct {
	DB *gorm.DB
}

// NewDepartmentService 创建一个新的服务实例
func NewDepartmentService(db *gorm.DB) *DepartmentService {
	return &DepartmentService{DB: db}
}

// buildTree 是核心的、可复用的私有方法
// includeEmployees 参数控制是否在结果中包含员工信息
func (s *DepartmentService) buildTree(includeEmployees bool) ([]*DepartmentNode, error) {
	// 1. 一次性获取所有部门
	var departments []Department
	if err := s.DB.Order("sort asc").Find(&departments).Error; err != nil {
		return nil, err
	}

	// 2. 如果需要，一次性获取所有员工和部门的关联关系
	employeeMap := make(map[uint][]*EmployeeInfo)
	if includeEmployees {
		// 定义一个临时结构体来接收JOIN查询的结果
		var relations []struct {
			DepartmentID uint
			Uin          string
			Name         string
		}

		// 使用JOIN查询，性能远高于循环查询
		err := s.DB.Table("employees as e").
			Select("ed.department_id, e.uin, e.name").
			Joins("join employee_departments as ed on e.id = ed.employee_id").
			Where("e.deleted_at IS NULL").
			Scan(&relations).Error

		if err != nil {
			return nil, err
		}

		// 将员工信息按部门ID分组
		for _, r := range relations {
			employeeMap[r.DepartmentID] = append(employeeMap[r.DepartmentID], &EmployeeInfo{
				Uin:  r.Uin,
				Name: r.Name,
			})
		}
	}

	// 3. 内存中组装树形结构
	// 使用map快速查找节点
	nodeMap := make(map[uint]*DepartmentNode, len(departments))
	var roots []*DepartmentNode

	// 第一次遍历：初始化所有节点，并放入map
	for _, dept := range departments {
		node := &DepartmentNode{
			ID:       dept.ID,
			Name:     dept.Name,
			ParentID: dept.ParentID,
			Sort:     dept.Sort,
		}
		// 如果需要，填充员工信息
		if includeEmployees {
			if employees, ok := employeeMap[dept.ID]; ok {
				node.Employees = employees
			}
		}
		nodeMap[dept.ID] = node
	}

	// 第二次遍历：构建父子关系
	for _, node := range nodeMap {
		if node.ParentID == nil || *node.ParentID == 0 {
			roots = append(roots, node)
		} else {
			if parent, ok := nodeMap[*node.ParentID]; ok {
				parent.Children = append(parent.Children, node)
			}
			// 如果父节点不存在（数据不一致），这个节点将被忽略，不会出现在树中
		}
	}

	// 4. 对每一层的子节点进行排序（因为原始查询已排序，这里是保证父子关系构建后顺序正确）
	// 根节点排序
	sort.Slice(roots, func(i, j int) bool {
		return roots[i].Sort < roots[j].Sort
	})

	// 各层级子节点排序
	for _, node := range nodeMap {
		if len(node.Children) > 1 {
			sort.Slice(node.Children, func(i, j int) bool {
				return node.Children[i].Sort < node.Children[j].Sort
			})
		}
	}

	return roots, nil
}

// GetOrganizationTree 获取包含员工的完整组织架构树 (需求1)
func (s *DepartmentService) GetOrganizationTree() ([]*DepartmentNode, error) {
	return s.buildTree(true)
}

// GetDepartmentTree 只获取部门层级树，不包含员工 (需求2)
func (s *DepartmentService) GetDepartmentTree() ([]*DepartmentNode, error) {
	return s.buildTree(false)
}
