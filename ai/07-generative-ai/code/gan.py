"""
GAN 实战: 从零实现生成对抗网络并在 MNIST 上训练
(GAN in Action: Implementing Generative Adversarial Network from Scratch on MNIST)
================================================================================
依赖 (Dependencies): torch>=2.1.0, torchvision>=0.16.0, matplotlib>=3.7.0, numpy>=1.24.0

涵盖 (Covers):
  1. GAN 模型: Generator + Discriminator (MLP)
  2. 完整训练循环与逐 epoch 日志
  3. D/G 损失曲线可视化
  4. 不同 epoch 的生成样本对比 (1, 50, 100, 200)
  5. D 对真假样本的准确率统计

数学核心 (Mathematical Core):
  min_G max_D V(D,G) = E_x[log D(x)] + E_z[log(1 - D(G(z)))]

运行 (Usage):
  python gan.py                       # 默认训练 200 个 epoch
  python gan.py --epochs 100          # 训练 100 个 epoch
  python gan.py --latent-dim 64       # 64 维潜在空间
"""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
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
print(f"PyTorch version: {torch.__version__}")
print()


# ============================================================
# 1. GAN 模型定义 (GAN Model Definition)
# ============================================================
class Generator(nn.Module):
    """生成器: 从随机噪声 z 生成图像 G(z).

    Generator: maps random noise z to image G(z).

    架构: z -> Linear(128) -> ReLU -> Linear(256) -> ReLU -> Linear(512) -> ReLU -> Linear(784) -> Tanh
    """

    def __init__(self, latent_dim: int = 100, img_dim: int = 784):
        super().__init__()
        self.latent_dim = latent_dim
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 128),
            nn.ReLU(True),
            nn.Linear(128, 256),
            nn.ReLU(True),
            nn.Linear(256, 512),
            nn.ReLU(True),
            nn.Linear(512, img_dim),
            nn.Tanh(),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.model(z)


class Discriminator(nn.Module):
    """判别器: 判断输入图像是真实 (1) 还是伪造 (0).

    Discriminator: classifies input image as real (1) or fake (0).

    架构: x -> Linear(512) -> LeakyReLU -> Linear(256) -> LeakyReLU -> Linear(1) -> Sigmoid
    """

    def __init__(self, img_dim: int = 784):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(img_dim, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


# ============================================================
# 2. 权重初始化 (Weight Initialization)
# ============================================================
def weights_init(m: nn.Module):
    """使用正态分布初始化权重 (DCGAN 初始化方案).

    Initialize weights with normal distribution (DCGAN scheme).
    """
    classname = m.__class__.__name__
    if classname.find("Linear") != -1:
        nn.init.normal_(m.weight.data, 0.0, 0.02)
        if m.bias is not None:
            nn.init.constant_(m.bias.data, 0)


# ============================================================
# 3. 数据加载 (Data Loading)
# ============================================================
def get_mnist_loaders(batch_size: int = 128):
    """加载 MNIST 数据集.

    Load MNIST dataset.

    返回 (Returns):
        train_loader, test_loader
    """
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])

    train_dataset = torchvision.datasets.MNIST(
        root=str(OUTPUT_DIR.parent / "data"),
        train=True,
        download=True,
        transform=transform,
    )
    test_dataset = torchvision.datasets.MNIST(
        root=str(OUTPUT_DIR.parent / "data"),
        train=False,
        download=True,
        transform=transform,
    )

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader


