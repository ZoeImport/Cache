"""
对比学习 (Contrastive Learning) — SimCLR on CIFAR-10
=======================================================
依赖: torch>=2.1.0, torchvision, numpy, matplotlib, scikit-learn

涵盖 (Covers):
  1. SimCLR 数据增强 (SimCLR Data Augmentation)
  2. InfoNCE 对比损失 (InfoNCE Contrastive Loss)
  3. 编码器 + 投影头 (Encoder + Projection Head)
  4. 训练循环 (Training Loop)
  5. k-NN 表征质量评估 (k-NN Representation Quality)
  6. t-SNE 可视化 (t-SNE Visualization)

数学公式 (Mathematical Formulation):
  InfoNCE Loss:
    L = -log[exp(sim(z_i,z_j)/tau) / sum_k exp(sim(z_i,z_k)/tau)]

  Similarity:
    sim(u, v) = u^T v / (||u|| ||v||)

  MI lower bound:
    I(x; y) >= log(K) - L_InfoNCE
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as T
from torch.utils.data import DataLoader
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

# ============================================================
# 0. 全局设置 (Global Settings)
# ============================================================
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"  Device: {DEVICE}")

plt.rcParams.update({
    "figure.dpi": 120,
    "font.size": 11,
    "axes.titlesize": 13,
    "figure.figsize": (10, 6),
})

SEED = 42
torch.manual_seed(SEED)
np.random.seed(SEED)

# ============================================================
# 1. SimCLR 数据增强 (SimCLR Data Augmentation)
# ============================================================
class SimCLRAugmentation:
    """
    SimCLR 风格的数据增强: 随机裁剪 + 色彩扭曲 + 高斯模糊 + 水平翻转
    Reference: SimCLR v1 (Chen et al., 2020)
    """

    def __init__(self, image_size=32):
        self.train_transform = T.Compose([
            T.RandomResizedCrop(image_size, scale=(0.2, 1.0)),
            T.RandomHorizontalFlip(p=0.5),
            T.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1),
            T.RandomApply([T.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0))], p=0.5),
            T.ToTensor(),
            T.Normalize([0.4914, 0.4822, 0.4465],
                        [0.2470, 0.2435, 0.2616]),
        ])


class ContrastiveDataset(torch.utils.data.Dataset):
    """包装 CIFAR-10: 每个样本返回两个增强视图"""

    def __init__(self, root="./data", train=True, download=True):
        self.dataset = torchvision.datasets.CIFAR10(
            root=root, train=train, download=download
        )
        self.aug = SimCLRAugmentation()

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        x, label = self.dataset[idx]
        x1 = self.aug.train_transform(x)
        x2 = self.aug.train_transform(x)
        return x1, x2, label


# ============================================================
# 2. 编码器与投影头 (Encoder & Projection Head)
# ============================================================
class Encoder(nn.Module):
    """编码器: ResNet-18 适配 CIFAR-10 的 32x32 输入, 输出 512 维"""

    def __init__(self, out_dim=512):
        super().__init__()
        self.backbone = torchvision.models.resnet18(num_classes=out_dim)
        self.backbone.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.backbone.maxpool = nn.Identity()

    def forward(self, x):
        return self.backbone(x)


class ProjectionHead(nn.Module):
    """投影头: 2 层 MLP (512 -> 512 -> 128), SimCLR 关键组件"""

    def __init__(self, in_dim=512, hidden_dim=512, out_dim=128):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, out_dim),
        )

    def forward(self, x):
        return self.mlp(x)


class SimCLR(nn.Module):
    """SimCLR: Encoder f(.) + Projection Head g(.)"""

    def __init__(self, encoder_out_dim=512, proj_hidden_dim=512, proj_out_dim=128):
        super().__init__()
        self.encoder = Encoder(out_dim=encoder_out_dim)
        self.projection = ProjectionHead(encoder_out_dim, proj_hidden_dim, proj_out_dim)

    def forward(self, x):
        h = self.encoder(x)
        z = self.projection(h)
        return h, z


# ============================================================
# 3. InfoNCE 对比损失 (InfoNCE Contrastive Loss)
# ============================================================
class InfoNCELoss(nn.Module):
    """
    InfoNCE 损失 (NT-Xent Loss)
    L = -log[exp(sim(z_i,z_j)/tau) / sum_k exp(sim(z_i,z_k)/tau)]
    """

    def __init__(self, temperature=0.1):
        super().__init__()
        self.temperature = temperature

    def forward(self, z_i, z_j):
        N, d = z_i.shape

        # L2 normalize
        z_i = F.normalize(z_i, dim=1)
        z_j = F.normalize(z_j, dim=1)

        # Concatenate: (2N, d)
        representations = torch.cat([z_i, z_j], dim=0)

        # Similarity matrix: (2N, 2N)
        sim_matrix = representations @ representations.T / self.temperature

        # Labels: for i in [0,N-1], positive is i+N; for i in [N,2N-1], positive is i-N
        labels = torch.arange(N, device=z_i.device)
        labels = torch.cat([labels + N, labels])

        # Mask out self-contrast
        mask = torch.eye(2 * N, dtype=torch.bool, device=z_i.device)
        sim_matrix = sim_matrix.masked_fill(mask, -float("inf"))

        loss = F.cross_entropy(sim_matrix, labels)
        return loss


# ============================================================
# 4. k-NN 表征质量评估 (k-NN Evaluation)
# ============================================================
@torch.no_grad()
def extract_features(model, loader):
    """提取编码器输出作为表征向量"""
    model.eval()
    features, labels = [], []
    for x, _, y in loader:
        x = x.to(DEVICE)
        h, _ = model(x)
        features.append(h.cpu())
        labels.append(y)
    return torch.cat(features).numpy(), torch.cat(labels).numpy()


def knn_evaluate(X_train, y_train, X_test, y_test, k=5):
    """使用 k-NN 分类器评估表征质量"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    knn = KNeighborsClassifier(n_neighbors=k, metric="cosine")
    knn.fit(X_train_scaled, y_train)
    accuracy = knn.score(X_test_scaled, y_test)
    return accuracy


