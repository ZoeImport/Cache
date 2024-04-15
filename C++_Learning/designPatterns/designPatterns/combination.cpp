#include <algorithm>
#include <iostream>
#include <list>
#include <string>
#include <vector>

class FileNode {
public:
  virtual void addChild(FileNode *){};
  virtual void removeChild(FileNode *){};
  // =============================================
  virtual std::list<FileNode *> getChildren() = 0;
  virtual bool hasChild() = 0;
  virtual void setParent(FileNode *) = 0;
  virtual FileNode *getParent() = 0;
  virtual void setInfo(std::string info) = 0;
  virtual std::string getInfo() = 0;
  virtual bool isRoot() = 0;

protected:
  FileNode *parent;
  std::list<FileNode *> children;
  std::string info;
};

class DirectoyNode : public FileNode {
public:
  FileNode *getParent() override { return this->parent; }
  bool hasChild() override { return !this->children.empty(); }
  void addChild(FileNode *node) override { this->children.push_back(node); }
  void removeChild(FileNode *node) override { this->children.remove(node); }
  void setParent(FileNode *node) override { this->parent = node; }
  void setInfo(std::string info) override { this->info = info; }
  std::string getInfo() override { return this->info; }
  bool isRoot() override { return this->parent == nullptr; }
  std::list<FileNode *> getChildren() override { return this->children; }
};

class LeafNode : public FileNode {
public:
  FileNode *getParent() override { return this->parent; }
  bool hasChild() override { return false; }
  void setParent(FileNode *node) override { this->parent = node; }
  void setInfo(std::string info) override { this->info = info; }
  std::string getInfo() override { return this->info; }
  bool isRoot() override { return false; }
  std::list<FileNode *> getChildren() override {
    std::list<FileNode *> temp;
    return temp;
  }
};

void Display(FileNode *node) {
  std::cout<<node->getInfo()<<std::endl;
  for (auto &file : node->getChildren()) {
    if (file->hasChild()) {
      std::cout << "dir info:" << file->getInfo() << std::endl;
      Display(file);
    } else {
      std::cout << file->getInfo()<<" ";
    }
  }
}

int main() {
  DirectoyNode *root = new DirectoyNode;
  root->setInfo("[root]");
  DirectoyNode *dir = new DirectoyNode;
  dir->setInfo("[first dir]");
  dir->setParent(root);
  LeafNode *node1 = new LeafNode;
  LeafNode *node2 = new LeafNode;
  LeafNode *node3 = new LeafNode;
  LeafNode *node4 = new LeafNode;
  node1->setInfo("[first son node]");
  node2->setInfo("[second son node]");
  node3->setInfo("[Third son node]");
  node4->setInfo("[Forth son node]");
  node1->setParent(root);
  node2->setParent(root);
  node3->setParent(dir);
  node4->setParent(dir);
  root->addChild(node1);
  root->addChild(node2);
  root->addChild(dir);
  dir->addChild(node3);
  dir->addChild(node4);

  Display(root);
}