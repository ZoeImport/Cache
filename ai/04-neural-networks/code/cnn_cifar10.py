"""
CNN 实战：从零实现 ResNet 并在 CIFAR-10 上训练
(CNN in Action: Implementing ResNet from Scratch on CIFAR-10)
================================================================
依赖 (Dependencies): torch>=2.1.0, torchvision>=0.16.0, matplotlib>=3.7.0, numpy>=1.24.0

涵盖 (Covers):
  1. CIFAR-10 数据加载与增强 (Data Loading & Augmentation)
  2. ResidualBlock / BasicBlock 从零实现 (Building a Residual Block)
  3. ResNet 模型组装 (Assembling the ResNet Architecture)
  4. 完整训练循环与日志 (Training Loop with Epoch Logging)
  5. 损失曲线可视化 (Training Curve Visualization)
  6. 模型保存 (Model Checkpointing)

数学核心 (Mathematical Core):
  Residual Block:  H(x) = F(x) + x
    - F(x):  Conv3x3 -> BN -> ReLU -> Conv3x3 -> BN
    - 捷径 (Shortcut):  x 直接传递给输出
    - 当维度不匹配时，shortcut 通过 1x1 卷积调整维度

运行 (Usage):
  python cnn_cifar10.py            # 训练 10 个 epoch
  python cnn_cifar10.py --epochs 5 # 训练 5 个 epoch
"""

import argparse
import os
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

# ============================================================
# 0. 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# 可重现性
RNG = torch.manual_seed(42)
np.random.seed(42)

# 超参数
BATCH_SIZE = 128
NUM_EPOCHS = 5  # 保持低 epoch 以便快速验证
LEARNING_RATE = 0.1
MOMENTUM = 0.9
WEIGHT_DECAY = 5e-4

# CIFAR-10 类别名称
CIFAR10_CLASSES = [
    "airplane", "automobile", "bird", "cat", "deer",
    "dog", "frog", "horse", "ship", "truck",
]


# ============================================================
# 1. Residual Block 实现 (ResidualBlock Implementation)
# ============================================================

