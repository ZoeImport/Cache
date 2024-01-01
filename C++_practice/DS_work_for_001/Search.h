#ifndef _SEARCH_
#define _SEARCH_

#include <iostream>
#include <vector>

template <typename T>
class TreeNode
{
public:
  T data;
  TreeNode<T> *left;
  TreeNode<T> *right;

  TreeNode(T value) : data(value), left(nullptr), right(nullptr) {}
};

template <typename T>
class BinarySearchTree
{
private:
  TreeNode<T> *root;

  TreeNode<T> *insert(TreeNode<T> *node, T value)
  {
    if (node == nullptr)
    {
      return new TreeNode<T>(value);
    }

    if (value < node->data)
    {
      node->left = insert(node->left, value);
    }
    else if (value > node->data)
    {
      node->right = insert(node->right, value);
    }

    return node;
  }

  void inOrderTraversal(TreeNode<T> *node)
  {
    if (node != nullptr)
    {
      inOrderTraversal(node->left);
      std::cout << node->data << " ";
      inOrderTraversal(node->right);
    }
  }

  TreeNode<T> *search(TreeNode<T> *node, T value)
  {
    if (node == nullptr || node->data == value)
    {
      return node;
    }

    if (value < node->data)
    {
      return search(node->left, value);
    }
    else
    {
      return search(node->right, value);
    }
  }

public:
  BinarySearchTree() : root(nullptr) {}

  void insert(T value) { root = insert(root, value); }

  void inOrderTraversal()
  {
    inOrderTraversal(root);
    std::cout << std::endl;
  }

  TreeNode<T> *search(T value) { return search(root, value); }
};

template <typename T>
int linearSearch(const std::vector<T> &arr, T target)
{
  for (size_t i = 0; i < arr.size(); ++i)
  {
    if (arr[i] == target)
    {
      return i; // 返回找到的元素的索引
    }
  }
  return -1; // 未找到返回-1
}

#endif