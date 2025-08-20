#include <iostream>
#include <queue>
#include <unordered_map>
#include <vector>
#include <string>

// Huffman树的节点
struct HuffmanNode
{
  char data;
  int frequency;
  HuffmanNode *left, *right;

  HuffmanNode(char c, int freq) : data(c), frequency(freq), left(nullptr), right(nullptr) {}
};

// 用于比较Huffman节点的优先级队列
struct CompareNodes
{
  bool operator()(HuffmanNode *left, HuffmanNode *right)
  {
    return left->frequency > right->frequency;
  }
};

// 生成Huffman树
HuffmanNode *buildHuffmanTree(std::unordered_map<char, int> &frequencyMap)
{
  std::priority_queue<HuffmanNode *, std::vector<HuffmanNode *>, CompareNodes> minHeap;

  // 创建叶子节点并加入最小堆
  for (const auto &entry : frequencyMap)
  {
    minHeap.push(new HuffmanNode(entry.first, entry.second));
  }

  // 构建Huffman树
  while (minHeap.size() > 1)
  {
    HuffmanNode *left = minHeap.top();
    minHeap.pop();

    HuffmanNode *right = minHeap.top();
    minHeap.pop();

    HuffmanNode *newNode = new HuffmanNode('$', left->frequency + right->frequency);
    newNode->left = left;
    newNode->right = right;

    minHeap.push(newNode);
  }

  return minHeap.top();
}

// 生成Huffman编码
void generateHuffmanCodes(HuffmanNode *root, std::unordered_map<char, std::string> &huffmanCodes, std::string currentCode)
{
  if (root == nullptr)
  {
    return;
  }

  if (root->data != '$')
  {
    huffmanCodes[root->data] = currentCode;
  }

  generateHuffmanCodes(root->left, huffmanCodes, currentCode + "0");
  generateHuffmanCodes(root->right, huffmanCodes, currentCode + "1");
}

// 压缩数据
std::string compressData(const std::string &data, std::unordered_map<char, std::string> &huffmanCodes)
{
  std::string compressedData;
  for (char c : data)
  {
    compressedData += huffmanCodes[c];
  }
  return compressedData;
}

// 解压缩数据
std::string decompressData(const std::string &compressedData, HuffmanNode *root)
{
  std::string decompressedData;
  HuffmanNode *current = root;

  for (char bit : compressedData)
  {
    if (bit == '0')
    {
      current = current->left;
    }
    else
    {
      current = current->right;
    }

    if (current->left == nullptr && current->right == nullptr)
    {
      decompressedData += current->data;
      current = root;
    }
  }

  return decompressedData;
}

int main()
{
  // 输入数据
  std::string data = "ABAACEGZBBZ";

  // 统计频率
  std::unordered_map<char, int> frequencyMap;
  for (char c : data)
  {
    frequencyMap[c]++;
  }

  // 构建Huffman树
  HuffmanNode *root = buildHuffmanTree(frequencyMap);

  // 生成Huffman编码
  std::unordered_map<char, std::string> huffmanCodes;
  generateHuffmanCodes(root, huffmanCodes, "");

  // 输出Huffman编码
  std::cout << "Huffman Codes:\n";
  for (const auto &entry : huffmanCodes)
  {
    std::cout << entry.first << ": " << entry.second << "\n";
  }

  // 压缩数据
  std::string compressedData = compressData(data, huffmanCodes);
  std::cout << "\nCompressed Data: " << compressedData << "\n";

  // 解压缩数据
  std::string decompressedData = decompressData(compressedData, root);
  std::cout << "Decompressed Data: " << decompressedData << "\n";

  return 0;
}