# ============================================================
# 4. 训练函数 (Training Function)
# ============================================================
def train_epoch(
    G: nn.Module,
    D: nn.Module,
    loader: DataLoader,
    optimizer_G: optim.Optimizer,
    optimizer_D: optim.Optimizer,
    criterion: nn.BCELoss,
    latent_dim: int,
    device: torch.device,
) -> tuple:
    """训练一个 epoch.

    Train for one epoch.

    返回 (Returns):
        epoch_loss_D, epoch_loss_G, epoch_acc_real, epoch_acc_fake
    """
    G.train()
    D.train()

    total_loss_D = 0.0
    total_loss_G = 0.0
    correct_real = 0
    correct_fake = 0
    total = 0

    for images, _ in loader:
        batch_size = images.size(0)
        images = images.view(batch_size, -1).to(device)

        real_labels = torch.ones(batch_size, 1, device=device)
        fake_labels = torch.zeros(batch_size, 1, device=device)

        # --- 训练判别器 (Train Discriminator) ---
        outputs_real = D(images)
        loss_real = criterion(outputs_real, real_labels)

        z = torch.randn(batch_size, latent_dim, device=device)
        fake_images = G(z)
        outputs_fake = D(fake_images.detach())
        loss_fake = criterion(outputs_fake, fake_labels)

        loss_D = loss_real + loss_fake

        optimizer_D.zero_grad()
        loss_D.backward()
        optimizer_D.step()

        # --- 训练生成器 (Train Generator) ---
        z = torch.randn(batch_size, latent_dim, device=device)
        fake_images = G(z)
        outputs = D(fake_images)
        loss_G = criterion(outputs, real_labels)

        optimizer_G.zero_grad()
        loss_G.backward()
        optimizer_G.step()

        # 统计 (Statistics)
        total_loss_D += loss_D.item() * batch_size
        total_loss_G += loss_G.item() * batch_size

        predicted_real = (outputs_real > 0.5).float()
        predicted_fake = (outputs_fake < 0.5).float()
        correct_real += (predicted_real == real_labels).sum().item()
        correct_fake += (predicted_fake == fake_labels).sum().item()
        total += batch_size

    avg_loss_D = total_loss_D / total
    avg_loss_G = total_loss_G / total
    acc_real = correct_real / total * 100
    acc_fake = correct_fake / total * 100

    return avg_loss_D, avg_loss_G, acc_real, acc_fake


# ============================================================
# 5. 可视化函数 (Visualization Functions)
# ============================================================
@torch.no_grad()
def save_sample_images(
    G: nn.Module,
    epoch: int,
    latent_dim: int,
    device: torch.device,
    output_dir: Path,
    nrows: int = 5,
    ncols: int = 10,
):
    """生成并保存样本图像.

    Generate and save sample images.
    """
    G.eval()
    z = torch.randn(nrows * ncols, latent_dim, device=device)
    samples = G(z).view(-1, 1, 28, 28).cpu()

    grid = torchvision.utils.make_grid(samples, nrow=ncols, normalize=True)
    grid_np = grid.numpy().transpose(1, 2, 0)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(grid_np, cmap="gray")
    ax.set_title(f"Generated Samples - Epoch {epoch}", fontsize=14)
    ax.axis("off")
    fig.savefig(output_dir / f"gan_samples_epoch_{epoch:03d}.png", dpi=100, bbox_inches="tight")
    plt.close(fig)