class ResidualBlock(nn.Module):
    """
    残差块 (Residual Block) -- ResNet 的核心构建单元。

    数学定义 (Mathematical Definition):
        output = F(x) + shortcut(x)

    其中 F(x) 包含两个 3x3 卷积层，shortcut 根据维度是否匹配选择：
      - 如果输入/输出通道相同：shortcut = identity（恒等映射）
      - 如果输入/输出通道不同：shortcut = 1x1 卷积（调整维度 + 步长下采样）
    """

    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        # 主路径 F(x): Conv3x3 -> BN -> ReLU -> Conv3x3 -> BN
        self.conv1 = nn.Conv2d(
            in_channels, out_channels, kernel_size=3,
            stride=stride, padding=1, bias=False,
        )
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3,
            stride=1, padding=1, bias=False,
        )
        self.bn2 = nn.BatchNorm2d(out_channels)

        # 捷径 (Shortcut / Skip Connection)
        # 当维度不匹配时（stride!=1 或 in!=out），使用 1x1 卷积调整
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(
                    in_channels, out_channels, kernel_size=1,
                    stride=stride, bias=False,
                ),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.shortcut = nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播 (Forward Pass):
            y = F(x) + shortcut(x)

        Args:
            x: 输入张量, shape (N, C_in, H, W)

        Returns:
            y: 输出张量, shape (N, C_out, H/stride, W/stride)
        """
        # 主路径
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))

        # 捷径连接
        shortcut = self.shortcut(x)

        # 残差相加 + ReLU
        out = F.relu(out + shortcut)
        return out


# ============================================================
# 2. ResNet 模型定义 (ResNet Model Definition)
# ============================================================

class ResNet(nn.Module):
    """
    ResNet 实现 -- 适配 CIFAR-10（小尺寸图像 32x32）

    架构 (Architecture):
        Conv1(3->16, 3x3) -> Block1(16->16) x N -> Block2(16->32) x N
        -> Block3(32->64) x N -> AvgPool -> FC(64->10)

    参数 (Parameters):
        num_blocks: 每个阶段的残差块数量（列表）
        num_classes: 类别数量（CIFAR-10 为 10）
    """

    def __init__(self, num_blocks: list, num_classes: int = 10):
        super().__init__()

        # CIFAR-10 版本的 ResNet 使用 3x3 卷积替代 7x7（因为图像只有 32x32）
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)

        # 三个阶段 (Stages)，通道数依次为 16->32->64
        self.layer1 = self._make_layer(16, 16, blocks=num_blocks[0], stride=1)
        self.layer2 = self._make_layer(16, 32, blocks=num_blocks[1], stride=2)
        self.layer3 = self._make_layer(32, 64, blocks=num_blocks[2], stride=2)

        # 全局平均池化 + 全连接分类头
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(64, num_classes)

        # 权重初始化
        self._initialize_weights()

    def _make_layer(
        self, in_channels: int, out_channels: int,
        blocks: int, stride: int,
    ) -> nn.Sequential:
        """
        构建一个阶段 (Stage)，包含多个残差块。

        第一个 block 可能进行下采样（stride=2）和通道数变化，
        后续 block 保持空间尺寸和通道数不变。
        """
        layers = []
        # 第一个 block 负责下采样和通道变换
        layers.append(ResidualBlock(in_channels, out_channels, stride=stride))
        # 后续 block 保持尺寸
        for _ in range(1, blocks):
            layers.append(ResidualBlock(out_channels, out_channels, stride=1))
        return nn.Sequential(*layers)

    def _initialize_weights(self):
        """Kaiming 初始化适配 ReLU"""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.avg_pool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x


def resnet20() -> ResNet:
    """
    构建 ResNet-20（适合 CIFAR-10）:
    每个阶段 3 个残差块，共 (3x3)+1 = 10 个卷积层
    """
    return ResNet(num_blocks=[3, 3, 3])


def resnet32() -> ResNet:
    """ResNet-32: 每个阶段 5 个残差块"""
    return ResNet(num_blocks=[5, 5, 5])


# ============================================================
# 3. 数据加载 (Data Loading)
# ============================================================

def get_cifar10_loaders(
    batch_size: int = 128,
    num_workers: int = 2,
) -> tuple[DataLoader, DataLoader]:
    """
    加载 CIFAR-10 数据集，带数据增强。

    增强策略 (Augmentation Strategy):
      - 训练: RandomCrop(32, padding=4) + RandomHorizontalFlip + Normalize
      - 测试: 仅 Normalize

    Returns:
        (train_loader, test_loader)
    """
    # 训练集：带数据增强
    train_transform = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=(0.4914, 0.4822, 0.4465),
            std=(0.2023, 0.1994, 0.2010),
        ),
    ])

    # 测试集：仅标准化
    test_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=(0.4914, 0.4822, 0.4465),
            std=(0.2023, 0.1994, 0.2010),
        ),
    ])

    # 下载并加载数据集
    train_dataset = torchvision.datasets.CIFAR10(
        root="./data", train=True, download=True, transform=train_transform,
    )
    test_dataset = torchvision.datasets.CIFAR10(
        root="./data", train=False, download=True, transform=test_transform,
    )

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=True,
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True,
    )

    print(f"Train samples: {len(train_dataset)}")
    print(f"Test samples:  {len(test_dataset)}")
    print(f"Batches per epoch (train): {len(train_loader)}")
    print()

    return train_loader, test_loader


# ============================================================
# 4. 训练与评估 (Training & Evaluation)
# ============================================================

def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    device: torch.device,
) -> tuple[float, float]:
    """
    训练一个 epoch。

    Returns:
        (avg_loss, accuracy)
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)

        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 统计
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    avg_loss = running_loss / total
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float]:
    """
    评估模型（无梯度计算）。

    Returns:
        (avg_loss, accuracy)
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    avg_loss = running_loss / total
    accuracy = 100.0 * correct / total
    return avg_loss, accuracy


# ============================================================
# 5. 可视化 (Visualization)
# ============================================================

def plot_training_curve(
    train_losses: list[float],
    train_accs: list[float],
    test_losses: list[float],
    test_accs: list[float],
    save_path: Path,
):
    """
    绘制训练曲线：损失和准确率随 epoch 变化。
    """
    epochs = range(1, len(train_losses) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # 损失曲线
    ax1.plot(epochs, train_losses, "b-o", label="Train Loss", markersize=4)
    ax1.plot(epochs, test_losses, "r-s", label="Test Loss", markersize=4)
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss")
    ax1.set_title("Training & Test Loss")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 准确率曲线
    ax2.plot(epochs, train_accs, "b-o", label="Train Acc", markersize=4)
    ax2.plot(epochs, test_accs, "r-s", label="Test Acc", markersize=4)
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Accuracy (%)")
    ax2.set_title("Training & Test Accuracy")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Training curve saved to: {save_path}")


# ============================================================
# 6. 主程序 (Main)
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Train ResNet on CIFAR-10")
    parser.add_argument("--epochs", type=int, default=NUM_EPOCHS, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--lr", type=float, default=LEARNING_RATE, help="Learning rate")
    args = parser.parse_args()

    print("=" * 60)
    print("ResNet on CIFAR-10 -- Training Starting")
    print("=" * 60)
    print(f"Device:        {DEVICE}")
    print(f"Epochs:        {args.epochs}")
    print(f"Batch size:    {args.batch_size}")
    print(f"Learning rate: {args.lr}")
    print(f"Weight decay:  {WEIGHT_DECAY}")
    print(f"Momentum:      {MOMENTUM}")
    print()

    # --- 数据加载 ---
    print("[1/4] Loading data...")
    train_loader, test_loader = get_cifar10_loaders(batch_size=args.batch_size)

    # --- 模型构建 ---
    print("[2/4] Building ResNet-20 model...")
    model = resnet20().to(DEVICE)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters:     {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Model architecture:\n{model}")
    print()

    # --- 损失函数与优化器 ---
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(
        model.parameters(),
        lr=args.lr,
        momentum=MOMENTUM,
        weight_decay=WEIGHT_DECAY,
    )
    # 学习率调度：每 30 epoch 衰减为原来的 1/10
    scheduler = optim.lr_scheduler.MultiStepLR(
        optimizer, milestones=[30, 60, 90], gamma=0.1,
    )

    # --- 训练循环 ---
    print("[3/4] Starting training...")
    print("-" * 80)
    print(f"{'Epoch':>6} | {'Train Loss':>11} | {'Train Acc':>10} | "
          f"{'Test Loss':>10} | {'Test Acc':>9} | {'Time':>8}")
    print("-" * 80)

    best_test_acc = 0.0
    train_losses, train_accs = [], []
    test_losses, test_accs = [], []

    for epoch in range(1, args.epochs + 1):
        start_time = time.time()

        # 训练一个 epoch
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, DEVICE,
        )

        # 在测试集上评估
        test_loss, test_acc = evaluate(
            model, test_loader, criterion, DEVICE,
        )

        epoch_time = time.time() - start_time

        # 记录
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)

        # 更新学习率
        scheduler.step()

        # 打印 epoch 结果
        print(f"{epoch:>6} | {train_loss:>11.4f} | {train_acc:>9.2f}% | "
              f"{test_loss:>10.4f} | {test_acc:>8.2f}% | {epoch_time:>7.1f}s")

        # 保存最佳模型
        if test_acc > best_test_acc:
            best_test_acc = test_acc
            model_path = OUTPUT_DIR / "resnet20_cifar10_best.pth"
            torch.save(model.state_dict(), model_path)
            print(f"  -> Best model saved! (test_acc={test_acc:.2f}%)")

    print("-" * 80)
    print(f"Training completed! Best test accuracy: {best_test_acc:.2f}%")
    print()

    # --- 可视化 ---
    print("[4/4] Plotting training curve...")
    curve_path = OUTPUT_DIR / "training_curve.png"
    plot_training_curve(
        train_losses, train_accs,
        test_losses, test_accs,
        curve_path,
    )

    # --- 最终保存 ---
    final_model_path = OUTPUT_DIR / "resnet20_cifar10_final.pth"
    torch.save(model.state_dict(), final_model_path)
    print(f"Final model saved to: {final_model_path}")
    print()
    print("Done!")


if __name__ == "__main__":
    main()
