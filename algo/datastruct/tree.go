package datastruct

type BinarySearchTree struct {
	Val   int
	Root  *BinarySearchTree
	Left  *BinarySearchTree
	Right *BinarySearchTree
}

func NewBinarySearchTreeNode(val int) *BinarySearchTree {
	return &BinarySearchTree{
		Val: val,
	}
}

func (tree *BinarySearchTree) Search(num int) *BinarySearchTree {
	root := tree.Root
	for root != nil {
		if root.Val > num {
			root = root.Left
		} else if root.Val < num {
			root = root.Right
		} else {
			return root
		}
	}
	return nil
}

func (tree *BinarySearchTree) Insert(num int) {
	root := tree.Root
	if root == nil {
		tree.Root = NewBinarySearchTreeNode(num)
	}
	var pre *BinarySearchTree = nil
	for root != nil {
		if root.Val == num {
			return
		}
		pre = root
		if root.Val > num {
			root = root.Left
		} else if root.Val < num {
			root = root.Right
		}
	}
	if pre.Val > num {
		pre.Left = NewBinarySearchTreeNode(num)
	} else {
		pre.Right = NewBinarySearchTreeNode(num)
	}
}

func (tree *BinarySearchTree) Remove(val int) {

}
