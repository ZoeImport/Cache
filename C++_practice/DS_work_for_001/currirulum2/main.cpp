#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <functional>
#include <fstream>

using namespace std;

// 节点类型：发电站、变电站、用户
enum NodeType
{
  GENERATOR,
  SUBSTATION,
  USER
};

// 图的节点
struct Node
{
  int id;
  NodeType type;

  Node(int _id, NodeType _type) : id(_id), type(_type) {}
};

// 图的边
struct Edge
{
  int from;
  int to;
  double cost;

  Edge(int _from, int _to, double _cost) : from(_from), to(_to), cost(_cost) {}
};

// 图类
class Graph
{
public:
  vector<Node> nodes;
  vector<Edge> edges;
  unordered_map<int, vector<Edge>> adjacencyList;

  void addNode(int id, NodeType type)
  {
    nodes.emplace_back(id, type);
  }

  void addEdge(int from, int to, double cost)
  {
    edges.emplace_back(from, to, cost);
    adjacencyList[from].emplace_back(from, to, cost);
    adjacencyList[to].emplace_back(to, from, cost); // 无向图需要双向边
  }

  void printAdjacencyList()
  {
    cout << "Adjacency List:" << endl;
    for (const auto &entry : adjacencyList)
    {
      cout << entry.first << ": ";
      for (const Edge &edge : entry.second)
      {
        cout << "(" << edge.from << "->" << edge.to << ", Cost: " << edge.cost << ") ";
      }
      cout << endl;
    }
  }

  void DFS(int startNode)
  {
    vector<bool> visited(nodes.size(), false);
    cout << "DFS Order: ";
    DFSUtil(startNode, visited);
    cout << endl;
  }

  void DFSUtil(int node, vector<bool> &visited)
  {
    cout << node << " ";
    visited[node] = true;

    for (const Edge &edge : edges)
    {
      if (edge.from == node && !visited[edge.to])
      {
        DFSUtil(edge.to, visited);
      }
    }
  }

  void BFS(int startNode)
  {
    vector<bool> visited(nodes.size(), false);
    queue<int> bfsQueue;

    cout << "BFS Order: ";

    bfsQueue.push(startNode);
    visited[startNode] = true;

    while (!bfsQueue.empty())
    {
      int node = bfsQueue.front();
      bfsQueue.pop();

      cout << node << " ";

      for (const Edge &edge : edges)
      {
        if (edge.from == node && !visited[edge.to])
        {
          bfsQueue.push(edge.to);
          visited[edge.to] = true;
        }
      }
    }

    cout << endl;
  }

  void generateDOTFile(const string &filename)
  {
    ofstream dotFile(filename);

    dotFile << "graph PowerNetwork {" << endl;

    for (const Edge &edge : edges)
    {
      dotFile << edge.from << " -- " << edge.to << " [label=\"" << edge.cost << "\"];" << endl;
    }

    dotFile << "}" << endl;

    dotFile.close();
  }

  void generateGraphImage(const string &dotFilename, const string &outputFilename)
  {
    string command = "dot -Tpng " + dotFilename + " -o " + outputFilename;
    system(command.c_str());
  }

  double findMinimumSpanningTreeCost()
  {
    priority_queue<Edge, vector<Edge>, function<bool(Edge, Edge)>> minHeap(
        [](Edge a, Edge b)
        { return a.cost > b.cost; });

    vector<bool> visited(nodes.size(), false);
    visited[0] = true;

    for (const Edge &edge : edges)
    {
      if (edge.from == 0)
      {
        minHeap.push(edge);
      }
    }

    double totalCost = 0.0;
    while (!minHeap.empty())
    {
      Edge minEdge = minHeap.top();
      minHeap.pop();

      if (!visited[minEdge.to])
      {
        visited[minEdge.to] = true;
        totalCost += minEdge.cost;

        for (const Edge &edge : edges)
        {
          if (edge.from == minEdge.to && !visited[edge.to])
          {
            minHeap.push(edge);
          }
        }
      }
    }

    return totalCost;
  }
};

int main()
{
  Graph powerNetwork;

  // 添加节点
  powerNetwork.addNode(0, GENERATOR);  // 发电站 A
  powerNetwork.addNode(1, GENERATOR);  // 发电站 B
  powerNetwork.addNode(2, SUBSTATION); // 变电站 C
  powerNetwork.addNode(3, SUBSTATION); // 变电站 D
  powerNetwork.addNode(4, USER);       // 用户 E
  powerNetwork.addNode(5, USER);       // 用户 F
  powerNetwork.addNode(6, USER);       // 用户 G

  // 添加边
  powerNetwork.addEdge(0, 2, 5.0); // A -> C, 成本 5.0
  powerNetwork.addEdge(0, 3, 8.0); // A -> D, 成本 8.0
  powerNetwork.addEdge(1, 2, 6.0); // B -> C, 成本 6.0
  powerNetwork.addEdge(1, 3, 7.0); // B -> D, 成本 7.0
  powerNetwork.addEdge(2, 4, 4.0); // C -> E, 成本 4.0
  powerNetwork.addEdge(2, 5, 2.0); // C -> F, 成本 2.0
  powerNetwork.addEdge(3, 6, 3.0); // D -> G, 成本 3.0

  // 输出邻接列表
  powerNetwork.printAdjacencyList();

  // 输出图的深度优先搜索序列
  powerNetwork.DFS(0);

  // 输出图的广度优先搜索序列
  powerNetwork.BFS(0);

  // 输出最小生成树的成本
  double minimumSpanningTreeCost = powerNetwork.findMinimumSpanningTreeCost();
  cout << "Minimum Spanning Tree Cost: " << minimumSpanningTreeCost << endl;

  return 0;
}