def plot_loss_curves(
    epochs: list,
    losses_D: list,
    losses_G: list,
    acc_real: list,
    acc_fake: list,
    output_dir: Path,
):
    """绘制 D/G 损失曲线和准确率曲线.

    Plot D/G loss curves and accuracy curves.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(epochs, losses_D, "b-", label="Discriminator Loss", linewidth=1.5)
    ax1.plot(epochs, losses_G, "r-", label="Generator Loss", linewidth=1.5)
    ax1.axhline(y=np.log(2), color="gray", linestyle="--", alpha=0.5, label=f"log(2)={np.log(2):.3f}")
    ax1.set_xlabel("Epoch", fontsize=12)
    ax1.set_ylabel("Loss", fontsize=12)
    ax1.set_title("D / G Loss Curves", fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    ax2.plot(epochs, acc_real, "g-", label="D(real) Accuracy", linewidth=1.5)
    ax2.plot(epochs, acc_fake, "m-", label="D(fake) Accuracy", linewidth=1.5)
    ax2.axhline(y=50, color="gray", linestyle="--", alpha=0.5, label="50% (random)")
    ax2.set_xlabel("Epoch", fontsize=12)
    ax2.set_ylabel("Accuracy (%)", fontsize=12)
    ax2.set_title("Discriminator Accuracy", fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_dir / "gan_loss_curves.png", dpi=100, bbox_inches="tight")
    plt.close(fig)


# ============================================================
# 6. 主函数 (Main)
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="GAN on MNIST")
    parser.add_argument("--epochs", type=int, default=200, help="number of epochs (default: 200)")
    parser.add_argument("--batch-size", type=int, default=128, help="batch size (default: 128)")
    parser.add_argument("--latent-dim", type=int, default=100, help="latent dimension (default: 100)")
    parser.add_argument("--lr", type=float, default=0.0002, help="learning rate (default: 0.0002)")
    args = parser.parse_args()

    EPOCHS = args.epochs
    BATCH_SIZE = args.batch_size
    LATENT_DIM = args.latent_dim
    LR = args.lr

    print("=" * 60)
    print("GAN Training on MNIST")
    print("=" * 60)
    print(f"  Epochs:        {EPOCHS}")
    print(f"  Batch size:    {BATCH_SIZE}")
    print(f"  Latent dim:    {LATENT_DIM}")
    print(f"  Learning rate: {LR}")
    print(f"  Device:        {DEVICE}")
    print("=" * 60)
    print()

    train_loader, test_loader = get_mnist_loaders(BATCH_SIZE)
    print(f"Train samples: {len(train_loader.dataset)}")
    print(f"Test samples:  {len(test_loader.dataset)}")
    print()

    G = Generator(latent_dim=LATENT_DIM).to(DEVICE)
    D = Discriminator().to(DEVICE)

    G.apply(weights_init)
    D.apply(weights_init)

    params_G = sum(p.numel() for p in G.parameters())
    params_D = sum(p.numel() for p in D.parameters())
    print(f"Model parameters:")
    print(f"  Generator:     {params_G:,}")
    print(f"  Discriminator: {params_D:,}")
    print(f"  Total:         {params_G + params_D:,}")
    print()

    optimizer_G = optim.Adam(G.parameters(), lr=LR, betas=(0.5, 0.999))
    optimizer_D = optim.Adam(D.parameters(), lr=LR, betas=(0.5, 0.999))
    criterion = nn.BCELoss()

    print("Starting training...")
    print("-" * 79)
    header = f" {'Epoch':>5} | {'D Loss':>7} | {'G Loss':>7} | {'D(real) acc':>11} | {'D(fake) acc':>11} | {'D(x)':>6} | {'D(G(z))':>8}"
    print(header)
    print("-" * 79)

    losses_D = []
    losses_G = []
    accs_real = []
    accs_fake = []
    sample_epochs = [1, 50, 100, 200]

    for epoch in range(1, EPOCHS + 1):
        loss_D, loss_G, acc_real, acc_fake = train_epoch(
            G, D, train_loader, optimizer_G, optimizer_D, criterion, LATENT_DIM, DEVICE
        )

        losses_D.append(loss_D)
        losses_G.append(loss_G)
        accs_real.append(acc_real)
        accs_fake.append(acc_fake)

        if epoch == 1 or epoch % 10 == 0 or epoch == EPOCHS:
            G.eval()
            D.eval()
            with torch.no_grad():
                sample_real, _ = next(iter(test_loader))
                sample_real = sample_real.view(sample_real.size(0), -1).to(DEVICE)
                d_real_mean = D(sample_real).mean().item()

                z_test = torch.randn(sample_real.size(0), LATENT_DIM, device=DEVICE)
                d_fake_mean = D(G(z_test)).mean().item()
            G.train()
            D.train()

            print(
                f" {epoch:>5} | {loss_D:>7.3f} | {loss_G:>7.3f} |"
                f" {acc_real:>9.2f}% | {acc_fake:>9.2f}% |"
                f" {d_real_mean:>6.3f} | {d_fake_mean:>8.3f}"
            )

        if epoch in sample_epochs:
            save_sample_images(G, epoch, LATENT_DIM, DEVICE, OUTPUT_DIR)

    print("-" * 79)
    print(f"Training complete! ({EPOCHS} epochs)")
    print()

    plot_loss_curves(
        list(range(1, EPOCHS + 1)),
        losses_D,
        losses_G,
        accs_real,
        accs_fake,
        OUTPUT_DIR,
    )

    print("Sample images saved:")
    for ep in sample_epochs:
        if ep <= EPOCHS:
            print(f"  {OUTPUT_DIR / f'gan_samples_epoch_{ep:03d}.png'}")
    print(f"  {OUTPUT_DIR / 'gan_loss_curves.png'}")
    print()

    print("=" * 60)
    print("Final Results")
    print("=" * 60)
    print(f"  Discriminator Loss:   {losses_D[-1]:.3f}")
    print(f"  Generator Loss:       {losses_G[-1]:.3f}")
    print(f"  D(real) Accuracy:     {accs_real[-1]:.2f}%")
    print(f"  D(fake) Accuracy:     {accs_fake[-1]:.2f}%")
    print("=" * 60)


if __name__ == "__main__":
    main()
