import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import jieba  # 中文分词库
from typing import List, Tuple, Dict, Any # 引入类型系统

# ==========================================
# 1. 数据定义 (模拟 JSON 文件)
# ==========================================
# 在真实项目中，这通常是从数据库或 json 文件读取的
raw_intents: Dict[str, List[Dict[str, Any]]] = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["你好", "您好", "哈喽", "在吗", "早上好"],
            "responses": ["你好！", "很高兴见到你", "请问有什么可以帮您的？"]
        },
        {
            "tag": "goodbye",
            "patterns": ["再见", "拜拜", "先走了", "下次聊"],
            "responses": ["再见！", "祝您生活愉快", "期待下次相见"]
        },
        {
            "tag": "coding",
            "patterns": ["写代码", "Python怎么学", "教我编程", "Bug"],
            "responses": ["人生苦短，我用 Python！", "多写多练是关键", "遇到 Bug 别慌，先 Print 一下"]
        }
    ]
}

# ==========================================
# 2. 工具函数 (NLP 预处理)
# ==========================================

def tokenize(sentence: str) -> List[str]:
    """
    分词函数：将句子切分成词列表
    类似于 Go: func Tokenize(s string) []string
    """
    # jieba.lcut 返回一个 list
    return jieba.lcut(sentence)

def bag_of_words(tokenized_sentence: List[str], all_words: List[str]) -> np.ndarray:
    """
    词袋模型 (One-hot 变种)：将词列表转为 0/1 向量
    
    输入: ["我", "爱"]
    全词表: ["你", "我", "爱", "它"]
    输出: [0, 1, 1, 0] (float32 数组)
    """
    set_sentence = set(tokenized_sentence)
    # 初始化一个全 0 的 float32 数组，长度等于词表长度
    bag = np.zeros(len(all_words), dtype=np.float32)
    
    for idx, w in enumerate(all_words):
        if w in set_sentence:
            bag[idx] = 1.0
            
    return bag

# ==========================================
# 3. 定义 PyTorch 数据集 (类似于 Go 的 Interface 实现)
# ==========================================

class ChatDataset(Dataset):
    """
    实现 PyTorch 的 Dataset 抽象类
    必须实现 __len__ 和 __getitem__ 两个方法
    """
    def __init__(self, x_data: np.ndarray, y_data: np.ndarray):
        self.n_samples = len(x_data)
        # 转换为 PyTorch 的 Tensor (张量)
        # 输入 X 必须是 float32
        # 标签 Y 必须是 long (int64)，因为是分类索引
        self.x_data = torch.from_numpy(x_data).float()
        self.y_data = torch.from_numpy(y_data).long()

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.x_data[index], self.y_data[index]

    def __len__(self) -> int:
        return self.n_samples

# ==========================================
# 4. 定义神经网络模型 (The Brain)
# ==========================================

class NeuralNet(nn.Module):
    def __init__(self, input_size: int, hidden_size: int, num_classes: int):
        """
        :param input_size: 词表大小 (BoW 向量长度)
        :param hidden_size: 隐藏层神经元数量 (脑容量)
        :param num_classes: 意图类别的数量
        """
        super(NeuralNet, self).__init__()
        # 定义三层全连接网络
        # Layer 1: 输入 -> 隐层
        self.l1 = nn.Linear(input_size, hidden_size) 
        # Layer 2: 隐层 -> 隐层
        self.l2 = nn.Linear(hidden_size, hidden_size) 
        # Layer 3: 隐层 -> 输出 (类别分数)
        self.l3 = nn.Linear(hidden_size, num_classes)
        # 激活函数
        self.relu = nn.ReLU()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播逻辑
        x: (batch_size, input_size)
        return: (batch_size, num_classes)
        """
        out = self.l1(x)
        out = self.relu(out) # 过滤负数特征
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # 注意：这里不需要 Softmax，因为 CrossEntropyLoss 内部包含了 Softmax
        return out

# ==========================================
# 5. 主流程 (Main)
# ==========================================

if __name__ == '__main__':
    # --- A. 数据预处理 ---
    all_words: List[str] = []
    tags: List[str] = []
    xy: List[Tuple[List[str], str]] = [] # 临时存放 (分词后的句子, 标签)

    # 1. 遍历原始数据，构建词表
    for intent in raw_intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = tokenize(pattern) # 使用 Jieba 分词
            all_words.extend(w)   # 把分出来的词加入总词表
            xy.append((w, tag))

    # 2. 清洗词表 (去重 + 排序)
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    print(f"📊 统计: 词汇量 {len(all_words)} | 意图类别 {len(tags)}")

    # 3. 生成训练矩阵
    X_train_list = []
    y_train_list = []

    for (pattern_sentence, tag) in xy:
        # X: 词袋向量 [0, 1, 0, ...]
        bag = bag_of_words(pattern_sentence, all_words)
        X_train_list.append(bag)
        
        # y: 标签索引 (例如 'greeting' -> 0)
        label = tags.index(tag)
        y_train_list.append(label)

    X_train = np.array(X_train_list)
    y_train = np.array(y_train_list)

    # --- B. 配置训练 ---
    # 超参数
    BATCH_SIZE = 8
    HIDDEN_SIZE = 16
    OUTPUT_SIZE = len(tags)
    INPUT_SIZE = len(all_words)
    LEARNING_RATE = 0.001
    NUM_EPOCHS = 1000

    # 加载器
    dataset = ChatDataset(X_train, y_train)
    train_loader = DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)

    # 初始化模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = NeuralNet(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE).to(device)

    # 损失函数与优化器
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # --- C. 开始训练 ---
    print("🚀 开始训练模型...")
    for epoch in range(NUM_EPOCHS):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)
            
            # 1. 前向
            outputs = model(words)
            loss = criterion(outputs, labels)
            
            # 2. 反向
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        if (epoch+1) % 200 == 0:
            print(f'Epoch [{epoch+1}/{NUM_EPOCHS}], Loss: {loss.item():.4f}')

    print("✅ 训练完成！")

    # --- D. 模拟预测 (Inference) ---
    print("\n💬 进入对话模式 (输入 'q' 退出)")
    
    model.eval() # 切换到评估模式 (锁定 Dropout 等层)
    
    while True:
        sentence = input("你: ")
        if sentence == "q":
            break

        # 1. 处理输入 (和训练时一样的步骤)
        sentence = tokenize(sentence)      # 分词
        X = bag_of_words(sentence, all_words) # 转向量
        
        # 2. 维度调整 (1, input_size)
        # 因为模型想要的是一批数据 (Batch)，哪怕只有一条，也要扩充维度
        X = X.reshape(1, X.shape[0]) 
        X = torch.from_numpy(X).to(device) # 转 Tensor

        # 3. 预测
        with torch.no_grad(): # 这一步不需要算梯度，省内存
            output = model(X)
        
        # 4. 解析结果
        # torch.max 返回 (最大值, 最大值索引)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        # 5. 计算置信度 (Softmax)
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            print(f"Bot (意图: {tag}, 置信度: {prob.item():.2f}): ", end="")
            # 找到对应意图的回复
            for intent in raw_intents['intents']:
                if intent['tag'] == tag:
                    import random
                    print(random.choice(intent['responses']))
        else:
            print("Bot: 我没听懂... (置信度太低)")