# ============================================================
# 5. 可视化 (Visualization)
# ============================================================
def plot_augmentation_pairs(dataset, save_path, num_pairs=4):
    """可视化数据增强后的正样本对"""
    fig, axes = plt.subplots(num_pairs, 2, figsize=(5, 2 * num_pairs))
    for i in range(num_pairs):
        x1, x2, _ = dataset[i]
        mean = torch.tensor([0.4914, 0.4822, 0.4465]).view(3, 1, 1)
        std = torch.tensor([0.2470, 0.2435, 0.2616]).view(3, 1, 1)
        x1_vis = (x1 * std + mean).clamp(0, 1).permute(1, 2, 0).numpy()
        x2_vis = (x2 * std + mean).clamp(0, 1).permute(1, 2, 0).numpy()

        axes[i, 0].imshow(x1_vis)
        axes[i, 0].axis("off")
        axes[i, 0].set_title(f"View A - sample {i}", fontsize=9)

        axes[i, 1].imshow(x2_vis)
        axes[i, 1].axis("off")
        axes[i, 1].set_title(f"View B - sample {i}", fontsize=9)

    plt.suptitle("SimCLR Augmentation: Positive Pairs", fontsize=13, y=1.02)
    plt.tight_layout()
    fig.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [Figure] Augmentation pairs saved: {save_path}")


