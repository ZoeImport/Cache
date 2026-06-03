# Arch Linux 安装与配置指南

> 从零开始的 Arch Linux 安装笔记，涵盖 Btrfs 文件系统、GRUB 引导、国内源配置等实操细节。

---

## 目录

- [pacman 包管理器](#pacman包管理器)
- [yay (AUR) 包管理器](#yay-aur-包管理器)
- [系统安装](#系统安装)

---

## pacman包管理器

| 命令 | 描述 |
|------|------|
| pacman -S | 安装包 |
| pacman -U | 安装本地包 |
| pacman -R | 只删除包不安装依赖 |
| pacman -Q | 查询本地包数据库 |
| pacman -Syu | 对整个系统进行更新，先同步再更新 |
| pacman -Rs | 在删除软件包的同时也删除其依赖 |
| pacman -Rd | 删除包是不检查依赖 |
| pacman -Ss | 搜索包含关键字的包 |
| pacman -Qi | 查看有关包名的信息 |
| pacman -Sw | 只下载不安装 |
| pacman -Sc | 清理未安装的包文件 |
| pacman -Scc | 清理所有的缓存文件 |

## yay (AUR) 包管理器

> 自动更新同步包：`yay`
>
> 清理包数据库中的不需要的依赖：`yay -Yc`
>
> yay 可以使用 pacman 下的所有功能，并且拥有部分拓展功能

## 系统安装

### 安装前的准备

- 准备 Arch Linux 镜像
- 制作启动 U 盘（实体机安装）
- 虚拟机准备设置（虚拟机安装）

### 分盘前的准备工作

```bash
systemctl stop reflector.service   # 停止 reflector 服务
timedatectl set-ntp true            # 设置系统时间
vim /etc/pacman.d/mirrorlist        # 配置国内源
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
```

### 分盘

```bash
# cfdisk 是一个图形化磁盘分区工具
cfdisk /dev/sdxn
# 或者
cfdisk /dev/nvmexn1
# 创建 btrfs 分区，swap 分区，efi 分区
# 分区后使用 lsblk 复查
```

### 格式化对应分区

#### 格式化 EFI 分区

```bash
mkfs.fat -F32 /dev/sdxn           # SATA 磁盘类型
mkfs.fat -F32 /dev/nvmexn1pn      # NVME 磁盘类型
```

#### 格式化 swap 分区

```bash
mkswap /dev/sdxn          # SATA 磁盘类型
mkswap /dev/nvmexn1pn     # NVME 磁盘类型
```

#### 格式化 Btrfs 分区

```bash
mkfs.btrfs -L myArch /dev/sdxn       # SATA 磁盘
mkfs.btrfs -L myArch /dev/nvmexn1pn  # NVME 磁盘
# -L 后的为 Label，表示此分区标签
```

### 创建并挂载 Btrfs 子卷及 swap 和 boot 分区

```bash
mount -t btrfs -o compress=zstd /dev/sdxn /mnt       # SATA
mount -t btrfs -o compress=zstd /dev/nvmexn1pn /mnt  # NVME
# -t 选项后指定挂载分区的文件系统类型
# -o 选项后添加挂载参数
# compress=zstd 开启透明压缩

df -h   # 复查分区挂载情况

# 创建 Btrfs 子卷
btrfs subvolume create /mnt/@       # 创建 / 目录子卷
btrfs subvolume create /mnt/@home   # 创建 /home 子卷

# 复查子卷情况
btrfs subvolume list -p /mnt

# 卸载 /mnt 挂载子卷
umount /mnt

mount -t btrfs -o subvol=/@,compress=zstd /dev/sdxn /mnt         # 挂载 / 目录
mkdir /mnt/home
mount -t btrfs -o subvol=/@home,compress=zstd /dev/sdxn /mnt/home # 挂载 /home 目录
mkdir -p /mnt/boot/efi
mount /dev/sdxn /mnt/boot/efi     # 挂载 boot 目录
swapon /dev/sdxn                   # 挂载交换分区

# 复查 swap 分区挂载情况
free -h
```

### 安装系统基础包

```bash
# 对 /etc/pacman.conf 文件添加 archlinuxcn 源
vim /etc/pacman.conf
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch

pacstrap /mnt base base-devel linux linux-firmware btrfs-progs
pacstrap /mnt dhcpcd networkmanager vim sudo zsh zsh-completions

# 若出现 GPG 证书错误更新 archlinux keyring
pacman -S archlinuxcn-keyring
# 或者
pacman-key --init
pacman-key --populate archlinux
pacman-key --populate archlinuxcn
```

### 生成 fstab 文件

```bash
genfstab -U /mnt > /mnt/etc/fstab   # 自动生成并写入 fstab
cat /mnt/etc/fstab                   # 复查文件
```

### change root

```bash
arch-chroot /mnt
```

### 设置主机名与时区

```bash
vim /etc/hostname         # 设置主机名，例如 myarch
vim /etc/hosts
127.0.0.1   localhost
::1         localhost
127.0.1.1   myarch.localdomain myarch

# 设置时区
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 硬件时间设置
hwclock --systohc

# 设置 Locale
vim /etc/locale.gen   # 去掉 en_US.UTF-8 UTF-8 及 zh_CN.UTF-8 UTF-8 行前的注释符号
locale-gen
echo 'LANG=en_US.UTF-8' > /etc/locale.conf
```

### 设置 root 密码

```bash
passwd root
```

### 安装微码

```bash
pacman -S intel-ucode   # Intel
pacman -S amd-ucode     # AMD
```

### 安装引导程序

```bash
pacman -S grub efibootmgr os-prober
# os-prober 用于双系统检测 Windows
# efibootmgr 被 grub 脚本用来将启动项写入 NVRAM
```

### 安装 GRUB 到 EFI 分区

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ARCH
# --efi-directory=/boot —— 将 grubx64.efi 安装到 EFI 分区
# --bootloader-id=ARCH —— 取名为 ARCH

vim /etc/default/grub
# 去掉 GRUB_CMDLINE_LINUX_DEFAULT 一行中最后的 quiet 参数
# 把 loglevel 的数值从 3 改成 5（方便排错）
# 加入 nowatchdog 参数（显著提高开关机速度）
# 为了引导 win10，添加新的一行 GRUB_DISABLE_OS_PROBER=false
```

```bash
grub-mkconfig -o /boot/grub/grub.cfg
# 推荐安装 update-grub
pacman -S update-grub
update-grub
```

### 完成安装

```bash
exit
umount -R /mnt
reboot
```

### 设置开机自启服务

```bash
systemctl enable --now NetworkManager
```

```bash
# 若为无线连接
nmcli dev wifi list
nmcli dev wifi connect "name_wifi" password "passwd"

# 查看系统信息
pacman -S neofetch
neofetch

# 关机
shutdown -h now
```