def plot_tsne(features, labels, save_path, title="t-SNE of Learned Representations"):
    """t-SNE 可视化表征空间"""
    if len(features) > 2000:
        idx = np.random.choice(len(features), 2000, replace=False)
        features_sub = features[idx]
        labels_sub = labels[idx]
    else:
        features_sub = features
        labels_sub = labels

    tsne = TSNE(n_components=2, perplexity=30, random_state=SEED, n_iter=2000)
    features_2d = tsne.fit_transform(features_sub)

    class_names = [
        "airplane", "automobile", "bird", "cat", "deer",
        "dog", "frog", "horse", "ship", "truck",
    ]
    colors = plt.cm.tab10(np.arange(10))

    fig, ax = plt.subplots(figsize=(9, 7))
    for cls in range(10):
        mask = labels_sub == cls
        ax.scatter(
            features_2d[mask, 0], features_2d[mask, 1],
            c=[colors[cls]], label=class_names[cls],
            s=15, alpha=0.7, edgecolors="none",
        )

    ax.set_title(title)
    ax.legend(loc="best", markerscale=2, fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
    print(f"  [Figure] t-SNE visualization saved: {save_path}")


def plot_training_curve(losses, knn_accs, save_path):
    """绘制训练曲线"""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    axes[0].plot(losses, linewidth=1.5)
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Contrastive Loss")
    axes[0].set_title("InfoNCE Loss Curve")
    axes[0].grid(alpha=0.3)

    axes[1].plot(knn_accs, linewidth=1.5, color="green")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("k-NN Accuracy")
    axes[1].set_title("k-NN Evaluation (k=5, cosine distance)")
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    fig.savefig(save_path)
    plt.close(fig)
    print(f"  [Figure] Training curve saved: {save_path}")


# ============================================================
# 6. 训练循环 (Training Loop)
# ============================================================
def train_epoch(model, loader, optimizer, criterion, epoch):
    """训练一个 epoch"""
    model.train()
    total_loss = 0.0
    n_batches = len(loader)

    for batch_idx, (x1, x2, _) in enumerate(loader):
        x1, x2 = x1.to(DEVICE), x2.to(DEVICE)

        _, z1 = model(x1)
        _, z2 = model(x2)

        loss = criterion(z1, z2)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

        if batch_idx == 0 or (batch_idx + 1) % 50 == 0:
            mi_lb = np.log(2 * x1.size(0) - 2) - loss.item()
            print(f"  Epoch {epoch:3d} | Batch {batch_idx+1:3d}/{n_batches} | "
                  f"Loss = {loss.item():.4f} | MI lower bound ~ {mi_lb:.2f} nats")

    return total_loss / n_batches


# ============================================================
# 7. 主函数 (Main)
# ============================================================
def main():
    print("=" * 72)
    print("  SimCLR Contrastive Learning Demo on CIFAR-10")
    print("=" * 72)

    # Configuration
    BATCH_SIZE = 128
    EPOCHS = 30
    LR = 3e-4
    TEMPERATURE = 0.1
    KNN_EVAL_EVERY = 5

    print(f"\n  Config:")
    print(f"    Batch size: {BATCH_SIZE}")
    print(f"    Epochs: {EPOCHS}")
    print(f"    Learning rate: {LR}")
    print(f"    Temperature: {TEMPERATURE}")

    # ---- Step 1: Data ----
    print("\n" + "=" * 72)
    print("Step 1: Load CIFAR-10 Dataset")
    print("=" * 72)

    train_dataset = ContrastiveDataset(root="./data", train=True, download=True)
    test_dataset = ContrastiveDataset(root="./data", train=False, download=True)

    train_loader = DataLoader(
        train_dataset, batch_size=BATCH_SIZE,
        shuffle=True, num_workers=0, pin_memory=True, drop_last=True
    )

    # ---- Augmentation visualization ----
    plot_augmentation_pairs(train_dataset, OUTPUT_DIR / "augmentation_pairs.png")

    # ---- Step 2: Model ----
    print("\n" + "=" * 72)
    print("Step 2: Initialize SimCLR Model")
    print("=" * 72)

    model = SimCLR().to(DEVICE)
    criterion = InfoNCELoss(temperature=TEMPERATURE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"  ResNet-18 (CIFAR) + MLP projection")
    print(f"  Total parameters: {total_params:,}")

    # ---- Step 3: Training ----
    print("\n" + "=" * 72)
    print("Step 3: Train Contrastive Learning Model")
    print("=" * 72)

    losses = []
    knn_accs = []

    for epoch in range(1, EPOCHS + 1):
        avg_loss = train_epoch(model, train_loader, optimizer, criterion, epoch)
        losses.append(avg_loss)
        scheduler.step()

        if epoch % KNN_EVAL_EVERY == 0 or epoch == 1:
            eval_train_loader = DataLoader(
                train_dataset, batch_size=256,
                shuffle=False, num_workers=0, pin_memory=True
            )
            eval_test_loader = DataLoader(
                test_dataset, batch_size=256,
                shuffle=False, num_workers=0, pin_memory=True
            )
            print(f"  [Eval] Extracting features...")
            X_train_feat, y_train_labels = extract_features(model, eval_train_loader)
            X_test_feat, y_test_labels = extract_features(model, eval_test_loader)
            acc = knn_evaluate(X_train_feat, y_train_labels, X_test_feat, y_test_labels)
            knn_accs.append(acc)
            print(f"  [Eval] Epoch {epoch} | k-NN Accuracy = {acc:.4f}")

        print(f"  --> Epoch {epoch:3d} done | Avg Loss = {avg_loss:.4f}")

    # ---- Step 4: Final Evaluation ----
    print("\n" + "=" * 72)
    print("Step 4: Final Evaluation")
    print("=" * 72)

    eval_train_loader = DataLoader(
        train_dataset, batch_size=256,
        shuffle=False, num_workers=0, pin_memory=True
    )
    eval_test_loader = DataLoader(
        test_dataset, batch_size=256,
        shuffle=False, num_workers=0, pin_memory=True
    )

    X_train_feat, y_train_labels = extract_features(model, eval_train_loader)
    X_test_feat, y_test_labels = extract_features(model, eval_test_loader)

    final_acc = knn_evaluate(X_train_feat, y_train_labels, X_test_feat, k=5)
    print(f"\n  Final k-NN accuracy (k=5, cosine): {final_acc:.4f}")

    # ---- Step 5: Visualization ----
    print("\n" + "=" * 72)
    print("Step 5: Visualization")
    print("=" * 72)

    plot_training_curve(losses, knn_accs, OUTPUT_DIR / "contrastive_training_curve.png")
    plot_tsne(X_test_feat, y_test_labels, OUTPUT_DIR / "tsne_representations.png",
              title="t-SNE: Contrastive Learning Representations (CIFAR-10 test)")

    print("\n" + "=" * 72)
    print("  SimCLR Contrastive Learning Demo Complete!")
    print(f"  Final k-NN accuracy: {final_acc:.4f}")
    print("=" * 72)


if __name__ == "__main__":
    main()
