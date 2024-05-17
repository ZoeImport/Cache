# 计算机网络体系

## OSI体系结构（七层）（Open System Interconnection Reference Model）

***应用层***：**为应用程序或用户请求提供各种请求服务**。OSI参考模型最高层，也是最靠近用户的一层，为计算机用户、各种应用程序以及网络提供接口，也为用户直接提供各种网络服务。

***表示层***：**数据编码、格式转换、数据加密**。提供各种用于应用层数据的编码和转换功能,确保一个系统的应用层发送的数据能被另一个系统的应用层识别。如果必要，该层可提供一种标准表示形式，用于将计算机内部的多种数据格式转换成通信中采用的标准表示形式。数据压缩和加密也是表示层可提供的转换功能之一。

***会话层***：**创建、管理和维护会话**。接收来自传输层的数据，负责建立、管理和终止表示层实体之间的通信会话，支持它们之间的数据交换。该层的通信由不同设备中的应用程序之间的服务请求和响应组成。

***传输层***：**数据通信**。建立主机端到端的链接，为会话层和网络层提供端到端可靠的和透明的数据传输服务，确保数据能完整的传输到网络层。

***网络层***：**IP选址及路由选择**。通过路由选择算法，为报文或通信子网选择最适当的路径。控制数据链路层与传输层之间的信息转发，建立、维持和终止网络的连接。数据链路层的数据在这一层被转换为数据包，然后通过路径选择、分段组合、顺序、进/出路由等控制，将信息从一个网络设备传送到另一个网络设备。

***数据链路层***：**提供介质访问和链路管理**。接收来自物理层的位流形式的数据，封装成帧，传送到网络层；将网络层的数据帧，拆装为位流形式的数据转发到物理层；负责建立和管理节点间的链路，通过各种控制协议，将有差错的物理信道变为无差错的、能可靠传输数据帧的数据链路。

***物理层***：**管理通信设备和网络媒体之间的互联互通**。传输介质为数据链路层提供物理连接，实现比特流的透明传输。实现相邻计算机节点之间比特流的透明传送，屏蔽具体传输介质和物理设备的差异。

## TCP/IP结构（四层）

***应用层***：主要有负责web浏览器的HTTP协议， 文件传输的FTP协议，负责电子邮件的SMTP协议，负责域名系统的DNS等。

***传输层***：主要是有可靠传输的TCP协议，特别高效的UDP协议。主要负责传输应用层的数据包。

***网络层***：主要是IP协议。主要负责寻址（找到目标设备的位置）

***链路层***：主要是负责转换数字信号和物理二进制信号。

## 五层协议体系结构

***应用层***：应用层是网络协议的最高层，主要任务通过进程间的交互完成特定网络应用。应用层协议定义的是应用程序（进程）间通信和交互的规则。

***传输层***：：它负责为两台主机中的进程提供通信服务。该层主要有以下两种协议：

传输控制协议 (Transmission Control Protocol，TCP)：提供面向连接的、可靠的数据传输服务，数据传输的基本单位是报文段（segment）：用户数据报协议 (User Datagram Protocol，UDP)：提供无连接的、尽最大努力的数据传输服务，但不保证数据传输的可靠性，数据传输的基本单位是用户数据报。

***网络层***：网络层负责为分组网络中的不同主机提供通信服务，并通过选择合适的路由将数据传递到目标主机。在发送数据时，网络层把运输层产生的报文段或用户数据封装成分组或 包进行传送。

​				*PS*：在TCP/IP体系中，由于网络层使用IP协议，因此分组也叫IP数据报

***数据链路层***：数据链路层通常简称为链路层。数据链路层在两个相邻节点传输数据时，将网络层交下来的IP数据报组装成帧，在两个相邻节点之间的链路上传送帧

***物理层***：保数据可以在各种物理媒介上进行传输，为数据的传输提供可靠的环境。

******

# 网络协议（Internet protocol）

## TCP协议（Transmission Protocol）

***应用层次：传输层	***

TCP/IP协议是互联网的基础协议，包括传输控制协议（TCP）和网络协议（IP），它们共同构成了互联网的通信协议标准。

### 三次握手

三次握手的过程如下：
客户端发送SYN包（SYN=1，ACK=0）给服务器端，进入SYN_SENT状态。

服务器端收到SYN包，发送一个SYN包（SYN=1，ACK=1）和确认包ACK（ACK=1）给客户端，进入SYN_RCVD状态。

客户端收到服务器端的SYN和ACK包，发送一个确认包ACK（ACK=1）给服务器端，建立连接，进入ESTABLISHED状态。

### 四次挥手

四次挥手的过程如下：
客户端发送一个FIN包（FIN=1）给服务器端，请求关闭连接，进入FIN_WAIT_1状态。

服务器端收到FIN包，发送一个确认包ACK（ACK=1）给客户端，进入CLOSE_WAIT状态。

服务器端关闭连接，发送一个FIN包（FIN=1）给客户端，进入LAST_ACK状态。

客户端收到服务器端的FIN包，发送一个确认包ACK（ACK=1）给服务器端，进入TIME_WAIT状态。在等待2MSL（最大报文段寿命）后，进入CLOSED状态。服务器端收到客户端的确认包ACK后，进入CLOSED状态。

## http协议（HyperText Transfer Protocol）

***应用层次：应用层***

超文本传输协议（HTTP）是一种用于传输超媒体文档（如HTML）的协议，是Web的基础协议。

***架构在TCP协议上***

> 请求数据分三部分
>
> 请求行:GET表示请求方式,HTTP/1.1 表示协议版本
>
> 请求头:格式为键值对形式
>
> 请求体:POST请求的最后一部分,存放请求参数
>
> ***GET与POST的请求区别:GET的请求参数在请求行中,没有请求体,POST请求请求参数在请求体中,GET请求参数大小有限制***

> 响应数据分3部分
>
> 响应行:HTTP/1.1表示协议版本,响应状态码,状态码描述
>
> 响应头:键值对形式
>
> 响应体:存放响应数据
>
> | 状态码分类 | 说明       |
> | ---------- | ---------- |
> | 1XX        | 响应中     |
> | 2XX        | 成功       |
> | 3XX        | 重定向     |
> | 4XX        | 客户端错误 |
> | 5XX        | 服务端错误 |
>
> 

## https协议（HyperText Transfer Protocol over Secure Socket Layer）

HTTP+SSL/TLS， 即 HTTP 下加入 SSL 层，HTTPS 的安全基础是 SSL，因此加密的详细内容就需要 SSL，用于安全的 HTTP 数据传输。

## DNS协议（Domain Name System）

***应用层次：应用层***

DNS（Domain Name System：域名系统），与 HTTP、FTP 和 SMTP 一样，DNS 协议也是应用层的协议，用于将用户提供的主机名（域名）解析为 IP 地址。

简单来说，DNS 就像是一个自动的电话号码簿，我们可以直接拨打 47.105.127.0 呼叫对方，但这不方便记录、记忆，DNS 提供一种手段能够让我们直接拨打对方的域名找到对方

## FTP协议（File Transfer Protocol）

***应用层次：传输层***

***B/S架构***

***默认端口：22***

是应用层的一个**文件传输协议** 。主要作用是在服务器和客户端之间实现文件的传输和共享。FTP协议运行在TCP连接上，保证了文件传输的可靠性。在传输时，传输双方的操作系统、磁盘文件系统类型可以不同。

允许TCP/IP网络上的两台计算机之间进行文件传输。而FTP服务是基于FTP协议的文件传输服务。工作时，一台计算机上运行FTP客户端应用程序，另一台计算机上需要运行FTP服务器端程序。只有拥有了FTP服务，客户端才能进行文件传输。

## SMTP协议（Simple Mail Transfer Protocol）

***默认端口：25***

SMTP是一种提供可靠且有效的电子邮件传输的协议。SMTP是建立在FTP文件传输服务上的一种邮件服务，主要用于系统之间的邮件信息传递，并提供有关来信的通知。SMTP独立于特定的传输子系统，且只需要可靠有序的数据流信道支持，SMTP的重要特性之一是其能跨越网络传输邮件，即“SMTP邮件中继”。使用SMTP，可实现相同网络处理进程之间的邮件传输，也可通过中继器或网关实现某处理进程与其他网络之间的邮件传输。

## POP3协议（Post Office Protocol - Version 3）

POP3，全名为“Post Office Protocol - Version 3”，即“邮局协议版本3”。是TCP/IP协议族中的一员，由RFC1939 定义。本协议主要用于支持使用客户端远程管理在服务器上的电子邮件。提供了SSL加密的POP3协议被称为POP3S。
POP 协议支持“离线”邮件处理。其具体过程是：邮件发送到服务器上，电子邮件客户端调用邮件客户机程序以连接服务器，并下载所有未阅读的电子邮件。这种离线访问模式是一种存储转发服务，将邮件从邮件服务器端送到个人终端机器上，一般是PC机或 MAC。一旦邮件发送到 PC 机或MAC上，邮件服务器上的邮件将会被删除。但POP3邮件服务器大都可以“只下载邮件，服务器端并不删除”，也就是改进的POP3协议。

## IMAP协议（Internet Message Access Protocol）

***应用层次：应用层***

***默认端口：143	***

IMAP（Internet Message Access Protocol）以前称作交互邮件访问协议（Interactive Mail Access Protocol），是一个应用层协议。IMAP是斯坦福大学在1986年开发的一种邮件获取协议。它的主要作用是邮件客户端可以通过这种协议从邮件服务器上获取邮件的信息，下载邮件等。当前的权威定义是RFC3501。IMAP协议运行在TCP/IP协议之上，使用的端口是143。它与POP3协议的主要区别是用户可以不用把所有的邮件全部下载，可以通过客户端直接对服务器上的邮件进行操作。

## SSL协议（Secure Socket Layer）

***应用层次：传输层***

SSL（Secure Socket Layer）安全套接层是Netscape公司率先采用的网络安全协议。它是在传输通信协议（TCP/IP）上实现的一种安全协议，采用公开密钥技术。SSL广泛支持各种类型的网络，同时提供三种基本的安全服务，它们都使用公开密钥技术。

## TLS协议（Transport Layer Security）

***应用层次：传输层***

安全传输层协议（TLS）用于在两个通信应用程序之间提供保密性和数据完整性。
该协议由两层组成： TLS 记录协议（TLS Record）和 TLS 握手协议（TLS Handshake）

## UDP协议（User Datagram Protocol）	

***应用层次：传输层***

是一个简单的面向消息的传输层协议，尽管UDP提供标头和有效负载的完整性验证（通过校验和），但它不保证向上层协议提供消息传递，并且UDP层在发送后不会保留UDP 消息的状态。因此，UDP有时被称为不可靠的数据报协议。如果需要传输可靠性，则必须在用户应用程序中实现。

UDP使用具有最小协议机制的简单无连接通信模型。UDP提供数据完整性的校验和，以及用于在数据报的源和目标寻址不同函数的端口号。它没有握手对话，因此将用户的程序暴露在底层网络的任何不可靠的方面。如果在网络接口级别需要纠错功能，应用程序可以使用为此目的设计的传输控制协议（TCP）。



# Linux

## Arch Linux

### pacman包管理器

| 命令        | 描述                             |
| ----------- | -------------------------------- |
| pacman -S   | 安装包                           |
| pacman -U   | 安装本地包                       |
| pacman -R   | 只删除包不安装依赖               |
| pacman -Q   | 查询本地包数据库                 |
| pacman -Syu | 对整个系统进行更新，先同步再更新 |
| pacman -Rs  | 在删除软件包的同时也删除其依赖   |
| pacman -Rd  | 删除包是不检查依赖               |
| pacman -Ss  | 搜索包含关键字的包               |
| pacman -Qi  | 查看有关包名的信息               |
| pacman -Sw  | 只下载不安装                     |
| pacman -Sc  | 清理未安装的包文件               |
| pacman -Scc | 清理所有的缓存文件               |



### yay包管理器

> 自动更新同步包 ：
>
> ​	yay
>
> 清理包数据库中的不需要的依赖
>
> ​	yay -Y -c	yay -Yc
>
> ***yay可以使用pacman下的所有功能，并且用有部分拓展功能***

### 系统安装

##### 安装前的准备

###### 准备ArchLinux镜像

###### 制作启动U盘（实体机安装）

###### 虚拟机准备设置（虚拟机安装）

##### 分盘前的准备工作

```bash
systemctl stop reflector.service	#停止reflextor服务
timedatectl set-ntp true			#设置系统时间
vim /etc/pacman.d/mirrorlist		#配置国内源
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch
```

##### 分盘

```bash
#cfdisk是一个图形化磁盘分区工具
cfdisk /dev/sdxn
#或者
cfdisk /dev/nvmexn1 
#创建btrfs分区，swap分区，efi分区
#在对磁盘进行分区后，使用lsblk对分区情况进行查看，对分区大小和分区情况切忌复查后再写入
```

##### 格式化对应分区并创建子卷

##### 格式化EFI分区

```bash
mkfs.fat -F32 /dev/sdxn	#SATA磁盘类型
mkfs.fat -F32 /dev/nvmexn1pn	#NVME磁盘类型
```

##### 格式化swap分区

```bash
mkswap /dev/sdxn	#SATA磁盘类型
mkswap /dev/nvmexn1pn	#NVME磁盘类型
```

##### 格式化Btrfs分区

```bash
mkfs.btrfs -L myArch /dev/sdxn	#SATA磁盘
mkfs.btrfs -L myArch /dev/nvmexn1pn	#NVME磁盘
#-L后的为Lable，表示此分区标签
```

##### 创建并挂载Btrfs子卷及swap和boot分区

```bash
mount -t btrfs -o compress=zstd /dev/sdxn /mnt	#SATA
mount -t btrfs -o compress=zstd /dev/nvmexn1pn /mnt  #NVME
#-t	选项后指定挂载分区的文件系统类型
#-o	选项后添加挂载参数
#compress=zstd	开启透明压缩

df -h	#复查分区挂载情况

#创建Btrfs子卷
btrfs subvolume create /mnt/@	#创建/目录子卷
btrfs subvolume	create /mnt/@home	#创建 /home子卷

#复查子卷情况
btrfs subvolume list -p /mnt

#卸载/mnt挂载子卷
umount /mnt

mount -t btrfs -o subvol=/@,compress=zstd /dev/sdxn /mnt	#挂载/目录
mkdir /mnt/home	#创建/home
mount -t btrfs -o subvol=/@home，compress=zstd /dev/sdxn /mnt/home	#挂载/home目录
mkdir -p /mnt/boot/efi	#创建/boot目录
mount /dev/sdxn /mnt/boot/efi	#挂载boot目录
swapon /dev/sdxn	#挂载交换分区


#复查swap分区挂载情况
free -h
```

##### 安装系统基础包

```bash
#对/etc/pacman.conf文件添加archlinuxcn源
vim /etc/pacman.conf
#追加以下几行
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
###########
pacstrap /mnt base base-devel linux linux-firmware btrfs-progs
pacstrap /mnt dhcpcd networkmanager vim sudo zsh zsh-completions
#pacstrap脚本安装基础包linux内核等基础包

	pacman	-S archlinuxcn-keyring	#若出现GPG证书错误更新archlinuxkeyring	
#出现keyring验证错误可以直接使用
#或者
	pacman-key --init
	pacman-key --populate archlinux
	pacman-key --populate archlinuxcn
```

##### 生成fstab文件

```bash
genfstab -U /mnt > /mnt/etc/fstab		#使用genfstab自动根据当前挂载情况生成并写入fstab文件
cat /mnt/etc/fstab						#复查文件
```

##### change root

```bash
arch-chroot /mnt	#切换系统环境
```

##### 设置主机名与时区

```bash
vim /etc/hostname		#设置主机名
#例如设置为myarch
vim /etc/hosts
#加入以内容
127.0.0.1	localhost
::1			localhost
127.0.1.1	myarch.localdomain myarch

#设置时区
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime			#创建符号链接

#硬件时间设置
hwclock --systohc

#设置Locale
vim /etc/locale.gen		#去掉 en_US.UTF-8 UTF-8 以及 zh_CN.UTF-8 UTF-8 行前的注释符号

#生成loacle
locale-gen

echo 'LANG=en_US.UTF-8' > /etc/locale.conf
```

##### 设置root密码

```bash
passwd root
```

##### 安装微码

```bash
pacman -S intel-ucode	#Intel
pacman -S amd-ucode		#AMD
```

##### 安装引导程序

```bash
pacman -S grub efibootmgr os-prober		#此处的os-prober为了双系统能检测到win10
#-S 选项后指定要通过 pacman 包管理器安装的包：
    grub —— 启动引导器
    efibootmgr —— efibootmgr 被 grub 脚本用来将启动项写入 NVRAM
```

##### 安装GRUB到EFI分区

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ARCH
#-efi-directory=/boot —— 将 grubx64.efi 安装到之前的指定位置（EFI 分区）
#--bootloader-id=ARCH —— 取名为 ARCH

vim /etc/default/grub
#    去掉 GRUB_CMDLINE_LINUX_DEFAULT 一行中最后的 quiet 参数
#    把 loglevel 的数值从 3 改成 5。这样是为了后续如果出现系统错误，方便排错
#    加入 nowatchdog 参数，这可以显著提高开关机速度
#	为了引导 win10，则还需要添加新的一行 GRUB_DISABLE_OS_PROBER=false(!!!!!!)
```

```bash
#生成GRUB所需文件
grub-mkconfig -o /boot/grub/grub.cfg
#推荐安装update-grub
pacman -S update-grub
#更新grub文件
update-grub
```



##### 完成安装

```bash
exit
umount -R /mnt
reboot
```

##### 设置开机自启服务

```bash
systemctl enable --now NetworkManager
```

```bash
#若为无线连接
nmcli dev wifi list
nmcli dev wifi connect "name_wifi" password "passwd"

#logo
pacman -S neofetch
neofetch

#关机
shutdown -h now
```



## 基础命令与权限控制

#### cd 

```
cd ..#返还上一级目录
```

```
cd #返回主目录
```

```
cd/ #从根目录开始
```

```
cd -user #进入个人主目录
```

```
cd - #返回上次操作目录
```

#### pwd

```
pwd #显示工作路径
```

#### ls

```
ls #查看目录中的文件
```

```
ls -l #显示目录内容的长列表 
```

***第一列***：第一个字母

​				d 意味着内容是目录或文件夹

​				‘-’ 代表其为文件

​				l 代表其内容是链接文件

​				其余9个字母 分别代表 **文件拥有者**，**文件所有组**，**其他人访问文件**的rwx权限

​					*Ps*： r（可读） w（可写） x（可执行）

***第二列***：有多少个链接指向这个文件

***第三列***：文件/文件夹拥有者

***第四列***：文件/文件夹所有组

***第五列***：文件/文件夹的字节大小

***第六列***：文件的最后修改时间

***第七列***：文件名/目录名

```
ls -lh  #-h参数意味着便于人识别，-h是以1024为单位
```

```
ls -si  #以1000为单位
```

```
ls -lhS #排序文件大小
```

```
ls -l -block-size=SIZE #使用-block-size 改单位的大小
```

***单位列表：*** K = kilobyte	M = Megebyte	G = Gigabyte	T = Terabyte	P = Petabyte

E = Exabyte	Z = Zettabyte	Y = Yottabyte	

```
ls -a	#显示隐藏文件
```

```
ls -d */	#只列出目录条目
```

```
ls -lg	#不打印所有者的信息
```

```
ls -lG	#不打印组信息
```

```
ls -ln	#打印UID/GID信息
```

```
ls --color=never	#不带彩色打印
```

```
ls -li	#打印每个文件的索引号
```

```
ls -p	#增加/（斜线）标记目录
```

```
ls -r	#排序时反转顺序
```

```
ls -R	#可以列出包含他子目录的目录
```

```
ls -IX	#可以使用-X参数或者--sort=extension来通过拓展名来排序
```

```
ls -lt	#按照修改时间排序，新的文件在前
```

```
ls ~	#列出你的主目录
```

```
ls ../	#列出父目录
```

```
ls ../../	#列出两层之上的目录
```

```
ls --version	#打印ls命令版本
```

#### cat

```
cat [-AbeEnstTuv] [--help] [--version] fileName
```

***参数说明***：

​				-n（--number）：对输出行数进行编号（由1开始）

​				-b（--number-nonblank）：与-n类似但是对于空白行不编号

​				-s（--squeeze-blank）：当遇到有连续两行以上的空白行，代替为一行

​				-v（--show-nonprinting）：使用^和M-符号，除了LFD和TAB之外

​				-E（--show-ends）：在每行结束显示$

​				-T（--show-tabs）：将TAB字符显示为^l

​				-A（--show-all）：等价于“-vET”

#### mkdir

```
mkdir [-afwx/] [目录]
```

***参数说明***：

​					-/ ：显示目录下的所有子目录和文件

​					-a：显示隐藏文件

​					-f：不显示磁盘剩余可用空间

​					-w：仅显示目录或文件名称，以横排方式呈现，以便一次显示较多的目录和文件

​					-X：仅显示目录下所有子目录与文件的完整路径，不显示其他信息

#### mv

```
mv [options] source dest
mv [options] source... directory
```

***参数说明***：

​					-b：当目标文件或目录存在时，在执行覆盖前，会为其创建一个备份

​					-i：如果指定移动的源目录或文件与目标的目录或文件同名，会先询问是否覆盖原文件，y/n判断

​					-f：如果指定移动的源目录或文件与目标的目录或文件同名，不会询问直接覆盖

​					-n：不要覆盖任何已存在的文件或者目录

​					-u：当源文件比目标文件新或者目标文件不存在时，才执行移动操作

#### cp

```
cp [options] source dest
cp [options] source...directory
```

***参数说明***：

​					-a：通常在复制目录时使用，保留链接，文件属性，并复制目录下的所有内容，其作用与dpR参数组合

​					-d：复制时保留链接，这里所说的链接相当于Windows中的快捷方式

​					-f：覆盖已经存在的文件而不给出提示

​					-i：再覆盖文件之前会给出y/n选项

​					-p：除复制文件的内容之外，还把修改时间和访问权限也复制到新文件中

​					-r：若给出的源文件是目录文件，此时复制该目录所有子目录和文件

​					-I：不复制文件，只生成链接文件

#### ln

```
ln [参数] [source][dest]

```

***软链接***：1.以路径形式存在，类似于windows的快捷方式

​				2.可以跨越系统，硬链接不可以

​				3.软连接可以对一个不存在的文件名进行链接

​				4.软连接可以对目录进行链接

***硬链接***：

​				1.以文件副本的形式存在，不占用实际空间

​				2.不允许给目录创建链接

​				3.硬链接只有在同一个文件系统中才可以创建

***必要参数***：

​				--backup[=CONTROL]	备份已存在的目标文件

​				-b	类似--backup，不接受参数

​				-d	允许超级用户制作目录的硬链接

​				-f	强制执行

​				-i	y/n交互模式，文件存在则提示用户是否覆盖

​				-n	把符号链接视为一般目录

​				-s	软链接

​				-v	显示详细的处理过程

***必要参数***：

​				-S	-S<字尾备份字符串> 或--suffix=<字尾备份字符串>

​				-V	-V<备份方式>或--version-control=<备份方式>

​				--help	显示帮助信息

​				--version	显示版本信息

#### chmod

> ```shell
> chmod [-cfvr] [--help] [--version] mode file...
> ```
>
> ***mode:***权限设定字符串，格式如下：
>
> ```shell
> [ugoa...] [[+-=] [rwxX]...] [,...]
> ```
>
> ***其中：***
>
> ​		u 表示文件的拥有者，g 表示与该文件的拥有者属于同意群体（group）， o 表示其他以外的人，a 表示三者皆是
>
> ​		+增加权限 -取消权限，=表示唯一设定权限
>
> ​		r可读 w可写 x表可执行 X表示只有当该文件是子目录或者该文件已经被设定过为可执行
>
> ***其他参数：***
>
> ​		-c 若文件权限已经更改，才显示其更改动作
>
> ​		-f 若文件权限无法被更改也不要显示错误信息
>
> ​		-v 显示权限变更的详细材料
>
> ​		-R 对当前目录下的所有文件与子目录进行相同的权限变更（即以递归方式逐个变更）
>
> ​		--help 显示辅助说明
>
> ​		-version 显示版本
>

#### chown

> 该命令用于更改文件的拥有者，即change owner

#### chgrp

> 该命令用于更改用户的当前组
>
> 即对于其对特定命令或者特定的文件进行访问进行即时的权限切换

#### usermod

> ***描述：用于修改用户账号的各项设定***
>
> ```shell
> usermod [-LU][-c <备注>][-d <登入目录>][-e <有效期限>][-f <缓冲天数>][-g <群组>][-G <群组>][-l <帐号名称>][-s <shell>][-u <uid>][用户帐号]
> ```
>
> ***使用说明：***
>
> - -c<备注> 　修改用户帐号的备注文字。
> - -d登入目录> 　修改用户登入时的目录。
> - -e<有效期限> 　修改帐号的有效期限。
> - -f<缓冲天数> 　修改在密码过期后多少天即关闭该帐号。
> - -g<群组> 　修改用户所属的群组。
> - -G<群组> 　修改用户所属的附加群组。
> - -l<帐号名称> 　修改用户帐号名称。
> - -L 　锁定用户密码，使密码无效。
> - -s<shell> 　修改用户登入后所使用的shell。
> - -u<uid> 　修改用户ID。
> - -U 　解除密码锁定。

## 基础工具

### grub

> grub用于引导系统的启动
>
> 系统启动的配置文件为/etc/default/grub文件中，可以对其中的配置项进行修改
>
> 修改完毕通过
>
> ```shell
> sudo update-grub
> ```
>
> 对grub进行更新，此处的update-grub包需要额外下载（有时）



### Vim

***描述：经典的命令行编辑器***

> 使用说明：
>
> ​	概述：对于Vim一共有三种模式，命令模式，输入模式，底线命令模式
>
> ​		命令模式：启动vim打开一个文件后的第一个模式就是命令模式，此时的所有键盘按键只要符合任何一个命令就会被视为一个命令
>
> ​		输入模式：进入文本编辑模式
>
> ​		底线命令模式：输入：后+字符即可使用各种命令
>
> ​	命令模式：
>
> ​			i：切换输入模式，在当前光标进行插入
>
> ​			x：删除当前光标所在处的字符
>
> ​			：：切换到底线命令模式
>
> ​			a：切换输入模式，在光标的下一个位置进行插入
>
> ​			o：在当前行的下一行插入一个新行，并且进入插入模式
>
> ​			O：在当前行的上一行插入一个新行，并且进入插入模式
>
> ​			dd：删除当前行
>
> ​			yy：复制当前行
>
> ​			p：在光标后粘贴剪贴板内容
>
> ​			P：在光标前粘贴剪贴板内容
>
> ​			u：撤销上次操作
>
> ​			Ctrl+r：重做上次撤销的操作
>
> ​		光标快速行切换：
>
> ​			G：移动到文件的最后一行
>
> ​			nG：移动到第n行
>
> ​			gg：移动到文件的第一行相当于	1G
>
> ​			n<Enter>：光标向下移动n行
>
> ​	
>
> ​	底线命令模式：
>
> ​		：q	退出编辑器
>
> ​		：w	保存
>
> ​		：q！	强制退出编辑器，不保存修改
>
> ​		：wq	保存并退出
>
> ​		/word	向下搜索word单词
>
> ​		？word	向上搜索word单词
>
> ​		n		重复上一个操作
>
> ​		N		反向重复上一个操作
>
> ***配置文件：***
>
> **常规配置如下：**
>
> #编辑/etc/vimrc追加如下内容
>
> " 自动缩进
> set autoindent
> set cindent
> " Tab键的宽度
> set tabstop=4
> " 统一缩进为4
> set softtabstop=4
> set shiftwidth=4
> " 不要用空格代替制表符
> set noexpandtab
> " 在行和段开始处使用制表符
> set smarttab
> " 显示行号
> set number
> " 历史记录数
> set history=1000
> "禁止生成临时文件
> set nobackup
> set noswapfile
> "搜索忽略大小写
> set ignorecase
> "搜索逐字符高亮
> set hlsearch
> set incsearch
> "行内替换
> set gdefault
> "编码设置
> set enc=utf-8
> set fencs=utf-8,ucs-bom,shift-jis,gb18030,gbk,gb2312,cp936
> "语言设置
> set langmenu=zh_CN.UTF-8
> set helplang=cn
> " 总是显示状态行
> set laststatus=2
> " 命令行（在状态行下）的高度，默认为1，这里是2
> set cmdheight=2
>
> ***插件管理Vundle：多插件集成的强大vim编辑器，需要编辑一个.vimrc文件在根目录下对其进行多插件配置***

### gzip,bzip2,xz

***描述：文件压缩工具，可以对压缩比进行控制并且对压缩文件进行查看***

> ```shell
> xz -[cdtlk#] fileName
> ```
>
> 使用说明：
>
> ​	-c：将数据在屏幕上输出
>
> ​	-d：解压缩文件
>
> ​	-t：测试文件完整性
>
> ​	-l：列出文件的相关信息
>
> ​	-k：保留原本文件不删除
>
> ​	-#：指定压缩率，0～9依次增加，常规为6
>
> 注：三个工具中xz拥有最高的压缩率，但是对于压缩文件所需时间最多，gzip时间最短

### cut,grep

***描述：cut纵向切割将数据切割为列单位，grep横向选择行对其中内容进行筛选***

> ```shell
> cut -d '分割' -f fields
> cut -c 字符序号区间
> ```
>
> ```shell
> grep [-acinv] [--color=auto] '查找字符' fileName
> ```
>
> ***使用说明：***
>
> ​	-a：将二进制文件以文本文件的方式查找
>
> ​	-c：计算找到的次数
>
> ​	-i：忽略大小写的不同
>
> ​	-n：输出行号
>
> ​	-v：反向选择,即排除满足的行

### sort,uniq,wc

***描述：sort作为排序命令，uniq为剔除重复行操作，wc为计算行数，字数，字符数***

> ```shell
> sort [-fbMnrtuk] [fileName or stdin]
> ```
>
> ***使用说明：***
>
> ​	-f：忽略大小写差异
>
> ​	-b：忽略空格
>
> ​	-M：以月份的数字进行排序
>
> ​	-n：使用纯数字进行排序
>
> ​	-r：反向排序
>
> ​	-u：uniq即仅使用重复行的一行
>
> ​	-t：分隔符号
>
> ​	-k：以哪个区间进行分隔
>
> ```shell
> uniq [-ic]
> ```
>
> ***使用说明：***
>
> ​	-i：忽略大小写的不同
>
> ​	-c：进行计数
>
> ```shell
> wc [-lwm]
> ```
>
> ***使用说明：***
>
> ​	-l：仅列出行号
>
> ​	-w：仅列出多少字
>
> ​	-m：多少字符

### find

***描述：***用于在指定目录下查找文件和目录，它可以使用不同的选项来过滤和限制查找的结果**

> ```shell
> find [path] [expression]
> ```
>
> ***使用说明：***
>
> ​	-name pattern：按文件名查找，支持使用通配符 * 和 ?
> ​	-type type：按文件类型查找，可以是 f（普通文件）、d（目录）、l（符号链接）	等
> ​	-size [+-]size[cwbkMG]：按文件大小查找，支持使用 + 或 - 表示大于或小于指定大	小，单位可以是 c（字节）、w（字数）、b（块数）、k（KB）、M（MB）或 G	（GB）
> ​	-mtime days：按修改时间查找，支持使用 + 或 - 表示在指定天数前或后，days 是	一个整数表示天数
> ​	-user username：按文件所有者查找
> ​	-group groupname：按文件所属组查找
>
> 

### which（脚本文件查找）

***描述的：脚本文件查找***

> ```shell
> which [-a] command
> ```
>
> ***使用说明：***
>
> ​	-a：将所有在PATH中符合的命令均列出

### whereis

***描述：在系统的特定目录查找文件***

> ```shell
> whereis [-bmsu] fileOrDirName
> ```
>
> ***使用说明：***
>
> ​	-l：列出查询的主要几个目录
>
> ​	-b：只查找二进制文件
>
> ​	-m：只查找man手册的说明文件
>
> ​	-s：只查找source源的文件
>
> ​	-u：只查找不再上述三个项目中的文件

### tee

***描述：数据双向重定向***

> ```shell
> tee [-a] fileName
> ```
>
> ***使用说明：***
>
> ​	-a：以追加的方式进行文件输入
>
> 注：tee会将数据流分送到文件与屏幕进行数据的双向重定向

### man	whatis	apropos

> 用与查询某个命令的人工手册

### 管道符	|

***描述：将前一个命令的输入当成后一个命令的输入***

> ```shell
> echo "hello" |cowsay
> ```
>
> ***注：管道命令只会处理标准输出，对于标准错误会忽略；后一个命令必须要接受前一个命令的数据成为标准输入***

### 重定向

***描述：对stdin,stdout,stderr进行数据的重定向***

> ```shell
> echo "hello world" > fileName
> cat > catFileName << "EOF"
> ```
>
> ***使用说明：***
>
> ​	>	>> ：覆盖和追加，对输出流的重定向，也可以是0> 0>>
>
> ​	<	<<：将键盘的标准输入改为文件的输入，对输入流的重定向；结束的输入字符

### 正则表达式

***描述：部分基础表达式与扩展表达式***

> ```shell
> #基础
> ^word	#待查找的word在行首
> word$	#待查找word在行尾
> .		#代表一定有任意一个字符存在
> \		#转义字符
> *		#重复前一个字符0次或无限次
> [list]	#在中括号中列出了待选择的字符，只能选择其中一个
> [n1-n2]	#在中括号中写出了待选择字符的范围
> [^list]	#在中括号中取反，代表不是中括号中的字符元素
> \{n,m\}	#代表前一个元素连续出现n-m次，如果只有{n,}，代表n到无穷次，如果为{n}代表			出现n次
> #扩展
> +		#重复前一个元素一次或一次以上
> ?		#零个或一个前一个元素
> |		#代表或，实现元素的或选择
> ()		#找出群组字符串，将一块元素设定为一组
> ()+		#即前一个群组元素出现一次或者一次以上
> ```

### sed

***描述：按照行为单位进行操作，对其进行增删改***

> ```shell
> sed [-nefr] [操作]
> ```
>
> 使用说明：
>
> ​		-n：设置为安静模式，即只显示出被处理的行
>
> ​		-e：直接在命令行模式进行sed的操作编辑
>
> ​		-f：使用-f filename 实现按照指定脚本文件运行sed
>
> ​		-r：使用拓展式正则表达式
>
> ​		-i：直接修改读取文件的内容
>
> ​	***[n1[,n2] function***
>
> ​		a：新增，相当于追加内容在文件之后
>
> ​		c：替换，直接可以在c之后接字符，会直接替换掉指定的全行
>
> ​		d：删除，直接删除指定行
>
> ​		i：插入，在指定行的前一行创建新行并插入数据
>
> ​		p：打印，对指定行数据进行打印
>
> ​		s：替换，可以直接进行替换，还可以搭配正则表达式进行查找，如			1,20s/old/new/g

### awk

***描述：以行为单位对行的每个列进行单独处理的工具***

> ```shell
> awk '条件1{操作1} 条件2{操作2} 条件3{操作3} ...'
> ```
>
> ***使用说明：***
>
> ​	三个特殊变量：
>
> ​		NF：每一行拥有的字段总数
>
> ​		NR：目前awk所处理的是第几行数据
>
> ​		FS：目前的分隔字符，默认是空格键
>
> ​	相关逻辑运算字符：
>
> ​		< > = ! <= >= ==
>
> ***Ps:***awk的所有操作都是在{}之间的进行

### diff

***描述：文本对比工具，对一个文件的新旧版本进行对比***

> ```shell
> diff [-bBi] from-file to-file
> ```
>
> ***使用说明：***
>
> ​	form-file to-file：分别为原始对比文件名和目标对比文件名
>
> ​	-b：忽略一行当中，仅有的多个空白差异，以可以称为空格差异
>
> ​	-B：忽略空白行的差异
>
> ​	-i：忽略大小写差异
>
> ***Ps：***
>
> ​	1.diff可以直接对比目录，除此之外还有cmp文件进行二进制文件的对比
>
> ​	2.cmp对比为二进制文件拥有选项-l可以列出所有的不同节点，因为其只会输出第一	个发现的不同节点
>
> ​	3.除此之外还有patch工具进行差异文件补丁制作再对旧文件进行更新（待补充）

### sh

***描述：shell脚本的测试工具***

> ```shell
> sh -[ceilox] shell.sh
> ```
>
> ***使用说明：***
>
> ​	用于shell脚本的测试以及多样化运行，包括展示其运行过程，退出方式等





## 有趣的拓展工具

### 其他

##### nmap

###### 基础格式

```
nmap<scan type><option><target>
```

###### 1.扫描指定IP下的地址

```
nmap 162.16.121.125-135
```

此处 IP 范围由破折号分隔

此处可以使用*通配符检测子网下的所有IP

扫描多个IP可以使用逗号隔开

###### 2.扫描指定IP下的指定端口

```
nmap -p <数值> <IP>
```

###### 3.通过发送Ping数据包返回主机信息

```
nmap -sP <IP address>
```

（使用-sP定位机器，确保机器正在响应，或者识别网络中的意外机器）

可以定义为 ping 扫描。在此扫描中，nmap 发送ICMP数据包来检查目标在线，而不是查找端口的状态。由于它只包括 ping 目标系统而不执行任何类型的扫描，因此它比上述扫描模式快太多了。默认情况下，任何目标都是任何扫描中执行的第一步。

###### 4.将扫描后的信息输出为指定格式的文件

```
nmap -oN output.txt example.com
```

```
nmap -oX output.xml example.com
```

###### 5.以指定数量扫描优先的端口

```
nmap –top-ports <numeric value> <IP address/Domain>
```

扫描固定数量的端口

 扫描指定IP的地址前15个端口

###### 6.检测开放端口

```
nmap -open <IP address>
```

检测开放端口  #响应UDP/TCP/SCTP请求的目标端口

###### 7.扫描指定IP同时排除指定IP/端口

```
 nmap <IP address> -exclude<No need IP address>
```

-exclude 接受单个IP地址 单个主机 特定范围和整个网络

###### 8.服务版本以及防火墙检测

```
nmap -sV <IP address> #该命令会返回服务列表和其版本
```

该命令（-sV）可以使用 -version-intensitylevel from 0to9 来确定此次搜索的强度级别

同样可以使用-version-trace 如果扫描结果未达到期望结果，可以使用其显示更详细的信息

```
nmap -sA <IP address>  # 扫描检测防火墙设置
```

###### 9.检测主机的操作系统信息

```
nmap -A <IP address> #发现主机的操作系统信息
```

###### 该命令可以与其它nmap命令结合

```
nmap -O <IP address> # -O启用操作系统检测
```

其他标签包括

-osscan-limit 简单猜测目标系统 

-osscan-guess 更加积极的猜测操作系统

###### 10.隐身模式扫描

```
nmap -sS  <IP address>
```

使用该-sS将启动带有TCP SYN的隐蔽扫描，-sS可以与其它类型的命令结合使用，但是其速度较慢，不会生成日志

###### 11.识别主机名

```
nmap -sL <IP address> 
```

-sL 将找到给给定主机的主机名字，为每个主机完成DNS查询，此外，-n 选项可以用于跳过DNS解析，-R可用于始终解析DNS

-Pn将完全跳过主机发现，而不是将主机视为在线而不管

###### 12.从指定文件扫描

```
nmap -iL /file.txt #如果要扫描的地址列表很长，可以直接通过命令行导入文件
```

###### 13.使用Verbose获取更多的信息

```
nmap -v <Ip address> #该标志将会提供已完成扫描的附加信息，它可以添加到大多数命令中，如果没有-v，nmap只会返回可用的关键信息
```

如果在调试一个棘手的情况，或者需要详细信息时，该命令将会将命令设置为详细模式

###### 14.扫描IPv6地址

```
nmap -6 <IPv6 address> #扫描IPv6的地址
```

###### 15.查找主机接口，路由，数据包

```
nmap --iflist#该命令将生成相关接口和路由的列表
```

```
nmap --packet-trace #该命令将会显示发送和接受的数据包
```

###### 16.控制扫描速度

```
nmap -T5 <IP address> #主动扫描会更快，但会更具破坏性和不准确性 对于大多数扫描T3 T4就可以
```

###### 17.帮助界面

```
nmap -h #显示nmap的命令的帮助界面，包括提供有关可用命令信息
```

###### 18.创建扫描时的诱饵

```
nmap -D <IP address>...#在-D后面加上诱饵地址列表，这些诱饵地址也将显示为他们正在扫描网络，混淆实际正在进行的扫描
```

同样，可以使用诸如

--spoof-mac 欺骗Nmap MAC地址之类的命令，以及-S欺骗源地址的命令

###### 19.通过建立TCP/UDP链接进行扫描

```
nmap -sT <IP address> #通过建立TCP链接进行扫描
```

但是会产生大量的日志，花费更多的时间

```
nmap -sU <IP address> #建立UDP连接进行扫描
```

当只需要进行UDP端口进行扫描时，这是首选，此扫描的结果将仅包含有关在UDP端口上运行的服务和端口状态详细信息

##### timeshift

###### 从 Timeshift 快照中恢复 

Timeshift 还能恢复到其它硬盘用作系统迁移，通过 arch 安装盘重新安装引导即可

若能够进入桌面环境 

直接打开 Timeshift，选择快照后根据提示还原即可。

若无法进入桌面环境

1. 通过 `Ctrl` + `Alt` + `F2 ~ F6` 进入 tty 终端
2. 使用快照还原系统：

```bash
sudo timeshift --list # 获取快照列表
sudo timeshift --restore --snapshot '20XX-XX-XX_XX-XX-XX' --skip-grub # 选择一个快照进行还原，并跳过 GRUB 安装，一般来说 GRUB 不需要重新安装
```

1. 根据提示继续，完成还原

若无法进入系统 

此时系统一般已经完全奔溃，可以通过 Live CD 进行还原。（若使用 arch 安装盘请连接网络和配置好源后安装 Timeshift，然后通过命令行方式还原）

1. 进入 Live 系统后打开 Timeshift，点击设置按钮，设置为原来快照的存储位置。
2. 选择快照后根据提示还原即可。

或者通过命令行进行还原，但需要首先设置原来快照存储的位置：

```bash
sudo timeshift --restore --snapshot-device /dev/sdbx
```

后续步骤同无法进入桌面环境

恢复后无法挂载目录 

Timeshift 恢复 Btrfs 快照时，可能出现由于子卷 ID 变更导致无法挂载目录而无法进入系统。

此时可以通过手动修改 fstab 配置，移除 `subvolid` 参数，改为通过名称指定子卷。

使用 `vim` 编辑器修改 `/etc/fstab` 文件：

```bash
vim /etc/fstab
```

进行如下修改：

- 删除 `/` 和 `/home` 条目中最后的 `subvolid=xxx` 参数

保存后重启即可正常使用。以后恢复快照时无需再次进行此操作。

也可以手动更正 `subvolid` ，通过以下命令查看正确的 ID：

bash

```bash
sudo btrfs sub list -u /
```

定时任务不生效 

Timeshift 设定任务后定时不生效那是因为相关的服务 `cron` 没有启动导致的问题。 在终端命令行下输入以下命令第一行为设置开机启动 第二行为启动相关服务

bash

```bash
sudo systemctl enable --now cronie.service
sudo systemctl start --now cronie.service
```

##### rsync 命令 

 `scp` 这个命令。它常被用来在服务器间传输文件。

但是目前它应该被更现代的工具 ***rsync***替代。其拥有即时压缩、差量传输等新特性。同时， `rsync` 也被用来进行备份操作（Timeshift 的 RSYNC 模式即基于此实现）。

```bash
rsync foo.txt me@server:/home/me/ # 最基础的复制文件。与 scp 的操作完全相同
rsync -a bar/ me@server:/home/me/ # -a：标记实现目录复制等。比 scp -r 能更好的处理符号链接等情况
```



### 命令行相关

##### tmux

工具概述：窗口复用工具，对多个会话实现同时监视以及命令行区域复用

> ***使用介绍***
>
> 前缀键：
>
> ​	Ctrl+b
>
> 新建自定义名字窗口（非内部命令）：
>
> ​	tmux new -s <new session name>
>
> 会话分离（内部命令）：
>
> ​	tmux detch
>
> 重新连接会话（非内部命令）：
>
> ​	tmux attach -t <num>				(使用会话编号)
>
> ​	tmux attach -t <session name> 	（使用会话名称） 
>
> 查看会话列表：
>
> ​	tmux ls
>
> 杀死会话：
>
> ​	tmux kill-session -t <num/session name>
>
> 切换会话：
>
> ​	tmux switch -t <num/session name>
>
> 重命名会话：
>
> ​	tmux rename-session -t <num/session name> <new name>
>
> 快捷键：
>
> ​	前缀键+d：分离当前会话
>
> ​	前缀键+s：列出当前所有会话
>
> ​	前缀键+$ ：重命名当前会话
>
> 窗格切分（内部命令）：
>
> ​	tmux split  	  （上下切分）
>
> ​	tmux split -h	（左右切分）
>
> 光标控制：
>
> ​	前缀键+方向键
>
> 窗格规格控制：
>
> ​	前缀键（长按）+方向键

##### oh my zsh

***描述：优秀的Linux命令行美化拓展包***

> 可以利用其配置文件，对终端的主题，字体。插件进行拓展

##### lolcat

***描述：通过管道符连接变成色彩输出***

> ```shell
> echo "hello world"|lolcat
> ```

##### cowsay

***描述：让一头牛输出信息，可以使用管道符连接***

> ```shell
> echo "hello"|cowsay
> ```

##### sl

***描述：开个小火车？***

> ```shell
> sl
> ```

##### neofetch	uwufetch

***描述：详细输出设备的版本信息***

> ```shell
> neofetch
> uwufetch
> ```

##### googler

***描述：在终端中进行google搜索，对信息进行查询***

> ```shell
> googler hello
> ```
>
> Ps：在国内无法进行google搜索的情况下需要使用科学上网的方法


##### code

***描述：Linux下的vscode***

> ```shell
> code filename
> ```
>
> ***使用方式：***
>
> ​	直接使用code+文件夹或者文件名就可以直接打开，其中插件和功能几乎相同

##### lf

***描述：终端下的文件管理助手***

> ```shell
> lf filename
> ```
>
> 使用说明：
>
> ​	lf可以对文件夹以及文件内容进行预览，利用左右方向键进行层级的选择，到达文件可以在终端的右边预览，终端的是对文件树的层级预览，按q退出，（待补充）

##### colorls

***描述：改进的多色彩ls工具***

> ```shell
> colorls --gs -la
> #对ls的改良可以实现文件的git状态显示，对文件，文件夹等进行多色彩显示
> ```
>
> 使用说明：
>
> ​	colorls与ls的相关选项大部分相同，同时增加了颜色以及git状态查询，还以进行目录树显示，由于命令较长，所以可以与alias结合使用


### 网络工具

##### proxychains

***描述：终端中的代理软件，可以通过proxychains+部分命令实现科学上网***

> ```shell
> proxychains	curl cip.cc
> ```
>
> ***使用方式：***
>
> ​	通过对proxychains的配置文件进行编辑，其中基础的包括：proxychains的运行模式，以及代理所使用的协议，IP端口（部分还需要有账号密码）
>
> ​	常规的例如clash的默认端口为127.0.0.1：7890端口，且无代理的用户密码，就可以直接写入
>
> ```shell
> http	127.0.0.1：7890	
> ```
>
> Ps：proxychains的配置文件地址为/etc/proxychains.conf

##### iptables



# mysql

## 数据类型

***整数类型***

| tinyint     | 1byte  | 小整数       |
| :---------- | ------ | ------------ |
| smallint    | 2bytes | 大整数       |
| mediumint   | 2bytes | 大整数       |
| int/integer | 3bytes | 大整数       |
| bigint      | 4bytes | 极大整数     |
| float       | 8bytes | 单精度浮点数 |
| double      | 4bytes | 双精度浮点数 |
| decimal     | 8bytes | 小数值       |

***字符串类型***

| char       | 定长字符串                 |
| ---------- | -------------------------- |
| varchar    | 变长字符串                 |
| tinyblob   | 不超255个字符的二进制数据  |
| tinytext   | 短文本字符串               |
| blob       | 二进制形式的长文本数据     |
| text       | 长文本数据                 |
| mediumblob | 二进制形式的中等长文本数据 |
| mediumtext | 中等长度文本数据           |
| longblob   | 二进制形式的极大文本数据   |
| longtext   | 极大文本数据               |

***日期类型***

| date      | YYYY-MM-DD          | 日期值                   | 3    |
| --------- | ------------------- | ------------------------ | ---- |
| time      | HH:MM:ss            | 时间值或持续时间         | 3    |
| year      | YYYY                | 年份值                   | 1    |
| datetime  | YYYY-MM-DD HH:MM:ss | 混合日期和时间值         | 8    |
| timestamp | YYYY-MM-DD HH:MM:ss | 混合日期和时间值，时间戳 | 4    |

## 条件运算符

| 比较运算符       | 功能                                       |
| ---------------- | ------------------------------------------ |
| >                | 大于                                       |
| >=               | 大于等于                                   |
| <                | 小于                                       |
| <=               | 小于等于                                   |
| =                | 等于                                       |
| <>或!=           | 不等于                                     |
| between...and... | 在某个范围内（含最大最小）                 |
| in(...)          | 在in之后列表中的值，多选1                  |
| like 占位符      | 模糊匹配（_匹配单个字符，%匹配任意个字符） |
| is null          | 是NULL                                     |

| 逻辑运算符 | 功能   |
| ---------- | ------ |
| and或&&    | 并且   |
| or 或\|\|  | 或者   |
| not或！    | 非不是 |

## 聚合函数

| 函数  | 功能     |
| ----- | -------- |
| count | 统计数量 |
| max   | 最大值   |
| min   | 最小值   |
| avg   | 平均值   |
| sum   | 求和     |

## DDL语句（数据定义语言）

```sql
show databases;#查询所有数据库
select databases();#查询当前数据库
create database[if not exists] 数据库名 [default charset 字符集][collate 排序规则];#创建,直接接名称不用加''
drop database[if exists] 数据库名;#删除
use 数据库名字;#使用
show tables;#查询所有表
desc 表名;#查询表结构
show create table 表名;#查询建表使用的语句
create table 表名(
		字段1 字段1类型[comment 字段1注释],
    	字段2 字段2类型[comment 字段2注释],
    
    	...
    	字段3 字段3类型[comment 字段3注释]

)[comment 表注释];

alter table 表名 add 字段名 类型(长度) [comment 注释] [约束];#添加字段
alter table 表名 modify 字段名 新数据类型(长度);#修改数据类型
alter table 表名 change 旧名字 新字段名 类型(长度) [comment 注释][约束];#修改字段名和数据类型
alter table 表名 drop 字段名;#删除字段
alter table 表名 rename to 新表名;#修改表名

drop table [if exists] 表名;#删除表
truncate table 表名;#删除指定表，并重新创建表
```

## DML语句（数据操作语言）

```sql
insert into 表名(字段1,字段2...)values(值1,值2,...);#给指定字段添加数据
insert into 表名 values(值1，值2,...)#给全部字段添加数据
insert into 表名(字段1,字段2,...)values(值1,值2,...),(值1,值2,...),(值1,值2,...);
insert into 表名 values(值1,值2,...),(值1,值2,...),(值1,值2,...);#批量添加数据
```

```sql
update 表名 set 字段名1=值1,字段名2=值2,字段名3=值3,...[where 条件];
```

```sql
delete from 表名 [where 条件]#删除数据
```

## DQL语句（数据查询语言）

```sql
select 字段列表 from 表名列表 where 条件列表 group by 分组字段列表 having 分组后条件列表 group by 排序字段列表 limit 分页参数
```

```sql
select 字段1,字段2...from 表名;
select from 表名;#查询多个字段
select 字段1[AS 别名1],字段2[AS 别名2]...from 表名#设置别名
select distinct 字段列表 from 表名;#去重
```

### 条件查询

```sql
select 字段列表 from 表名 where 条件列表;
```

### 分组查询

```sql
select 字段列表 from 表名 [where 条件] group by 分组字段名 [having 分组过滤条件];#分组过滤
```

***where与having区别***：

​		**1**.执行时机不同，where是分组之前进行过滤，不满足where条件，不参加分组；而having是分组之后对结果进行过滤

​		**2**.执行条件不同：where不能对聚合函数进行判断，而having可以 

***PS：执行顺序：where>聚合函数>having***

***分组之后，查询的字段一般为聚合函数和分组字段，查询其他字段无任何意义***

### 排序查询

```sql
select 字段列表 from 表名 order by 字段1 排序方式1，字段2 排序方式2;
```

***排序方式：***升序(ASC),降序(DESC)

**Ps:**多字段排序，当第一个字段值相同才会按照第二个字段进行排序

### 分页查询

```sql
select 字段列表 from 表名 limit 起始索引,查询记录数;
```

***Ps：***

​	1.起始索引从0开始，起始索引=（查询页码-1）*每页显示记录数

​	2.分页查询是数据库的方言，不同的数据库有不同的实现，MySQL中是limit

​	3.如果查询的第一页是数据，起始索引可以忽略，直接简写为limit  [num]，此处num为需要查找的序号

### DQL执行顺序

***FROM->WHERE->GROUP BY->HAVING->SELECT->ORDER BY->LIMIT***

***表名列表->条件列表->分组字段列表->分组后条件列表->字段列表->排序字段列表->分页参数***

## DCL（数据控制语言）

***用户操作***

```sql
use mysql;
select *from user;#查询用户
```

```mysql
create user 'user'@'host' identified by 'password';
```

```mysql
alter user 'user'@'host' identified with mysql_native_password by "new password";#修改用户密码
```

```mysql
drop user'user'@'host';#删除用户
```

***PS：主要为DBA人员使用***

***权限控制***

| 权限              | 说明          |
| ----------------- | ------------- |
| all,all privilege | 所有权限      |
| select            | 查询数据      |
| insert            | 插入数据      |
| update            | 修改数据      |
| delete            | 删除数据      |
| alter             | 修改表        |
| drop              | 删除数据库/表 |
| create            | 创建数据库/表 |

```MYSQL
show grants for 'user'@'host';#查询权限
grants 权限列表 on 数据库名,表名 to 'user'@'host';#授予权限
revoke 权限列表 on 数据库名,表名 from 'user'@'host';#撤销权限
```

## 函数

### 字符串函数

| 函数                     | 功能                                                      |
| ------------------------ | --------------------------------------------------------- |
| concat(s1,s2,s3,...)     | 自负床链接，将s1，s2，s3拼接成一个字符串                  |
| lower(str)               | 将字符串全部转为小写                                      |
| upper(str)               | 将字符串转换为大写                                        |
| lpad(str,n,pad)          | 左填充，用字符串pad对str的左边进行填充，达到n个字符长度   |
| rpad(str,n,pad)          | 右填充，用字符串pad对str的右边进行填充，达到n个字符串长度 |
| trim(str)                | 去掉字符串头和尾部的空格                                  |
| substring(str,start,len) | 返回字符串str从start位置起的len个长度的字符串             |

### 数值函数

| 函数       | 功能                               |
| ---------- | ---------------------------------- |
| ceil(x)    | 向上取整                           |
| floor(x)   | 向下取整                           |
| mod(x,y)   | 返回x/y的模                        |
| rand()     | 返回0~1内的随机数                  |
| round(x,y) | 求参数x的四舍五入的值，保留y位小数 |

### 日期函数

| 函数                              | 功能                                            |
| --------------------------------- | ----------------------------------------------- |
| curdate()                         | 返回当前日期                                    |
| curtime()                         | 返回当前时间                                    |
| now()                             | 返回当前日期和时间                              |
| year(date)                        | 获取指定date的年份                              |
| month(date)                       | 获取指定date的月份                              |
| day(date)                         | 获取指定date的日期                              |
| date_add(date,interval expr type) | 返回一个日期/时间值加上一个时间间隔expr后的天数 |
| datediff(date1,date2)             | 返回起始时间date1和结束时间date2之间的天数      |

### 流程函数

| 函数                                                      | 功能                                                     |
| :-------------------------------------------------------- | :------------------------------------------------------- |
| if(value,t,f)                                             | 如果value为true，则返回t，否则返回f                      |
| ifnull(value1,value2)                                     | 如果value不为空，返回value1，否则返回value2              |
| case when [val1] then [res1] ...else [default] end        | 如果value为true，返回res1，...否则返回default默认值      |
| case [expr] when [val1] then [res1] ...else [default] end | 如果expr的值等于val1，返回res1，...否则返回default默认值 |

## 约束

| 约束     | 关键字      |
| -------- | ----------- |
| 非空约束 | NOT NULL    |
| 唯一约束 | UNIQUE      |
| 主键约束 | PRIMARY KEY |
| 默认约束 | DEFAULT     |
| 检查约束 | CHECK       |
| 外键约束 | FOREIGN KEY |

***Ps:作用于字段，为字段添加约束***

### 示例

```mysql
create table employ(
    id int primary key auto_increment comment 'primary key' 
    name varchar(10) not null unique comment 'name',
    age int check ( age>0&&age<=120 ),
    status char(1) default 1,
    gender char(1)
)comment 'employ table';
```

### 外键的添加，删除

```mysql
#创建表时添加
create table house(
    id int primary key auto_increment,
    constraint fk_house_id foreign key(id) references employ(id on update cascade on delete cascade
);

#创建后修改字段
alter table employ ADD CONSTRAINT fk_emp_id foreign key (dept_id) references dept(id) on update on cascade on delete cascade;

#删除外键
alter table employ drop foreign key fk_emp_id;

```

#### 外键的行为

| 行为        | 说明                     |
| ----------- | ------------------------ |
| NO ACTION   | 若更改，则不允许         |
| RESTRICT    | 若更改则不允许           |
| CASCADE     | 若更改则同步操作关联数据 |
| SET NULL    | 若更改则设定NULL         |
| SET DEFAULT | 若更改则设定为默认值     |

## 多表查询

### 多表关系

#### 一对一

***在一方加入外键同时设置为unique***

#### 一对多，多对一

***在多的一方设置外键关联另一方的主键***

#### 多对多

***建立中间的表，中间表包含两个外键，关联两张表的主键***

***笛卡尔积：A，B集合的所有组合情况***

***多表查询需要消除无效的笛卡尔积***

```mysql
select * from a,b where a.id = b.id;
```

### 内连接

***查询a，b表的交集***

*隐式内连接*

```mysql
select * from a,b where a.id = b.id;
select * from use u ,dept d where u.id = d.id;#对表起别名，不能再使用表名进行查询
```

*显示内连接*

```mysql
select * from a inner join b on a.id = b.id;
select * from a join b on a.id = b.id;#省略inner
```

### 外连接

***左外连接：查询左表和交集***

```mysql
select * from a left outer join b on a.id = b.id;
```

***右外连接：右表和交集***

```mysql
select * from a right outer join b on a.id = b.id;
```

***Ps:outer可以省略***

### 自连接

```mysql
select * from U u,dept d where u.id = d.id;
```

## 联合查询

```mysql
select * from a where a.id=1
union all
select * from a where a.age.15;
#union可以对查询结果去重，all保留所有结果，联合查询保证字段数量，数据一致
```

### 子查询

```mysql
select * from t1 where column1=(select column1 from t2);
#子查询外部语句可以是insert select delete update
```

#### ***标量子查询：子查询结果为单个值***

```mysql
select * from emp where dept.id=(select id from dept where name = 'aaa');
```

#### ***列子查询：子查询结果为一列***

| 关键字 | 说明         |
| ------ | ------------ |
| IN     | 在集合中     |
| NOT IN | 不在集合中   |
| ANY    | 任意满足即可 |
| SOME   | 与any相同    |
| ALL    | 必须全部满足 |

```mysql
select * from emp where dept.id in (select id from dept where name='aaa' or name 'bbb');
```

#### ***行子查询：子查询结果为一行***

***常用子查询：=，<,>,	IN,NOT IN***

```mysql
select * from a where (id,name)=(select id,name from b where name='aaa');
```

#### ***表子查询：子查询结果为多行多列（表）***

```mysql
select * from emp where (job,salary) in (select job,salary from emp where name='aaa' or name='bbb');
```

### 案例

```mysql

#查询小于本部门平均工资的员工信息
select * from employ e1 where e1.salary <(select avg(e2.salary) from employ e2 where e2.dept_id=e1.dept_id)


#查询每个部门的员工数量
select id,name ,(select count(*) from employ where employ.id=d.id)'count' from dept d ;


#查询所有的学生信息和选课信息,多表联查（两个外连接，保证没有选课的学生也应出现）
select student.*,c.name
from student left join stu_course on student.id = stu_course.stu_id left join course c on stu_course.course_id = c.id;
```



## 事务

***一组操作的集合，要么同时成功，要么同时失败***

### 事务操作

#### 查看/设置事务的提交方式

```mysql
select @@autocommit;
#1为自动提交，0为手动提交
set @@autocommit=0;
```

#### 提交事务

```mysql
commit；
```

#### 回滚事务

```mysql
rollback;
#在报错时需要使用rollback进行数据回滚
```

#### 开启事务

```mysql
start transaction；
#或
begin;
```

### 四大特性

***A原子性：不可分割***

***C一致性：事务完成需要保证数据是一致状态***

***I隔离性：保证各个事务是独立环境运行***

***D持久性：事务一旦提交，对数据的改变是永久的***

### 并发事务问题

***脏读：读取到另一个事务未提交的数据***

***不可重复读：对一条记录进行两次读取，但两次读取数据不同***

***幻读：查询数据时未查询到，但在插入时又发现该数据已存在***

### 事务的隔离级别

| 隔离级别                 | 脏读 | 不可重复读 | 幻读 |
| ------------------------ | ---- | ---------- | ---- |
| Read uncommitted         | 1    | 1          | 1    |
| Read committed           | 0    | 1          | 1    |
| Repeatable Read(default) | 0    | 0          | 1    |
| Serializable             | 0    | 0          | 0    |

#### 查看事务的隔离级别

```mysql
select @@transaction——isolation;
```

#### 设置事务的隔离级别

```mysql
set[session|global] transaction isolation level [read uncommitted|read committed|repeatable read |serializable]
```

















# Shell

## 数值计算方式

| 计算方法                        | 实例                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| declare定义整数型，直接进行运算 | declare两个整数型a，b，c=a+b                                 |
| expr或；let                     | expr 整数运算表达式  let 整数运算表达式，其中let可以运算多个表达式，expr除了可以运算计算表达式之外，还可以对字符串进行操作 |
| $(()) 或者 $[]                  | $(( 计算表达式 )) 或者 $[ 计算表达式 ]                       |
| bc 计算                         | bc可以对文件中的计算式进行计算，同时也可以进行管道计算 "计算表达式 \| bc [ options ]"，其中可以进行进制转换，内置数学函数调用等操作 |

## 数值比较方式

下表列出了常用的比较运算符，假定变量 a 为 1，变量 b 为 2：

| 运算符 | 说明                                                         | 举例                     |
| :----- | :----------------------------------------------------------- | :----------------------- |
| `-eq`  | equals 检测两个数是否相等，相等返回 0, 否则返回1。           | `[ $a -eq $b ]` 返回 1。 |
| `-ne`  | not equals检测两个数是否不相等，不相等返回 true。            | `[ $a -ne $b ]` 返回 0。 |
| `-gt`  | greater than检测左边的数是否大于右边的,<br>是返回0, 否则1    | `[ $a -gt $b ]` 返回 1。 |
| `-lt`  | lower than检测左边的数是否小于右边的,<br>是返回0, 否则1      | `[ $a -lt $b ]` 返回 0。 |
| `-ge`  | greater equals检测左边的数是否大于等于右边的,<br>是返回0, 否则1 | `[ $a -ge $b ] `返回 1。 |
| `-le`  | lower equals检测左边的数是否小于等于右边的,<br>是返回0, 否则1 | `[ $a -le $b ] `返回 0。 |
| `<`    | 检测左边的数是否小于右边的,<br/>是返回0, 否则1               | `(($a<$b))` 返回0        |
| `<=`   | 检测左边的数是否小于等于右边的,<br/>是返回0, 否则1           | `(($a<=$b))` 返回0       |
| `>`    | 检测左边的数是否大于右边的,<br/>是返回0, 否则1               | `(($a>$b))` 返回1        |
| `>=`   | 检测左边的数是否大于等于右边的,<br/>是返回0, 否则1           | `(($a>=$b))` 返回1       |
| `==`   | 检测左边的数是否等于右边的,<br/>是返回0, 否则1               | `(($a==$b))` 返回1       |
| `!=`   | 检测左边的数是否不等于右边的,<br/>是返回0, 否则1             | `(($a!=$b))` 返回0       |

> 注意:
>
> 整数比较运算符只支持整数，不支持小数与字符串(字符串比较后续讲解)，除非字符串的值是整数数字。
>
> 每个命令都有返回值,  这个后面我们会讲解退出状态再具体说明,  返回0代表成功, 返回1代表失败

## 字符串比较方式

下表列出了常用的字符串运算符，假定变量 a 为 "abc"，变量 b 为 "efg"：

字符串比较可以使用 `[[]]` 和 `[]` 2种方式

| 运算符  | 说明                                                         | 举例                                                         |
| :------ | :----------------------------------------------------------- | :----------------------------------------------------------- |
| == 或 = | 相等。用于比较两个字符串或数字，相同则返回 0。可以使用`=`    | `[ $a == $b ] `返回1 <br>`[  $a = $b ]` 返回 1<br>`[[ $a == $b ]]` 返回1<br>`[[ $a = $b ]]` 返回1 |
| !=      | 不相等。用于比较两个字符串或数字，不相同则返回 0。           | `[ $a != $b ]` 返回 0<br>`[[ $a != $b ]]` 返回 0             |
| <       | 小于, 用于比较两个字符串或数字， 小于返回0， 否则返回1       | `[ $a \< $b ]` 返回 0<br/>`[[ $a < $b ]]` 返回 0             |
| >       | 大于, 用于比较两个字符串或数字， 大于返回0， 否则返回1       | `[ $a \> $b ]` 返回 1<br/>`[[ $a > $b ]]` 返回 1             |
| -z      | 检测字符串长度是否为0，如果长度为0返回则返回0, 否则返回1。   | [ -z $a ] 返回 false。                                       |
| -n      | 检测字符串长度是否不为 0，如果长度不为 0 则返回0, 否则返回1。 | [ -n "$a" ] 返回 true。                                      |
| $       | 检测字符串是否不为空，不为空返回0, 为空返回1。               | [ $a ] 返回 true。                                           |

> 字符串比较没有 `<=`  可以通过 `[[ "a" < "b" && "a" == "b" ]]`

## 逻辑运算符

| 运算符 | 说明       | 举例                       |
| :----- | :--------- | :------------------------- |
| &&     | 逻辑的 AND | `[[ 表达式1 && 表达式2 ]]` |
| `||`   | 逻辑的 OR  | `[[ 表达式1 || 表达式2 ]]` |
| !      | 逻辑非     | `[[ ! 表达式 ]]`           |

> 注意
>
> 使用`&&`  和  `||`  的运算符必须放在 `[[]]`  或 `(())`中才有效, 否则报错
>
> `!` 可以用在`[]`,`[[]]`中, 不可以在(())

## cut工具（字符串及文件操作）

操作文件

```shell
cut [options] file name
```

操作字符串

```shell
echo "string demo 001" | cut -d " " -f 2
```



***options参数说明：***

| 选项参数        | 功能                                                         |
| --------------- | ------------------------------------------------------------ |
| -f 提取范围     | 列号，获取第几列                                             |
| -d 自定义分隔符 | 自定义分隔符，默认为制表符。                                 |
| -c 提取范围     | 以字符为单位进行分割                                         |
| -b 提取范围     | 以字节为单位进行分割。这些字节位置将忽略多字节字符边界，除非也指定了 -n 标志。 |
| -n              | 与“-b”选项连用，不分割多字节字符；                           |

***提取范围说明：***

| 提取范围  | 说明                                                       |
| --------- | ---------------------------------------------------------- |
| n-        | 提取指定第n列或字符或字节后面所有数据                      |
| n-m       | 提取指定第n列或字符或字节到第m列或字符或字节中间的所有数据 |
| -m        | 提取指定第m列或字符或字节前面所有数据                      |
| n1,n2,... | 提前指定枚举列的所有数据                                   |

## 字符串截取操作

### ***cut工具操作：使用方法转上***

### ***常见字符串截取格式：***

| 格式                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| `${变量名:start:length}`   | 从 string 字符串的左边第 start 个字符开始，<br>向右截取 length 个字符。start从0开始 |
| `${变量名:start}`          | 从 string 字符串的左边第 start 个字符开始截取，直到最后。    |
| `${变量名:0-start:length}` | 从 string 字符串的右边第 start 个字符开始，<br>向右截取 length 个字符。start从1开始, 代表右侧第一个字符 |
| `${变量名:0-start}`        | 从 string 字符串的右边第 start 个字符开始截取，直到最后。    |
| `${变量名#*chars}`         | 从 string 字符串左边第一次出现 *chars 的位置开始，<br>截取 *chars 右边的所有字符。 |
| `${变量名##*chars}`        | 从 string 字符串左边最后一次出现 *chars 的位置开始，<br>截取 *chars 右边的所有字符。 |
| `${变量名%chars*}`         | 从 string 字符串右边第一次出现 chars* 的位置开始，<br>截取 chars* 左边的所有字符。 |
| `${变量名%%chars*}`        | 从 string 字符串右边最后一次出现 chars* 的位置开始，<br>截取 chars* 左边的所有字符 |

# Go

## hello world

```go
package main//每个文件必须有且仅有一个main包
import "fmt"//导入库
func main(){//此处不换行
    fmt.Println("hello world")//无分号结尾
}
```

## 安装tips

### vscode出现Installing github.com/ramya-rao-a/go-outline@latest FAILED报错

```shell
#依次输入以下
mkdir -p $env:GOPATH/src/golang.org/x/
 
cd $env:GOPATH/src/golang.org/x/
 
git clone https://github.com/golang/tools.git
 
go env -w GOPROXY=https://goproxy.cn,direct
```



## 变量

```go
package main

import "fmt"

func main() {
	fmt.Println("Hello, World!")

	//变量一旦声名必须使用,即必须对其进行除初始化以外的操作

	//变量的类型推导
	c := 30
	fmt.Printf("type of c is : %T", c)

	//多重赋值
	a, b := 1, 2
	fmt.Printf("a = %d b=%d", a, b)

	//匿名变量
    //匿名变量不占用命名空间,不会分配内存,所以匿名变量之间不存在重复说明
	var i, j int
	i, _ = a, b
	j, _ = a, c
	fmt.Printf("i = %d,j= %d ", i, j)

	//变量初始化
	var d int = 20
	var e = 100
	fmt.Printf("d: %v\n", d)
	fmt.Printf("e: %v\n", e)
	
    
}
```

> ***格式化 : ***
>
> %T:类型输出
>
> %d:十进制	%b:二进制	%x:十六进制	%o:八进制 

## 数据类型

### int,bool,const

```go
package main

import (
	"fmt"
	"unsafe"
)

var g = "全局变量"

func main() {
	fmt.Println("Hello, World!")

	//变量一旦声名必须使用,即必须对其进行除初始化以外的操作

	//变量的类型推导
	c := 30
	fmt.Printf("type of c is : %T", c)

	//多重赋值
	a, b := 1, 2
	fmt.Printf("a = %d b=%d", a, b)

	//匿名变量
	var i, j int
	i, _ = a, b
	j, _ = a, c
	fmt.Printf("i = %d,j= %d ", i, j)

	//变量初始化
	var d int = 20
	var e = 100
	f := 200
	fmt.Printf("d= %d,e= %d,f= %d\n", d, e, f)
	fmt.Println("--------------------------")
	var (
		name   string
		age    int
		gender string
	)
	name = "Girl"
	age = 18
	gender = "Woman"
	fmt.Printf("name=%s,age=%d,gender=%s", name, age, gender)
	fmt.Println("--------------------------")

	//全局变量调用
	fmt.Println(g)

	//常量
	//常量可以声名不使用?
	const pi = "3.14.59265358979323846"
	fmt.Println("pi=", pi)
	//多个常量的声名
	const (
		E = "2.714"
		g = "9.8"
	)
	fmt.Println("e=", E, "g=", g)
	const (
		//未直接赋值与上一个变量相同值与上一个相同
		con1 = "21"
		con2
		con3 = "31"
		con4
	)
	fmt.Println("con1=", con1, "con2=", con2, "con3=", con3, "con4=", con4)
	//iota计数器
	//iota在const关键字出现时将被重置为0(const内部第一行之前)
	const (
		//自动进行累加
		n1 = iota
		_        //进行跳过占位?
		n2 = 100 //或者直接插队
		n3 = iota
		n4
	)
	fmt.Println("n1=", n1, "n2=", n2, "n3=", n3, "n4=", n4)
	//多个iota可以定义在一行
	const (
		d1, d2 = iota + 1, iota + 2
		d3, d4
		d5, d6
	)
	fmt.Println("d1=", d1, "d2=", d2)
	fmt.Println("d3=", d3, "d4=", d4)
	fmt.Println("d5=", d5, "d6=", d6)
	fmt.Println("--------------------------")

	//基本数据类型
	//整形
	//有符号整型int,无符号整形uint
	//默认值为0
	var num int8 = 10
	fmt.Printf("num: %v,类型:%T\n", num, num)
	fmt.Println(unsafe.Sizeof(num)) //unsafe.Size()获取存储大小(字节)
	//类型的转换(注意空间是否足够)
	fmt.Println(int16(num))
	//浮点型
	//64位系统中go默认对浮点使用float64
	//默认值为0
	var f1 float32 = 3.1415926535
	fmt.Printf("f1 = %v\n", f1)
	fmt.Printf("f1 = %f\n", f1)   //默认保留6位小数点
	fmt.Printf("f1 = %.4f\n", f1) //默认保留4位小数点
	//科学计数法
	var f2 float64 = 3.14e-3
	fmt.Printf("f2 = %v\n", f2)
	//通常条件下二进制小数和十进制小数互转会出现精度丢失的问题
	var f3 float64 = 3.296666666666
	fmt.Println("f3 * 10000 =", f3*10000)
	fmt.Println(f2 - f3)
	//使用其他包进行扩展
	f4 := 7.3
	f5 := 2.1
	f6 := f4 - f5
	fmt.Println(f6) //精度丢失问题,结果5.199999999999999
	//使用第三方包decimal
	fmt.Println("--------------------------")
	//布尔类型
	//布尔类型只有true和false两个值
	//布尔类型变量默认为false
	var flag1 bool
	fmt.Println(flag1) //false
	//不允许将整形转换为bool型,bool型也无法参加数值运算,无法与其他类型进行转换

	//string类型
	//string型变量默认为空

	fmt.Println("--------------------------")
	//输出格式化
	var num1 = 31
	fmt.Printf("num3 = %v\n", num1) //原样输出
	fmt.Printf("num3 = %d\n", num1) //十进制
	fmt.Printf("num3 = %b\n", num1) //二进制
	fmt.Printf("num3 = %o\n", num1) //八进制
	fmt.Printf("num3 = %x\n", num1) //十六进制(小写)
	fmt.Printf("num3 = %X\n", num1) //十六进制(大写)

}

```

### string,byte(ASCII,rune)

```go
package main

import (
	"fmt"
	"strings"
)

func main() {

	//string
	var s1 string = "aaa"
	var s2 = "bbb"
	s3 := "ccc"
	fmt.Printf("s1=%v,s2=%v,s3=%v\n", s1, s2, s3)

	//字符串转义字符\
	s4 := "this is \nstar" //换行转义字符
	fmt.Println("s4=", s4)
	s5 := "c\\desktop\\node.js"
	fmt.Println("s5=", s5)

	//多行字符串
	s6 := `hello go
	this is lines
	 of string
	`
	fmt.Println("s6=", s6)

	//字符串常用操作
	fmt.Println(len(s1))         //len(str)
	fmt.Println("s1+s2=", s1+s2) //拼接字符串+或fmt.Sprintf()
	s7 := fmt.Sprintf("%v%v", s1, s2)
	fmt.Println("s7=", s7)
	s8 := "welcome to newyork\n" +
		"welcome to China\n" +
		"........."
	fmt.Println("s8=", s8)
	//字符串切割(需要引入strngs包)
	s9 := "2003.6.20"
	arr := strings.Split(s9, ".")
	fmt.Println("arr=", arr)
	//join操作:把切片链接成字符串
	str1 := strings.Join(arr, "-")
	fmt.Printf("str1: %v\n", str1)
	//contains判断是否包含
	str2 := "aa"
	str3 := "hello aa"
	flag1 := strings.Contains(str3, str2)
	fmt.Printf("flag: %v\n", flag1) //true
	//判断字符串前缀和后缀HasPrefix(),HasSuffix()
	flag2 := strings.HasPrefix(str3, "he")
	flag3 := strings.HasPrefix(str3, "aa")
	fmt.Printf("flag2: %v\n", flag2)
	fmt.Printf("flag3: %v\n", flag3)
	//子串出现的位置Index,LastIndex,找不到会返回-1
	locat1 := strings.Index(str3, "aa")
	fmt.Printf("locat1: %v\n", locat1)
	locat2 := strings.LastIndex(str3, "a")
	fmt.Printf("locat2: %v\n", locat2)

	fmt.Println("----------------------------------------------")
	//字符,字符属于int类型
	//uint8类型:ASCII
	//rune:代表一个UTF-8字符

	c1 := 'a'
	fmt.Printf("c1: %v,type:%T,character:%c\n", c1, c1, c1) //c1: 97,type:int32
	c2 := '国'
	fmt.Printf("c2: %v,type;%T,character:%c\n", c2, c2, c2) //使用UTF-8编码

}

```

### map slice

```go
package main

import "fmt"

func main() {
	//slice
	var str1 string = "hello world"
	var sl1 []string
	for index, char := range str1 {

		sl1 = append(sl1, string(char))
		sl1 = append(sl1, "--")
		fmt.Println(index, ":", string(char))
	}
	fmt.Println(sl1)
	fmt.Println(len(sl1))
	fmt.Println(cap(sl1))
	fmt.Println("---------------------------")

	//map
	mp1 := map[string]string{
		"name": "张三",
	}
	fmt.Println(mp1["name"])
	//如果使用var声名一个nil的Map那么向其中插入数据会出现panic异常,因为并没有对Map进行内存的地址分配
	//使用make函数可以进行内存地址的分配
	mp2 := make(map[string]string)
	mp2["begin"] = "gogogo"
	mp2["mid"] = "running"
	mp2["end"] = "over"
	fmt.Println(mp2["begin"])
	delete(mp2, "end")
	fmt.Println(mp2)
	s, ok := mp2["mid"]
	//使用两个参数进行接收,第二个参数代表了键值对是否真的存在,可以避免键对应的值干扰判断结果
	if !ok {
		fmt.Println("this key is not insist for this map")
	} else {
		fmt.Println(s)
	}
	mp3, mp4 := map[int]string{1: "bbb"}, map[int]string{1: "aaa"}
	fmt.Println(EquallMap(mp3, mp4))

}

//判断两个Map是否相等(int:string类型)
func EquallMap(x, y map[int]string) bool {
	// 首先对长度进行判断
	if len(x) != len(y) {
		return false
	}
	// 对xmap进行key:value遍历
	for key, xv := range x {
		//对当前键对应的yval与本次迭代的xval进行比较,同时也可以利用ok进行判断
		if yv, ok := y[key]; !ok || xv != yv {
			return false
		}
	}
	return true
}

```

```go
man.go
package main

type Man struct {
	Name string
}

```

## 包的使用

```go
//pkg.go
package pkgstu

type Stu struct {
	Name string
}

type Score struct {
	Stu
	score int
}

/*对于包的导入有以下细节：
1.对于一个目录下的所有包应该拥有同一个包名
2.对于包中可导出变量和方法应该让其首字母大写，对于同一个包名中的数据可以互相使用对于导出性没有要求，即小写不可导出大写可导出
3.import中所写的导入格式为module名加上目录名
*/

```

```go
//work.go
package pkgstu

import "fmt"

func Learning(stu Stu) {
	fmt.Printf("%v's work is learning", stu.Name)
}
func showScore(stu Stu) {
	fmt.Printf("%v's score is %v")
}

```



### struct

```go
//struct.go
package main

import (
	"fmt"
	// man "test_001/struct"
	pkgStu "test_001/pkgStu"
)

type Point struct {
	X int
	Y int
}
type Circle struct {
	Point
	Radius int
}
type Wheel struct {
	Circle
	Spokes int
}
type Student struct {
	name string
	age  int
}

// 在结构体声名中，对类型相同，导出要求相同的变量进行简化书写
type Score struct {
	Student
	en, ch, math int
}

func main() {
	//匿名嵌入特性使得访问叶子属性时可以不再写全路径
	var w Wheel
	w.X = 8
	w.Y = 8
	w.Radius = 5
	w.Spokes = 20
	//等价于
	//w.Cicle.Point.X = 8
	//但是对于结构体字面量的声名需要分层次写出，并没有简短的方法，下方第一种方法将出现编译错误
	//w = Wheel{8, 8, 5, 20}
	//w = Wheel{X: 8, Y: 8, Radius: 5, Spokes: 20}
	//正确的声名
	w = Wheel{Circle{Point{8, 8}, 5}, 20}
	w = Wheel{
		Circle: Circle{
			Point:  Point{X: 8, Y: 8},
			Radius: 5,
		},
		Spokes: 20, //此处（以及半径处）需要跟随逗号
	}
	fmt.Printf("Wheel's Attributes are %v \n", w)
	fmt.Printf("Wheel's Attributes are %#v \n", w)
	// Wheel's Attributes are {{{8 8} 5} 20}
	// Wheel's Attributes are main.Wheel{Circle:main.Circle{Point:main.Point{X:8, Y:8}, Radius:5}, Spokes:20}
	// 使用匿名嵌入的结构体时，可以直接访问其内部的属性，但是在声名结构体字面量时，需要分层次写出，且需要跟随逗号
	fmt.Println("---------------------------------------------------------------------------")
	//想要改变结构体的内部值只能传入指针(由于所有的函数传入都是值传入)
	stu1 := new(Score)
	initScore(stu1)
	fmt.Println(stu1)
	stu2 := Score{Student{"Tom", 20}, 50, 50, 50}
	doubleScore(&stu2)
	fmt.Println(stu2)
	adScore := &stu1
	fmt.Println(adScore)
	//结构体的字面值可以对每个属性显示的填入，也可以按照声名顺序进行隐式的填入，但是对于不可导出的属性无论是哪一种方式都不可以对其进行外部操作
	// man1 := Man{"Jake"}
	// fmt.Println(man1)
	// 	# command-line-arguments
	// .\struct.go:65:10: undefined: man
	//出现如上报错
	stu3 := pkgStu.Stu{Name: "Jake"}
	fmt.Println(stu3)
	pkgStu.Learning(stu3)
}

// 初始化结构体数据(假设有一个init函数)
func initScore(score *Score) {
	score.name = "null"
	score.age = 18
	score.en, score.ch, score.math = 11, 11, 11
}

// 传入指针直接改变结构体变量内部值
func doubleScore(score *Score) {
	score.ch *= 2
	score.en *= 2
	score.math *= 2
}

```



## 运行流程

> ***go build :***先编译,后运行,会生成可执行文件在同样的windows环境可直接执行
>
> ***go run:***编译运行一步到位,没有生成可执行文件
>
> ***Ps :*** 静态编译

# docker

***介绍：Docker 是一个开源平台，支持开发人员构建、部署、运行、更新和管理*容器*，这些容器是标准化的可执行组件，结合了应用源代码以及在任何环境中运行该代码所需的操作系统 (OS) 库和依赖项。***

> 常用使用命令：
>
> ```shell
> #拉取镜像
> docker pull <image>
> #使用一个镜像以命令行模式哦启动容器，同时执行命令
> #-i 交互模式操作	-t	终端启动 -d 在后台运行 --name 指定相应的对应的容器name
> # -p 指定端口映射，如5000：5000	-P 随机端口映射	-h hostname设定
> #--network 指定容器连接到的网络 rm 容器退出时自动清理内部的文件系统
> docker run -it <image> <command>
> #退出
> exit
> #查看所有在运行的容器
> docker ps
> #查看所有的容器
> docekr ps -a
> #启动一个已经停止的容器
> docker start <container>
> #重新启动一个容器
> docekr restart <container>
> #停止一个容器
> docker stop <container>
> #进入后台运行的容器
> docker attatch <container>
> #进入容器退出容器不会自动退出
> dcoerk exec -it <container> /bin/bash
> #删除容器
> docker rm -f <container>
> #查看容器的端口映射
> docekr port <container>
> #查找镜像
> docekr search <image>
> #删除镜像
> docekr rmi <image>
> #创建镜像
> docker commit -m <message> -a <author> <containerId> <imageName>
> #使用Dockfile通过docker build构建docker image
> docker build -t <imageName> <DockerfileDir>
> #为镜像添加一个新的tag
> docker tag <containerId> <tag>
> #docker容器互联
> docker network create -d <NetType> <netName>
> ```
>
> 

# Python

## Python基础

### 列表，元组，集合，字典

| 类型               | 声明符号                  | 特点                             | 相关操作 |      |
| ------------------ | ------------------------- | -------------------------------- | -------- | ---- |
| 列表（List）       | [temp1,temp2]             | 可重复，可变                     |          |      |
| 元组（Tuple）      | (temp1,temp2)             | 可重复，不可变                   |          |      |
| 集合（Set）        | {temp1,temp2}             | 不可重复，可进行集合运算，无序   |          |      |
| 字典（Dictionary） | {key1:value1,key2:value2} | 不可重复（按照键进行区分），无序 |          |      |

1. ***列表（List）***
- append(), insert(): 在列表中添加元素。
- pop(), remove(), del(): 在列表中删除元素。
- index(), count(): 在列表中查找元素。
- sort(), reverse(): 对列表进行排序和反转。
- extend(), +: 合并列表。

2. ***元组（Tuple）***
由于元组是不可变的，其支持的方法相对较少，主要包括：
- index(), count(): 在元组中查找元素。

3. ***集合（Set）***
- add(), update(), remove(): 在集合中添加或删除元素。
- union(), intersection(), difference(), symmetric_difference(): 对集合进行运算，如并集、交集、差集、对称差集等。
- issubset(), issuperset(), isdisjoint(): 判断集合是否为另一个集合的子集、超集或者两个集合是否没有交集。

4. ***字典（Dictionary）***
- keys(), values(), items(): 获取字典的键、值和键值对。
- get(), setdefault(): 获取字典中的元素。
- update(): 更新字典。
- pop(), popitem(): 删除字典中的元素。
- clear(): 清空字典。

***PS:***比如列表的元素可以被修改，而元组则是不可变的，适用于表示一些常量和只读变量；集合可以用于去重和数学运算，字典常常用于存储键值对信息。

### 文件操作

***open函数***

```python
open(filepath,mode)
```

open()方法在Python中用来打开文件，并返回一个文件对象。下面是open()方法的参数详解：

- file:要打开的文件名（包括路径）。一般来说，在Windows上使用反斜杠\，在Unix和Linux中使用斜线/。
- mode:打开文件的模式。常见的模式有：
  - r:只读模式（默认，如果省略mode参数）
  - w:写入模式，会将文件内容全部清空并覆盖原有内容
  - x:独占写入模式，仅在文件不存在时创建文件，否则抛出FileExistsError异常
  - a:追加模式，在原有内容后添加新内容
  - b:二进制模式，用于非文本文件，如图片、视频等
  - t:文本模式（默认，如果省略b选项），用于文本文件，如txt、html等
  - +:读写模式（可添加到其他模式中，如r+、w+、a+等）
- buffering:设置缓存大小，0为不缓存，大于0为缓存大小，默认为-1，即使用系统默认缓存机制。
- encoding:设置字符编码，常见的编码有UTF-8、GBK、GB2312等。
- errors:设置编码错误的处理方式，“strict”表示抛出异常，“ignore”表示忽略错误，直接跳过。
- newline:设置文本模式下的换行符号，可选参数包括None、''、'\n'、'\r'、'\r\n'。

例如，使用open()打开一个名为“test.txt”的文件，以只读方式读取，代码为：

```
file = open("test.txt", "r") # r是read mode的意思，不能写成R
```

如果要以写入模式打开文件并清空原有内容：

```
file = open("test.txt", "w")
```

同时以读写模式打开文件：

```
file = open("test.txt", "r+")
```

***利用with关键字：***

```python
with open("aim_address/aim001.txt", "r") as file_read:
    with open("aim_address/aim002.txt", "a") as file_write:
        read_lists = file_read.readlines()
        temp_lists = read_lists
        for i in read_lists:
            if i:
                ip = i.split(" ")[1]
                file_write.write(ip + "\n")
#with
```

### 类，对象，成员方法，构造方法，封装，继承，多态

***类：***

```python
class Student:
    name = None
    gender = None
    age = None
```

***对象：***

```python
stu_s1 = Student("aaa","man",18)
```

***成员方法：***

```python
    def echo (self):
        print(self.name,self.gender,self.age)
    #使用self关键字在参数列表中进行声明，表名该函数为类的成员方法
```

***构造方法：***

```python
    def __init__(self,name,gender,age):
        self.name = name
        self.gender = gender
        self.age = age
    #类的构造方法需要使用__init__()来进行声明，调用时可以直接使用 类名(参数列表) 进行调用
```

***封装：***

```python
#在python中，封装依赖于单下划线，其代表受保护的可在类内和子类内直接访问，无法在类外直接访问，和双下划线，其代表私有的无法再类外直接访问
class Teacher:
    name = None
    _ID = None
    __address = None
    def __init__(self,name,_ID,__address):
        self.name = name
        self._ID = _ID

t1 = Teacher("Lucy","2001","street__001")
print(t1.name)
print(t1._ID)
print(t1.__address)

```

***继承：***

```python
#类的继承可以分为单继承，多继承，多级继承
class Teacher:
#此为父类
    name = None
    _ID = None
    __address = None

    def __init__(self, name, _ID, __address):
        self.name = name
        self._ID = _ID

    def teach(self):
        print("teacher teaching")


class Trainee_teacher(Teacher):
#此为子类，括号中声明其父类即可实现继承，如果需要实现多继承可以使用,分隔开
    age =None

    def __init__(self,name,_ID,__address,age):
        super().__init__(name,_ID,__address)
        self.age = age
    def teach(self):
        print("Trainee teachers are teaching")


teacher_t1 = Teacher("aaa","2001","street_001")
trainee_teachers_t1 = Trainee_teacher("aaa","2001","street_001",18)

teacher_t1.teach()
trainee_teachers_t1.teach()

```

***多态：***

```python
#python中的多态需要借助ABCMeta或者是abstramethod等模块实现
#其中抽象类中只需要声明抽象方法不需要实现
#接口是一个只包含方法声明的类不包括方法的实现
from abc import ABCMeta, abstractmethod

class MyInterface(metaclass=ABCMeta):
    @abstractmethod
    def print_hello(self):
        pass

class MyClass(MyInterface):
    def print_hello(self):
        print("Hello World!")

obj = MyClass()
obj.print_hello()

```

### 变量注解，函数参数注解

**变量注解**

***方法一：***

```python
val_1:int = 2023
#在原先声明变量的变量名后加上  :变量类型   即可实现变量注解
```

***方法二：***

```python
val_2 = "hello world "   # type : str 
#在原先声明变量后加上   # type : 变量类型
```

**函数参数注解**

```python
def fun(var_1 :int) ->str:
    return str(var_1)
#在参数后跟上 :参数类型 即可注解函数参数     在函数参数括号后跟上 ->参数类型  即可对函数返回值类型进行注解
```



******

******

## 利用爬虫建立IP池

### 具体流程

***获取网站链接->伪造访问的消息头(检查网站的网络,获取伪造的请求头)->获取网站源代码—>提取IP信息结构特点->利用正则表达式筛选IP端口信息->利用字符串截取将信息整合到列表中再将列表信息变为字典存储->对字典数据进行可用性测试***

### IP爬虫代码示例

```python
import requests
from bs4 import BeautifulSoup
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
}
Response = requests.get("https://www.89ip.cn/index_%7B%7D.html", headers=headers)

Text_Html = Response.text
# print(Text_Html)
soup = BeautifulSoup(Text_Html, "html.parser")
Ip_crew = soup.findAll("td")
IP_pattern = re.compile(r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
                        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
                        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\."
                        r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)")
Port_pattern = re.compile("[1-5]\\d\\d\\d\\d|\\d\\d\\d\\d|6[0-5][0-5][0-3][0-5]")

proxys = {"host": "port"}

IP_pool = {}
ip_list = []
with open("C:\\Users\\Administrator\\Desktop\\101.txt", "w+") as file:
    for i in Ip_crew:
        ip_crew = i.string
        if re.search(IP_pattern, ip_crew):
            temp1 = ip_crew.split("\t")[3]
        if re.search(Port_pattern, ip_crew):
            if len(ip_crew) < 17:
                temp2 = ip_crew.split("\t")[3]
                ip_list.append(temp1 + ":" + temp2)

for i in ip_list:
    ip_port = i
    IP_pool[ip_port] = "Stopping"
print(IP_pool)
for i in IP_pool:
    print(i + "=" + IP_pool[i])

```

### shell数据二次处理脚本

```shell
#!/bin/bash
#flash proxychains
python3 proxychains4_flash.py
#crew IP from net and save in IP_pool.txt
python3 FreeIP_crew.py >IP_pool.txt

while read -r line
do
	IP=$(echo "$line"|cut -d " " -f 2)
	if
		ping -c 1 $IP
	then
		echo "$line" >>/etc/proxychains4.conf
	else
		continue
	fi
done<IP_pool.txt
```

## OpenCv库

***使用案例一：常规图形绘画及颜色配置***

```python
import cv2
import numpy as np

source_img = "img_fangzhou/home.png"
puke_img = "img_fangzhou/puke.png"

img_num = np.zeros((512, 512, 3), np.uint8)

img_pristine = cv2.imread(source_img)
img_num[:] = (255, 0, 0)
cv2.line(img_num, (0, 0), (300, 300), (100, 100, 100), 3)
cv2.rectangle(img_num, (0, 0), (400, 400), (0, 0, 255), 3)
cv2.circle(img_num, (300, 300), 30, (0, 255, 0), 3)
cv2.putText(img_num, "Hello opencv", (200, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 233, 101), 1)

cv2.imshow("Num img", img_num)
cv2.waitKey(0)

```

***使用案例二：图像的透视变换***

```python
import cv2
import numpy as np

# 图像的透视变换

source_img = "img_fangzhou/home.png"
puke_img = "img_fangzhou/puke.png"

puke = cv2.imread(puke_img)

width, height = 250, 350
# puke_resize= cv2.resize(puke_img,(900,900))
# img_puke_delete = puke[500:1800,2200:3800]
pts1 = np.float32([[103, 91], [547, 63], [161, 612], [725, 575]])
pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
puke_output = cv2.warpPerspective(puke, matrix, (width, height))

cv2.imwrite("img_fangzhou/puke_hor.png",puke_output)
cv2.imshow("puke", puke_output)
cv2.waitKey(0)

```

***使用案例三：图像的水平及垂直堆叠***

```python
import cv2
import numpy as np

source_img = "img_fangzhou/home.png"
puke_img = "img_fangzhou/puke_hor.png"

puke = cv2.imread(puke_img)
hor = np.hstack((puke, puke, puke, puke))
ver = np.vstack((puke, puke, puke, puke))
cv2.imshow("hor puke", hor)
cv2.imshow("ver puke", ver)
cv2.waitKey(0)

```

***使用案例四：颜色探测***

```python
import cv2
import numpy as np


def empty(a):
    pass


puke_img = "img_fangzhou/puke_hor.png"

puke = cv2.imread(puke_img)

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 12, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 62, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 118, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    puke_HSV = cv2.cvtColor(puke, cv2.COLOR_BGR2HSV)

    print(h_min, h_max, s_min, s_max, v_min, v_max)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(puke_HSV, lower, upper)
    img_result = cv2.bitwise_or(puke, puke, mask=mask)

    cv2.imshow("puke source", puke)
    cv2.imshow("HSV puke", puke_HSV)
    cv2.imshow("mask", mask)
    cv2.imshow("result puke ", img_result)
    cv2.waitKey(1)

```

#### 



# JavaSE

## 代码实例

### 字符串

```java
import java.security.PublicKey;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        String s1 = "acd";

        String s2 = new String();//使用次数较少

        char[] c1 = {'a', 'c', 'd'};

        String s3 = new String(c1);

        byte[] b1 = {'5', '4'};

        String s4 = new String(b1);

        String s5 = "acd";

        String s6 = "ACD";

        Scanner sc=new Scanner(System.in);
        String s7=sc.next();
        System.out.println(s7);
        System.out.println(s1);
        System.out.println(s2);
        System.out.println(s3);
        System.out.println(s4);
        System.out.println(s7);
        System.out.println("------------------------------------------------------------------");
        System.out.println(s1 == s3);//地址值不一样 false
        System.out.println(s1 == s5);//地址值一样，string的复用性 true

        //equal 方法比较的是字符串本身
        //equalignorecase 会忽略比较的的字符串之间的大小写
        //Scanner 底层利用了new 关键字 在堆中开辟了一块内存
        //String s=""   利用了串池 stringtable jdk7 以前在方法区，在以后的版本串池被移入堆内存中
        System.out.println(s1.equals(s3));//返回为 true
        System.out.println(s1.equalsIgnoreCase(s6)); //return true
        System.out.println(s1 == s7);//return false
        System.out.println(s1.equals(s7));//return true
        System.out.println("-------------------------------------------------------------------");

        Scanner sc1=new Scanner(System.in);
        String s8 = sc1.next();
        System.out.println(s8);
        for (int i = 0; i < s8.length(); i++) {
            //charat 利用字符串的索引返回对应的字符
            char c2=s8.charAt(i);
            System.out.println(c2);
        }
        System.out.println("--------------------------------------------------------------------");

        int [] i1={1117,0221,804,904,218};
        String s13 = arrTostring(i1);
        System.out.println(s13);
        String s14="zfdsgjbhdhdjgh";
        System.out.println(s14.substring(1, 2));//substring方法 截取字符串
        System.out.println(s14.replace("z", "!"));//字符串中字符的替换
    }
    public static String arrTostring(int  []  arr) {
        if (arr.length == 0) {
            return "字符为空";
        } else if (arr==null) {
            return"";

        }
        String s12="[";
        for (int i = 0; i < arr.length; i++) {

            if(i== arr.length-1){
                s12=s12+arr[i]+"]";
                break;
            }
            s12=s12+arr[i]+",";
        }
        return s12;
    }
}

```

#### 字符串容器StringBuilder

```java
import java.util.Scanner;
import java.util.StringJoiner;

public class Main {
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        String s2 = sc.next();

        System.out.println(reverse(s2));

        StringBuilder sb1=new StringBuilder("hello world!");
        System.out.println(sb1.reverse());//此处直接输出STringbuilder的反转 !dlrow olleh
        //reverse(sb1);//此处报错，sb1为Stringbuilder对象
        System.out.println(reverse(sb1.toString()));//此处转换对象类型即可使用  hello world!
        System.out.println(sb1);//!dlrow olleh 此处sb1对象已经被反转
        System.out.println(sb1.append("Bye!")); //!dlrow ollehFuch u
        System.out.println(sb1);//!dlrow ollehFuch u
        System.out.println(sb1.length());
        //PS：SB对象中的数据是可以直接改变，但是string 类型的数据无法直接对其进行操作
        System.out.println(boolreverse(s2));

    }
    public static  String reverse(String  arr){

        String s1="";

        for (int length = arr.length()-1; length >= 0; length--) {

                char c=arr.charAt(length);
                s1=s1+c;
        }
        return s1;
    }
    public static boolean boolreverse(String s1){
        Scanner sc=new Scanner(System.in);
        String s2 = sc.next();
        StringBuilder sb=new StringBuilder(s2);
        if(s2.equals(sb.reverse().toString())){
            return true;
        }else {
            return false;
        }
    }
    public  static String arrTostring(int[]arr){
        StringJoiner sj=new StringJoiner(",","","]");
        for (int i = 0; i < arr.length - 1; i++) {
            sj.add("---");
        }
        return sj.toString();

    }
}

```

### 泛型

```java
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        MyArraylist<String> MYlist=new MyArraylist<>();
        //MyArraylist3<Integer> list5=new MyArraylist3();

        //由于定义中的给定泛型为String 所以在在上一行的Integer 类型会报错，（错误名为没有类型形参）
        MyArraylist3 list6=new MyArraylist3();//默认创建的是String 类型


        System.out.println("------------------------------------------------------------------------");

        //泛型不具备继承性，但数据可以继承
        ArrayList<ye> list7=new ArrayList<>();
        ArrayList<fu> list8=new ArrayList<>();
        ArrayList<zi> list9=new ArrayList<>();
        method1(list7);
        method1(list8);
        method1(list9);//此处在method1使用了E所以可以使用所有类型的变量

        System.out.println("------------------------------------------------------------------------");

        method2(list7);
        method2(list8);
        method2(list9);//此处使用method2使用了? extends E


        System.out.println("------------------------------------------------------------------------");


        method3(list7);
        method3(list8);
        method3(list9);//此处使用了method3使用了? super E


    }
    public static <E>void method1(ArrayList<E> list7){}
    public static void method2(ArrayList<? extends ye> list7){}//? extends E 表示可以从传递E或者E的子类
    public static void method3(ArrayList<? super zi> list7){}//? super E 表示可以从传递E或者E的父类

}
class ye{};
class fu extends ye{};
class zi extends fu{};
```

#### 泛型小结

```java
import java.util.ArrayList;
import java.util.Iterator;

public class Main {
    public static void main(String[] args) {
        ArrayList list=new ArrayList<>();
        list.add("aaa");
        list.add("bbb");
        //如果没有给集合添加特定类型，集合的所有数据类型都是obj类型，
        //优点是可以添加任何类型的元素
        //缺点是不能使用add等特有操作，就算使用了类型强转，也容易发生类型转换错误
        //添加泛型可以统一集合的数据类型
        //Java中的泛型是伪泛型，底层使用了强转
        list.add(new Student(18,"zhengsan"));
        Iterator it = list.iterator();
        //创建迭代器对象，其中的迭代器泛型与集合的泛型一致
        while(it.hasNext()){
            Object next = it.next();
            //next.add;//该行会报错，原因是多态不能访问子类特有的功能
        }
        MyArraylist<Integer> list1=new MyArraylist<>();//自定义泛型类，使用E泛型保证数据多样
        list1.add(123);
        list1.add(456);
        list1.add(789);
        System.out.println(list1.tostring());
        System.out.println("----------------------------------------------------------");
        ArrayList<String> list4=new ArrayList<>();
        util.add(list4,"aaaaa","cccc","a","deeeee","aaaaa","aaaaa");
        System.out.println(list4);
    }
}
```



### 递归

```java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        int sum=0;
        for (int i = 10; i <= 20; i++) {
            sum=sum+factorial(i);
        }
        System.out.println(sum);

    }
    public static int factorial(int num){
        if(num==0){
            return 1;
        }else {
            return (num*factorial(num-1));//递归调用计算阶乘
        }
    }
}
```

### 集合

#### List集合

```java
import com.sun.jdi.IntegerValue;

import java.sql.SQLOutput;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;

public class Main {
    public static void main(String[] args) {
        List<String> list=new ArrayList<>();
        list.add("nihao");
        list.add("HI");
        list.add("China");
        list.add("3");
        //startwith方法，顾名思义
        System.out.println("------------------------------------------");
        System.out.println(list);
        System.out.println("------------------------------------------");
        //在索引处添加需要的元素
        list.add(1,"adad");
        System.out.println(list);//[nihao, adad, HI, China, 3]

        System.out.println("------------------------------------------");
        //在索引处删除指定的元素同时返回被删除的元素
        list.remove(3);

        //手动装箱
        Integer i= Integer.valueOf(3);
        list.remove(i);
        System.out.println(list);//[nihao, adad, HI, 3]
        System.out.println("------------------------------------------");
        //set方法修改指定索引的元素
        //get方法获取指定索引的元素
        String s1=list.set(3,"kkkkkk");
        list.get(2);
        System.out.println(s1);//3
        System.out.println(list);//[nihao, adad, HI, kkkkkk]

        System.out.println("------------------------------------------");
        //迭代器遍历
        Iterator<String> it= list.iterator();
        while(it.hasNext()){
            System.out.println(it.next());

        }
        System.out.println("------------------------------------------");
        //增强for
        for (String s:list){
            System.out.println(s);
        }
        System.out.println("------------------------------------------");
        //Lambda遍历
        list.forEach(s -> System.out.println(s));
        System.out.println("------------------------------------------");
        //列表迭代器
        //区别是可以在遍历的时候修改元素
        ListIterator<String>it1= list.listIterator();
        while(it1.hasNext()){


            String str= it1.next();
            if("HI".equals(str)){
                it1.add("klkl");
            }
            System.out.println(str);
        }
        System.out.println("------------------------------------------");
        System.out.println("------------------------------------------");
    }
}
```

#### Map与Hashmap集合

```java
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        //map主要是键值对的
        //map是一个接口，所以创建对象必须要创建实现类的对象
        Map<String,String>m1=new HashMap<>();
        m1.put("郭靖","黄蓉");//put添加数据（键值对的形式）
        m1.put("aa","bb");
        m1.put("aa","cc");
        m1.put("bb","ee");
        m1.put("kk","gg");
        //put方法的细节：
        //添加数据的时候，如果键不存在，就会把数据添加在map中
        //在添加数据时，如果数据存在，就会把原有的键值对对象覆盖，同时会把被覆盖的值返回
        System.out.println(m1.put("aa", "dd"));//此处cc被覆盖 输出cc
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.remove("bb"));//返回键对应的被删除的值
        System.out.println(m1.remove("cc"));//null  不存在返回为空
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.containsKey("aa"));//true 存在返回就真（其返回类型为布尔类型）
        System.out.println(m1.containsKey("cc"));//false
        System.out.println(m1.containsValue("ee"));//false 此处false因为上面移除了bb键值对
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1);//集合打印  {aa=dd, kk=gg, 郭靖=黄蓉}
        System.out.println("-----------------------------------------------------------------");
        System.out.println(m1.size());//集合的长度  3
        System.out.println("-----------------------------------------------------------------");
        m1.clear();//清空集合
        System.out.println(m1.isEmpty());//true
        System.out.println("-----------------------------------------------------------------");
        //map的遍历方式
        //1.键找值的方法
        Map<String,String> m2 =new HashMap<>();
        m1.put("aa","AA");
        m1.put("bb","BB");
        m1.put("cc","CC");
        //增强for遍历方式
        Set<String> keys = m1.keySet();
        for (String s : keys) {
            System.out.println(s);
        }
        System.out.println("-----------------------------------------------------------------");
        //LAmbda遍历
        keys.forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------------------------------------");
        //迭代器遍历
        Iterator<String> it1= keys.iterator();//创建迭代器对象
        while (it1.hasNext()){
            System.out.println(it1.next());
        }
        System.out.println("-----------------------------------------------------------------");
        //第二种遍历方式，键值对遍历
        Map<String,String> m3=new HashMap<>();
        m3.put("AA","BB");
        m3.put("bb","CC");
        m3.put("cc","DD");
        Set<Map.Entry<String, String>> en1 = m3.entrySet();//返回键值对对象，其中前者接受的泛型为键值对
        //Lambda表达式遍历
        en1.forEach(stringStringEntry -> System.out.println(stringStringEntry));
        System.out.println("-----------------------------------------------------------------");
        //增强for
        for (Map.Entry<String, String> stringStringEntry : en1) {
            System.out.println(en1);
        }
        System.out.println("-----------------------------------------------------------------");
        //迭代器遍历
        Iterator<Map.Entry<String, String>> it3=en1.iterator();//Map.Entry<String, String>，此时创建的迭代器的对象泛型需要使用键值对的类型，否则会报错，前后对应的关系
        while (it3.hasNext()){
            System.out.println(it3.next());
        }
        System.out.println("-----------------------------------------------------------------");
        //Lambda表达式遍历map
        Map<String,String> m4=new HashMap<>();
        m3.put("hh","JJ");
        m3.put("jj","KK");
        m3.put("ll","FF");
        System.out.println("-----------------------------------------------------------------");
        m3.forEach((s, s2) -> System.out.println(s +"="+s2));//此处的sout中不能直接写(s,s2),会报错,可以写成(s +"="+s2)
        System.out.println("-----------------------------------------------------------------");
        //hashmap都用的map的方法，没有其余的方法
        //1，hashmap时map里的一个实现类
        //2，方法用map的方法
        //3，特点由键值对决定（无序，不重复，无索引）
        //4，hashmap和hashset的底层原理都是哈希表结构（数组加链表，同时还会有红黑树）
        //hashmap的底层是哈希表，依靠hashcode方法，和equals方法保证键的唯一，如果建存储的是自定义对象，需要重写hashcode和equals方法，如果值存储自定义对象，则不需要重写上述两种方法
    }
}
```

#### Hashtree

```java
import java.lang.invoke.LambdaConversionException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.TreeSet;
import java.util.function.Consumer;

public class Main {
    public static void main(String[] args) {
        Student s1=new Student("zhangsan",18);
        Student s2=new Student("zhangsan",18);
        Student s3=new Student("lisi",18);
        System.out.println(s1.hashCode());//-1461067297
        System.out.println(s2.hashCode());//s1=s2在类中重写了hashcode的方法，使其对属性值进行计算，属性相同哈希值相同
        System.out.println(s3.hashCode());//102983072
        System.out.println("===========================================================================");

        System.out.println("abc".hashCode());
        System.out.println("abc".hashCode());//String内部重写了hashcode方法
        System.out.println("acb".hashCode());
        System.out.println("===========================================================================");



        //hashset可以保证在添加数据时可以去重
        //通过equals方法 以及hashcode保证数据不会重复
        //必须要在对象类中重写hsahcode以及equals方法（快捷键是alt insert 方法）
        //在new是开辟了新空间地址值不一样，所以在创建属性值相同时时也不会去重，因为他俩地址值不一样，这也是在面对在面对自定义对象时必须要重写hashcode 以及equals 方法
        //但对于Integer String 来说，Java在底层已经重写好了他们的这两个方法，保证这两只数据的遍历使用

        Student s4=new Student("aa",12);
        Student s5=new Student("bb",13);
        Student s6=new Student("cc",15);
        Student s7=new Student("aa",12);

        HashSet<Student> set1=new HashSet<>();
        boolean b1 = set1.add(s4);//true
        boolean b2 = set1.add(s5);//true
        boolean b3 = set1.add(s6);//true
        boolean b4 = set1.add(s7);//false
        System.out.println(b1);
        System.out.println(b2);
        System.out.println(b3);
        System.out.println(b4);

        System.out.println("===========================================================================");
        //Linkedhashset
        //有序，无重复 无索引
        //底层利用了双向链表，保证数据的添加顺序，在最后读取时，也通过双向链表进行读取
        Student s8=new Student("aa",11);//true
        Student s9=new Student("bb",11);//true
        Student s10=new Student("cc",11);//true
        Student s11=new Student("aa",11);//false
        LinkedHashSet<Student> linkedHashSet=new LinkedHashSet<>();

        System.out.println(linkedHashSet.add(s8));
        System.out.println(linkedHashSet.add(s9));
        System.out.println(linkedHashSet.add(s10));
        System.out.println(linkedHashSet.add(s11));
        System.out.println(linkedHashSet);
        System.out.println("===========================================================================");
        new eat(){
            //匿名内部类
            //eat为接口名

            @Override
            public void eat() {
                System.out.println("在吃饭");
            }
        };
        System.out.println("===========================================================================");

        //Treeset 有序的，无索引，无重复
        TreeSet<Integer> ts=new TreeSet<>();
        System.out.println(ts.add(1));//true
        System.out.println(ts.add(4));//true
        System.out.println(ts.add(2));//true
        System.out.println(ts.add(3));//true
        System.out.println(ts.add(1));//false
        System.out.println(ts);//[1, 2, 3, 4]

        System.out.println("===========================================================================");

        //迭代器遍历
        Iterator<Integer> it2= ts.iterator();
        while(it2.hasNext()){
            System.out.println(it2.next());
        }

        //增强for

        for(int i:ts){
            System.out.println(i);
        }

        //Lambda遍历

        ts.forEach(integer -> System.out.println(integer));

        //下方使用了匿名内部类改进得到上方的Lambda遍历
        ts.forEach(new Consumer<Integer>() {
            @Override
            public void accept(Integer integer) {
                System.out.println(integer);
            }
        });



        System.out.println("===========================================================================");

        Student ss1=new Student("aa",1);
        Student ss2=new Student("bb",2);
        Student ss3=new Student("kk",5);
        Student ss4=new Student("cc",3);
        Student ss5=new Student("dd",3);
        Student ss6=new Student("aa",1);
        Student ss7=new Student("aa",2);

        TreeSet<Student>ts1=new TreeSet<>();
        System.out.println(ts1.add(ss1));//true
        System.out.println(ts1.add(ss2));//true
        System.out.println(ts1.add(ss3));//true
        System.out.println(ts1.add(ss4));//true
        System.out.println(ts1.add(ss5));//false  虽然属性值不是完全相同但是年龄相同，再重写的compareto 方法中是根据年龄比较的，所以在集合中根据年龄排序
        System.out.println(ts1.add(ss6));//false
        System.out.println(ts1.add(ss7));//false
        System.out.println(ts1);//[Student{name = aa, age = 1}, Student{name = bb, age = 2}, Student{name = cc, age = 3}, Student{name = kk, age = 5}]
        //只要数据有重复就会去重，无论是年龄还是名字
        //言多必失


        System.out.println("===========================================================================");
        TreeSet<String> ts3=new TreeSet<>((o1, o2) -> {
            //创建比较器的对象，（使用匿名内部类改进得到Lambda表达式的写法，
            int i=o1.length()-o2.length();
            i=i==0? o1.compareTo(o2):i;//按照字符串的长度进行红黑树的比较，从小到大
            return i;
        });
        System.out.println(ts3.add("m"));//true
        System.out.println(ts3.add("aad"));//true
        System.out.println(ts3.add("ef"));//true
        System.out.println(ts3.add("gaaaaaa"));//[m, ef, aad, gaaaaaa]
        System.out.println(ts3);
        System.out.println("===========================================================================");
        System.out.println("===========================================================================");
    }
}

//学生类
import java.util.Objects;

public class Student implements Comparable<Student>{
    private String name;
    private int age;

    public Student() {
    }

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return age == student.age && Objects.equals(name, student.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + "}";
    }

    @Override
    public int compareTo(Student o) {
        return this.getAge()-o.getAge();
        //-1 表示添加的元素比当前元素小，按要求加载红黑树中
        //1 表示添加的元素比当前元素大，按要求加载红黑树中
        //0 表示添加的元素已经有相同，不加载红黑树中
    }
}


public interface eat {
    public  void eat();
}

```

#### Treemap集合

```java
import java.util.TreeMap;

public class Main {
    public static void main(String[] args) {

        //Treemap底层为红黑树的结构，不重复无索引，实现comparato比较器对象，指定比较规则，或者实现comparable的接口，指定比较规则(此时不重复无索引，是指键的关系)
        //基于红黑树的结构，增删改查的性能比较好

        TreeMap<Character,Integer>tm1=new TreeMap<>();
        String s1="abcddeabaebb";
        for (int i = 0; i < s1.length(); i++) {
            char c1=s1.charAt(i);
            //利用countainskey对集合进行判断，当其存在时，创建一个整形，将c1字符的数量进行提取，并且自增，最终将count和c1进行添加到集合中，输出结果
            //关键为对字符串的遍历时，对字符串的每一个字符进行提取，字符串调用charAt(index)的方法(其中index为字符串中每个字符的索引)，常用fori遍历，其中i即为字符串的索引
            if(tm1.containsKey(c1)){
                int count=tm1.get(c1);
                count++;
                tm1.put(c1,count);
            }else{
                tm1.put(c1,1);
            }
        }
        System.out.println(tm1);
        System.out.println("----------------------------------------------");
        StringBuilder sb1=new StringBuilder();
        tm1.forEach((character, integer) -> sb1.append("(").append(character).append(":").append(integer).append(")"));
        System.out.println(sb1);
    }
}
```

#### Treeset

```java
import java.util.TreeSet;

public class Main {
    public static void main(String[] args) {

        Student s1 = new Student("aa", 56, 24, 55, 45, 55);
        Student s2 = new Student("bb", 42, 54, 41, 45, 66);
        Student s3 = new Student("cc", 56, 78, 65, 79, 77);
        Student s4 = new Student("dd", 44, 43, 60, 99, 88);
        Student s5 = new Student("aa", 34, 21, 79, 77, 99);
        TreeSet<Student> ts = new TreeSet<>();
        System.out.println(ts.add(s1));
        System.out.println(ts.add(s2));
        System.out.println(ts.add(s3));
        System.out.println(ts.add(s4));
        System.out.println(ts.add(s5));

        System.out.println(ts);
        for (Student s:ts){
            System.out.println(s);
        }
    }
}


//////////////////////////////////


public class Student implements Comparable<Student> {
    private String Name;
    private int Age;
    private int Chinese;
    private int Math;
    private int English;
    private int Allscore;

    public Student() {
    }

    public Student(String Name, int Age, int Chinese, int Math, int English, int Allscore) {
        this.Name = Name;
        this.Age = Age;
        this.Chinese = Chinese;
        this.Math = Math;
        this.English = English;
        this.Allscore = Allscore;
    }

    /**
     * 获取
     * @return Name
     */
    public int allscore(){
        return this.getEnglish()+this.getChinese()+this.getMath();
    }
    public String getName() {
        return Name;
    }

    /**
     * 设置
     * @param Name
     */
    public void setName(String Name) {
        this.Name = Name;
    }

    /**
     * 获取
     * @return Age
     */
    public int getAge() {
        return Age;
    }

    /**
     * 设置
     * @param Age
     */
    public void setAge(int Age) {
        this.Age = Age;
    }

    /**
     * 获取
     * @return Chinese
     */
    public int getChinese() {
        return Chinese;
    }

    /**
     * 设置
     * @param Chinese
     */
    public void setChinese(int Chinese) {
        this.Chinese = Chinese;
    }

    /**
     * 获取
     * @return Math
     */
    public int getMath() {
        return Math;
    }

    /**
     * 设置
     * @param Math
     */
    public void setMath(int Math) {
        this.Math = Math;
    }

    /**
     * 获取
     * @return English
     */
    public int getEnglish() {
        return English;
    }

    /**
     * 设置
     * @param English
     */
    public void setEnglish(int English) {
        this.English = English;
    }

    /**
     * 获取
     * @return Allscore
     */
    public int getAllscore() {
        return Allscore;
    }

    /**
     * 设置
     * @param Allscore
     */
    public void setAllscore(int Allscore) {
        this.Allscore = Allscore;
    }

    public String toString() {
        return "Student{Name = " + Name + ", Age = " + Age + ", Chinese = " + Chinese + ", Math = " + Math + ", English = " + English + ", Allscore = " + Allscore + "}";
    }

    @Override
    public int compareTo(Student o) {
        int sumofthis=this.allscore();
        int sumofo=o.allscore();
        int i=sumofthis-sumofo;
        i=i==0? this.getChinese()-o.Chinese:i;
        i=i==0? this.getMath()-o.Math:i;
        i=i==0?this.getEnglish()-o.getEnglish():i;
        i=i==0?this.getAge()-o.getAge():i;
        i=i==0?this.getName().compareTo(o.getName()):i;
        return i;
    }
}

```



### 正值表达式

```java
public class Main {
    public static void main(String[] args) {


        System.out.println("---------------------------------------------------");

        String regex1 = "1[3-9]\\d{9}";//手机号码
        System.out.println("手机号码");



        System.out.println("13251083456".matches(regex1));//true
        System.out.println("1325108345".matches(regex1));//false
        System.out.println("132adadadd5".matches(regex1));//false


        System.out.println("---------------------------------------------------");

        String regex2 = "[2-9]\\d{5,11}";//QQ号码
        System.out.println("QQ号码");


        System.out.println("838992123".matches(regex2));//true
        System.out.println("838adad".matches(regex2));//false
        System.out.println("8323".matches(regex2));//false

        System.out.println("---------------------------------------------------");


        String regex3="\\w{6,9}@[\\w^_]{2,7}(\\.com|\\.cn){1,2}";
        System.out.println("邮箱号码");



        System.out.println("123134@qq.com".matches(regex3));//true
        System.out.println("123134qq.com".matches(regex3));//false
        System.out.println("123d34@q.com.cn".matches(regex3));//false
        System.out.println("1ada34@qq.c".matches(regex3));//false
        System.out.println("123aad4@qq.cm".matches(regex3));//false


        System.out.println("-------------------------------------------------------------------------");

        String regex4="((?i)\\w){1,9}";
        System.out.println("忽略大小写的1-9位字符");



        System.out.println("dadad".matches(regex4));//true
        System.out.println("@@@@@".matches(regex4));//faLse
        System.out.println("da??/".matches(regex4));//false
        System.out.println("dadad_".matches(regex4));//true

        System.out.println("-------------------------------------------------------------------------");

        String regex5="((?i)\\w){1,9}";
        System.out.println("adadaD#".matches(regex5));//false


    }

}
```



### 流操作

```java
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //filter 过滤操作
        //limit  获取前几个元素
        //skip   跳过前几个元素
        //ps: 1.中间方法，返回新的Stream流，原来的Stream流只能使用一次，建议使用链式编程
        //    2.修改Stream流中的数据，不会影响原来集合或者数组中的数据
        ArrayList<String> al1=new ArrayList<>();
        Collections.addAll(al1,"张三","李四","王五","赵六","张无忌","张三丰");
        ArrayList<String> al2=new ArrayList<>();
        Collections.addAll(al2,"赵子龙","黄忠","吕布","张飞");
        //filter过滤元素满足的留下，不满足的去除
        //创建s变量，对其进行筛选，对不满足要求的进行去除（使用lambda表达式）
        al1.stream().filter(s -> s.startsWith("张")).filter(s -> s.length()==3).forEach(System.out::println);
        System.out.println("------------------------------------------------------------------------------------------------------");
        //换行
        System.out.println("------------------------------------------------------------------------------------------------------");
        //skip方法的参数：n(其中n为想要跳过流中的数量)
        //跳过前两个
        al1.stream().skip(2).forEach(s -> System.out.println(s));
        //limit方法的参数：n(n代表前几个元素)
        //
        al1.stream().limit(3).forEach(System.out::println);
        //distinct方法：
        //元素去重，其依赖hashcode equals方法
        al1.stream().distinct().forEach(s -> System.out.println(s));
        //concat方法：
        //合并两个流为一个流
        //尽可能保持a，b两个流的数据类型保持相同，两个流合并为c，那么c为其父类
        //零散数据（必须保证零散数据的类型是相同的）
        Stream.of(1,2,3,4).forEach(System.out::println);
        Stream.of("a","b","c").forEach(System.out::println);
        System.out.println("------------------------------------------------------------------------------------------------------");
        Stream.concat(al1.stream(),al2.stream()).forEach(s -> System.out.println(s));
        System.out.println("------------------------------------------------------------------------------------------------------");
        //map转换流中的数据类型
        ArrayList<String> al3=new ArrayList<>();
        Collections.addAll(al3,"zhangsan-18","lisi-19","wangwu-20");//String->int parseint转换为整形
        al3.stream().map(s -> Integer.parseInt(s.split("-")[1])).forEach(s-> System.out.println(s));
        System.out.println("-------------------------------------");
        //stream终结方法
        //forEach
        al1.stream().forEach(s -> System.out.println(s));
        //count
        long count = al1.stream().count();
        System.out.println(count);
        //toArray
        //收集流中的数据放到数组中
        //先创建一个指定类型的数组，toArray的底层，会依次得到流里面的每一个数据，并把数据放到数组中，方法的返回值是一个装着流里面所有数据的数组
        Object[] objects = al1.stream().toArray();
        System.out.println(objects);
        System.out.println("-----------------------------");
        //collect 收集流中的数据放在集合中
        ArrayList<String> al4=new ArrayList<>();
        Collections.addAll(al4,"aa-man-17","bb-man-15","cc-woman-14","dd-man-20","ee-man-21","ff-woman-9");
        //tolist
        List<String> collect = al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toList());
        System.out.println(collect);
        //toset
        //对于list与set，在面对set时底层会自动去重（list与set的区别）
        al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toSet());
        System.out.println("---------------------------------------------------------------------");
        //tomap（明确指定键值对的对应）
        //在tomap方法中明确指定键值对的对应方法
        //参数1：Function泛型1：表示流中的每一个数据的类型  泛型2：表示Map集合中的键的数据类型
        //方法apply形参：以此表示流里面的每一个数据返回值：已经生成的键
        //参数2：Function 泛型1 表示流里面的每一个数据的类型  泛型2：Map集合中的值的数据类型
        //apply形参：依次表示流里面的每一个数据，方法体：生成值的代码 返回值：已经生成的值123567
        Map<String, String> collect1 = al4.stream().filter(s -> "man".equals(s.split("-")[1])).collect(Collectors.toMap(s -> s.split("-")[0], s -> s.split("-")[2]));
        System.out.println(collect1);
        System.out.println("----------------------------------------------------------------");
        String s1="welcome-China-Beijing";
        System.out.println(s1.split("-")[0]);//welcome
        System.out.println(s1.split("-")[1]);//China
        System.out.println(s1.split("-")[2]);//Beijing
        System.out.println("-----------------------------------------------------------------");

    }
}
```

### Scanner

```java
import java.util.Scanner;

public class MyScanner {
    public static void main(String[] args) {
        Scanner sc1 =new Scanner(System.in);
        while (sc1.hasNext()){
            String line = sc1.nextLine();
            System.out.println(line);
        }
    }
    //循环读取打印到标准输出流
    //nextLine读取用户的一行数据
    //next读取下一个标记，默认空格作为分隔符

}
```

### Math类与Biginteger

#### Math类

Math类是Java中的一个标准类，提供了许多数学计算相关的静态方法，例如求绝对值、幂次方、三角函数、对数函数、随机数等等。以下是Math类常用的一些方法：

1. abs(x)

该方法返回参数x的绝对值，例如：

```java
TXT复制int x = -10;
int absX = Math.abs(x);
System.out.println(absX); // 输出：10
```

1. pow(x, y)

该方法返回x的y次幂，例如：

```java
TXT复制double x = 2.0;
double y = 3.0;
double powXY = Math.pow(x, y);
System.out.println(powXY); // 输出：8.0
```

1. sqrt(x)

该方法返回x的平方根，例如：

```java
TXT复制double x = 16.0;
double sqrtX = Math.sqrt(x);
System.out.println(sqrtX); // 输出：4.0
```

1. random()

该方法返回一个[0,1)之间的随机浮点数，例如：

```java
TXT复制double randomNum = Math.random();
System.out.println(randomNum); // 输出：0.398734867473452
```

1. round(x)

该方法返回参数x的四舍五入值，例如：

```java
TXT复制double x = 3.49;
int roundX = Math.round(x);
System.out.println(roundX); // 输出：3
```

1. sin(x)、cos(x)、tan(x)

这三个方法分别返回参数x的正弦、余弦和正切值（单位是弧度），例如：

```java
TXT复制double x = Math.PI / 6;
double sinX = Math.sin(x);
double cosX = Math.cos(x);
double tanX = Math.tan(x);
System.out.println(sinX + " " + cosX + " " + tanX); // 输出：0.5 0.8660254037844386 0.5773
```

#### Biginteger

1. BigInteger(String val)

该构造方法用于创建一个BigInteger对象，其值与参数val相等，例如：

```java
TXT
复制BigInteger bigInt = new BigInteger("12345678901234567890");
```

上述代码会创建一个BigInteger对象，其值为12345678901234567890。

1. add(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象与参数val相加的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("123456789");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.add(b);
System.out.println(c); // 输出：1111111110
```

1. subtract(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象减去参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("987654321");
BigInteger b = new BigInteger("123456789");
BigInteger c = a.subtract(b);
System.out.println(c); // 输出：864197532
```

1. multiply(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象乘以参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("123456789");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.multiply(b);
System.out.println(c); // 输出：1219326311376555329
```

1. divide(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象除以参数val的结果，例如：

```java
TXT复制BigInteger a = new BigInteger("1219326311376555329");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.divide(b);
System.out.println(c); // 输出：123456789
```

1. mod(BigInteger val)

该方法返回一个BigInteger对象，其值为当前对象除以参数val的余数，例如：

```java
TXT复制BigInteger a = new BigInteger("1219326311376555329");
BigInteger b = new BigInteger("987654321");
BigInteger c = a.mod(b);
System.out.println(c); // 输出：864197532
```

### Swing与awt

```java
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Main {
    public static void main(String[] args) {
        //JFrame对象
        JFrame jFrame1 =new JFrame("hello world");
        //设置JFrame的大小
        //setSize设置窗口大小
        //setLocation设置窗口
        //setBounds设置窗口的初始位置，窗口高度
        //setVisible设置窗口是否可见
        //setResizable设置窗口是否可调整大小，默认可调整
        //dispose撤销当前窗口，释放资源
        //JFrame的关闭方式
        //setDefaultCloseOperation：DO_NOTHING_ON_CLOSE,HIDE_ON_CLOSE,DISPOSE_ON_CLOSE(隐藏窗口，释放窗口占用资源),EXIT_ON_CLOSE

        jFrame1.setBounds(200,200,400,400);
        jFrame1.setVisible(true);
        jFrame1.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //JDialog
        JDialog jDialog =new JDialog(jFrame1,"I Love U");
        jDialog.setBounds(100,100,100,100);
        jDialog.setVisible(true);
        jDialog.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);

        //常用的面板
        //JPanel
        JFrame jFrame2 =new JFrame("test2");
        jFrame2.setBounds(500,500,100,100);
        jFrame2.setVisible(true);
        jFrame2.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        JPanel jPanel =new JPanel();
        JButton jb1=new JButton("open");
        JButton jb2=new JButton("close");
        JButton jb3=new JButton("apple");
        JButton jb4=new JButton("banana");
//        jPanel.setBounds(300,300,200,200);
        jPanel.add(jb1);
        jPanel.add(jb2);
        jPanel.add(jb3);
        jPanel.add(jb4);
        jPanel.setVisible(true);
//        jFrame.add(jPanel);
//        jPanel.setVisible(true);
//        jFrame.add(jPanel);
        //JScrollPane
        JScrollPane jScrollPane =new JScrollPane(jPanel);
        jScrollPane.setVisible(true);
        jFrame2.add(jScrollPane);

        //常用的组件
        //JLabel
        //构造方法方法，设置图标，水平对齐方式，设置文本
        JFrame jFrame3 =new JFrame("003");
        jFrame3.setBounds(250,250,50,50);
        jFrame3.setVisible(true);
        JLabel jLabel=new JLabel("test");
        jLabel.setVisible(true);
        jFrame3.add(jLabel);
        jFrame3.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        //JButton
        //按钮
        //setEnable设置按钮是否可用
        //setBorderPainted设置边界是否可用

        //单选按钮组件
        //JRadioButton，ButtonGroup
        //单选按钮需要被加入到按钮组中
        JFrame jFrame4 =new JFrame("005");
        jFrame4.setBounds(400,400,50,50);

        ButtonGroup buttonGroup =new ButtonGroup();
        jFrame4.setLayout(new FlowLayout());
        JRadioButton jRadioButton1 =new JRadioButton("test001");
        JRadioButton jRadioButton2 =new JRadioButton("test004");
        buttonGroup.add(jRadioButton1);
        buttonGroup.add(jRadioButton2);
        jFrame4.add(jRadioButton1);
        jFrame4.add(jRadioButton2);

        jFrame4.setVisible(true);
        jFrame4.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //下拉列表框组件
        //JComboBox
        //JComboBox(ComboBox dataModel) 使用list model创建一个下拉列表
        //方法addItem() 添加下拉内容

        JFrame jFrame5 =new JFrame("006");
        jFrame5.setBounds(50,50,200,200);
        jFrame5.setLayout(new FlowLayout());
        jFrame5.setVisible(true);
        jFrame5.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        JComboBox box =new JComboBox<>();
        box.addItem("hello world");
        box.addItem("I LOVE U");
        jFrame5.add(box);

        //菜单栏
        //一级菜单栏
        //二级菜单栏
        //创建菜单条JMenuBar  创建菜单 JMenu  创建菜单项 JMenuItem
        JFrame jFrame6 =new JFrame("menu test");
        jFrame6.setBounds(600,600,200,200);
        jFrame6.setLayout(new FlowLayout());
        jFrame6.setVisible(true);
        jFrame6.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        JMenuBar jMenuBar =new JMenuBar();
        JMenu jMenu =new JMenu("main menu !");
        JMenuItem jMenuItem1 =new JMenuItem("001");
        JMenuItem jMenuItem2 =new JMenuItem("002");
        JMenuItem jMenuItem3 =new JMenuItem("003");
        jMenuBar.add(jMenu);
        jMenu.add(jMenuItem1);
        jMenu.add(jMenuItem2);
        jMenu.add(jMenuItem3);
        jFrame6.add(jMenuBar);

        /*
        文本组件
        JTextField是单行文本框 JTextArea是多行文本框,可以使用转义字符进行操作
                JTextField和JTextArea都是Swing中的文本框组件，用于在GUI中显示和编辑文本内容。
                它们的区别如下：

                大小和样式：JTextField是一个单行文本框，只能显示一行文本；
                而JTextArea是一个多行文本框，可以显示多行文本。JTextField通常比较小，适合用于输入简短的文本；而JTextArea通常比较大，适合用于输入较长的文本。

                输入方式：JTextField只能输入单行文本，不能换行；
                而JTextArea可以输入多行文本，并支持换行。

                布局方式：JTextField默认使用FlowLayout布局，可以方便地对齐其他组件；
                而JTextArea默认使用BorderLayout布局，需要放在JScrollPane中才能正确显示滚动条。

                方法和属性：JTextArea相比JTextField拥有更多的方法和属性，
                例如设置行数、列数、自动换行、滚动条等等。
        */


        JFrame jFrame7 =new JFrame("text area!");
        jFrame7.setLayout(new FlowLayout());
        jFrame7.setBounds(0,400,200,200);
        JTextField jTextField1 =new JTextField("hell world  I LOVE U");
        JTextArea jTextArea1 =new JTextArea("hello asdasdasassda\nsdasiorhwfhfbcudd",2,5);
        jFrame7.add(jTextField1);
        jFrame7.add(jTextArea1);
        jFrame7.setVisible(true);
        jFrame7.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        //密码框组件
        JPasswordField jPasswordField1=new JPasswordField("psw");
        jPasswordField1.setColumns(10);//设置宽度
        jFrame7.add(jPasswordField1);


        /*
        事件监听
        基于接口的监听器
            基于接口的监听器是指实现了特定接口的类，用于响应特定的事件。
            例如，ActionListener接口用于响应按钮的点击事件，MouseListener接口用于响应鼠标的点击事件。
        基于适配器的监听器
            基于适配器的监听器是指继承了特定适配器类的类，用于响应特定的事件。适配器类是一个抽象类，实现了特定接口的所有方法，但是方法体为空。
            例如MouseAdapter类是MouseListener接口的适配器类，它实现了MouseListener接口的所有方
        */
        JFrame jFrame8 =new JFrame("action listener!");
        jFrame8.setBounds(800,400,300,300);
        jFrame8.setLayout(new FlowLayout());
        JButton jButton3 =new JButton("click me 001");
        JButton jButton4 =new JButton("click me 002");
        jButton3.addActionListener(new MyActionListener());
        jButton4.addMouseListener(new MyMouseListener());
        jFrame8.add(jButton3);
        jFrame8.add(jButton4);
        jFrame8.setVisible(true);
        jFrame8.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);


        //test
        JFrame jFrame9 =new JFrame("testing!");
        jFrame9.setBounds(400,400,300,300);
        JPanel jPanel1=new JPanel(new FlowLayout());
        jPanel1.setVisible(true);
        JPasswordField jPasswordField =new JPasswordField(5);
        jPasswordField.setVisible(true);

        JButton jButton5 =new JButton("click me and get password!");
        jButton5.addActionListener(e -> {
            char [] password=jPasswordField.getPassword();
            JOptionPane.showMessageDialog(null,new String(password));
        });
        jPanel1.add(jPasswordField);
        jPanel1.add(jButton5);
        jFrame9.add(jPanel1);
        jFrame9.setVisible(true);
        jFrame9.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    }
}




////////////////////////



import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class MyMouseListener extends MouseAdapter {
    @Override
    public void mouseClicked(MouseEvent e) {
        System.out.println("click me!!!");
    }
}


//////////////////////////



import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class MyActionListener implements ActionListener {
    @Override
    public void actionPerformed(ActionEvent e) {
        //按钮点击触发事件
        System.out.println("hello world!");
    }
}

```



#### 利用流对集合数据进行流水线处理

```java
import java.lang.reflect.Array;
import java.util.*;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //Stream的使用方法
        //单列集合        default Stream<E> stream()                            Collection中的默认方法
        //双列集合        无                                                   无法直接使用Stream流
        //数组           public static <T> Stream<T> stream(T[] array)        Arrays工具类中的静态方法
        //一堆零散数据     public static<T> Stream<T> of (T...values)           Stream接口中的静态方法
        //单列集合
        ArrayList<String> l1=new ArrayList<>();
        l1.add("张三");
        l1.add("李四");
        l1.add("王五");
        l1.add("赵六");
        l1.stream().forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //双列集合
        HashMap<Integer,String>hm1=new HashMap<>();
        //方法1：创建单列集合进行添加
        //Collections.addAll(m1,1,"a1",2,"b2",3,"c3");
        hm1.put(1,"a1");
        hm1.put(2,"b2");
        hm1.put(3,"c3");
        hm1.put(4,"d4");
        ArrayList<Integer>al1=new ArrayList<>();
        ArrayList<String>al2=new ArrayList<>();
        hm1.forEach((integer, s) -> {
            al1.add(integer);
            al2.add(s);
        });
        al1.stream().forEach(System.out::println);
        al2.stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //方法2:直接利用keyset方法和values方法进行键，值的单列集合的获取
        hm1.keySet().stream().forEach(System.out::println);
        hm1.values().stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //方法3：使用entryset方法进行键值对对象的获取，再利用流进行操作
        hm1.entrySet().stream().forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");
        //数组
        int [] arr1 ={1,2,3,4,5,6,5,43,21};
        Arrays.stream(arr1).forEach(System.out::println);
        System.out.println("-----------------------------------------------------------------------------------------------------------------");

    }
}
```

#### 流操作实例

```java
import java.lang.reflect.Array;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        //定义一个集合，并添加一些参数 1，2，3，4，5，6，7,8,9
        //过滤奇数
        ArrayList<Integer> al1=new ArrayList<>();
        Collections.addAll(al1,1,2,3,4,5,6,7,8,9);
        al1.stream().filter(s-> s%2==0).forEach(s-> System.out.println(s));
        System.out.println("--------------------------------------------------");
        //添加数据进入集合中，对每个数据的年龄进行判断，排除年龄小于等于24的并将数据添加到map集合中
        ArrayList<String>al2 =new ArrayList<>();
        Collections.addAll(al2,"zhangsan,23","lisi,24","wangwu,25");
        //在此处的字符串的判断中需要对字符串进行类型转换，利用Integer下的parseInt方法进行转换后对整形进行判断
        Map<String, String> m1 = al2.stream().filter(s -> Integer.parseInt(s.split(",")[1]) > 24).collect(Collectors.toMap(s -> s.split(",")[0], s -> s.split(",")[1]));
        m1.forEach((s, n)-> System.out.println(s+":"+n));
        System.out.println("-------------------------------------------------------");
        //创建两个集合，分别为男演员，女演员的集合
        //要求：男演员只需要名字为3个字的前两个人，女演员只要姓杨的，并且不要第一个，将过滤后的两个集合进行合并，同时将其变为Actor对象，将所有的对象添加到list集合中
        //Ps：演员类Actor，属性有name，age
        ArrayList<String> actor=new ArrayList<>();
        ArrayList<String> actress=new ArrayList<>();
        Collections.addAll(actor,"李华，18","白岩松，33","杨开山，25","张维为，40","赵匡胤，18","杨梅梅，19");
        Collections.addAll(actress,"李里，18","白江波，33","杨十五，25","杨十六，40","赵事实，18","杨萃萃，16");
        //System.out.println(actor);
        //actor.stream().filter(s->s.startsWith("杨")&&s.split(",")).forEach(s -> System.out.println(s));
        Stream<String> sm1 = actor.stream().filter(s -> s.split("，")[0].length() == 3).limit(2);
        Stream<String> sm2 = actress.stream().filter(s -> s.split("，")[0].startsWith("杨")).skip(1);//分别对两个流进行分别筛选打印
        List<Actor>l1=Stream.concat(sm1,sm2).map(s -> new Actor(Integer.parseInt(s.split("，")[1]),s.split("，")[0])).collect(Collectors.toList());
        //此处流的合并需要创建一个流的对象，方便后续的操作，在创建list的对象添加Actor的泛型，利用map进行匹配，
        System.out.println(l1);
//        sm3.forEach(s -> new Actor((Integer.parseInt(s.split("，")[0])),s.split("，")[1]));
//        System.out.println(sm3.collect(Collectors.toList()));
        System.out.println("-------------------------------------------------------");


    }
    static class Actor{
        private int age;
        private String name;

        public Actor() {
        }

        public Actor(int age, String name) {
            this.age = age;
            this.name = name;
        }

        /**
         * 获取
         * @return age
         */
        public int getAge() {
            return age;
        }

        /**
         * 设置
         * @param age
         */
        public void setAge(int age) {
            this.age = age;
        }

        /**
         * 获取
         * @return name
         */
        public String getName() {
            return name;
        }

        /**
         * 设置
         * @param name
         */
        public void setName(String name) {
            this.name = name;
        }

        public String toString() {
            return "Actor{age = " + age + ", name = " + name + "}";
        }
    }
}
```



### 方法引用

```java
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        Integer[] ite1={5,2,39,34,45,46,77,68,39};
        //匿名内部类
        Arrays.sort(ite1, new Comparator<Integer>() {
            @Override
            public int compare(Integer o1, Integer o2) {
                return o1-o2;
            }
        });
        //lambda表达式
        Arrays.sort(ite1,(Integer o1,Integer o2) ->{return (o1-o2);});
        //lambda简化表达式
        Arrays.sort(ite1,((o1, o2) -> o1-o2));
        //方法引用
        //Ps:方法引用处需要函数时接口，被引用的方法需要已经存在，被引用的形参和返回值需要与需要的形参由于返回值相同，满足当前的要求
        Arrays.sort(ite1,Main::Func);
        //此处静态的方法需要用类名对函数进行调用
        //::方法引用符

        //方法引用的分类
        //引用静态方法
        ArrayList<String>al1=new ArrayList<>();
        Collections.addAll(al1,"1","111111","11111","111","11","2");
        al1.stream().map(Integer::parseInt).forEach(s-> System.out.println(s));
        System.out.println("---------------------------------------------");
        //Integer::parseInt
        //引用成员方法
        //静态的方法中无法使用this关键字，需要使用时稚只能创建其对象进行操作，例如本类想要使用this只能创建本类的对象对其进行引用
        //对象::方法  1.其他  类名::方法名  2.本类this::方法名   3.父类super::方法名
        //关于本类与父类的方法需要注意:无法引用静态的方法，静态方法中无super与this关键字
        ArrayList<String>al2 = new ArrayList<>();
        Collections.addAll(al2,"张三","王五","李四","赵是三","张二三","张一三");
        al2.stream().filter(s -> s.length()==3).filter(s->s.startsWith("张")).forEach(s -> System.out.println(s));
        //al2.stream().filter(this::StringJudge)  此处为上述的实例
        al2.stream().filter(new Main()::StringJudge).forEach(s -> System.out.println(s));
        System.out.println("-----------------------------------");
        //引用构造方法(目的是为了创建对象)
        //格式：  类名::new
        ArrayList<String> al3=new ArrayList<>();
        al3.add("张无忌，15");
        //⬇此处详见类中注释
        List<Student> list1_stu = al3.stream().map(Student::new).collect(Collectors.toList());
        System.out.println(list1_stu);
        System.out.println("----------------------------------------------------------");
        //其他调用方法
        //使用类名引用构造方法，引用数组的构造方法
        //格式:  类名::成员方法   eg：String::subString
        //此方法的弊端在于，不能引用所有的方法，在只有一个参数时，能引用的方法仅仅是其类型的类，例如当参数为String 类下的参数时，只能引用在String类下的方法
        //第一个参数与引用的方法类型相同，第二个到最后一个需要保证原参数与引用方法的类型相同，
        ArrayList<String> al4=new ArrayList<>();
        Collections.addAll(al4,"aaa","bbb","ddd","ccc");
        al4.stream().map(String::toUpperCase).forEach(s -> System.out.println(s));
        //此处调用String类下的uppercas方法进行大小写转换

        System.out.println("-----------------------------------------------------------");
        //引用数组的构造方法
        //数组类型[]::new
        ArrayList<Integer> at1=new ArrayList<>();
        Collections.addAll(at1,1,2,3,4,5,6,7,8,9);
        //数组的类型与流中的数据类型保持一致
        Integer[] it1=at1.stream().toArray(Integer[]::new);
        //Arrays下的toString方法，保证其能合理输出
        System.out.println(Arrays.toString(it1));;

        //方法引用要点：1，被引用的方法需要有函数式接口，   2，被引用的方法必须已经存在，   3，被引用方法的形参必须和抽象方法的形参保持一致  4，满足需求
        ArrayList<String> al5=new ArrayList<>();
        Collections.addAll(al5,"张三，11","李四，12","王五，13");
        Student[] stu1 = al5.stream().map(Student::new).toArray(Student[]::new);
        System.out.println(Arrays.toString(stu1));

        System.out.println("-----------------------------------------------------------------");
        ArrayList<Student> astu1=new ArrayList<>();
        astu1.add(new Student(10,"张三"));
        astu1.add(new Student(11,"李四"));
        astu1.add(new Student(12,"王五"));
        String[] str2 = astu1.stream().map(new Function<Student, String>() {
            @Override
            public String apply(Student student) {
                return student.getName();
            }
        }).toArray(String[]::new);
        System.out.println(Arrays.toString(str2));
        System.out.println("------------------------------------------------");
        String[] str3 = astu1.stream().map(Student::getName).toArray(String[]::new);
        System.out.println(Arrays.toString(str3));
        System.out.println("------------------------------------------------");

        String[] str4 = astu1.stream().map(Student::toinformation).toArray(String[]::new);
        System.out.println(Arrays.toString(str4));


    }
    public static int Func(int o1, int o2)
    {
        return o1-o2;
    }
    public  boolean StringJudge(String s)
    {
        return s.startsWith("张")&&s.length()==3;
    }

}




//学生类
public class Student {
    private int age;
    private String name;

    public Student() {
    }

    public Student(int age, String name) {
        this.age = age;
        this.name = name;
    }
    public Student(String str)
    {
        String [] arr_str=str.split("，");
        age=Integer.parseInt(arr_str[1]);
        name=arr_str[0];
    }
    //由于对象的构造方法在创建时就已经返回了对象，所以上述的构造方法不会有返回值，
    //由于方法的引用需要参数与返回值的相同，所以在此处重载新的构造函数同时保证只有一种需要的参数即(String)
    //上述方法利用临时的字符串数组对参数进行截取，split如果无后续指定，默认将截取的剩下的存入字符串数组中

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return "Student{age = " + age + ", name = " + name + "}";
    }
    public String toinformation(){
        return (this.getName()+"-"+this.age);
    }
}
	

```

### 可变参数

```java
public class Main {
    public static void main(String[] args) {
        //可变参数：方法的形参数可以变化（从jdk5进行改进）
        //格式：属性类型...名字（例如int...args）
        //注意：方法的形参只能使用一个可变参数，当大于一个时会报错
        int sum=getSum(1,2,3,4,5,6,7,8,9,10);
        System.out.println(sum);

    }
    public static int getSum(int...args){
        int sum=0;
        for(int i:args){
            sum+=i;
        }
        return sum;
    }
}
```

### IO流

#### 文件File常用方法

```java
import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.sql.Array;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws IOException {
        //文件file的使用
        //路径：相对路径与绝对路径
        //1.根据文件路径创建对象
        String all="C:\\Users\\83899\\Desktop\\File_test.txt";//此处使用绝对路径
        File f1=new File(all);
        System.out.println(f1);
        //2.根据父路径与子路径   子路径：eg:a.txt
        String parent="C:\\Users\\83899\\Desktop";
        String children="File_test.txt";
        File f2=new File(parent,children);//此时在底层会根据操作系统使用不同的分隔符
        File f3=new File(parent+"\\"+children);

        File f4=new File(parent);
        File f5=new File(f4,children);//此处表示利用上一个file对象的路径作为父路径，第二个参数是子路径


        System.out.println("------------------------------1---------------------------------");
        //file判断和获取方法
        //isDriectory()      isFile()     exists()   length()     getAbsolutPath()       getpath()     getName()
        //length方法：只能获取文件的大小，如果获取的是文件夹，那么会导致其获取的数据显示为0   （单位是字节）

        File f8=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\text.txt");//此处路径下为文件
        File f9=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\test");//此处为文件的绝对路径
        System.out.println(f8.length());//39字节
        System.out.println(f9.length());//0

        //需要获取文件夹的大小需要累加各种文件的大小
        System.out.println("-----------------------------2------------------------------");
        //对文件夹进行判断
        File f6=new File(parent);//此处为文件夹
        System.out.println(f6.isDirectory());//判断是否为文件夹
        //对文件路径判断
        File f7=new File(all);
        System.out.println(f7.isFile());//判断是否为文件
        //判断文件路径是否存在
        System.out.println(f7.exists());
        System.out.println("-------------------------------3----------------------------");
        //获取文件绝对路径
        System.out.println(f7.getAbsolutePath());
        //获取文件相对路径
        System.out.println(f7.getPath());
        //返回文件的大小
        System.out.println(f7.length());
        //获取文件名字的大小
        System.out.println(f7.getName());//调用者为文件时会返回文件的名字+后缀，如果是文件夹会指返回文件夹的名称
        System.out.println("-------------------------------4--------------------------");
        //获取文件的上一次的更改时间（利用时间日期类SimpleDateFormat）
        File f10=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\src\\text.txt");
        long l1 = f10.lastModified();
        System.out.println(l1);//1677755995279   此处为毫秒
        Date dt1=new Date(l1);
        SimpleDateFormat sp1=new SimpleDateFormat("yyyy-mm-dd-HH-MM-SS");
        System.out.println(sp1.format(dt1));
        System.out.println("--------------------------------5------------------------");
        //文件的删除 创建
        //创建一个新的空的文件
        File f11=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\a1.txt");
        boolean b1 = f11.createNewFile();//此方法会出现两个选择，catch或者是抛出
        System.out.println(b1);
        //Ps：1.如果当前路径没有该文件，那么会创建这个文件，同时返回true，反之返回false，
        // 2.如果该路径的父级路径是不存在的，会出现IOException的异常
        // 3.利用createNewfile方法创建的一定是文件，如果没有指定后缀，他会直接创建一个没有后缀的文件
        System.out.println("----------------------------------6-------------------------------------");
        //创建单极文件夹（目录）
        File f12=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\b");
        boolean b2 = f12.mkdir();//mkdir方法make Directory
        System.out.println(b2);
        //创建多级文件夹（目录）
        File f13=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\c\\b\\a");
        boolean b3 = f13.mkdirs();
        System.out.println(b3);//创建多级文件夹也能创建单级文件夹，使用时可以使用多级文件夹，但是其底层是利用了mkdir()
        System.out.println("-----------------------------------7-------------------------");
        //删除文件夹
        File f14=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\text.txt");
        boolean b4 = f14.delete();
        System.out.println(b4);//PS:1.如果删除的是文件或者空的文件夹，直接删除不走回收站  2。如果删除的是非空的文件夹，会删除失败
        //获取并遍历
        File f15=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File");
        File[] ff1 = f15.listFiles();//该方法获取该路径下的所有文件内容
        for (File file : ff1) {
            System.out.println(file);
            //其中的file依次表示文件之中的各种文件夹和文件
        }//当调用者表示的路径是文件或不存在会返回null    当调用者的路径是空文件夹会返回长度为0的file数组   当调用者的路径是需要权限才能访问的文件是会返回null   除此之外都可以将文件夹中的文件依次返回（包括隐藏文件）


        //**************************************************************************//
        //lisiRoots()  获取系统所有盘符             list() 获取该路径下的所有文件名   list(文件名过滤器)    listFiles()
        File f16=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File");
        String s1 = ".txt";
        File[] ff2 = f16.listFiles(new FileFilter() {
            @Override
            public boolean accept(File pathname) {
                return pathname.isFile() && pathname.getName().endsWith(".txt");
            }
        });
        System.out.println(Arrays.toString(ff2));
        //同时与创建对象时相同会有相似之处，在pathname 和子路径，父路径匹配的相似



    }
}
```

#### 文件File对象训练

```java
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test\\a.txt");
        File f2=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test\\a");
        File f3=new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\lqb111\\ArryList\\File\\File_test");
        boolean b1 = f1.createNewFile();//创建文件
        boolean b2 = f2.mkdirs();//创建文件夹
        System.out.println(b1);
        System.out.println("------------------1-------------");
        boolean b3 = Search_avi(f1);
        System.out.println(b3);//整体思路对文件的每个文件进行遍历（不考虑子文件夹）
        boolean b4 = Search_Avi(f3);
        System.out.println(b4);//对该路径下的所有文件夹进行遍历，包括(子级目录下的)
        System.out.println("------------------2-------------");
        File f4=new File("D:\\DY3rn2jPq2_d5");
        delete(f4);//删除一个多级文件夹
        System.out.println("------------------3-------------");
        long getlen = Getlen(f4);//获取文件的总大小
        System.out.println("------------------4-------------");
        HashMap<String, Integer> getcount = getcount(f4);//统计相关后缀的文件夹数量
        System.out.println(getcount);
        System.out.println("------------------5-------------");
    }

    public static void Search_avi(){
        File[] files = File.listRoots();
        for (File file : files) {
            Search_avi(file);
        }
    }
    public static boolean Search_avi(File pathname){
        File[] ff1 = pathname.listFiles();
        for (File ff2 : ff1) {
            if(ff2.isFile()&&ff2.getName().endsWith(".avi")){
                return true;
            }
        }
        return false;
    }
    public static boolean Search_Avi(File pathname){
        File[] ff1 = pathname.listFiles();
        for (File ff2 : ff1) {
            if(ff2.isFile()){
                if (ff2.getName().endsWith(".avi")) {
                    System.out.println(ff2);
                }
            }else {
                Search_Avi(ff2);
                //此处直接递归，当调用者为文件夹时，直接对子级文件夹进行遍历，重复此过程
            }

        }
        return false;

    }
    public static void delete(File pathname){
        File[] files = pathname.listFiles();//进入文件
        for (File file : files) {//文件遍历
            if(file.isFile()){//判断是否为文件
                delete(file);//删除文件
            }else {
                delete(file);//若为文件夹，递归后删除文件夹
            }
        }
        pathname.delete();//删除自己
    }
    public static long Getlen(File pathname){
        File[] files = pathname.listFiles();
        long length=0;
        for (File file : files) {
            if(file.isFile()){
                 length = file.length()+ length;
            }else {
                 length = Getlen(file)+length;
            }
        }
        return length;
    }
    public static HashMap<String,Integer> getcount(File pathname){
        HashMap<String,Integer> hm1=new HashMap<>();//创建新Map集合
        File[] files = pathname.listFiles();//文件数组
        for (File file : files) {
            if(file.isFile()){//如果是文件
                String name = file.getName();
                String[] split = name.split("\\.");//对文件名进行分割处理
                if(split.length>=2){//当文件名为xxx.xxx或者xxx.xx.xxx
                    String Name=split[split.length-1];//获取最后一位
                    if(hm1.containsKey(Name)){//如果Map集合中已经存在
                        hm1.put(Name,hm1.get(Name)+1);////直接对其进行加1
                    }else {
                        hm1.put(Name,1);//如果不存在创建一个键值对且值初始化为1
                    }
                }
            }else {//如果不是文件
                HashMap<String, Integer> SonMap = getcount(file);//子文件集合
                for (Map.Entry<String, Integer> stringIntegerEntry : SonMap.entrySet()) {//增强for对集合进行遍历
                    String key= stringIntegerEntry.getKey();//获取键
                    int value= stringIntegerEntry.getValue();//获取值
                    if(hm1.containsKey(key)){
                        hm1.put(key,value+hm1.get(key));
                    }else{
                        hm1.put(key,value);
                    }
                }
            }
        }
        return hm1;//返回主集合
    }
}

```



#### 文件复制拷贝

```java
public static void File_copy(File pathname01,File pathname02) throws IOException {//文件拷贝方法（包含子级文件夹）
        pathname02.mkdirs();//在该路径创建一个文件夹（前提是该路径无文件夹）
        File[] files = pathname01.listFiles();
        for (File file : files) {//对文件数组进行遍历
            if(file.isFile()){//是文件
                int len = 0;
                byte []bytes1=new byte[20];
                FileInputStream fi1=new FileInputStream(file);
                FileOutputStream fo1=new FileOutputStream(new File(pathname02,file.getName()));
                while((len=fi1.read(bytes1))!=-1){//读入数组
                    fo1.write(bytes1,0,len);//按照数组依次写入
                }
                fo1.close();
                fi1.close();
            }else {//是文件夹
                File_copy(file,new File(pathname02,file.getName()));//递归时，父级路径使用pathname02，子级路径用new File 创建对象以及 getNname方法去创建同名文件夹
            }
        }
    }
```

#### 文件加密

```java
public static boolean File_lock(File pathname01,File pathname02) throws IOException {
        if(pathname01.isFile()){
            FileInputStream fi1=new FileInputStream(pathname01);
            FileOutputStream fo1=new FileOutputStream(pathname02);
            int len=0;
            byte[]bytes1=new byte[20];
            while((len=fi1.read())!=-1);{
                fo1.write(len^2);
            }
            fo1.close();
            fi1.close();
            return true;
        }else {
            return false;
        }
    }
```

#### 序列化流

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        File f1=new File("101.txt");
        //序列化流：用于输出对象的流（生于字节流中），需要关联基本流
        //构造方法
        ObjectOutputStream oos=new ObjectOutputStream(new FileOutputStream(f1));
        Student s1=new Student(18,"Lisa");
        oos.writeObject(s1);//此方法用于写对象
        oos.close();
        //反序列化流
        ObjectInputStream ois1=new ObjectInputStream(new FileInputStream(f1));
        Student o =(Student) ois1.readObject();//利用Stu对象接受反序列化流读取的对象
        System.out.println(o);
        ois1.close();
    }
}

//学生类
import java.io.Serial;
import java.io.Serializable;

public class Student implements Serializable {
    @Serial
    private static final long serialVersionUID=20230313L;//版本号的不变性可以让类中所有数据更改后依旧保持序列化的数据版本号不变
    private int age;
    private String name;

    public Student() {
    }

    public Student(int age, String name) {
        this.age = age;
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    public String toString() {
        return "Student{age = " + age + ", name = " + name + "}";
    }
}
```

#### 多对象写入文件

```java
import java.io.*;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) throws IOException, ClassNotFoundException {
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        
        //方法一：直接进行最原始的逐个写入逐个读取，速度较慢，且在读取到末尾时，会出现EOFException(文件末尾异常)

        //方法二直接使用Arraylist

        Student s1=new Student(18,"王梦楠","北京");
        Student s2=new Student(19,"林云龙","西安");
        Student s3=new Student(20,"李小龙","中国");
        ArrayList<Student> als1=new ArrayList<>();
        als1.add(s1);
        als1.add(s2);
        als1.add(s3);//存入Arraylist集合中
        /*
序列化多个对象
        ObjectOutputStream oos1=new ObjectOutputStream(new FileOutputStream(f1));
        oos1.writeObject(als1);
        oos1.close();             将上述集合直接写入
*/

        ObjectInputStream ois1=new ObjectInputStream(new FileInputStream(f1));
        ArrayList<Student>als2= (ArrayList<Student>) ois1.readObject();

        for (Student student : als2) {
            System.out.println(student);
        }
        //Student{age = 18, name = 王梦楠, address = 北京}Student{age = 19, name = 林云龙, address = 西安} Student{age = 20, name = 李小龙, address = 中国}
        ois1.close();//文件的读取末尾会出现EOFException文件末尾异常
    }
}
```

#### 字节打印流

```java
import java.io.*;
import java.nio.charset.Charset;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        //打印流(只写不读)
        //打印流的底层构造会依据你提供的，创建outputStream，他的构造参数有字符集编码类型，指定字符编码，自动刷新，Ps:打印流的底层没有缓冲区，所以自动刷新可有可无
        //write println print printf   都可以保证数据的原样写出
        File f1=new File("101.txt");
        PrintStream ps1=new PrintStream(new FileOutputStream(f1),true, Charset.forName("UTF-8"));
        ps1.println(99);
        ps1.print(true);
        ps1.println();
        ps1.printf("%s 爱上了 %s","阿珍","阿强");
        ps1.close();



    }
}
```

#### 字符打印流

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        //字符打印流在构造方法上与字节打印流一致
        //字符打印流拥有底层的缓冲区，所以效率比字节打印流要高
        PrintWriter pw1=new PrintWriter(new FileWriter(f1),true);//此处关联基本字符流
        pw1.write(99);
        pw1.println();
        pw1.println("I love YOU"); 
        pw1.print(true);
        pw1.printf("%s你来自何处呢","阿飞");
        pw1.close();
//        System.out.println();
        //上一行代码可以用以下方法代替
        PrintStream out = System.out;//此打印流在虚拟机启动时，由虚拟机创建，默认指向控制台
        out.println();//通过打印流调用方法（合理）
        System.out.println();//直接写法变为如此sout+
        //该打印流是唯一的，不关闭，在被关闭后会导致后续代码无法执行

    }
}
```

#### hutool包IO流操作

```java
import cn.hutool.core.io.FileUtil;
import cn.hutool.core.util.ReUtil;
import cn.hutool.http.HttpUtil;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        //hutool包使用
        //FileUtil类
        File f1=new File("101.txt");
        File f2=new File("102.txt");
        File f3=new File("103.txt");
        File f4=new File("Test_java");
        File f5=new File("Test(02)_java");
        File f6=new File("105.txt");
        File f7=new File("106.txt");


        File f8 = FileUtil.file();//此处查看其中的参数包含可变参数使用
        FileUtil.touch(f2);//touch方法创建一个新的文件夹，如果父级路径不存在，不报错直接创建父级路径，根据参数创建文件
        ArrayList<String>als1=new ArrayList<>();
        als1.add("aaa");
        als1.add("ccc");
        als1.add("bbb");
        FileUtil.writeLines(als1,f2,"UTF-8",true);//四个参数分别表示：集合名，文件写出的路径，字符集名称，是否追加
        FileUtil.appendLines(als1,f2,"UTF-8");
        List<String> str1 = FileUtil.readLines(f2, "UTF-8");//第三个参数是自己创建一个集合然后把数据存在集合中，其中它会把一行数据认为是集合中的一个
        String str2 = HttpUtil.get("https://hanyu.baidu.com/s?wd=%E7%99%BE%E5%AE%B6%E5%A7%93&device=pc&from=home");
        List<String> all = ReUtil.findAll("(.{4})(，|。)",str2, 1);//三个参数：正则表达式，传入的需要筛选的字符串，分组的所选组号
        System.out.println(all);
    }
}
```



### 异常

#### 异常概念

```java
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws ParseException {
        //Error 系统级别错误
        //Exception   异常，程序出现的问题，异常体系最上层父类为Exception
        // 1.编译时异常，未继承RuntimeException，直接继承于Exception，编译阶段就会错误提示
        //2.运行时异常：RuntimeException本身和子类，编译阶段没有错误提示，运行时出现的

        //编译时期异常
        String time="2023.3.1";
        SimpleDateFormat sdf1=new SimpleDateFormat("yyyy.mm.dd");
        Date date=sdf1.parse(time);
        //此处parse方法需要手动签名，否则报错
        System.out.println(date);


        //运行时期异常
        int[]arr1={1,2,3,4,5};
        System.out.println(arr1[10]);
        //次数数组索引越界但是不会在编译时期报错，在运行时会出现异常

        /*
         Java文件->（过程1）(通过javac命令)字节码文件->（过程2）(通过java命令)运行结果
        过程一：编译时异常     过程二：运行时异常
        编译时java不会运行代码，只会检查语法是否错误，或者优化性能
        编译异常就是为了提醒程序员检查本地信息 运行时期异常就是程序运行的错误
        throw 抛出关键字，在面对数据错误时，可以选择抛出数据错误去提醒操作者去更改数据
        例如：throw RuntimeException
        异常可以用来调试bug，也可以使代码调用者更改代码
        虚拟机异常Jvm：将异常打印在控制台，同时异常后的代码停止执行，
        自己处理异常
         */
        //自己处理异常（捕获异常）
//        try {
//            //可能出现的异常的代码                    //此处出现错误会创建相应错误的对象，下方catch会对异常进行捕获，在异常被捕获后会执行catch下的代码
//        }catch(异常类名 变量名){
//            异常的处理代码
//        }

        //目的时让代码出现异常时可以正常运行下去
        //try中不报错，直接执行try不会执行catch
        //try遇到了多个问题，多个catch进行捕获，如果存在异常的父子类关系，要把父类写在最下面
        //在jdk7拥有的新功能：异常中使用|隔开表示其是同一种解决方案
        //未捕获就会直接报错：很合理
        //try中遇到了问题：下面的代码不会执行，会跳到对应catch的语句中
        //getMessage 方法返回此throwable的详细信息字符串
        //tostring返回此错误的简短描述
        //printstackTrace把异常的错误输出在控制台，其中，printstackTrace是输出错误信息最多的方法，最为常用
        System.err.println(123);//错误的输出语句
        //throw 将异常抛出写在方法内，throws，写在方法定义处，告诉编写者此处需要注释异常




        //自定义异常1。定义异常类  2.写继承关系  3.空参构造  4.带参构造
        //目的是让报错信息更加的见名之意（方便查找问题）


    }
}
```

异常练习

```java
public class Girlfriend {
    private int age;
    private String name;

    public Girlfriend() {
    }

    public Girlfriend(int age, String name) {
        this.age = age;
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        if(age<18||age>40){
            throw new OverboundsException();
        }
        this.age=age;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        if(name.length()<3||name.length()>10){
            throw new OverboundsException();
        }
        this.name = name;
    }

    public String toString() {
        return "Girlfriend{age = " + age + ", name = " + name + "}";
    }
}


/////////////////////////////////////





import java.io.Serial;

public class OverboundsException extends RuntimeException{
    @Serial
    private static final long serialVersionUID = 2254863261008994300L;

    //在类名的命名时Exception
    //Exception主要是给维护人员检查用的
    public OverboundsException(){}
    public OverboundsException(String message){
        super(message);
    }
}


/////////////////////////////////////////////


import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Girlfriend gf1=new Girlfriend();
        Scanner sc1=new Scanner(System.in);
        while (true) {
            try{


                String agegf=sc1.nextLine();
                int age_gf = Integer.parseInt(agegf);//此处为第一个错误，NumberformatException错误
                gf1.setAge(age_gf);//此处报错RuntimeException

                String name_gf=sc1.nextLine();
                gf1.setName(name_gf);//此处也有可能会出现RuntimeException错误
                break;//如未捕捉到错误，直接停止循环，代表数据正常
            }catch(NumberFormatException n){
                n.printStackTrace();
            }catch (OverboundsException r){//Runtime Exception是NumberFormatException的父类，写在下面,二次改为OverboundExcrption,此处为自定义异常
                r.printStackTrace();//catch执行完之后无break继续执行
            }
            System.out.println("输入有误，重新输入");
        }

        System.out.println(gf1);
    }
}


/////////////////////////////////////////////
```



### 线程

#### 线程对象创建

```java
//方法1
public class ForThread1 extends Thread{
    @Override
    public void run() {
        while (true) {
            System.out.println(getName()+"开始发车！");
        }
    }
}
//方法2
public class ForThread2 implements Runnable{
    @Override
    public void run() {
        while (true){
            Thread t=Thread.currentThread();//获取当前线程的对象，同时返回给t
            System.out.println(t.getName()+"你好！");
        }
    }
}

//方法3
import java.util.concurrent.Callable;

public class ForThread3 implements Callable<String> {//此处Callable有泛型，表示返回线程结果的类型
    @Override
    public String call() throws Exception {
        return "你好我回来了";
    }
}


//////////////////////////////////


import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class Main {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        //线程
        //并发：同一时刻多个指令在单个CPU上同步运行
        //并行：同一时刻多个指令在多个CPU上同时运行
        //三种实现方式：
        //1，继承Threa类
        //特点：编程比较简单，可以直接使用Thread类中的方法，缺点是由于Java中类只能实现单继承，不能继承其他的类所以拓展性较大
        ForThread1 pc1=new ForThread1();
        ForThread1 pc2=new ForThread1();
        pc1.setName("Thread 1");
        pc2.setName("Thread 2");
        pc1.start();
        pc2.start();


        //2，实现Runnable接口
        //特点：拓展性强，实现该接口的同时还可以继承其他的类，编程相对于复杂，不能直接使用Thread类中的方法

        ForThread2 ft1=new ForThread2();
        Thread t1=new Thread(ft1);
        Thread t2=new Thread(ft1);
        t1.setName("THread 1");
        t2.setName("THread 2");
        t1.start();
        t2.start();
        //3，利用callable和Future接口方式实现，特点与方式2相同

        ForThread3 f3=new ForThread3();//创建实现了Callable接口的类的对象
        FutureTask<String> ft2=new FutureTask<>(f3);//创建FutureTask
        Thread t3=new Thread(ft2);//创建线程对象
        t3.start();//启动线程

        String str1 = ft2.get();//利用FutureTask对象的get方法获得其运行结果
        System.out.println(str1);//打印出结果

        //线程的生命周期
        //创建线程对象（新建）-> 有执行资格，无执行权（就绪，各个线程对CPU进行抢夺）->有执行资格有执行权（运行），如果被其他的线程抢走执行权，就会接着去就绪状态
        //当遇到其他的阻塞方法时线程会停止，没有执行资格也没有执行权，在run（）方法执行完毕后，线程会死亡

    }
}
```

#### 线程常用方法

```java
public class Main {
    public static void main(String[] args) {
        //常用方法：
        //String getName() 返回此线程的名称
        //void setName(String name)   设置线程的名字（构造方法也可以设置名字）
        //static Thread currentThread()   获取当前线程的对象
        //static void sleep(long time)     让线程休眠指定的时间，单位为毫秒


        //getName()          线程如果没有初始化名字，线程会有自己的默认名字Thread-X（x是从0开始的）
        ForThread ft1=new ForThread();
        Thread t1=new Thread(ft1);
        t1.setName("getName演示线程");
        t1.start();
        //在使用构造方法设置时，需要在子类重写一个对象
        //currentThread：获取当前线程的对象   
        Thread t2 = Thread.currentThread();
        System.out.println(t2.getName());//此处显示main  代表当前存在一个main线程
        // 当Java运行时，虚拟机会自动启动多条线程，其中的main线程就是所写的main方法里的代码，在之前所写代码基本都在mian线程中
        //sleep:那条线程执行到这个代码，就会休眠，休眠的时间长短与其中的参数有关，休眠结束继续执行之后的代码
        ForThread ft2=new ForThread("Thread构造方法演示");
        Thread t3=new Thread(ft2);
        t3.start();
        System.out.println(t3.getName());
    }
}

//线程优先级
public class Main {
    public static void main(String[] args) {
        //Thread方法
        //优先级：线程的优先级越高，优先运行的概率越大
        //线程的默认优先级为5         1~10
        //获取优先级的方法getPriorityd()
        //main线程的优先级默认为5
        ForThread01 ft1=new ForThread01();
        Thread t1=new Thread(ft1,"First");
        Thread t2=new Thread(ft1,"Second");
//        t1.start();
//        t2.start();
        System.out.println(t1.getPriority());//5
        System.out.println(t2.getPriority());//5

        t1.setPriority(10);
        t2.setPriority(1);
        //优先级不是绝对的而是概率问题

        t1.start();
        t2.start();


    }
}


/////////////////////////////////////



//守护线程
public class Main {
    public static void main(String[] args) throws InterruptedException {
        //守护线程
        //setDaemon() 设置守护线程
        // 当其他的非守护线程执行完毕，守护线程会陆续结束
        //应用场景  QQ聊天
        //出让线程
        //yield()
        //出让当前的CPU的执行权，尽可能的使线程执行的密集一点
        ForThread01 ft1=new ForThread01();
        Thread t1=new Thread("出让线程测试方法测试线程");
        Thread t2=new Thread("线程2");

        //插入线程
        //join()
        //将调用该方法的线程插入到当前的线程之前
        t1.join();
        for (int i = 0; i < 100; i++) {
            System.out.println("main线程"+i);
        }
    }
}

public class ForThread01 implements Runnable{
    @Override
    public void run() {
        for (int i = 0; i < 100; i++) {
            System.out.println(Thread.currentThread().getName()+i);
        }
    }
}

```

#### 线程锁

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ForThread01 implements Runnable{
    static int tickets=1;
    static Lock lock=new ReentrantLock();//Lock锁，创建Lock对象，由于Lock只是一个接口，只能创建他的实现类的对象，锁对象有上锁方法和解锁方法

    //锁线程关键字：synchronized(锁){
    //                       操作共享数据的代码
    //}
    //特点：1.锁默认打开，有一个线程进去后锁会自动关闭     2.里面的代码全部执行完毕，线程出来，锁自动打开


    //创建一个唯一的锁对象(使用static关键字修饰),或者使用类的字节码文件进行传入
    public void run() {

        while (true){
            //lock.lock();//上锁
            //将能共享数据操作的代码锁起来，在一个线程操作时，其余的线程就算有执行资格，也无法对其进行操作
            //解决线程问题方法：1，同步代码块
            //把操作共享数据的代码锁起来
            synchronized (ForThread01.class) {//对其中的代码上锁，Ps：锁对象一定得是唯一的
                if(tickets<=100){
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println(Thread.currentThread().getName()+"正在卖"+(tickets++)+"张票！");
                }else{
                    System.out.println("票已经卖完了！");
                    break;
                }
            }
            //lock.unlock();//解锁
            //在上述实例中，如果直接使用unlock()，会导致在循环中断后，锁对象未解锁，从而导致程序无法结束
            //解决方案：将代码块用try catch finally包裹，其中finally中的代码无论无论循环中断与否都可以正常执行，保证锁一定会被解开
        }
    }
}

////////////////////////////////////////


public class ForThread02 extends Thread{
    //同步方法
    int tickets=1;

    @Override
    public void run() {
        while (true)
         if(method()) break;
        }

    private synchronized boolean method() {//使用了synchronized关键字
            if(tickets==101){
                return true;
            }else {
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e);
                }
                System.out.println(Thread.currentThread().getName()+"在卖第"+(tickets++)+"张票！");
            }
        return false;
    }
}


////////////////////////////////


public class Main {
    public static void main(String[] args) {
        ForThread02 ft1=new ForThread02();
        Thread t1=new Thread(ft1,"1号窗口");
        Thread t2=new Thread(ft1,"2号窗口");

        Thread t3=new Thread(ft1,"3号窗口");
        t1.setPriority(1);
        t2.setPriority(5);
        t3.setPriority(10);
        //由于多个线程在操作时具有随机性，所以在面对多个线程操作同一个数据时会出现实际数据错误的情况
        t1.start();
        t2.start();
        t3.start();
        //StringBuffer是线程安全的
    }
}

```



### 反射

```java
import java.lang.reflect.*;

public class Learn_reflex {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException, NoSuchFieldException {
        //反射：允许对成员变量 成员方法 构造函数进行编程访问的操作
        //获取class对象的三种方式：
        //1.全类名：Class.forName("全类名") 2.类名.class  3.对象.getclass
        Class clazz1 = Class.forName("Student");
        Class clazz2 = Student.class;
        Student s1=new Student();
        Class clazz3 = s1.getClass();
//        System.out.println(clazz1);
//        System.out.println(clazz2);
//        System.out.println(clazz3);
        //获取构造方法的对象
        //getConstructors()           返回所有公共构造方法对象的数组
        //getDeclaredConstructors()   返回所有构造方法对象的数组
        //getConstructors()           返回单个公共构造方法对象
        //getDeclaredConstructor()    返回单个构造方法对象


        //Constructor类中用于创建对象的方法
        //T newInstance(Object。。。initargs)   根据指定的构造方法创建对象
        //setAccessible(boolean flag)          设置为true，表示取消访问检查
        System.out.println("=======================0=====================");
        Class<?> clazz4 = Class.forName("Student");//字节码文件对象
        Constructor<?>[] cons1 = clazz4.getConstructors();
        for (Constructor<?> con1 : cons1) {
            System.out.println(con1);
        }//获取所有的公共构造方法
        System.out.println("=======================1=====================");
        //获取所有的构造方法
        Constructor<?>[] dcons1 = clazz4.getDeclaredConstructors();
        for (Constructor<?> constructor : dcons1) {
            System.out.println(constructor);
        }
        System.out.println("========================2====================");
        //获取单个构造
        Constructor<?> dcon1 = clazz4.getDeclaredConstructor();//括号里面的参数需要和构造方法里面的参数保持一致
        Constructor<?> cons2 = clazz4.getConstructor(String.class, int.class, String.class);
        System.out.println("=========================3===================");
        int modf1 = cons2.getModifiers();
        System.out.println(modf1);
        //每个权限修饰符都有属于自己的一个值，即权限修饰符的整数形式
        Parameter[] cons2Parameters = cons2.getParameters();
        for (Parameter cons2Parameter : cons2Parameters) {
            System.out.println(cons2Parameter);
        }
        //返回构造方法中的所有参数
        System.out.println("=========================4==================");
        //利用构造方法创建对象
        //暴力反射
        cons2.setAccessible(true);//要想使用newInstance方法创建对象需要使用setAccessible方法去取消权限修饰符的校验
        Student stu1 = (Student)cons2.newInstance("张三", 18,"male");//创建对象
        System.out.println(stu1);
        System.out.println("=========================5==================");
        //                  利用反射获取成员变量
        //getFileds()                返回所有公共成员变量对象的数组
        //getDeclaredFileds()        返回所有成员变量对象的数组
        //getFiled(String name)                   返回单个公共成员变量对象
        //getDeclaredFiled(String name)           返回单个成员变量

        //Filed类中的创建对象的方法
        //void set(Object obj,Object value) 赋值
        //Object get(Object obj)            获取值
        System.out.println("=========================6==================");
        Class<?> clazz5 = Class.forName("Student");//字节码文件对象
        Field[] clazz5Fields = clazz5.getFields();
        for (Field field : clazz5Fields) {
            System.out.println(field);//遍历输出
        }
        //获取所有的公共的成员变量
        System.out.println("=========================7==================");
        Field[] clazz5DeclaredFields = clazz5.getDeclaredFields();//获取所有的成员变量
        for (Field field : clazz5DeclaredFields) {
            System.out.println(field);//遍历输出
        }
        System.out.println("=========================8==================");
        //获取单个公共成员变量
        Field gender = clazz5.getDeclaredField("gender");//返回成员变量gender
        //此处为私有变量无法获取，需要用Declared
        //获取单个成员变量
        Field age = clazz5.getDeclaredField("age");//返回成员变量age
        int genderModifiers = gender.getModifiers();//权限修饰符号
        String genderName = gender.getName();//成员变量的名字
        Class<?> genderType = gender.getType();//成员变量的数据类型
        //获取成员变量对象的值
        gender.setAccessible(true);//临时取消修饰符权限检查
        Student stu2=new Student("张三",18,"male");
        Object gender_stu2 = gender.get(stu2);//返回stu2对象的gender
        //修改对象里面的值
        gender.set(stu2,"Formal");//修改stu2对象里的gender为Formal
        System.out.println("=========================9==================");
        //                      反射获取成员方法
        //getMethods()                  返回共有的成员方法对象的数组，包括继承的
        //getDeclaredMethods()          返回成员方法对象的数组，不包括继承的
        //getMethod()                   返回单个公有成员方法对象
        //getDeclaredMethod()           返回单个成员方法对象


        //Method类中用于创建对象的方法
        //object invoke(Object obj,Objecct ...args):运行方法
        //其中  参数一：用obj对象调用该方法  参数二：调用该方法的传递的参数(如果没有就不写)  返回值：方法的返回值(如果没有就不写)
        System.out.println("========================10==================");
        Class<?> clazz6 = Class.forName("Student");
        Method[] clazz6Methods = clazz6.getMethods();//获取所有公共方法对象数组
        for (Method method : clazz6Methods) {
            System.out.println(method);
        }
        Method[] clazz6DeclaredMethods = clazz6.getDeclaredMethods();//获取所有的方法对象的数组
        for (Method method : clazz6DeclaredMethods) {
            System.out.println(method);
        }
        System.out.println("========================11==================");
        Method clazz6Method1 = clazz6.getMethod("setName", String.class);
        Method clazz6Method2 = clazz6.getMethod("setAge", int.class);
        //获取指定的方法
        Method getName = clazz6.getDeclaredMethod("getName");
        Method setName = clazz6.getDeclaredMethod("setName", String.class);
        Method testReflex = clazz6.getDeclaredMethod("test_reflex", String.class);//此方法为私有使用DeclaredMethod
        //获取方法的所有信息
        //获取方法的权限修饰符
        int setNameModifiers = setName.getModifiers();
        //获取方法名字
        String setNameName = setName.getName();
        //获取参数的个数
        int setNameParameterCount = setName.getParameterCount();
        //获取参数的类型
        Class<?>[] setNameParameterTypes = setName.getParameterTypes();
        //获取参数的对象数组
        Parameter[] setNameParameters = setName.getParameters();
        for (Parameter parameter : setNameParameters) {
            System.out.println(parameter);
        }
        //获取方法的返回值
        //获取方法的抛出异常
        Class<?>[] testReflexExceptionTypes = testReflex.getExceptionTypes();
        for (Class<?> exceptionType : testReflexExceptionTypes) {
            System.out.println(exceptionType);
        }
        System.out.println("========================11==================");
        //invoke 方法
        Student stu3=new Student();
        Object invoke = testReflex.invoke(stu3, "李四");//设置stu3对象的名字为李四，利用反射调用testreflex方法
        System.out.println(invoke);//此处输出返回值，即invoke方法的接受值就是返回值
        System.out.println("========================12==================");
    }
}


//学生类
public class Student {
   private String name;
   private int age;
   private String gender;

    public Student() {
    }

    public Student(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return gender
     */
    public String getGender() {
        return gender;
    }

    /**
     * 设置
     * @param gender
     */
    public void setGender(String gender) {
        this.gender = gender;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + ", gender = " + gender + "}";
    }
    private char test_reflex(String name){
        System.out.println(name);
        if (name.equals("0000"))throw new NullPointerException();
        if(name.equals("9999"))throw new RuntimeException();
        return name.charAt(1);

    }
    public void study(){
        System.out.println("学生在学习！");
    }
}

```

#### 利用反射写入将对象写入文件

```java
import java.io.*;
import java.lang.reflect.Field;

public class Test_Reflex {
    public static void main(String[] args) throws IllegalAccessException, IOException {
        Student s1=new Student("aaa",18,"male");
        Teacher t1=new Teacher(30,"bbb","English");
        File f1=new File("101.txt");
        saveObject(s1,f1);
    }
    public static void saveObject(Object obj, File pathname) throws IllegalAccessException, IOException {
        Class<?> objClasz = obj.getClass();
        BufferedWriter bw= new BufferedWriter(new FileWriter(pathname));//缓冲流
        Field[] objClaszDeclaredFields = objClasz.getDeclaredFields();
        for (Field field : objClaszDeclaredFields) {
            field.setAccessible(true);
            String name = field.getName();
            Object value = field.get(obj);
            bw.write(name+"="+value);
            bw.newLine();//换行
            System.out.println(name+"="+value);
        }
        bw.close();
    }
}
```

### Java_net

```java
import java.io.IOException;
import java.net.InetAddress;
import java.net.MulticastSocket;

public class group_net {
    public static void main(String[] args) throws IOException {
        //组播：IP范围：224.0.0.0~239.255.255.255
        //其中：224.0.0.0~224.0.0.255为预留的组播地址
        MulticastSocket ms=new MulticastSocket();//与单播的区别在于此处创建的为组播的对象
        //同样的，在没有参数的构造中使用随机的端口进行发送
        //打包数据和定义端口号操作相同（见SendData类）
        //在创建address对象时候，需要对多个数据接收对象进行同一个地址限制
        InetAddress address=InetAddress.getByName("224.0.0.1");

    }
}

```

```java
import java.util.ArrayList;

public class Java_net_learn {
    //三次握手：1.发出请求等待确认  2.回应请求   3.发出确认消息，链接建立
    //四次挥手：1.发出取消请求     2.接受请求同时验证服务的所有信息处理完毕  3.服务端发出确认信息
    // 4.客户端再次发送确认信息链接取消
    public static void main(String[] args) {

    }
}

```

```java
public class radio_net {
    public static void main(String[] args) {
        //广播地址：255.255.255.255
        //广播对象可以将IP改为255.255.255.255,直接就可以将信息发送在局域网的所有设备
    }
}

```

```java
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.SocketException;

public class ReceiveData {
    public static void main(String[] args) throws IOException {
        //接收数据包
        //创建端口对象
        DatagramSocket ds=new DatagramSocket(10086);
        byte []bytes=new byte[1024];

        DatagramPacket dp=new DatagramPacket(bytes,bytes.length);//接收的数据包不需要IP和端口

        while (true) {
            ds.receive(dp);//接收数据包
            byte[] data = dp.getData();
            int length = dp.getLength();
            System.out.println(new String(data,0,length));//打印数据
        }
    }
}

```

```java
import java.io.IOException;
import java.net.*;
import java.util.Scanner;

public class SendData {
    public static void main(String[] args) throws IOException {
        DatagramSocket ds=new DatagramSocket();//创建端口对象
        //空参构造：在可用的端口中随机选择一个进行发送
        //带参构造：指定端口
        Scanner sc=new Scanner(System.in);
        while (true) {
            System.out.println("Please enter words!");
            String s = sc.nextLine();
            if(s.equalsIgnoreCase("886")){//输入886结束数据包输入
                break;
            }
            byte []bytes=s.getBytes();
            InetAddress address=InetAddress.getByName("127.0.0.1");//定义IP对象
            int port=10086;//定义端口（整形）
            DatagramPacket dp=new DatagramPacket(bytes,bytes.length,address,port);//打包数据包
            ds.send(dp);//利用端口对象调用send方法发送数据包
        }
        ds.close();//释放资源
    }
}
```

```java
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class TCP_net {
    public static void main(String[] args) throws IOException {
        //客户端 Socket   服务端 SeverSocket
        //创建Socket对象，链接服务端，如果无法连接就会报错
        Socket socket=new Socket("127.0.0.1",1000);
        String s1 = "Hello China!";
        String s2 = "Hello 中国!";
        OutputStream os = socket.getOutputStream();
        os.write(s2.getBytes());
        socket.close();//关闭流
        //由此可见 TCP的底层是利用了IO流进行数据的操作

    }
}

```

```java
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class TCP_receive {
    public static void main(String[] args) throws IOException {
        //创建服务器端
        ServerSocket serverSocket=new ServerSocket(1000);//绑定端口
        Socket accept = serverSocket.accept();//监听用户的链接
        InputStream inputStream = accept.getInputStream();
        InputStreamReader ir=new InputStreamReader(inputStream);//此处使用转换流，使得输入的中文可以被读取出来，不出现乱码
        // 字节流->字符流
        int b=0;
        while ((b=ir.read())!=-1){
            System.out.println((char) b);
        }

        accept.close();//断开与客户端的链接
        serverSocket.close();//关闭服务器

    }
}

```



### 大学Java实验

#### 实验一

```java
//贪心猪
public class Main {
    public static void main(String[] args) {
        Player_computer pc1=new Player_computer(0,0);
        Player_person pp1=new Player_person(0,0);
        Game_TanxinPig(pp1,pc1);
        System.out.println("最终比分：  "+"人类"+pp1.getSum_score()+":"+"电脑"+pc1.getSum_score());
        System.out.println( (pp1.getSum_score()> pc1.getSum_score()? "人类":"电脑")+"是赢家！");
    }
    public static void Game_TanxinPig(Player_person pp,Player_computer pc){
        System.out.println("贪心猪游戏开始！");
        System.out.println("你先手，输入R（r）重新投掷骰子，输入H（h）保留本轮已得分数，进入电脑回合");
        System.out.println("--------------------------------------------------------------");
        while (pp.getSum_score()<100&&pc.getSum_score()<100){
            //当任意一方的总分达到100结束
            System.out.println("你的分数为："+pp.getSum_score()+"分");
            System.out.println("电脑分数为："+pc.getSum_score()+"分");
            //输出双方成绩和与点数
            pp.Play();
            //人类玩家先手
            pc.Play();
            //电脑玩家后手
            System.out.println("=========================================================");
        }
    }
}

////////////////////////////////////////////////////////




public class Play {
    public void Game_TanxinPig(Player_person pp,Player_computer pc){
        while (pp.getSum_score()<100&&pc.getSum_score()<100){
            //当任意一方的总分达到100结束
            System.out.println(pp);
            System.out.println(pc);
            pp.Play();
            //人类玩家先手
            pc.Play();
            //电脑玩家后手
        }
    }
}


////////////////////////////////////////////////////////

import java.util.Random;

/**

 玩家类，代表电脑玩家
 */
public class Player_computer {
    private int Sum_score; // 玩家获得所有分数之和
    private int Now_score; // 玩家在本轮获得的分数

    /**

     构造函数，创建一个新的玩家对象
     */
    public Player_computer() {
    }
    /**

     构造函数，创建一个新的玩家对象，指定总得分和本轮得分
     @param Sum_score 玩家获得所有分数之和
     @param Now_score 玩家在本轮获得的分数
     */
    public Player_computer(int Sum_score, int Now_score) {
        this.Sum_score = Sum_score;
        this.Now_score = Now_score;
    }
    /**

     获取玩家获得所有分数之和
     @return 玩家获得所有分数之和
     */
    public int getSum_score() {
        return Sum_score;
    }
    /**

     设置玩家获得所有分数之和
     @param Sum_score 玩家获得所有分数之和
     */
    public void setSum_score(int Sum_score) {
        this.Sum_score = Sum_score;
    }
    /**

     获取玩家在本轮获得的分数
     @return 玩家在本轮获得的分数
     */
    public int getNow_score() {
        return Now_score;
    }
    /**

     设置玩家在本轮获得的分数
     @param Now_score 玩家在本轮获得的分数
     */
    public void setNow_score(int Now_score) {
        this.Now_score = Now_score;
    }
    /**

     重写toString方法，返回玩家对象的字符串表示形式
     @return 玩家对象的字符串表示形式
     */
    public String toString() {
        return "Player_computer{Sum_score = " + Sum_score + ", Now_score = " + Now_score + "}";
    }
    /**

     玩家进行游戏的方法，模拟电脑玩家的游戏过程
     */
    public void Play(){
        Random r=new Random(); // 创建随机数生成器
        int Dice=r.nextInt(6)+1; // 随机生成1-6之间的整数，模拟骰子投掷结果
        System.out.println("电脑投掷点数为："+Dice+"点"); // 输出电脑投掷结果
        if(this.Now_score<20){ // 如果本轮点数总数小于20
            if(Dice==1){ // 如果电脑投掷骰子为1，直接中断
                this.Now_score=0; // 本次不得分
            }else { // 如果电脑投掷骰子数为2-6，继续下去
                this.Now_score=this.Now_score+Dice; // 累加本轮所得分数
                Play(); // 递归，再次调用Play方法
            }
        }else { // 如果本轮点数总数大于等于20
            this.Sum_score=this.Sum_score+this.Now_score; // 总得分为：原总得分+本轮所得分
            this.Now_score=0; // 重置本轮的已得分数供下一轮使用
        }
        this.Sum_score=this.Sum_score+this.Now_score; // 累加总得分
    }
}



////////////////////////////////////////////////////////

import java.util.Random;
import java.util.Scanner;
/**
 * @author 计算机2103 郑子豪
 */

/**

 玩家类，用于描述一个玩家的信息和行为

 包括总分数和本轮得分数

 可以进行投掷骰子、保留得分或重新投掷的操作
 */
public class Player_person {

    /**

     玩家获得所有分数之和
     */
    private int Sum_score;
    /**

     玩家本轮所得分数之和
     */
    private int Now_score;
    /**

     空参构造器
     */
    public Player_person() {
    }
    /**

     全参构造器，第一个参数为Sum_score，第二个参数为Now_score
     @param Sum_score 玩家获得所有分数之和
     @param Now_score 玩家本轮所得分数之和
     */
    public Player_person(int Sum_score, int Now_score) {
        this.Sum_score = Sum_score;
        this.Now_score = Now_score;
    }
    /**

     获取玩家总得分数
     @return 玩家总得分数
     */
    public int getSum_score() {
        return Sum_score;
    }
    /**

     设置玩家总得分数
     @param Sum_score 玩家总得分数
     */
    public void setSum_score(int Sum_score) {
        this.Sum_score = Sum_score;
    }
    /**

     获取玩家本轮得分数
     @return 玩家本轮得分数
     */
    public int getNow_score() {
        return Now_score;
    }
    /**

     设置玩家本轮得分数
     @param Now_score 玩家本轮得分数
     */
    public void setNow_score(int Now_score) {
        this.Now_score = Now_score;
    }
    /**

     重写toString方法，返回玩家总得分数和本轮得分数
     @return 玩家总得分数和本轮得分数
     */
    public String toString() {
        return "Player_person{Sum_score = " + Sum_score + ", Now_score = " + Now_score + "}";
    }
    /**

     玩家游玩方法，投掷骰子、保留得分或重新投掷
     */
    public void Play(){
        Random r=new Random();
        int Dice = r.nextInt(6) + 1;//随机数构成的6面骰子
        System.out.println("你本次投掷点数为："+Dice+"点");

        if(Dice==1){
            this.Now_score=0;
        }else {
            Scanner sc=new Scanner(System.in);
            String s = sc.nextLine();
            if(s.equalsIgnoreCase("r")){//如果输入R（忽略大小写），重新投掷筛子，
                this.Now_score=this.Now_score+Dice;//再玩一局得分为：目前已经获得的分数+骰子的点数
                Play();//再次Play，进行递归
            } else if (s.equalsIgnoreCase("h")) {//如果输入H保留得分
                this.Sum_score=this.Sum_score+this.Now_score+Dice;//保留得分的分数为：目前总得分数为：原总分数+已得分数+骰子点数
                this.Now_score=0;
            }else{
                System.out.println("请玩家按要求重新输入");
                Play();//输入非R（r） 非H（h）玩家重新输入
            }
        }
    }
}

```

#### 实验二

```java
public class ItemnotFound extends RuntimeException{
    //异常类
    public ItemnotFound() {};
    public ItemnotFound(String message) {
        super(message);
    };
}


////////////////////////////////////////////////////////
import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.LinkedList;

public class Main {
    public static void main(String[] args) throws IOException {
        File f1=new File("C:\\Users\\83899\\Desktop\\101.txt");
        LinkedHashMap<String,Integer> itemList=new LinkedHashMap<>();
        itemList.put("Books",1);
        itemList.put("Magazine",1);
        itemList.put("DVD",1);
        itemList.put("Blurays",1);
        itemList.put("MusicCD",1);
        Store s1=new Store(itemList);
        Warehouse w1= new Warehouse(s1);
        boolean porn = w1.addItem(s1, "Porn");
        System.out.println(porn);//true
        boolean dvd = w1.borrowItem(s1, "DVD");
        System.out.println(dvd);//DVD已经成功借出
        boolean books = w1.deletItem(s1, "Books");
        System.out.println(books);//true
        int blurays = w1.searchItem(s1, "Blurays");
        System.out.println(blurays);//2
        boolean dvd1 = w1.InputFile(f1, s1, "DVD");
        System.out.println(dvd1);//true
    }
}

////////////////////////////////////////////////////////
import java.io.Serial;
import java.io.Serializable;
import java.util.LinkedHashMap;
import java.util.LinkedList;
//商店类
public class Store implements Serializable {
    @Serial
    private static final long serialVersionUID = -2478039495513913839L;
    public LinkedHashMap<String,Integer> itemList;


    public Store() {
    }

    public Store(LinkedHashMap<String, Integer> itemList) {
        this.itemList = itemList;
    }

    /**
     * 获取
     * @return itemList
     */
    public LinkedHashMap<String, Integer> getItemList() {
        return itemList;
    }

    /**
     * 设置
     * @param itemList
     */
    public void setItemList(LinkedHashMap<String, Integer> itemList) {
        this.itemList = itemList;
    }

    public String toString() {
        return "Store{itemList = " + itemList + "}";
    }
}



////////////////////////////////////////////////////////
import org.jetbrains.annotations.NotNull;

import java.io.*;


//仓库类
public class Warehouse extends Store {

    @Serial
    private static final long serialVersionUID = -3707654935347249552L;

    public Warehouse() {
    }

    public Warehouse(Store store) {
        this.itemList=store.itemList;
    }

    public boolean addItem(@NotNull Store store, String item){
        if (store.itemList.containsKey(item)){
            System.out.println("货物已经存在！");
            return false;
        }else {
            store.itemList.put(item,1);
            return true;
        }

    }
    public boolean deletItem(@NotNull Store store, String item){
        if (store.itemList.isEmpty()){
            return false;
        }
        else if(store.itemList.containsKey(item)){
            store.itemList.remove(item);
            return true;
        }else {
            return false;
        }

    }
    public int searchItem(@NotNull Store store, String item){
        if (store.itemList.isEmpty()){
            return -1;//如果货物链表为空返回-1
        }
        else {
            return (store.itemList.get(item)+1);
            //返回链表的逻辑位序
        }
    }
    public boolean borrowItem(@NotNull Store store, String item){
        if(store.itemList.isEmpty()){
            return false;//如果商店为空返回错误
        }else {
            if(store.itemList.get(item)==1){//货物未被借走
                System.out.println(item+"已经成功借出");
                store.itemList.remove(item);
                store.itemList.put(item,0);
                return true;
            }else if (store.itemList.get(item)==0){//货物已经被借出
                System.out.println(item+"已经被借出");
                throw new ItemnotFound();//抛出货物未找到异常
            }else {
                return false;//货物不存在
            }
        }
    }
    public boolean InputFile(File pathname, @NotNull Store store, String item) throws IOException {
        if(store.itemList.isEmpty()){
            return false;//如果列表为空
        }else if(store.itemList.containsKey(item)){//如果列表中包含货物
            char[]chars=new char[30];
            FileWriter fileWriter=new FileWriter(pathname);
            Integer integer = store.itemList.get(item);
            fileWriter.write(item+":"+integer);
            fileWriter.close();//关闭流
            return true;
        }else {
            //货物未找到
            throw new ItemnotFound();
        }
    }

    public String toString() {
        return "Warehouse{}";
    }
}
```

#### 实验三

##### 1.

```java
import java.util.ArrayList;

public class TimerAlarm extends Thread{

    private int totalSeconds = 0;
    private boolean isRunning = true;

    public void run() {
        while (isRunning) {
            totalSeconds++;
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public void stopTimer() {
        isRunning = false;
    }

    public void displayTime() {
        int hours = totalSeconds / 3600;
        int minutes = (totalSeconds % 3600) / 60;
        int seconds = totalSeconds % 60;
        System.out.printf("%02d:%02d:%02d\n", hours, minutes, seconds);
    }

    public void displayTotalSeconds() {
        System.out.println("Total seconds: " + totalSeconds);
    }
}
////////////////////////////////////////////////////////
import java.math.BigInteger;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        TimerAlarm timer = new TimerAlarm();
        timer.start();

        try {
            while (true) {
                timer.displayTime();
                Thread.sleep(1000);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            timer.stopTimer();
            timer.displayTotalSeconds();
        }
    }
}

```

##### 2.

```java
import cn.hutool.core.io.FileUtil;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        File word_sorce = new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\MyJava\\Code in (college)\\Test_13\\src\\words.txt");
        File newwords_sorce = new File("D:\\Learning\\code in college(2AB)\\code in(2AB)\\LanQiaoBei111\\MyJava\\Code in (college)\\Test_13\\src\\newwords.txt");
        ArrayList<String> als = new ArrayList<>();
        FileUtil.readLines(word_sorce, "UTF-8", als);
        Collections.reverse(als);
        FileUtil.writeLines(als, newwords_sorce, "UTF-8", true);
    }
}
```

#### 实验四

```java
import javax.swing.*;
import java.util.ArrayList;
public class Windows extends JFrame  {
    public Windows() {
        this.setLayout(null);
        this.setVisible(true);
        this.setBounds(0,0,1000,600);

        JButton button_sort=new JButton("字典排序");
        button_sort.setBounds(200,300,100,20);//排序按钮
        this.add(button_sort);
        button_sort.setVisible(true);

        JButton button_clear=new JButton("清空");
        button_clear.setBounds(600,300,100,20);//清空按钮
        this.add(button_clear);
        button_clear.setVisible(true);

        JTextArea text_in=new JTextArea();
        text_in.setBounds(0,0,500,300);//输入文本框
        this.add(text_in);
        text_in.setVisible(true);

        JTextArea text_sort=new JTextArea();
        text_sort.setBounds(500,0,500,300);//排序文本框
        this.add(text_sort);
        text_sort.setVisible(true);

        button_clear.addActionListener(e -> {
            text_sort.setText("  ");
            text_in.setText("  ");
        });


        button_sort.addActionListener(e -> {
            ArrayList<String> als=new ArrayList<>();
            String s1=" ";
            String text []= text_in.getText().split("\n");
            for (String s : text) {
                als.add(s);
            }
            als.sort(String::compareTo);

            for (int i = 0; i < als.size(); i++) {
                if(i==1){
                    s1=als.get(i);
                }
                s1=s1+"\n"+als.get(i);
            }
            text_sort.setText(s1);
        });
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}


////////////////////////////////////////////



public class Main {
    public static void main(String[] args) {
        new Windows();
    }
}
```

# 前端框架

> ***bootcdn引入***

## Vue2

> vue2的标签引入

```html
  <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.13/vue.js"></script>
```

> 前提:安装node.js(版本大于16.0)
>
> 使用npm进行vue项目的创建或者直接使用标签引入

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>for vue</title>
  <link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/4.5.3/css/bootstrap.min.css">
  <script src="https://cdn.bootcdn.net/ajax/libs/axios/1.3.6/axios.min.js"></script>
  <script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.13/vue.js"></script>
</head>

<body>
  <div id="app">
  </div>
  <script>
    const vue1 = new Vue({
      el: '#app',//指定挂载点
      data: {
          //数据域用于存放变量
      },
      methods: {
        //methods用于存放方法,可以使用this.变量进行调用
      },
    })


  </script>
</body>
</html>
```

### vue2代码实例

```html
<!DOCTYPE html>
<html lang="zh" xmlns:th="http://www.thymeleaf.org">

<head>
  <meta charset="UTF-8">
  <title>demo</title>
</head>
<style>
  .big {
    height: 100px;
    width: 100px;
    /* 边框实线 */
    border: 1px solid black;
  }

  .pink {
    background-color: pink;
    height: 100px;
    width: 100px;
    border: 1px solid pink;
  }

  /* 添加表格边框每个单元格都是单实线 */
  table,
  th,
  td {
    width: 500px;
    height: 30px;
    border: 1px solid black;
    text-align: center;
    border-collapse: collapse;
  }

  /* div加边框线 */
</style>

<body>



  <div id="app">
    <template>
      <!-- 插值表达式:利用表达式插值 -->
      <!-- 不能在标签中使用 -->
      {{msg}}
      <br>
      <!-- 动态设置innerHTML -->
      <div v-html="location"></div>
      <!-- show -->
      <!-- 切换样式的隐藏,display:none -->
      <div v-show="flag">v-show</div>
      <!-- 条件渲染 -->
      <!-- 直接不显示 -->
      <div v-if="flag==1">条件渲染</div>
      <div v-else-if="flag==2">那就渲染</div>
      <div v-else>否则渲染</div>
      <!-- v-on事件绑定 -->
      <button v-on:click="count--">--</button>
      {{count}}
      <button @click="add">++</button>
      <br>
      <button @>取反</button>
      <!-- v-bind -->
      <div :title="title">你好</div>
      <!-- v-for -->
      <ul>
        <li v-for="(item,index) in name_list" :key="index" :title="item">
          {{item}}
        </li>
      </ul>
      <!-- v-model数据的双向绑定 -->
      <!-- trim自动去首尾空格 -->
      <!-- stop阻止冒泡,prevent阻止默认行为 -->
      <input type="text" v-model.trim="username">
      <span>{{username}}</span>
      <br>
      <!-- keyup.enter回车监听 -->
      <input @keyup.enter="password=''" type="password" v-model="password">
      <span>{{password}}</span>
      <br>
      <button @click="username='',password=''">重置</button>
      <!-- 控制类选择器,大括号的键值对选择和(类名的来回切换),中括号的类名全选(class列表) -->
      <div :class="{big:true,pink:pink_disp}">big</div>
      <button @click="ret">粉色切换{{pink_disp}}</button>
      <div :class="['big','pink']">big</div>
      <!-- 动态操作css样式 -->
      <!-- 加粗 -->
      <button :style="{color:'red',fontSize:'20px',bold:'normal'}">一行红字</button>
      <br>
      <!-- v-model多种绑定 -->
      <input type="text" v-model="words" value="text">{{words}}
      <br>
      <input type="checkbox" v-model="isCheck" value="checkbox">{{isCheck}}
      <br>
      <input type="radio" name="gender" v-model="gender" value="男">男
      <input type="radio" name="gender" v-model="gender" value="女">女
      <br>
      <div>性别:{{gender}}</div>
      <br>
      <select v-model="countryId">
        <option value="001">中国</option>
        <option value="002">美国</option>
        <option value="003">意大利</option>
      </select>
      <div>国家:{{countryId}}</div>
      <br>
      <textarea v-model="cv"></textarea>
      <p>简历:{{cv}}</p>
      <!-- computed计算属性和methods计算属性 -->
      <!-- computed封装了对数据的处理,求得了一个结果
      写在computed配置项中,作为属性直接使用
      拥有缓存特性
      -->
      姓:<input type="text" style="width: 15px;" v-model="firstName">
      名:<input type="text" style="width: 15px;" v-model="lastName">
      <br>
      <div>顺序全名:{{ fullName }}</div>
      <div>倒转全名:{{ secondName }}</div>
      <table>
        <thead>
          <tr>
            <th>学号</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>性别</th>
            <th>分数</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody v-if="stuList.length>0">
          <tr v-for="(item,index) in stuList" :key="index">
            <td>{{item.stuId}}</td>
            <td>{{item.姓名}}</td>
            <td>{{item.年龄}}</td>
            <td>{{item.性别}}</td>
            <td>{{item.分数}}</td>
            <td>
              <button v-if="stuList.length>0" @click="delStu(index)">删除</button>
            </td>
          </tr>

        </tbody>
        <tbody v-else>
          <tr>
            <td colspan="7">暂无数据</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="7">
              学号<input type="text" style="width: 30px;" v-model="stuId">
              姓名<input type="text" style="width: 50px;" v-model="stuName">
              年龄<input type="text" style="width: 30px;" v-model="stuAge">
              性别<input type="text" style="width: 20px;" v-model="stuGender">
              分数<input type="text" style="width: 20px;" v-model="stuScore">
              <button @click="stuAdd()">添加</button>
            </td>
          </tr>
          <tr>
            <td v-if="stuList.length>0" colspan="7">学生共{{stuList.length}}人,平均分{{avg_score}}</td>
          </tr>
        </tfoot>
      </table>
      <br>
      <br>
      <!-- watch监听器 -->
      <!-- 存在深度监听可将对象数组的每一层属性同时监听 -->
      <textarea v-model="translate" name="trans">
      </textarea>
      <br>
      <input type="text" v-model="objRed.name">
      <br>
      <br>
      <!-- vue的生命周期的4个阶段 -->
      <!-- 创建阶段created,挂载阶段mounted,更新阶段updated,销毁阶段destroyed -->
      <!-- 创建阶段进行数据的初始化,挂载阶段进行实例的挂载,更新阶段数据不断在修改与更新视图中进行切换,销毁阶段vue实例会被销毁,各类定时器等资源会被释放,被卸载后不会进行任何的更新视图等操作 -->
      <!-- 分别对应8个相应的钩子函数 -->
      <!-- 搜索输入框案例:mounted后自动获取焦点 -->
      <input type="text" v-model="words" id="inp">
      <br>
      <br>
      <div id="eg" style="height: 450px;width: 500px;border: 1px solid black;"></div>



    </template>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/vue@2.7.14/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
  <script>
    const app = new Vue({
      // 指定挂载点
      el: '#app',
      // 数据渲染
      data: {
        msg: 'Hello Vue!',
        location: `<a href="https://www.baidu.com">百度</a>`,
        flag: 2,
        count: 0,
        title: '你好啊',
        name_list: ["张三", "李四", "王五"],
        username: '',
        password: '',
        pink_disp: false,
        words: '',
        isCheck: true,
        gender: '',
        countryId: '002',
        cv: '',
        firstName: '张',
        lastName: '三',
        stuAge: '',
        stuId: '',
        stuName: '',
        stuGender: '',
        stuScore: '',

        stuList: [
          { stuId: "001", 姓名: "张三", 年龄: 18, 性别: '男', 分数: 100 },
          { stuId: "002", 姓名: "李四", 年龄: 19, 性别: '女', 分数: 88 },
          { stuId: "003", 姓名: "王五", 年龄: 20, 性别: '男', 分数: 92 }
        ],
        translate: '',
        objRed: {
          name: 'redBox',
          style: {
            color: 'red'
          }
        },
        words: '',
      },
      computed: {
        fullName() {
          return this.firstName + this.lastName
        },
        // 计算属性两种写法,简易写法是属性值(),全写法(属性值:{get(){},set(){}},其中get代表是属性计算,而set是属性赋值)
        secondName: {
          get() {
            return this.lastName + this.firstName
          },
          set(value) {
            this.firstName = value.slice(0, 1)
            this.lastName = value.slice(1)
          }
        },
        avg_score() {
          // var sum = 0
          // this.stuList.forEach(item => {
          //   return item.分数 + sum
          // })
          // 求学生分数均值
          return (this.stuList.reduce((sum, item) => {
            return item.分数 + sum
          }, 0) / this.stuList.length).toFixed(1)
        }
      },
      methods: {
        add() {
          this.count++
        },
        ret() {
          this.pink_disp = !this.pink_disp
        },
        delStu(index) {
          this.stuList.splice(index, 1)
        },
        stuAdd() {
          if (isNaN(this.stuId) || isNaN(this.stuAge) || isNaN(this.stuScore) || (this.stuGender != '男' && this.stuGender != '女')) {
            alert('数据非法')
            return
          }
          if (this.stuId == '' || this.stuName == '' || this.stuAge == '' || this.stuGender == '' || this.stuScore == '') {
            alert('请填写完整信息')
            return
          } else {
            this.stuList.push({
              stuId: this.stuId,
              姓名: this.stuName,
              年龄: this.stuAge,
              性别: this.stuGender,
              分数: this.stuScore
            })
            // 再次置空
            this.stuId = this.stuName = this.stuAge = this.stuGender = this.stuScore = ''
          }
        },
      },
      watch: {
        translate(newValue, oldValue) {
          console.log(newValue, oldValue);
        },
        objRed: {
          deep: true,
          handler(newValue, oldValue) {
            console.log(newValue, oldValue);
          }
        },
      },
      mounted() {
        // document.querySelector('#inp').focus()
        var myChart = echarts.init(document.getElementById('eg'))
        var option = {
          title: {
            text: 'Referer of a Website',
            subtext: 'Fake Data',
            left: 'center'
          },
          tooltip: {
            trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            left: 'left'
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: '50%',
              data: [
                { value: 1048, name: 'Search Engine' },
                { value: 735, name: 'Direct' },
                { value: 580, name: 'Email' },
                { value: 484, name: 'Union Ads' },
                { value: 300, name: 'Video Ads' }
              ],
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
      }

    })

  </script>
</body>

</html>
```

## axios

> axios的标签引入

```html
<script src="https://cdn.bootcdn.net/ajax/libs/axios/1.3.6/axios.min.js"></script>
```

# JavaWeb

## JDBC

***(Java DataBase Connectivity)***

***面向接口编程,操作所有关系型数据库,对于不同的数据库进行不同的jar包进行导入***

### 基础实例

***1.导入对应数据库的jar包(以下使用MYSQL)***

```java
package org.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class Main {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
//        1.注册驱动
        Class.forName("com.mysql.jdbc.Driver");//可以省略
        String url = "jdbc:mysql://localhost:3306/jdbc_learning";
        String username = "root";
        String psw = "123456";
        //2.获取链接
        Connection connection = DriverManager.getConnection(url, username, psw);
//        3.定义sql语句
        String sql = "update student set age=25 where id=2  ";
//      4.获取执行sql对象
        Statement statement = connection.createStatement();
//        5.执行sql语句
        int update = statement.executeUpdate(sql);
//        6.返回处理结果
        System.out.println(update);
//        7.释放资源
        statement.close();
        connection.close();

    }
}

```

### API详解

#### DriverManager

***1.注册驱动***

***2.建立连接***

***在本机状态,默认端口可以直接写jdbc:mysql:///数据库名称,配置useSSL=false参数,解决警告提示***

#### Connection

***1.获取执行sql对象***

> 普通执行sql对象
>
> ```java
> Statement createStatement()
> ```
>
> 预编译sql执行的sql对象:防止sql注入
>
> ```java
> PreparedStatement prepareStatement(sql)
> ```
>
> 执行存储过程的对象
>
> ```java
> CallableStatement prepareCall(sql)
> ```
>
> 

***2.事务管理***

> JDBC事务管理:Connection接口中定义了3个对象的方法
>
> 开启事务:setAutocommit(boolean autoCommit):true为自动提交事务,false为手动提交
>
> 提交事务:commit()
>
> 回滚事务:rollback()

#### Statement

***1.执行sql语句***

> int excuteUpdate(sql):执行DML,DDL语句
>
> ResultSet excuteQuery(sql):执行DQL语句,返回值为结果集对象

#### ResultSet

***1.封装了DQL语句的查询结果***

> ```java
> boolean next():光标向下移动一行,判断当前行是否为有效行
> xxxgetInt(参数)
> xxxgetString(参数):int,列的编号从一开始;String,列的名称
> ```
>
> 

#### PreparedStatement

***1.预编译sql语句的对象,PreparedStatement继承于Statement***

***2.设置参数值***

> ```java
> PreparedStatement对象:setXxx(参数1,参数2):给?赋值
> 	Xxx:数据类型;如setInt(参数1,参数2)
> 	参数:
> 		参数1:?位置标号,1开始
> 		参数2:?的值
> ```

***3.执行sql***

> ```java
> excuteUpdate();/excuteQuery();:不需要传递sql
> ```

### 数据库连接池

> 标准接口(任何连接池都需要实现):DataSource
>
> ```java
> Connection getConnection()
> ```
>
> 常见数据库连接池:DBCP,C3P0,Druid



## HTML

### 常见标签

| 标签名              | 用法                                                         |
| ------------------- | ------------------------------------------------------------ |
| <br                 | html源码中换行                                               |
| <p</p               | 段落标签，用于在展示效果中划分段落，并自动在段前段后添加空白行<br />align参数：段落的对齐方式 |
| <h1</h1             | 标题标签，一共六级，h6最小                                   |
| &nbsp               | html源码中的多个空格，效果中最终合并为一个                   |
| <img/               | 图片标签  src参数：文件路径  weight，height：宽高            |
| <ul</ul             | 无序列表标签                                                 |
| <li</li             | 列表条目项标签，定义列表的条目                               |
| <ol</ol             | 有序列表标签                                                 |
| <a</a               | 超链接标签  href参数：超链接跳转路径  （可以跳转到网站链接，文件链接） |
| <table</table       | 表格标签，定义一个表格，  border：表格边框粗细，  width属性：设置表格的宽度 |
| <tr</tr             | 表格行标签                                                   |
| <td</td             | 表格单元格标签                                               |
| <th</th             | 表格的表头单元格标签，用于在效果中定义一个表格行中的表头单元格，<th  <td区别在于<th内容居中加粗<br />colspan属性：跨列合并单元格  rowspan属性：跨行合并单元格<br />属性值为需要合并的单元格的数量 |
| <span</span         | 行级的块标签，用于在效果中定义一个块，span有多少内容就会占多大空间，不会自动换行 |
| <div</div           | 块级的块标签，用于在效果中定义一块，默认占满一行，进行内容的展示，默认占满一行会自动换行 |
| <frameset</frameset | 框架标签，多个窗口页面整合在一起的一个集合（框架集），每个页面（框架）都是一个单独文档，都需要用子标签<frame来确定页面的位置，<frameset通过列和行来确定整体布局，使用cols确定列数，使用rows确定行数，多个<frameset可以嵌套使用<br /><frameset与<body不可以并存 |
| <frame              | src属性：确定页面的路径  noresize属性：框架分割线不移动<br />target属性：确定需要显示的页面在何处显示 |
|                     |                                                              |
|                     |                                                              |



## JavaScript

### jQuery库的在线引用

```html
  <script src="https://code.jquery.com/jquery-3.0.0.min.js"></script>
```

### 引入方式

#### 内部脚本

```html
<script>
	alert("hello world")
</script>
<!--可以出现任意次-->
```

#### 外部脚本

```html
<script src="test.js"></script>
<!--不能自闭合-->
```

### 基础语法

#### 输出

***Ps：1.单行注释和多行注释与Java相同  ***

***2.分号可有可无***

```html
<script>
    window.alert("hello world");//浏览器弹出警告框
	
	document.write("hello js!")//写入html在浏览器显示

	console.log("hello my js ")//写入浏览器控制台
 </script>
```

#### 变量

```js
//弱类型语言，用var关键字声明变量
var a=20
a=“test”

//var定义的变量为全局变量，可以重复声名


//在ECMAScript中新增了let关键字，其声名的变量仅在let代码块内有效，不允许重复声名
//新增const关键字，一旦声名不可更改
```

#### 数据类型

```js
//原始类型
number	//数字（整数，小数，NaN（Not a number））
string	//字符串（单双引号皆可）
boolean	//布尔
null	//空
undefined	//当声名的变量未初始化时默认为undefined

//引用类型

```

#### 运算符

```js
//算数运算符：	+ - * / % ++ --
//赋值运算符：	= += -= *= /= %=
//比较运算符：	> < >= <= != == ===		
//==会进行类型转换  ===不会进行类型转换
//逻辑运算符：	&& || ！
//三元运算符：	条件表达式?true_value:false_value

/*
类型转换
将字符串字面值转换为数字，如果字面值不是数字转为NaN
其他类型转boolean：1.Number：0，NaN均为false，其他true
					2.string：空字符串为false
					3.Null和undefined均为false
利用parseInt进行转数值操作
*/
//插值表达式：{{表达式}},内容可以是变量，三元运算符，函数调用，算术运算

```

#### 函数

```js
//定义方式1：利用function关键字进行定义
function func(a,b){
    console.log(a+b);
} 

//定义方式2：
var sum=function(a,b){
    return a+b
}
//形式参数不需要类型，返回值不需要定义类型，在内部直接进行返回
//如果参数传递超过形参接受数量只会接受前几个（取决于形参数量）
```

#### 对象

```js
//Array
//定义
	var arr1=new Array(1,"world")
	var arr2=[1,"hello"]
//访问
	var a=arr[index]
//特点：长度可变,类型可变
//属性：length
/*
   方法：forEach():遍历每个有值的元素，并调用一次传入的函数
    	push():追加元素到末尾并返回新数组长度
        splice():删除元素
        */
//forEach
	arr3[5]=[1,2,3,4,5]
	arr3.froEach(function(e){
    	console.log(e)
	})
//可优化为Lambda表达式
	arr3.froEach(e=>console.log(e))
//push
	var len=arr3.push(4)
//splice
    arr3.splice(begin_index,count_delete)

//String
//定义
	var str1=new String("hello world")
    var str2="hello world"
//属性：length
/*方法：
		charAt()：返回指定位置字符
		indexOf()：检索字符串
		trim()：去除头尾的空格
		substring():提取指定索引间的字符
	*/
//自定义对象
    var obj={
        name:"tom",
        age:20,
        learn:function(){
            alert("learning")
        }
    }
    obj.learn()
//JSON
//定义:JavaScript对象标记法
/*
	{
		"name":"Tom",
		"age":20
	}
	要求键值对的键使用双引号包含，多用于数据载体在网络进行数据传输
*/
    var var1='{"key1":"value1","key2":"value2"}'
/*
	value数据类型为：数字，字符串（在双引号中），逻辑值（true或false），数组（在中括号中），对象（在大括号中），null
*/
//属性
/*方法
	JSON.parse(jsStr):将JSON字符串转换为JS对象
	JSON。stringify(obj):将JS对象转换为JSON字符串
*/
//BOM
//定义：浏览器的每个部分被封装成BOM对象
/*属性：window：浏览器窗口对象	
		Navigator：浏览器对象	
		Screen：屏幕对象	         		
		History：历史记录对象
		Location：地址栏对象
*/
    /*
    	Window属性：history，location，navigator
    	Window方法：alert(),
    				confirm(),显示一段消息以及确认取消按钮的对话框,返回值为bool
    				setInterval(),在指定周期调用函数或计算式（ms）
    				setTimeout()，在指定的时间调用（ms）
    	
    	Location属性：href（设置返回完整的URL）
    	
    
    */
//DOM
//将标记型语言的每个部分标记为DOM对象
/*
	属性：Document：整个文档
			Element：元素对象（标签）
				Attribute：属性对象（标签的属性）
					Text:文本对象（标签的文本）
		Comment：注释对象

	Core DOM-所有文档类型的标注模型
	XML DOM-XML-XML文档的标准模型
	HTML DOM-HTML文档的标准模型
	
	方法:document.getElemnetById(),
		document.getElementBygetName(),
		document.getElementByName(),
		document.getElementByClassname()
*/

```

#### 时间监听

```js
/*
事件绑定
	方式1：通过HTML标签的事件属性 eg:<onclick>
	方式2：通过DOM的元素属性绑定 eg:document.getElementById('id').onclick=function(){
		alert("hello world")
	}
*/
/*
常见事件：
		onclick：鼠标点击事件
		onblur：元素失去焦点
		onfocus：元素获得焦点
		onload：某个页面或图像被完成加载
		onsubmit：当表单被提交触发
		onkeydown：键盘某个键按下
		onmouseover：鼠标被移到某元素上
		onmouseout:鼠标从某元素移开
*/
```

### Vue

```html
<!--新建文件引入Vue.js-->
<script src="js/vue.js"></script>

<!--定义Vue对象，el：Vue接管的区域，data对象-->
<script>
    new Vue({
        el: "#test",
        data: {
            message: "hello world"
        }
    })
</script>

<!--数据绑定-->
<div id="test">
    <input type="TEXT" v-model="message">
    {{ message }}
</div>
```

#### 常用指令

| 指令名    | 作用                                                         |
| --------- | ------------------------------------------------------------ |
| v-bind    | 为HTML标签绑定属性值<a v-bind:href="test”>                   |
| v-model   | 在表单元素上创建数据的双向数据绑定                           |
| v-on      | 为HTML绑定事件<input type="text" value="text...",v-on:click="handle()"> |
| v-if      |                                                              |
| v-else-if | 条件性的渲染某元素，绑定为true渲染                           |
| v-else    |                                                              |
| v-show    | 根据条件展示某元素，区别在于切换的是display属性的值          |
| v-for     | 列表渲染，遍历容器的元素或者对象的属性                       |
|           |                                                              |

#### 生命周期

| 状态（钩子方法） | 阶段周期 |
| ---------------- | -------- |
| beforeCreate     | 创建前   |
| created          | 创建后   |
| beforeMount      | 挂载前   |
| mounted          | 挂载后   |
| beforeUpdate     | 更新前   |
| updated          | 更新后   |
| beforeDestroy    | 销毁前   |
| destroyed        | 销毁后   |

## JSP

### 基础语法

#### 注释方式

```jsp
显示注释
	继承html中的注释语法,能够在客户端查看的注释
	<!--这是显式注释-->
隐式注释
	不能在客户端查看的注释
	1.&lt;%--JSP的自带注释--%&gt;
	2.继承JAVA风格的注释,需要写在JAVA的代码段中
	<%
		//这是java注释(单行)
		/*java多行注释*/
	%>
```

#### Scriptlet

```JSP
第一种
	<%     %>:java脚本段
第二种
	<%!    %>:声明,可以定义全局成员变量,方法,类
第三种
	<%=    %>:输出表达式,数据一个变量或者具体内容
```

#### JSP的指令标签

##### include静态包含

```JSP
<%@ include file="path" %> <!--相对路径-->
静态包含是将内容直接进行替换,不能出现同名变量
```

##### 动态包含

```jsp
<jsp:include page="path"></jsp:include>
可以包含同名的变量
```

### 四大域对象(在合理范围内尽可能小)

#### page范围

***pageContext:只能在一个页面保存属性,跳转之后无效***

> 

#### request范围

***request:只在一次请求中保存,服务器跳转仍然有效***

> 

#### session范围

***session:在一次会话范围中,无论何种跳转都可能使用***

> 

#### application范围

***application:在整个服务器中保存***

> 

### 跳转

#### 服务端跳转

```JSP
<jsp:forward page="path"></jsp:forward>
```



#### 客户端跳转

```jsp
<a href="link">jump</a>
```

## Maven

***专门用于构建项目的工具***

> 提供标准项目构建工具
>
> 提供项目一整套打包流程
>
> 提供项目的依赖

***对于java版本不同的解决***

**方法一**

```xml
<properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
</properties>

```

**方法二,Maven的setting.xml配置文件**

```xml
<profile>
     <id>jdk-13</id>
     <activation>
         <activeByDefault>true</activeByDefault>
         <jdk>13</jdk>
     </activation>
     <properties>
         <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
         <maven.compiler.source>17</maven.compiler.source>
         <maven.compiler.target>17</maven.compiler.target> 
     </properties> 
</profile>
<!-- jdk自行选择--!>
```



### 仓库

> ***本地仓库:本地的目录***
>
> ***中央仓库:Maven维护的仓库***
>
> ***远程仓库:私人,公司维护的仓库***

### 常用命令

```shell
compile,test,package,install
```

### 坐标详解

> groupid:当前的Maven项目的隶属机构(包名)
>
> artifactid:定义当前的Maven项目名称(通常是模块名)
>
> version:定义当前版本号
>
> scope依赖范围
>
> ```xml
> <dependency>
>     <groupid>mysql</groupid>
>     <artifactid>mysql-connector-java</artifactid>
>     <version>5.1.46</version>
>     <scope>runtime</scope>
> </dependency>
> 
> ```



# Tomcat

## 安装配置

配置Tomcat环境变量前一定要配置好java的环境变量，尤其是JAVA_HOME

以下环境变量均在系统环境变量中设置。

> ***新建 CATALINA_HOME 环境变量，变量：CATALINA_HOME 值：D:\DevelopmentTool\apache-tomcat-9.0.43***
> ***修改 Path ，在 Path 后添加(新建)：***
>
> *** %CATALINA_HOME%\lib、%CATALINA_HOME%\bin%CATALINA_HOME%\lib\servlet-api.jar***

*环境变量中，环境变量名对大小写不敏感，可将CATALINA_HOME小写，但需要保持一致*
*注意：在环境变量中，如果新建有两个相同仅大小写不同的的变量名，会覆盖设置。如：path和PATH*

> Tomcat文件目录
>
> bin：可执行文件（启动文件startup.bat、关闭文件shutdown.bat）
> conf：配置文件（修改端口号：server.xml，建议将server.xml备份）
> lib：依赖的jar包
> log：日志文件（记录出错等信息）
> temp：临时文件
> webapps：可执行的项目。默认作为存放开发项目的目录
> work：存放由jsp翻译成的.java源文件,以及编译的.class字节码文件(jsp ->java ->class)
> 其他文件

## 常见问题

### 闪退

> 可能原因是：环境变量配置不正确
>
> JAVA_HOME中的路径不能用分号结尾，如C:\Program Files\Java\jdk1.8.0_121
> JAVA_HOME的路径是JDK路径，而不是JRE的路径。
> CATALINA_HOME中的路径不能以\结尾。
> 在环境变量中修改添加变量时，一定要注意分号、空格，是否有多余的字母。

### 乱码

> 问题描述：打开startup.bat后汉字乱码
> 解决方法：在.\apache-tomcat-9.0.43\conf下打开logging.properties文件
>
> 将java.util.logging.ConsoleHandler.encoding = UTF-8
> 替换为java.util.logging.ConsoleHandler.encoding = GBK

### 与其他服务的端口号冲突

**tomcat端口号默认8080，如果和其他服务的端口号冲突，则可对端口号进行修改**
**在.\apache-tomcat-9.0.43\conf下打开server.xml文件，在文件的69行左右，将port="8080"修改为指定的某一端口号，重新启动。**

```properties
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443" />
```

### 常见状态码

> 200：一切正常
> 300/301：页面重定向 （跳转）
> 404：资源不存在
> 403：权限不足 （如果访问a目录，但是a目录设置 不可见）
> 500：服务器内部错误（代码有误）
> 其他编码：积累

## 启动Tomcat

***方法一**：**在.\apache-tomcat-9.0.43\bin目录下，双击startup.bat打开窗口，双击shutdown.bat关闭窗口。***

***如果点startup.bat窗口的×直接关闭，可能会造成关闭异常***

***方法二：***通过命令行窗口打开。cmd命令cd到.\apache-tomcat-9.0.43\bin，然后输入命令：startup，出现如下对话框，表明服务启动成功。

# Servlet

## 入门案例

### Servlet Demo1.java

```java
package com.zoe;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import java.io.IOException;

@WebServlet("/demo1")
public class ServletDemo1 implements Servlet {
    @Override
    public void init(ServletConfig servletConfig) throws ServletException {

    }

    @Override
    public ServletConfig getServletConfig() {
        return null;
    }

    @Override
    public void service(ServletRequest servletRequest, ServletResponse servletResponse) throws ServletException, IOException {

        System.out.println("hello Servlet,coming!");
    }

    @Override
    public String getServletInfo() {
        return null;
    }

    @Override
    public void destroy() {

    }
}



```

### 依赖

***解决servlet-api冲突***

```xml
<dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
</dependency>
```

## Servlet生命周期

> 加载和实例化:默认下,当Servlet第一次被访问,由容器创建Servlet对象
>
> ​	loadOnStartup属性:何时调用init方法
>
> 初始化:Servlet实例化后,容器调用init方法,初始化Servlet对象(只执行一次)
>
> 请求处理:每次请求Servlet,都会调用service方法
>
> 服务终止:调用destroy方法,释放init申请的资源
>
> ​	调用时机:内存释放和服务关闭的时候

> getServletConfig() :获取ServletConfig对象
>
> getServletInfo():获取Servlet的信息

## Servlet体系结构

> Servlet(Servlet体系根接口)
>
> GenericServlet(Servlet抽象实现类)
>
> HttpServlet(对HTTP协议封装的Servlet实现类)

## Servlet的urlPattern配置

> 1.一个Servlet可以配置多个urlPattern
>
> 2.匹配规则
>
> ​	精确匹配:
>
> ```java
> @WebServlet(urlPatterns="/demo")
> ```
>
> ​	目录匹配
>
> ```java
> @WebServlet(urlPatterns="/demo/*")
> ```
>
> ​	扩展名匹配
>
> ```java
> @WebServlet(urlPatterns="*.do")
> ```
>
> ​	任意匹配
>
> ```java
> @WebServlet(urlPatterns="/")
> @WebServlet(urlPattern="/*")
> ```
>

## XML配置方式编写Servlet

```xml
    <servlet>
        <servlet-name>demo2</servlet-name>
        <servlet-class>com.zoe.ServletDemo2</servlet-class>
    </servlet>

    <servlet-mapping>
        <servlet-name>demo2</servlet-name>
        <url-pattern>/demo2</url-pattern>
    </servlet-mapping>
```

## Request

### Request获取请求数据

```JAVA
请求行
	String getmethod();//获取请求方式
	String getContextPath();获取虚拟目录(项目访问路径)
	StringBuffer getRequestURL();获取URL(统一资源定位符)
	String getRequestURI();获取URI(统一资源标识符)
	String getQueryString();获取请求参数(GET)
    
请求头
    String getHeader(String name);根据请求头名称获取值
请求体
    ServletInputStream getInputStream();获取字节输入流
    BufferedReader getReader();获取字符输入流
        
        
```

### Request获取请求参数

```java
Map<String,String []> getParameterMap();获取所有参数的集合
String [] getParameterValues(String name);根据名称获取参数值(数组)
String getParameter(String name);根据名称获取参数值(单个)
```

### Request请求转发

```java
request.getRequestDispacher("/path").forward(request,response)
```

```java
//请求转发资源间共享:使用Request对象
void setAttribute(String name,Object o);//存储数据在request域中
Object getAtttribute(String name);//根据key 获取值
void removeAttribute(String name);根据key删除键值对
```

> 特点:1.网址栏不变 2.只能在服务器内部转发 3.一次转发可在转发的资源间使用request共享数据

## Response

### Redirect重定向

```java
response.setHeader("Location","/path-module/resp");
//或者
response.sendRedirect("/path");

```

> 特点:1.地址栏发生变化  2.可以重定向任意位置 3.两次请求不能在多个资源使用request贡献数据

#### 路径问题

> 浏览器使用:需要加虚拟目录
>
> 服务端使用:不需要加虚拟目录

### Response响应字符数据

```java
resp.getWriter().write("test");
```



### Response响应字节数据

```java
resp.getOutputStream().write("qwe");
```

## MVC

> M:module
>
> V:view
>
> C:Contoller

## 三层架构

> 表现层:接受请求,封装数据,调用业务逻辑层,响应数据
>
> 业务逻辑层:对业务逻辑进行封装组合数据访问层层中的基本功能,形成复杂的业务逻辑功能
>
> 数据访问层:对数据CURD进行基本的操作

## Cookie

> Cookie:客户端会话技术,将数据保存在客户端,以后每次请求都携带Cookie数据进行访问

```java
//发送Cookie
Cookie cookie=new Cookie("key","value");
response.addCookie(cookie);

//获取Cookies
Cookie [] cookies=request.getCookies();
cookie.getName();
cookie.getValue();
```

### Cookie原理(基于HTTP)

> 响应头:set-cookie
>
> 请求头:cookie

### Cookie使用细节

> Cookie存活时间:默认状态下,存在浏览器中,当浏览器关闭,内存释放,Cookie销毁,setMaxAge(int seconds)设置存活时间
>
> Cookie存储中文

## Session

> 服务端会话跟踪技术,JavaEE的HttpSessioon技术
>
> void setAttribute(String name,Object o);存储到session域中
>
> Object getAttribute(String name);根据key,获取值
>
> void removeAttribute(String name);根据key,删除该键值对

### Session原理

> 基于Cookie实现

### Session使用细节

> 钝化:服务器正常关闭后,Tomcat会自动将Session数据写入硬盘的文件中
>
> 活化:再次启动服务器后,从文件中加载Session
>
> Session销毁:默认下无操作30min自动销毁 ,或者调用invalidate()方法

> 小结:
>
> ​	存储位置:Cookie存储在客户端,Session存储在服务端
>
> ​	安全性:Cookie不安全,Session安全
>
> ​	数据大小:Cookie最大3KB,Session大小无限制
>
> ​	存储时间:Cookie无时间限制,Session默认30min
>
> ​	服务器性能:Cookie不占服务器资源,Session占服务器资源

## Fileter

```java
//定义类实现Fileter接口,并重写所有方法
public class FilterDemo implements Filter {
	public void init(FilterConfig filterConfig);
	public void doFilter(ServletRequest request);
	public void destroy();
}

//配置Filter拦截的资源路径,在类上定义@Webservlet注解
@WebFilter("/*")

//在doFilter方法中输出一句话,并放行
public void doFilter(ServletRequest request,Ser.........){
	System.out.println("filter被执行");
	chain.doFilter(request,response);
}
```

#### Filter拦截路径

> 拦截具体资源:/index.jsp:只有访问index.jsp会被拦截
>
> 目录拦截:/user/*:拦截/user下的所有资源,都会被拦截
>
> 后缀名拦截:*.jsp:访问后缀名为jsp的资源,都会被拦截
>
> 拦截所有:/*:拦截所有的资源,都会被拦截

#### 过滤器链

> 根据XML决定顺序,没有配置XML就由类名决定(字符串类名自然排序)

## Listener

> 监听application,session,request的创建,销毁,其中属性添加修改的删除属性时自动执行代码功能的组件

## AJAX

> 异步的JavaScript和XML
>
> 使用AJAX和HTML替换JSP页面

# Spring框架

## 第一部分核心容器

### 核心概念

***Ioc  DI***

### 项目实例

#### 文件实例

```xml
<dependencies>
        <!-- https://mvnrepository.com/artifact/org.springframework/spring-context -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>5.2.10.RELEASE</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
<!--导入依赖-->
```

```xml
<!--1. import spring-context,map the 5.2.10 RELEASE-->

<!--   2. bean config-->
    <bean id="bookDao" class="Spring_Learning.mysping_program.dao.impl.BookDaoImpl">
    </bean>
    <bean id="booService" class="Spring_Learning.mysping_program.service.impl.BookServiceImpl">
    </bean>
```

***提供依赖对象的setter方法***

```java
public class BookServiceImpl implements BookService {


    //5.
    private BookDao bookDao;

    @Override
    public void save() {
        System.out.println("book service save");
        bookDao.save();
    }


    //6.set method
    public void setBookDao(BookDao bookDao) {
        this.bookDao = bookDao;
    }
}

```

***配置service与dao之间的关系***

```xml
<!--   2. bean config-->
    <bean id="bookDao" class="Spring_Learning.mysping_program.dao.impl.BookDaoImpl"/>

    <bean id="booService" class="Spring_Learning.mysping_program.service.impl.BookServiceImpl">
<!--        set the relation of bean,property:obj  ref :reference-->
        <property name="bookDao" ref="bookDao"/>
    </bean>
```

#### ***实例化bean三种方法：***

> *1.构造方法：空参*
>
> *2.使用静态工厂实例化bean，即用bean标签的factory-method参数指定方法*
>
> *3.实例工厂造bean，非静态*

##### Bean的生命周期

> **初始化容器**
>
> *创建对象（内存分配）*
>
> *执行构造方法*
>
> *执行属性注入*
>
> ***执行bean初始化方法***
>
> **使用bean**
>
> *执行业务操作*
>
> **关闭/销毁容器**
>
> 执行销毁方法
>
> 方式：
>
> ​		1.手动关闭
>
> ​		2.注册关闭钩子
>
> **依赖注入**
>
> ​		1.setter注入
>
> ​					简单类型：可访问的set方法和property标签设置
>
> ```xml
> <bean id="bookDao" class="Spring_Learning.myspring_program.dao.impl.BookDaoImpl" init-method="init" destroy-method="destroy">
>         <property name="connectionCount" value="10"/>
>         <property name="mysql" value="database"/>
>     </bean>
> ```
>
> ​					引用类型
>
> ​		2.构造器注入
>
> ​					简单类型
>
> ​					引用类型
>
> ***Ps：依赖注入setter较为灵活***
>
> ##### 依赖自动装配
>
> ***Ps:1.自动装配用于引用类型的依赖注入，不对简单类型操作  2.使用ByType必须保证容器中相同类型的数据唯一  3.使用byName时必须保证容器中有指定名称的bean  4.自动装配优先级低于setter注入与构造器注入***
>
> ##### 集合注入
>

### 标签介绍

> bean标签
>
> id：别名，可以使用一个或多个，多个需用空格 分号和逗号隔开  
> class：全类名 
> scope：多例与单例（默认）切换，控制对象创建 ,作用范围 (request,session,globalsession)
> factory-method：静态工厂创建  
> factory-bean：实例化工厂对象 
> init-method destroy-method 初始化和销毁方法
> autowire：自动装配

> property标签:属性注入
>
> name:属性名称
>
> value:普通属性值
>
> ref:对象引用值

> list标签,map标签,properties标签,constructor-arg标签

> import标签:导入其他Spring的配置文件

### Spring相关API

> getBean()方法:1.使用ID匹配	2.使用Class字节码

> ApplicationContext可以用XML或者File实例化

### Spring原始注解

| 注解           | 说明                                           |
| -------------- | ---------------------------------------------- |
| @Component     | 类上实例化Bean                                 |
| @Controller    | 使用web层类上用于实例化Bean                    |
| @Service       | 使用Service层类上用于实例化Bean                |
| @Repository    | 使用在dao层类上用于实例化                      |
| @Autowired     | 使用在字段上用于根据类型依赖注入               |
| @Qualifier     | 结合@Autowired一起使用用于根据名称进行依赖注入 |
| @Resource      | 相当于@Autowired+@Qualfier,按照名称进行注入    |
| @Value         | 注入普通属性                                   |
| @Scope         | 标注Bean的作用范围                             |
| @PostConstruct | 使用在方法上标注该方法是Bean的初始化方法       |
| @PreDestroy    | 使用在方法上标注该方法是Bean的销毁方法         |

### Spring新注解

| @Configuration  | 说明                                                         |
| --------------- | ------------------------------------------------------------ |
| @ConponentScan  | 用于指定当前类是一个Spring配置类,创建容器时会从该类上加载注解 |
| @Bean           | 用与指定Spring在初始化容器哦时要扫描的包,作用和在Spring的xml文件中的<context:comonent-scan-base-package="com.zoe"/>一样 |
| @PropertySource | 用于加载properties文件中的配置                               |
| @Import         | 用于导入其他配置类                                           |



### 容器基本操作

## 第二部分整合

### 整合数据层技术MyBatis

#### Json格式获取

> Controller:
>
> ​	获取普通pojo的json信息:
>
> ```json
> {
> 	"name":"Jhon",
> 	"age":"15",
> 	"address":{
> 		"province":"shanxi",
> 		"city":"xian"
> 	}
> }
> ```
>
> ```java
> @ResponseBody
> @Requestmapping
> public String pojoParamForJson(@RequestBody User user){
> 	return user;
> }
> ```
>
> ​	获取pojo集合的json信息:
>
> ```json
> 	[	
> 
> 		{"name":"Jhon","age":28},
> 
> 		{"name":"Kitty","age":18}
> 
> 	]
> ```

#### Restful风格处理

> 1. 使用HTTP动词来代表不同的操作：
>    - `GET /users`：获取所有用户列表。
>    - `GET /users/{id}`：获取指定id的用户信息。
>    - `POST /users`：添加新用户。
>    - `PUT /users`：更新单个用户信息。
>    - `PUT /users/batch`：批量更新多个用户信息。
>    - `DELETE /users/{id}`：删除指定id的用户。
> 2. URL中使用名词表示资源，避免使用动词：
>    - 不推荐使用`/select`、`/insert`、`/update`、`/delete`等动词表示操作，而是直接使用资源名`/users`，并通过HTTP动词来表示操作类型。
> 3. 使用复数名词来表示集合资源：
>    - `/users`表示所有用户列表。
>    - `/users/{id}`表示单个用户。

## 第三部分AOP

### 核心概念

### AOP基础操作

### AOP实用开发

## 第四部分事务

### 事务实用开发

# MyBatis

***JavaEE三层架构：表现层，业务层，持久层(MyBatis)***

## 核心配置文件

***Program-config.xml***

| 字段            | 使用       |
| --------------- | ---------- |
| mapper          | 映射       |
| environment     | 环境控制   |
| typeAliases     | 引入别名   |
| settingsplugins | 设置       |
| properties      | 属性       |
| plugins         | 插件       |
| typeHandlers    | 类型处理器 |
| objectFactory   | 对象工厂   |

## 基础步骤

***编写接口方法：Mapper接口----编写SQL语句：SQL映射文件----执行方法，测试***

```java
//导入配置文件
String resource = "MyBatis_program-config.xml";
        InputStream inputStream = Resources.getResourceAsStream(resource);
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

//获取SqlSession对象
        SqlSession sqlSession = sqlSessionFactory.openSession();

//使用SQL语句



//关闭流


sqlsession.close();
```

### 数据库的字段名称与实体类的名字不同步

***1.可以在SQL数据库中给字段起别名，即在Mapper映射文件中的SQl语句使用as对字段起别名      缺点：效率过低，每次查询需要重写***

***对于上述方法推出在xml文件中使用sql标签，对字段取别名，再在原语句进行引用***

```xml
<sql id="newname">id as name</sql>

<select id="selectALl" resultType="classname">
	select
    	<include refid="newname"/>
    from table_class;
    
</select>
```

***2.resultMap(灵活操作)***

```xml

<!--id：唯一标识   type：类的别名-->
<resultMap id="nameresultMap" type="table_newname">
	<result> column="name in database column" property="property in class"</result>
</resultMap>


<!--id: 主键字段的标签   result：一般字段的标签，分别有两个属性：column,property-->

<select id="method name" resultMap="nameresultMap">
	select
    	*
    from tablename;

</select>
```

### 查询案例

### 方法映射文件xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-mapper.dtd">

<mapper namespace="mybatis_test.mapper.BrandMapper">
    <select id="selectAll" resultType="Brand">
        select * from Brand;
    </select>

    <!--selectByid方法映射文件-->
	<select id="selectByid" parameterType="int "resultType="Brand">    
        select *
        <!--在参数查询使用小于号‘<’可以使用&lt -->
        <!--可以使用<![CDATA[内容]]，简写CD-->
        from Brand where id = #{id};
    <!--此处使用#{id} 可以保证运行是为?占位符   使用${id}会直接出现参数会有Sql注入安全隐患-->
    </select>
    
    <select id="selectByCondition" resultType="Brand">
        select *
        from Brand
        where status_now = #{status_now}
        and name_company like #{name_company}
        and name_goods like #{name_goods}
    </select>
    
     <!--dynamic sql-->
    <select id="selectByCondition" resultType="Brand">
        
        select *
        from Brand
        where
            1=1
        
        <!--if标签，用于判断参数是否有值，使用test属性进行条件判断，存在问题：第一个条件不需要逻辑运算符，使用where标签保证语句的正确性，可以使用恒等式解决-->
            <if test="status_now != null">and status_now = #{status_now}</if>
            <if test="name_company != null and name_company != ''">and name_company like #{name_company}</if>
            <if test="name_goods != null and name_goods != ''">and name_goods like #{name_goods}</if>


    </select>
    
    
     <select id="selectByCondition" resultType="Brand">
        select *
        from Brand
        <where>
<!--使用where标签，自动补全语句，-->
            <if test="status_now != null">status_now = #{status_now}</if>
            <if test="name_company != null and name_company != ''">and name_company like #{name_company}</if>
            <if test="name_goods != null and name_goods != ''">and name_goods like #{name_goods}</if>

        </where>
    </select>
    
    <!--单条件的动态查询-->
    <select id="selectByConditionSingle" resultType="Brand">

        <
        select *
        from Brand
        <where>
            <choose>
                <!--choose标签相当于switch语句，同样的when是case,otherwise相当于default,可以不写oherwise标签加上where标签-->
                <when test="status_now != null ">
                    status_now= #{status_now}
                </when>
                <when test="name_company != null and name_company != '' ">
                    name_company=#{name_company}
                </when>
                <when test="name_goods != null and name_goods != '' ">
                    name_goods = #{name_goods}
                </when>
                <otherwise>
                    1=1
                </otherwise>
            </choose>
        </where>;
    </select>



<!--添加操作，添加了useGenerateKeys属性和keyproperty属性使得id属性可以主键传递-->
    <insert id="add" useGeneratedKeys="true" keyProperty="id" >
        insert into Brand (name_goods, name_company, status_now, logo, id)
        VALUES(#{name_goods}, #{name_company}, #{status_now}, #{logo}, #{id})
    </insert>
<!--修改操作，使用了动态语句，if标签的test对输入进行判断-->
    <update id="update" useGeneratedKeys="true" keyProperty="id" >
        update Brand
        <set>
            <if test="status_now != null">status_now = #{status_now},</if>
            <if test="name_company != null and name_company != ''">name_company = #{name_company},</if>
            <if test="name_goods != null and name_goods != ''">name_goods = #{name_goods},</if>
            <if test="logo != null">logo = #{logo},</if>
        </set>
        where id = #{id}
    </update>
<!--删除操作，删除指定id的数据-->
    <delete id="deleteByid">
        delete from Brand
        where id = #{id}
    </delete>

<!--批量删除，设定一个集合或者列表，利用foreach标签对其进行遍历，collections是集合名，也可以添加注解使用array,separate为分隔符，open,close分别表示开头与结尾字符，例中为(?,?)-->
    <delete id="deleteByids">
        delete from Brand
        where id in 
        <foreach collection="ids" item="id" separator="," open="(" close=")">
            #{id}
        </foreach>
    </delete>


</mapper>
```

### 核心配置文件xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "https://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>

    <typeAliases>
        <package name="mybatis_test.pojo"/>
    </typeAliases>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <!--database connection info-->
                <property name="driver" value="org.mariadb.jdbc.Driver"/>
                <property name="url" value="jdbc:mariadb://localhost:3306/mybatis"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
<!--    waiting :    load sql mapper file-->
<!--        <mapper resource="mybatis_test/mapper/userMapper.xml"/>-->
            <package name="mybatis_test.mapper"/>
        
    </mappers>
</configuration>
```

### 方法接口

```java
package mybatis_test.mapper;

import mybatis_test.pojo.Brand;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

public interface BrandMapper {

    //select all
    @Select("select * from Brand")
    List<Brand> selectAll();


    //check info of brand
    Brand selectByid(int id);

    //tiaojian chaxun

    //unpacked property


    /**
     *
     * @param status_now
     * @param name_company
     * @param name_goods
     * @return
     */

    List<Brand> selectByCondition(@Param("status_now") int status_now,@Param("name_company") String name_company, @Param("name_goods")String name_goods);


    //make it a duixiang
    List<Brand> selectByCondition2(Brand brand);
    List<Brand> selectByCondition3(Map map);



    //single condition
    @Select("select * from brand where status_now = #{status_now} and name_company = #{name_company} and name_goods = #{name_goods}")
    List<Brand> selectByConditionSingle(Brand brand);


    //add brand
    void add(Brand brand);

    //update brand
    Integer update(Brand brand);

    //delete Byid
    void deleteByid(int id);

    //delete By ids
    void deleteByids(@Param("ids") List<Integer> ids);


}


```

### 实体类

```java
package mybatis_test.pojo;

public class Brand {
//    name_goods varchar(10),
//    name_company varchar(10),
//    status_now boolean

    private int id;
    private String logo;
    private String name_goods;
    private String name_company;
    private int status_now;


    public Brand() {
    }

    public Brand(int id, String logo, String name_goods, String name_company, int status_now) {
        this.id = id;
        this.logo = logo;
        this.name_goods = name_goods;
        this.name_company = name_company;
        this.status_now = status_now;
    }

    public Brand(int statusNow, String nameCompany, String nameGoods) {
        this.status_now=statusNow;
        this.name_company=nameCompany;
        this.name_goods=nameGoods;
    }

    public Brand(int id, int statusNow, String nameCompany, String nameGoods, String logo) {
        this.id = id;
        this.status_now = statusNow;
        this.name_company = nameCompany;
        this.name_goods = nameGoods;
        this.logo = logo;
    }


    /**
     * 获取
     * @return id
     */
    public int getId() {
        return id;
    }

    /**
     * 设置
     * @param id
     */
    public void setId(int id) {
        this.id = id;
    }

    /**
     * 获取
     * @return logo
     */
    public String getLogo() {
        return logo;
    }

    /**
     * 设置
     * @param logo
     */
    public void setLogo(String logo) {
        this.logo = logo;
    }

    /**
     * 获取
     * @return name_goods
     */
    public String getName_goods() {
        return name_goods;
    }

    /**
     * 设置
     * @param name_goods
     */
    public void setName_goods(String name_goods) {
        this.name_goods = name_goods;
    }

    /**
     * 获取
     * @return name_company
     */
    public String getName_company() {
        return name_company;
    }

    /**
     * 设置
     * @param name_company
     */
    public void setName_company(String name_company) {
        this.name_company = name_company;
    }

    /**
     * 获取
     * @return status_now
     */
    public int getStatus_now() {
        return status_now;
    }

    /**
     * 设置
     * @param status_now
     */
    public void setStatus_now(int status_now) {
        this.status_now = status_now;
    }

    public String toString() {
        return "Brand{id = " + id + ", logo = " + logo + ", name_goods = " + name_goods + ", name_company = " + name_company + ", status_now = " + status_now + "}";
    }
}

```



## mybatis概念

### mybatis事务

***openSession():默认开启事务，进行增删改操作后需要使用sqlSession.commit手动提交事务***

***openSession(true)：可以设置为自动提交事务（关闭事务）***  

### mybaitis参数封装

***常规单个参数可以使用arg,param代替，即arg0,param0-9，也可以使用@param(“eg”)注解变量***

***Map集合：直接使用，键名与参数占位符名称一致***

***Collection，List,Array都是封装为Map集合，可以使用@Param注解，替换集合中的默认atg键名***

> 批量更新是一次执行多个update语句，所以mybatis需要额外的配置：
>
> 在`spring.datasource.url`后加上`allowMultiQueries=true`
>
> 如：`jdbc:mysql://10.10.20.36:3306/test?allowMultiQueries=true`

# Git

## 基础命令和分支

> 本地仓库
>
> 暂存区
>
> 仓库区
>
> 远程仓库

> 文件四种状态
>
> Utrackd:未跟踪,使用git add状态变为staged
>
> Unmodify:文件已经入库,未修改被修改就变为Modified,使用git rm就会变为				Untracked
>
> Modified:文件已修改,仅仅是修改,使用git add变为Staged暂存状态,使用git 				checkout则丢弃修改变为Umodify,此处的git checkout即从库取出				文件覆盖修改
>
> Staged:暂存状态,实行commit将修改同步到库中,这时库中文件与本地文件又			变为一致,文件未Umodify,执行git reset HEAD filename 取消暂存,文			件状态为Modified

> 工作流程:  
>
> 创建Git项目(Git项目初始化):使用git ini或者git clone url获取在线git项目
>
>  

```shell
#查看指定文件状态
git status [filename]

#查看所有文件状态
git status

#git add .		添加所有文件到暂存区
#git commit -m	提交暂存区的内容到本次仓库 -m 提交信息
```

***忽略部分文件的git版本控制***

> .gitignore
>
> 1.忽略文件的空行或以#开始的行会被忽略
>
> 2.使用Linux通配符:*代表任意字符,?代表一个字符,[abc]代表可选字符范围,{Str1,Str2}代表可选字符串等
>
> 3.如果名称前带有!,表示例外规则,将不被忽略
>
> 4.如果名称最前面是一个路径分隔符/:表示要忽略的文件在此目录下,而子目录	的文件不忽略
>
> 5.如果名称的最后一个是路径分隔符/:表示要忽略的是此目录下该名称的子目	录,而非文件(默认文件或目录都忽略)
>
> ```shell
> #注释
> *.txt		#忽略所有.txt结尾的文件
> !lib.txt	#当lib.txt除外
> /temp		#仅仅忽略项目根目录下的TEMP文件,你包含其他目录的TEMP
> build/		#忽略build/目录下的所有文件
> doc/.*.txt	#忽略doc/motes.txt但不包括doc/server/arch.txt
> ```

***Git分支***

```shell
#列出所有本地分支
git branch

#列出所有远程分支
git branch -r

#查看已配置的远程仓库
git remote -v

#新建分支
git branch [branch_name]

#新建一个分支并且切换到该分支
git checkout -b [branch]

#合并指定分支到当前分支
git merge [branch]

#删除分支
git branch -d [branch_name]

#删除远程分支
git push orign --delete [branch_name]
git branch -dr [remote/branch] 

#将本地的master分支push到远程Mybatis分支
git push origin master:Mybatis

#添加远程仓库
git remote add orign <远程仓库的URL>

#增加新的远程仓库,远程仓库即为对应url的仓库别名
git remote add <远程仓库名> <远程仓库的URL>
如:
	git remote add orign2 <远程仓库2的URL>
	git push orign2
```

## Git基本操作

**创建版本库**

创建版本库有两种方式，一种是将本地的文件夹直接变成一个git仓库，另一种是直接将远程的仓库克隆到本地

```bash
git init # 将本地文件夹变为一个git仓库
git clone <url> #将远程仓库克隆到本地
```

**修改与提交操作**

```bash
git add <file> # 将单个文件从工作区添加到暂存区
git add . # 将所有文件添加到暂存区
git commit -m "messenge" # 将暂存区文件提交到本地仓库
git status # 查看工作区状态，显示有变更的文件。
git diff # 比较文件的不同，即暂存区和工作区的差异。
```

**远程操作**

```bash
git push origin master # 将本地的master分支推送到远程对应的分支
git pull  # 下载远程代码并合并，相当于git fetch + git pull
git fetch   # 从远程获取代码库，但不进行合并操作

git remote add origin <url> # 将远程仓库与本地仓库关联起来
git remote -v # 查看远程库信息
```

**撤销与回退操作**

撤销操作：当修改了工作区/暂存区的文件，但是还没有commit时，想要撤销之前的操作：

```bash
# 场景1：当你改乱了工作区某个文件的内容，但还没有add到暂存区
git checkout <file> # 撤销工作区的某个文件到和暂存区一样的状态

# 场景2：当乱改了工作区某个文件的内容，并且git add到了暂存区
git reset HEAD <file> # 第1步，将暂存区的文件修改撤销掉
git checkout <file> # 第2步，将工作区的文件修改撤销掉

# 场景3：乱改了很多文件，想回到最新一次提交时的状态
git reset --hard HEAD # 撤销工作区中所有未提交文件的修改内容
```

回退操作：当已经进行了commit操作，需要回退到之前的版本：

```bash
git reset --hard HEAD^ # 回退到上次提交的状态
git reset --hard HEAD~n # 回退到n个版本前的状态
git reset --hard HEAD commitid # 回退到某一个commitid的状态
git reset --soft HEAD commitid # 回退到某一个commitid的状态，并且保留暂存区的内容
git reset --mixed(默认) HEAD commitid # 回退到某一个commitid的状态，并且保留工作区的内容
```

## Git分支管理

git的最强大之处就在于分支管理了，具体有两种应用场景：

1. 多人协作：每个人都基于主分支创建一个自己的分支，在分支上进行开发，然后再不断将写好的代码合并到主分支
2. 自己修复bug/增加feature：创建一个bug分支或者feature分支，写好代码后合并到自己的分支然后删除bug/feature分支

```bash
git branch <name> # 创建分支
git checkout <name> # 切换到某个分支
git checkout -b <name> # 创建并切换到新分支，相当于同时执行了以上两个命令
git merge <name> # 合并某个分支到当前分支中，默认fast forward
git branch -a # 查看所有分支
git branch -d <name> # 删除分支
```

## Git多人协作

多人协作在同一个分支上进行开发的工作模式：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功！
5. 如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

## git回滚

1. 首先，使用`git log`命令查看提交历史，找到你想要回滚到的提交(commit)的哈希值或者简写：

   ```shell
   $ git log
   commit c12a3b45e7890123456789abcdef0123456789
   Author: Your Name <yourname@example.com>
   Date:   Mon Jul 1 12:00:00 2023 +0800
   
       Commit message
   
   commit 9876543210abcdef0123456789abcdef0123456
   Author: Your Name <yourname@example.com>
   Date:   Sun Jun 30 12:00:00 2023 +0800
   
       Commit message
   ```

2. 根据你的需求选择合适的回滚方法：

   a. 回滚并保留回滚之后的更改（使用`git reset --soft`）：

      ```shell
      $ git reset --soft c12a3b45e7890123456789abcdef0123456789
      ```

   b. 回滚并取消暂存区中的更改（使用`git reset --mixed`）：

      ```shell
      $ git reset --mixed c12a3b45e7890123456789abcdef0123456789
      ```

   c. 回滚并丢弃回滚之后的所有更改（使用`git reset --hard`）：

      ```shell
      $ git reset --hard c12a3b45e7890123456789abcdef0123456789
      ```

   在上述命令中，将`c12a3b45e7890123456789abcdef0123456789`替换为你要回滚的提交的哈希值或者简写。

3. 如果你想将回滚后的更改推送到远程仓库，可以使用`git push`命令：

   ```shell
   $ git push origin <branch-name>
   ```

   将`<branch-name>`替换为你想要推送到的远程分支的名称。

请注意，回滚操作会改变Git仓库的历史记录，因此请谨慎操作，并确保在进行任何修改之前进行备份。

### HEAD

> `HEAD`在不同情况下可以指向不同的提交，具体取决于你的操作和上下文。
>
> 1. 最新提交：当你切换到一个分支或者在分支上进行新的提交时，`HEAD`会指向该分支的最新提交。这表示你当前所在的位置是最新的代码状态。
>
> 2. 特定提交：有时你可能需要查看或操作历史提交，这时你可以将`HEAD`指向一个特定的提交。通常，你可以使用提交的哈希值或者简写形式来指定特定的提交。这样做可以让你浏览、比较或回滚到特定的提交，而不一定是最新的提交。
>
> 以下是一些使用情境：
>
> - 查看特定提交：通过将`HEAD`指向一个特定的提交，你可以查看该提交的详细信息，包括更改的文件、作者、日期等。例如，`git show HEAD`将显示当前分支最新提交的详细信息。
>
> - 比较提交：你可以使用`HEAD`指向的特定提交与其他提交进行比较。例如，`git diff HEAD~1 HEAD`将显示当前提交与前一次提交之间的差异。
>
> - 回滚提交：如果你想回滚到之前的某个提交，你可以使用`HEAD`指向的特定提交来执行回滚操作。例如，`git revert HEAD`将撤销当前分支的最新提交。

需要注意的是，`HEAD`指向的特定提交是相对于当前所在的分支而言的。如果你切换到不同的分支，`HEAD`会自动更新为该分支的最新提交。因此，使用`HEAD`指向的特定提交时要确保你在正确的分支上。

## 小结

>  步骤
>
>   初始化：本地建库（即文件夹），git init
>   添加到仓库：代码文件放入本地库，git add .
>   提交： git commit -m “注释内容”，提交到仓库
>   新建远程仓库并关联：在Github上设置好SSH密钥后，新建一个远程仓库， git remote add origin <url>关联
>   推送：git push (-u) origin master，把本地仓库的代码推送到远程仓库Gihub上

# C++

## gcc/g++

> ```shell
> g++ [optinons] file/files [options] resultFile/files
> ```
>
> 
>
> ```shell
> #-E 编译器对文件进行预处理
> 
> g++ -E test.cpp -o test.i     
> 
> #-S编译器告诉g++再为c++代码产生汇编语言后停止编译
> 
> g++ -S test.i -o test.s    
> 
> #-c 选项告诉g++仅把源代码编译为机器语言的目标代码
> 
> g++ -c test.s -o test.o    
> 
> #-o产生可执行文件名
> g++ test.o -o test
> ```
>
> ***最快速编译单个文件：***
>
> ```shell
> g++ test.cpp -o test
> #直接运行编译后的可执行文件
> ./test
> ```
>
> ***编译多个文件***
>
> ```shell
> g++ test1.h test2.h test3.cpp -o test
> #直接运行编译完成后的可执行文件
> ./test
> ```
>

## make

***make：利用makefile对多个c++文件进行编译，链接，生成目标可执行文件***

> ```shell
> #编译
> make
> #清除生成的中间文件和可执行文件
> make clean
> ```
>
> 

## Cmake

***跨平台自动生成makefile,不需要手动编写makefile***

> ***cmake基础用法实例***
>
> ```cmake
> #指定cmake需要的最低版本要求
> cmake_minimum_required(VERSION 3.0)
> #指定生成的项目名称
> project(projectName)
> #在指定的目录下扫描所有的源文件，并将名称保存到DIR_SRCS变量中
> aux_source_directory(. DIR_SRCS)
> #假设拥有多个子目录，首先需要将目录文件添加
> add_subdirectory(sonDirName)
> #生成可执行文件需要的所有cpp文件
> add_executable(list ${DIR_SRCS})
> #对于多个子目录需要进行子目录库的链接
> target_link_libraries(projectName sonDirlibName)
> 
> #对于子目录则需要编写相应的CMakeLists.txt文件
> #扫描指定目录下的所有源文件并将名称保存到某个变量中
> aux_source_directory(. SON_DIR_CPP)
> #再将所有的源文件生成为链接库
> add_library(sonDirlibName ${SON_DIR_CPP})
> target_compile_options(${EXECUTABLE_NAME} PRIVATE -g)
> #此处的PRIVATE代表只会依赖于这一个文件
> ```
>

## 预编译指令

> ***在文件预编译时进行控制***
>
> **1.防止头文件被重复引入**
>
> ```c++
> //条件编译
>      #define        //  宏定义 
>      #undef         //  取消宏 
>      #include       //  文本包含 
>      #ifdef         //  如果宏被定义就进行编译 
>      #if defined    //  与ifdefine的区别在于可以可以组成复杂的判别条件
>      #ifndef        //  如果宏未被定义就进行编译 
>      #if !defined   //  与if !define的区别在于可以可以组成复杂的判别条件
>      #endif         //  结束编译块的控制 
>      #if   defined        //  表达式非零就对代码进行编译 
>      #else          //  作为其他预处理的剩余选项进行编译 
>      #elif          //  这是一种#else和#if的组合选项 
>      #elif defined    //  与ifdefine的区别在于可以可以组成复杂的判别条件
> 	 #elif !defined    //  与ifdefine的区别在于可以可以组成复杂的判别条件
> //编译指令
>      #line          //  改变当前的行数和文件名称 
>      #error         //  输出一个错误信息 
>      #pragma        //  为编译程序提供非常规的控制流信息，可跟once，message等许多参数。
> ```
>
> 
>

## GDB

***描述：C/C++开源命令调试器(GNU debugger)***

> ```shell
> file                            # 装入想要调试的可执行文件.
> kill            k              #终止正在调试的程序.
> list            l               #列出产生执行文件的源代码的一部分.
> next           	n              #执行一行源代码但不进入函数内部.
> step          	s              #执行一行源代码而且进入函数内部.
> continue  		c               #继续执行程序，直至下一中断或者程序结束。
> run            	r               #执行当前被调试的程序.
> quit           	q               #终止 gdb.
> watch                        #使你能监视一个变量的值而不管它何时被改变.
> catch                         #设置捕捉点.
> thread       	t               #查看当前运行程序的线程信息.
> break        	b             #在代码里设置断点, 这将使程序执行到这里时被挂起
> make                        #使你能不退出 gdb 就可以重新产生可执行文件.
> shell                         #使你能不离开 gdb 就执行 UNIX shell 命令. 
> print          	p              #打印数据内容。
> examine			x               #打印内存内容。
> backtrace 		bt             #查看函数调用栈的所有信息。
> info			i				#查看相关信息
> ```
>
> 

## C++11

## 值的类别

> ***左值：***
>
> ​	  能够用&取地址的表达式是左值表达式。
>
> ​	举例
>
>    		函数名和变量名（实际上是函数指针和具名变量，具名变量如std::cin
>
> ​	std::endl等）、返回左值引用的函数调用、前置自增/自减运算符连接的表达式++i/--	i、由赋值运算符或复合赋值运算符连接的表达式(a=b、a+=b、a%=b）、解引用表	达式*p、字符串字面值"abc"（关于这一点，后面会详细说明）等。
>
> ***纯右值：***
>
> ​	本身就是赤裸裸的、纯粹的字面值，如3、false；
>
> ​	求值结果相当于字面值或是一个不具名的临时对象。
>
> ​	举例:
> ​			除字符串字面值以外的字面值、返回非引用类型的函数调用、后置自增/自	减运算符连接的表达式i++/i--、算术表达式（a+b、a&b、a<<b）、逻辑（a&&b、	a||b、~a）、比较表达式（a==b、a>=b、a<b）、取地址表达式（&a）等。
>
> ***将亡值：***
>
> ​	 在C++11之前的右值和C++11中的纯右值是等价的。C++11中的将亡值是随着右值引用④的引入而新引入的。换言之，“将亡值”概念的产生，是由右值引用的产生而引起的，将亡值与右值引用息息相关。所谓的将亡值表达式，就是下列表达式：
>
>    	1）返回右值引用的函数的调用表达式
>  	  2）转换为右值引用的转换函数的调用表达式
>    会问：这与“将亡”有什么关系？
>    在C++11中，我们用左值去初始化一个对象或为一个已有对象赋值时，会调用拷贝构造函数或拷贝赋值运算符来拷贝资源（所谓资源，就是指new出来的东西），而当我们用一个右值（包括纯右值和将亡值）来初始化或赋值时，会调用移动构造函数或移动赋值运算符⑤来移动资源，从而避免拷贝，提高效率（关于这些知识，在后续文章讲移动语义时，会详细介绍）。当该右值完成初始化或赋值的任务时，它的资源已经移动给了被初始化者或被赋值者，同时该右值也将会马上被销毁（析构）。也就是说，当一个右值准备完成初始化或赋值任务时，它已经“将亡”了。而上面1）和2）两种表达式的结果都是不具名的右值引用，它们属于右值（关于“不具名的右值引用是右值”这一点，后面还会详细解释）。又因为
>    	 1）这种右值是与C++11新生事物——“右值引用”相关的“新右值”
>   	  2）这种右值常用来完成移动构造或移动赋值的特殊任务，扮演着“将亡”的角色
>     所以C++11给这类右值起了一个新的名字——将亡值。
>
> 关于“三值”：
>
>    1）字符串字面值是左值。
>
>    不是所有的字面值都是纯右值，字符串字面值是唯一例外。
>    早期C++将字符串字面值实现为char型数组，实实在在地为每个字符都分配了空间并且允许程序员对其进行操作，所以类似
>
> ```c++
> cout<<&("abc")<<endl;
> char *p_char="abc";//注意不是char *p_char=&("abc");
> ```
>
> 这样的代码都是可以编译通过的。
>     注意上面代码中的注释，"abc"可以直接初始化指针p_char，p_char的值为字符串"abc"的首字符a的地址。而&("abc")被编译器编译为const的指向数组的指针const char (*) [4]（之所以是4，是因为编译器会在"abc"后自动加上一个'\0'），它不能初始化char *类型，即使是const  char *也不行。另外，对于char  *p_char="abc";，在GCC编译器上,GCC4.9(C++14)及以前的版本会给出警告，在GCC5.3(C++14)及以后的版本则直接报错：ISO C++ forbids converting a string constant to 'char*'（ISO  C++禁止string常量向char*转换）。但这并不影响“字符串字面值是左值”这一结论的正确性，因为cout<<&("abc")<<endl;一句在各个版本的编译器上都能编译通过，没有警告和错误。
>
> ​    2)具名的右值引用是左值，不具名的右值引用是右值。
>
>    见下例（例一）
>
> ```c++
> void foo(X&& x)
> {
>     X anotherX = x;
>    //后面还可以访问x
>  }
> ```
>
>    上面X是自定义类，并且，其有一个指针成员p指向了在堆中分配的内存；参数x是X的右值引用。如果将x视为右值，那么，X  anotherX=x;一句将调用X类的移动构造函数，而我们知道，这个移动构造函数的主要工作就是将x的p指针的值赋给anotherX的p指针，然后将x的p指针置为nullptr。（后续文章讲移动构造函数时会详细说明）。而在后面，我们还可以访问x，也就是可以访问x.p，而此时x.p已经变成了nullptr，这就可能发生意想不到的错误。 
>
>    又如下例（例二）
>
> ```c++
> X& foo(X&& x)
> {
>      //对x进行一些操作
>      return x;
> }
> 
> //调用
> foo(get_a_X());//get_a_X()是返回类X的右值引用的函数
> ```
>
>    上例中，foo的调用以右值（确切说是将亡值）get_a_X()为实参，调用类X的移动构造函数构造出形参x，然后在函数体内对x进行一些操作，最后return  X，这样的代码很常见，也很符合我们的编写思路。注意foo函数的返回类型定义为X的引用，如果x为右值，那么，一个右值是不能绑定到左值引用上去的。 
>    为避免这种情况的出现，C++规定：具名的右值引用是左值。这样一来，例一中X anotherX = x;一句将调用X的拷贝构造函数，执行后x不发生变化，继续访问x不会出问题；例二中，return x也将得到允许。
>      例二中，get_a_X返回一个不具名右值引用，这个不具名右值引用的唯一作用就是初始化形参x，在后面的代码中，我们不会也无法访问这个不具名的右值引用。C++将其归为右值，是合理的，一方面，可以使用移动构造函数，提高效率；另一方面，这样做不会出问题。

### default

```c++
//default关键字
class MyClass {
public:
    MyClass() = default;
    MyClass(const MyClass &other) = default;
    MyClass(MyClass &&other) = default;
    MyClass &operator=(const MyClass &other) = default;
    MyClass &operator=(MyClass &&other) = default;
    ~MyClass() = default;

private:
    int *ptr_;
};
/*使用default关键字的函数必须是特殊成员函数，即默认构造函数、拷贝构造函数、移动构造函数、拷贝赋值运算符、移动赋值运算符和析构函数中的一种。此外，我们还可以在声明特殊成员函数时使用=default来代替{}，这也是一种使用default关键字的方式。*/
```

### auto

```c++
//自动推断变量类型
auto x = 1; // x的类型是int
auto y = 3.14; // y的类型是double
auto z = "hello"; // z的类型是const char *
```

### nullptr

```c++
int *p = nullptr;
```

### final

```c++
//final关键字用于指定一个类或虚函数是不能被继承或重载的
class Base final {
public:
    virtual void foo() final; // 声明了一个不能被覆盖的虚函数
};

class Derived : public Base { // 错误，Derived不能继承Base
public:
    virtual void foo(); // 错误，不能覆盖Base中的虚函数
};
```

### constexpr

```c++
//constexpr关键字用于指定一个函数或变量在编译期间就可以计算出来
constexpr int fib(int n) {
    return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}

constexpr int x = fib(10); // x的值在编译期间就可以计算出来
```

### range-based for loop语法

```c++
vector<int> v = {1, 2, 3};
for (auto x : v) {
    cout << x << endl;
}

int a[] = {1, 2, 3};
for (auto x : a) {
    cout << x << endl;
}
```

### override

```c++
class Base {
public:
    virtual void foo();
};

class Derived : public Base {
public:
    virtual void foo() override; // 显式地覆盖了Base中的foo函数
};
```

### using

```c++
using MyString = std::string; // 将std::string起一个别名MyString
using namespace std; // 给std命名空间起一个别名
```

### static_assert

```c++
//在编译期间进行断言，如果断言失败则会导致编译错误
static_assert(sizeof(int) == 4, "int必须是4字节");
```



## c++20

### 模块

```c++
//定义模块
//定义一个模块需要使用module关键字
module my_module;

//导入模块
//使用import关键字来导入其他模块的内容
import my_module;

//导出模块
//使用export关键字来导出当前模块中的内容
export module my_module;
export int my_function(int x);
export class my_class;

//以上，使用`export`关键字将模块中的`my_function`函数和`my_class`类导出到外部
```



# 周易

## 序卦传

## 64卦

***乾为天,坤为地,水雷屯,山水蒙,水天需,天水讼,地水师,水地比,风天小蓄,天泽履,地天泰,天地否,天火同人,火天大有,地山谦,雷地豫,泽雷随,山风蛊,地泽临,风地观,火雷噬嗑,山火贲,山地剥,地雷复,天雷无妄,山天大蓄,山雷颐,泽风大过,坎为水,离为火***

***泽山咸,雷风恒,天山遁,雷天大壮,火地晋,地火明夷,风火家人,火泽睽,水山蹇,雷水解,山泽损,风雷益,泽天夬,天风姤,泽地萃,地风生,泽水困,水风井,泽火革,火风鼎,震为雷,艮为山,风山渐,雷泽归妹,雷火丰,火山旅,巽为风,兑为泽,风水涣,水泽节,风泽中孚,雷山小过,水火既济,火水未济***

# 奇门遁甲

## 烟波钓叟赋

> 《烟波钓叟歌》是北宋通人所作，后经明朝罗通增删修改。世间有关奇门遁甲的文献甚多，而此书是一部纲领性著作，遁甲术之大要，己尽包其中；若能熟读细玩，参透要旨，实为掌握奇门一术的捷径。其中，《烟波钓叟歌串解》 该书以串解形式，对《烟波钓叟歌》所涉及的内容，作全面论述，而侧重於对‘数奇门’的探讨。
>
>
> 全文
>
>
> 阴阳顺逆妙难穷，二至还乡一九宫。若能了达阴阳理，天地都在一掌中。
>
> 轩辕黄帝战蚩尤，涿鹿经年苦未休，偶梦天神授符诀，登坛致祭谨虔修。
>
> 神龙负图出洛水，彩凤衔书碧云里，因命风后演成文，遁甲奇门从此始。
>
> 一千八十当时制，太公删成七十二。逮于汉代张子房，一十八局为精艺。
>
> 先须掌上排九宫，纵横十五在其中。次将八卦论八节，一气统三为正宗。
>
> 阴阳二遁分顺逆，一气三元人莫测。五日都来换一元，超神接气为准则。
>
> 认取九宫为九星，八门又逐九宫行。九宫逢甲为直符，八门值使自分明。
>
> 符上之门为直使，十时一位堪凭据。直符常遣加时干，直使逆顺遁宫去。
>
> 六甲元号六仪名，三奇即是乙丙丁。阳遁顺仪奇逆布，阴遁逆仪奇顺行。
>
> 吉门偶尔合三奇，值此须云百事宜。更合从旁加检点，余宫不可有微疵。
>
> 三奇得使诚堪使，六甲遇之非小补。乙逢犬马丙鼠猴，六丁玉女骑龙虎。
>
> 又有三奇游六仪，号为玉女守门扉。若作阴私和合事，请君但向此中推。
>
> 天三门兮地四户，问君此法如何处？太冲小吉与从魁，此是天门私出路。
>
> 地户除危定与开，举事皆从此中去。六合太阴太常君，三辰元是地私门。
>
> 更得奇门相照耀，出门百事总欣欣。太冲天马最为贵，卒然有难宜逃避。
>
> 但当乘取天马行，剑戟如山不足畏。三为生气五为死，胜在三兮衰在五。
>
> 能识游三避五时，造化真机须记取。就中伏吟最为凶，天蓬加着地天蓬。
>
> 天蓬若到天英上，须知即是反吟宫。八门反复皆如此，生在生兮死在死。
>
> 假令吉宿得奇门。万事皆凶不堪使。六仪击刑何太凶，甲子直符愁向东。
>
> 戌刑在未申刑虎，寅巳辰辰午刑午。三奇入墓好思推，甲日那堪见未宫。
>
> 丙奇属火火墓戌，此时诸事不须为。更加天乙来临六，月奇临六亦同论。
>
> 又有时干入墓宫，课中时下忌相逢。戊戌壬辰兼丙戌，癸未丁丑一同凶。
>
> 五不遇时龙不精，号为日月损光明。时干来克日干上，甲日须知时忌庚。
>
> 奇与门兮共太阴，三般难得总加临。若还得二亦为吉，举措行藏必遂心。
>
> 更得值符值使利，兵家用事最为贵。常从此地击其冲，百战百胜君须记。
>
> 天乙之神所在宫，大将宜居击对冲。假令直符居离九，天英坐取击天篷。
>
> 甲乙丙丁戊阳时，神居天上要君知。坐击须凭天上奇，阴时地下亦如之。
>
> 若见三奇在五阳，偏宜为客自高强；忽然逢着五阴位，又宜为主好裁详。
>
> 直符前三六合位，太阴之神在前二，后一宫中为九天，后二之神为九地。
>
> 九天之上好扬兵，九地潜藏可立营，伏兵但向太阴位，若逢六合利逃形。
>
> 天地人分三遁名，天遁月精华盖临，地遁日精紫云蔽，人遁当知是太阴。
>
> 开门六乙合六己，地遁如斯而已矣。休门六丁共太阴，欲求人遁无过此。
>
> 要知三遁何所宜，藏形遁迹斯为美。庚为太白丙荧惑，庚丙相加谁会得？
>
> 六庚加丙白入荧，六丙加庚荧入白。白入荧兮贼即来，荧入白兮贼须灭。
>
> 丙为悖兮庚为格，格则不通悖乱逆。丙加天乙为悖符，天乙加丙为飞悖。
>
> 庚加日干为伏干，日干加庚飞干格。加一宫兮战在野，同一宫兮战在国。
>
> 庚加直符天乙伏，直符加庚天乙飞。庚加癸兮为大格，加己为刑最不宜。
>
> 加壬之时为上格，又嫌岁月日时逢；更有一般奇格者，六庚谨勿加三奇。
>
> 此时若也行兵去，匹马只轮无返期。六癸加丁蛇夭矫，六丁加癸雀入江，
>
> 六乙加辛龙逃走，六辛加乙虎猖狂。请观四者是吉神，百事逢之莫措手。
>
> 丙加甲兮鸟跌穴，甲加丙兮龙反首。只此二者是吉神，为事如意十八九。
>
> 八门若遇开休生，诸事逢之总称情。伤宜捕猎终须获，杜好邀遮及隐形。
>
> 景上投书并破阵，惊能擒讼有声名。若问死门何所主，只宜吊死与行刑。
>
> 篷任冲辅禽阳星，英芮柱心阴宿名。辅禽心星为上吉，冲任小吉未全亨。
>
> 大凶篷芮不堪使，小凶英柱不精明。大凶无气变为吉，小凶无气亦同之。
>
> 要识九星配五行，各随八卦考羲经：坎篷星水离英火，中宫坤艮土为营，
>
> 乾兑为金震巽木，旺相休囚看重轻。与我同行即为相，我生之月诚为旺。
>
> 废于父母休于财，囚于鬼兮真不妄。假令水宿号天篷，相在初冬与仲冬，
>
> 旺于正二休四五，其余仿此自研穷。急则从神缓从门，三五反复天道亨。
>
> 十干加伏若加错，入库休囚吉事危。十精为使用为贵，起宫天乙用无遗。
>
> 天目为客地为主，六甲推兮无差理。劝君莫失此玄机，洞彻九宫扶明主。
>
> 宫制其门不为迫，门制其宫是迫雄。天网四张无路走，一二网低有路通，
>
> 三至四宫行入墓，八九高强任西东。节气推移时候定，阴阳顺逆要精通。
>
> 三元积数成六纪，天地未成有一理。请观歌里精微诀，非是贤人莫传与。
>
>
> 注释
>
>
> ● 轩辕黄帝战蚩尤，涿鹿经年苦未休，偶梦天神授符诀，登坛致祭虔精修，龙龟出自河洛水。彩凤衔书碧云里。
>
>
> 昔轩辕战蚩尤于涿鹿，不胜，遂祷于神，梦九天玄女授以符诀，即河图洛书之诀。彩凤衔书即太乙、六壬、遁甲之书也。
>
>
> ● 因命风后演成文，遁甲奇门从此始。
>
>
> 帝命风后演成三式之文，而行兵有阵，出入有门，进退有法，以擒蚩尤。遁者，隐也，甲者，仪也，谓六甲六仪为直符贵神也。六甲隐于六戊，以六戊有神明之德，隐显之机，故以遁甲为名，其甲戌隐于六己、甲申隐于六庚、甲午隐于六辛、甲辰隐于六壬、甲寅隐于六癸，此所谓遁甲也。奇者，乙、丙、丁三奇也。门者，休、死、伤、杜、开、惊、生、景也。遁甲奇门之名由此而起。
>
>
> ● 一千八十当时制，太公删定七十二，逮及汉代张子房，一十八局为精艺。
>
>
> 法以一年三百六十日配作廿四节，一节分三元，一元有五日，一节分为十五日，共得一百八十时。二十四节计四千三百二十时，即有四千三百二十局也。风后约制阳遁五百四十局，阴遁五百四十局，合一千八十局。至太公以七十二候，一候制一局，五日一易，则删定七十二局。汉张子房则又分阳遁九局，阴遁九局，共成十八局，以为万古不易之定式。
>
>
> ● 先从掌上排九宫，纵横十五在其中。
>
>
> 九宫者，一坎、二坤、三震、四巽、五中、六干、七兑、八艮、九离。排于掌上，任其纵横飞布也。十五者，纵横配合图书，无不成十五之数，如太阳之一九十也，少阳之三七十也，太阴之六四十也，少阴之二八十也，以中五乘之，皆成十五，此图之纵横也﹔北一南九十也，东三西七十也，西北之六东南之四十也，西南之二东北之八十也，以中五乘之，亦皆十五，此书之纵横也，故曰纵横十五在其中，此天地之数目，有配合之妙用，所以行兵布阵岂能外此纵横之法哉。
>
>
> ● 次将八卦轮八节，一气统三为正宗。
>
>
> 乾坤定位，山泽通气，雷风相薄，水火不相射，此八卦循序之理。是以八节辅配八卦—冬至主坎，立春主艮，春分主震，立夏主巽，夏至主离，立秋主坤，秋分主兑，立冬主干。所以八方风动，纳天地之气，化为出入抵向之门户也。一气者，卦气也。统三者，一气领三候也，如冬至、小寒、大寒统坎，立春、雨水、惊蛰统艮，春分、清明、谷雨统震，立夏、小满、芒种统巽，夏至、小暑、大暑统离，立秋、处暑、白露统坤，秋分、寒露、霜降统兑，立冬、小雪、大雪统干。以八宫分布二十四气，此为遁甲奇门之正宗，每卦统三节，每节统三候也。三候者，上、中、下三元为三候也。如冬至一七四、小寒二八五、大寒三九六、立春八五二、雨水九六三、惊蛰一七四、春分三九六、清明四一七、谷雨五二八、立夏四一七、小满五二八、芒种六三九，此为阳遁上中下三元三候起局之法也﹔如夏至九三六、小暑八二五、大暑七一四、立秋二五八、处暑一四七、白露九三六、秋分七一四、寒露六九三、霜降五八二、立冬六九三、小雪五八二、大雪四七一，此阴遁上中下三元三候起局之法也。
>
>
> ● 阴阳二遁分顺逆，一气三元人莫测。
>
>
> 冬至为一阳之始生，阳气上升，故阳遁顺行，迎生气也，六甲从坎至离止，以一二三四五六七八九顺而进之。夏至为一阴之始生，阴气下降，故阴遁逆行，迎杀气也，六甲从离至坎止，以九八七六五四三二一逆而退之。以岁气计之，四时代谢，寒暑迭更，三百六十日而一周天，以二至分二遁，体天地阴阳之气，而为人事之用。若以一卦气论之，一气十五日，五日为一元，十五日为三元，一元十二时，三元共一百八十时，然一气之内，按三元之妙用，节气轮转，浑然无迹，而其间盈缩刻数分秒之不齐，全在神气超接之法以补之。
>
>
> ● 五日都来换一元，接气超神为准的。
>
>
> 五日为一元，以甲己为符头，四仲—子、午、卯、酉为上元，四孟—寅、申、巳、亥为中元，四季—辰、戌、丑、未为下元。都来两字必须周六十时耳，其三元之中有节气之迟速，未可据以五日而换一元，故有超接之法为准的。今时符先节到，则用超，节后符到则用接。视超接之法，节令尚可得其真，气一经置闰，重用元局法可闰，而节令断难准矣，故以二至超接为阴阳生育之根蒂，恰要在此处体会分析明白，以超接二字为主宰故曰︰「准的」，犹大匠之准绳，射者之中的也。
>
>
> ● 认取九宫分九星。八门又逐九宫行。
>
>
> 认取者，详审之谓也。九宫者，一坎、二坤、三震、四巽、五中、六干、七兑、八艮、九离也。分者，布列也。九星者，蓬、芮、冲、辅、禽、心、柱、任、英也，以蓬分位于坎，芮分于坤，冲分于震，辅分于巽，禽分于中，心分于干，柱分于兑，任分于艮，英分于离也。八门者，休、死、伤、杜、开、惊、生、景也。逐者，相随而行也，谓休蓬同行，死芮同行，伤冲同行，杜辅同行，开心同行，惊柱同行，生任同行，景英同行。可见自有次第之用法，而吉凶大局定矣。
>
>
> ● 九星常为值符用，八门直使自分明。
>
>
> 直符者，六仪也，其所用时之旬甲谓之直符，如某甲在某宫，则某星随直符而转运，故为直符用也。直使者，其所用时之旬甲之门谓之直使，如某甲在某宫，某门即为直使也。
>
>
> ● 符上之门为值使，十时一易堪凭据。
>
>
> 直符之上其门为直使，随直符而十时一易，有所凭依，无杂乱之纷更也。
>
>
> ● 直符到处加时干，直使顺逆随宫行。
>
>
> 此遁甲奇门之用法，最要认得真切。直符者，系用时之旬甲，乃六仪也，直符所到之处加于所用时干之宫。直使者，八门也，盖门逐符行。假如一局甲子旬，直符在坎一宫，则直使应在休门，占时得甲子时，则甲子直符加甲干应到一宫，直使即在一宫﹔如乙丑时，直符加乙应到九宫，则直使应在二宫﹔丙寅时，直符加丙应到八宫，直使应在三宫。是直使分顺逆随宫而行，直符随时干而行。
>
>
> ● 六甲原号六仪名。
>
>
> 六甲者，甲子、甲戌、甲申、甲午、甲辰、甲寅也。其甲子隐戊，甲戌隐己，甲申隐庚，甲午隐辛，甲辰隐壬，甲寅隐癸。受甲为仪，谓之六仪也。
>
>
> ● 三奇即是乙丙丁。
>
>
> 经云︰「乙居卯位，帝出乎震，丙丁俱抱火德，有离明之象，此三光，所以丽奇于乙丙丁也。」故以乙阴木为日奇，丙阳火为月奇，丁阴火为老人星，其光芒现于丁位，故为星奇。
>
>
> ● 阳遁顺仪奇逆布，阴遁逆仪奇顺行。
>
>
> 阳遁布局之法，如冬至属坎，用一局，即在一宫起甲子戊，顺飞九宫，甲戌己在坤二，甲申庚在震三，甲午辛在巽四，甲辰壬在中五，甲寅癸在干六，是仪顺布也。三奇者，则丁奇在兑七，丙奇在艮八，乙奇在离九宫也。以戊己庚辛壬癸丁丙乙为次序，顺布一二三四五六七八九之宫，则布阳遁九局顺仪逆奇之捷法也，余局仿此。
>
>
> 阴遁布局之法，如夏至属离，用九局，即在九宫起甲子戊，逆布九宫，甲戌己在艮八，甲申庚在兑七，甲午辛在干六，甲辰壬在中五，甲寅癸在巽四，是仪逆行也。顺布三奇者，则乙奇在坎一，丙奇在坤二，丁奇在震三宫也。以戊己庚辛壬癸丁丙乙为次序，逆布九八七六五四三二一之宫，则布阴遁九宫逆仪顺奇之捷法也，余局仿此。
>
>
> ● 吉门仍要合三奇，取用须云百事宜，更合从旁加检点，临宫不可有微疵。
>
>
> 门为执事之始，最要关键，门一得吉，所趋正矣。仍须合乙丙丁三奇之灵，大概利于谋为，犹未可据，谓之全吉，更加检点宫分之有无微疵，如乙奇临震宫，谓之日出扶桑，融合之气，为吉﹔兑乃木之绝地，乙奇克则受制。如丙奇临离九宫谓之月照瑞门，身居帝旺为纯吉﹔而临干则丙火之墓地，光明暗昧，不吉。如丁奇临兑，贵人升殿，为吉﹔而临于坎则谓之朱雀投江，威德收藏，则不吉也。故谓之临宫不可有微疵也。
>
>
> ● 三奇得使诚堪使，六甲遇之非小补，乙逢犬马丙鼠猴，六丁玉女临龙虎。
>
>
> 此法三奇即是乙丙丁矣，然未可执得奇便为堪使。所云得使者，是得直使也。三奇得开休生之直使，所谓得奇得门方，可谓诚堪使也。六甲遇之非小补者，更合地盘上之六甲，相为表里，三奇三门得仪神佐之，岂小补哉？乙奇加甲戌、甲午，丙奇加甲子、甲申，丁奇加甲辰、甲寅，是为犬马鼠猴龙虎之谓也，然以本旬三奇六甲为的也。
>
>
> ● 又有三奇游六仪，号为玉女守门时，若作阴私合和事，请君但向此中推。
>
>
> 此法以地盘丁奇所到之宫为主，遁得本旬直使之门加临，即为玉女守门。其法以甲子旬庚午时、甲戌旬己卯时、甲申旬戊子时、甲午旬丁酉时、甲辰旬丙午时、甲寅旬乙卯时。宜举阴私合和之事，须遇三吉门为宫也。
>
>
> ● 天三门兮地四户，问君此法归何处，天冲小吉与从魁，此是天门私出路，地户除危定与开，举事皆从此方去。
>
>
> 考古法以干为天门﹔此以太冲卯、小吉未、从魁酉为天三门也，又曰天私门。止利于逃行隐迹，乃隐遁之门户也。其法以月将加所用之正时，顺寻太冲、小吉、从魁所临之方，即是天三门，如正月雨水后日缠娵訾之次，月将是亥，用卯时，以亥加卯，则太冲在未，从魁在丑，小吉在亥，其未丑亥上乃天三门也，于仿此推。
>
>
> 考卦例，巽为地﹔此以除、危、定、开为地户也。其四者，五行属土，故所加临处，利于屯营、筑城，有城高池深之保障也。既云地户，地户法以地气将加所用之时，即以建加建，是月分之除、危、定、开日以建加本时，是日分之除、危、定、开时也。如正月建寅，即从寅上起建，顺数，则卯上是除，午上是定，酉上是危，子上是开，其卯、午、子、酉是地四户也。如以建加所用之子时，则丑、未、辰、戌得除、危、定、开，是地四户也。
>
>
> ● 六合太阴太常君，三神原是地私门，更得奇门相照应，用门举事总欣欣。
>
>
> 地私门者，隐藏、潜伏之谓也。六合卯为本家，太阴酉为本家，太肠未为本家。卯酉乃日月出入之门户，所以出门举事迪吉，更合三奇吉门斯为全美。但取贵神之法，与六壬稍异，其法以月将加正时，分旦暮寻其方向，旦暮贵人各有分属，以八干四维分配十二支，以分上下，如用乙巽丙丁坤庚时，系上六字，而辰巳午未申酉属焉，是用旦贵也﹔如用辛干壬癸艮甲时，系下六字，而戌亥子丑寅卯属焉，是用暮贵也。再视贵神临于何宫，以分顺逆。若亥子丑寅卯辰六宫，为阳顺起贵神，求三神阴常六，即是地私门也﹔若在巳午未申酉戌六宫，为阴逆起贵神，求三神阴常六，即是地私门也。假如正月雨水后，太阳缠娵訾之次，亥为月将，以甲戊庚日用卯时，卯属下六字，用暮贵，即以亥加卯时，以暮贵在未，未临亥宫，亥为阳支，起贵神顺行，则太常在未，六合在寅，太阴在酉，而未寅酉之方，乃地私门也。又如甲戊庚日，用午时，午属上六字，用旦贵，以亥将加午时顺行，旦贵在丑，丑临申宫，申为阴支，起贵神逆行，则太阴在戌，太常在子，六合在巳，是戌子巳三方乃地私门也。天三门、地四户、地私门三者，法异而用同，乃遁甲最要之神，若得全和奇门，则所向无阻矣。
>
>
> ● 太冲天马最为贵，卒然有难宜逃避，但当乘取天马行，剑戟如山不足畏。
>
>
> 考神煞有天马，即天马方也。盖太冲以卯为本神，即房宿也，故为天马其所加临处不空不陷不囚不墓，利于骏奔万里。法以月将加所用之正时，视太冲所临之方，即天马方也，更合门奇，纵剑戟如林，有何畏焉﹖
>
>
> ● 三为生气五为死，盛在三兮衰在五，能知趋三避五时，便自嵬然常独处。
>
>
> 郭氏元经曰︰「五凶三吉就门推，吉有吉兮不用疑。」抑见三吉五凶以门论也。五凶者，乃杜惊伤死景也，又以五为宫分者，止言避五而未及之三，则阴阳驳集之处，岂可不避之乎，故避五以方言之为确论也。
>
>
> ● 就中伏吟为最凶，天蓬加着地天蓬，天蓬若列天英上，须知即是返吟宫，八门反复皆如此，死在生兮生在死，假令吉宿得奇门，万事皆凶不可使。
>
>
> 天上地下星伏而不易位，在于本宫，故曰伏吟。天上地下九星动而易位，加于对冲之宫，故曰返吟。死门加于生门曰返吟，死门加于死门曰伏吟。假令吉宿得奇门，值返吟、伏吟之时，亦不堪用事也。
>
>
> ● 六仪击刑何太凶，甲子直符愁向东，戌刑在未申刑虎，寅巳辰辰午自午。
>
>
> 此言直符加所刑之地相刑与自刑也。如甲子临三宫，子卯相刑﹔甲戌临二宫，戌未相刑﹔甲申临八宫，申寅相刑﹔甲午临九宫，午自刑﹔甲辰临四宫，辰自刑﹔甲寅临四宫，寅巳相刑也。百事谨慎不宜相犯。
>
>
> ● 三奇入墓好推详，乙日何堪见未方，丙火墓戌丁墓丑，此时诸事见灾殃。
>
>
> 乙为阴木，长生于亥，墓于未，故乙奇临二宫为入墓。丙为阳火，长生于寅，墓于戌，故丙奇临六宫为入墓也。丁为阴火，长生于酉，墓于丑，故丁奇临八宫为入墓也。
>
>
> ● 又有时干入墓宫，课中时下忌相逢，戊戌壬辰兼丙戌，癸未丁丑己丑凶。
>
>
> 六甲子一周有六日，时干入墓谓丙戌时丙入戌墓、丁丑时丁入丑墓、壬辰时壬入辰墓、癸未时癸入未墓、己丑时己入丑墓、戊戌时戊入戌墓。凡入墓之时，运筹图谋、建立营寨皆昏迷无气。
>
>
> ● 五不遇时龙不精，号为日月损光明，时干来克日干上，甲日须知时忌庚。
>
>
> 盖甲日庚午时、己日乙丑时，乙日新巳时、庚日丙子时，丙日壬辰时，丁日癸卯时、壬日戊辰时，戊日甲寅时、癸日己未时，辛日丁酉时，此时时干克日干，故主客不合，极凶之时，纵得奇门皆不宜用。
>
>
> ● 奇与门兮共太阴，三般难得总加临，若还得二亦为吉，举措行藏必遂心。
>
>
> 谓乙丙丁三奇、开休生三门、太阴六合九地三神，三者不可兼得。若还得三者，或门与三神会合，或奇与三神会合，虽未全吉，其谋亦可遂愿矣。
>
>
> ● 更得直符直使利，兵家用事最为贵，当从此地击其冲，百战百胜君须记。
>
>
> 直符以言星，直使以言门，若有会合，直符不犯刑墓，直使不犯迫制，利于行兵谋事。大将屯兵直符直使之本宫，而进兵于直符直使对冲之宫，战自胜矣。
>
>
> ● 天乙之神所在宫，大将宜居击对冲，假令直符居离九，天英坐取击天蓬。
>
>
> 天乙者，直符也。主帅居直符之本宫击敌于对冲之宫，如直符居离九宫，故坐英星而击蓬也。其法，在阳遁利于天上直符所居之宫，阴遁利于地下直符所居之宫。
>
>
> ● 甲乙丙丁戊阳时，神居天上要君知，坐击须凭天上奇，阴时地下亦如之。
>
>
> 得五阳时用事，主清虚之气上浮于天，所谓九天之上好扬兵，故布阵坐击须凭天上三奇，以依神灵赫奕也。甲乙丙丁戊为五阳时。得五阴时用事，沉厚之气下降于地，其神镇静，所谓九地之下利潜藏，故伏奇固守须凭地下三奇，以藉神灵庇佑也。己庚辛壬癸为五阴时。
>
>
> ● 若见三奇在五阳，偏宜为客自高强，忽然逢着五阴位，又宜为主好裁详。
>
>
> 此承上文而言也。若五阳之时，而天上三奇在于五阳之东部，利于为客﹔若五阴之时，而天上三奇在于五阴之西部，利于为主。夫主客之分，用兵最要之机，故黄帝云︰「审动静之理，察先后之机。」动则为客，静则为主，主客既定，胜负斯分。其先起者为客，后起者为主。先起者，待敌未动，扬兵而先进﹔后起者，屯兵偃旗，待敌至而后应之，此主客变通之法也，合三奇用之，百战百胜。
>
>
> ● 直符前三六合位，太阴之神在前二，后一宫兮为九天，后二之神为九地。
>
>
> 阳遁，直符、螣蛇、太阴、六合、白虎、元武、九地、九天也﹔阴遁，直符、九天、九地、朱雀、勾陈、六合、太阴、螣蛇也。其法不用飞宫，以甲为旬首，隐直符分顺逆而布之。
>
>
> ● 九天之上好扬兵，九地潜藏可立营，伏兵但向太阴位，若逢六合利逃形。
>
>
> 九天者，言攻之至极也，乃杀伐之气，运在此方，可以行兵，依此气以扬威武。九地者，言守之至深也，乃朦胧之气，运在此方可以行兵，依此气结寨安营。太阴之下可埋伏设险御敌，可遣行间谍。六合之下利避难逃危。此四星各有所宜，而得奇门乃合此法。
>
>
> ● 天地人兮三遁名，天遁月精华盖临，地遁日精紫云蔽，人遁当知是太阴。生门六丙合六丁，此为天遁自分明。开门六己合六乙，地遁如斯而已矣。休门六丁共太阴，欲求人遁无过此。风云龙虎并鬼神，始知九遁能为用。
>
>
> 天遁—生门、丙奇合地盘六丁。地遁—开门、乙奇合地盘六己。人遁—休门、丁奇合太阴。风遁—开、休、生三门合天盘六辛加地己，利水战、火战，飞沙走石。云遁—三门、乙奇加地辛，宜祈祷、雨泽、学道、修仙、隐遁。龙遁—休门、乙奇下临坎宫，宜行船、水战、穿井、通渠。虎遁—三门、六辛临艮，宜探围、射猎、捕捉、出师、战阵。神遁—生门、丙奇合九天，宜出师、大战、赛社、迎神、驱邪、治病。鬼遁—开门、乙奇合九地，宜驱邪、酬神、祭祀。以上神奇九大遁，最宜隐遁，人莫能窥。惟天地人三遁之时，人间万事无不宜也。
>
>
> ● 丙加甲兮鸟跌穴，甲加丙兮龙回首，只此二者为最吉，百事如意十八九。
>
>
> 龙回首者，谓天上六甲临于地下六丙是也。经曰：「飞龙在天，回首顾源。」若举兵利为客，扬威万里，一人可敌万夫，凡百谋为，所向皆宜。鸟跌穴者，谓天上丙奇临地下六甲是也。经曰：「进飞得地，龙云聚会。」若此时行兵，地辟千里，凡百举事皆利。
>
>
> ● 庚为太白丙荧惑，庚丙相加谁会得，六庚加丙白入荧，六丙加庚荧入白，白人荧兮贼即来，荧入白兮贼即灭。
>
>
> 太白入荧惑谓天上六庚加地下六丙，乃金入火乡而受克，此时防有贼即来，掩袭以罹其祸。荧惑入太白者，为天上六丙加地下六庚，乃火入金乡而受克，此时不可入敌人之境而索战，若有贼至，必畏而遁去。故兵帐赋云：「荧入白而敌寇自去，白入荧而城垒宜坚。」
>
>
> ● 丙为勃兮庚为格，格则不通勃乱逆。直符加庚天乙飞，庚加直符天乙伏。庚加日干为伏干，日干加庚飞干格。加一宫兮战于野。同一宫兮战于国。庚加癸兮为大格，加己刑格最不宜，加壬之时为小格。又嫌岁月日时驱。更有一般奇格者，六庚慎勿加三奇，此时若也行兵去，疋马只轮无返期。
>
>
> 勃者，颠倒也，天上六丙加今日之干为日勃，加时亦然，若用兵则纪律乱矣。凡庚所加皆谓之格。格者，隔绝不通也。庚加年月日时干皆为格，惟宜固守莫先举，然此时行兵多有凶咎，应避此格也。天上直符加地下六庚为飞宫格，此时主客皆不利，为宜坚壁固守，出战必遭擒。天上六庚加地下直符之宫为伏宫格，战斗不利为主，不宜。天上六庚加于今日之干为伏干格，此时行兵主客不利。天上所用之日干加于地下六庚为飞干格，用兵出战则主客皆有所伤。天上六庚加地下六癸为大格，此时出军车破马毙。天上六庚加地下六己为刑格，此时出兵为主不利，士卒逃亡，从此方捕捉反有凶殃。天上六庚加地下六壬为小格，又为伏格，此时不利行兵动众。天上六庚加地下三奇乙丙丁为奇格，此时行兵，疋马只轮定无返期，又云庚加丙丁奇遇景门英星乃下克上，用兵先举者败，故疋马只轮所向皆失，若庚加乙奇或遇冲辅伤杜两门乃上克下，用兵先举者胜，所向皆克。天盘六庚加于坎一宫谓之加一宫，如天盘庚加地盘庚同在坎宫，为之同一宫，故有战于野，战于国之分也。
>
>
> ● 六癸加丁蛇妖矫。六丁加癸雀投江。六乙加辛龙逃走。六辛加乙虎猖狂。请观四者是凶神，百事逢之莫措手。
>
>
> 天上六癸加地下六丁为妖矫格，此时纵合奇门，不宜举事。天上六丁加地下六癸为为投江格，此格行兵防有丧失之祸，举事主有口舌争斗之祸。天上六辛加地下六乙为猖狂格，此时行兵主客两伤必见杀戮，为主有暗害之忧。天上六乙加地下六辛为逃走格，此时不宜举兵动众，有败亡之祸。
>
>
> ● 八门若遇开休生，诸事逢之总称情。伤宜捕猎终须获。杜好逃亡及隐形。景上投书并破阵。惊能擒讼有声名。若问死门何所主，只宜吊死与行刑。
>
>
> 此八门所主之吉凶，三吉者，开休生也﹔五凶者，死伤惊杜景也。不曰：「吉者终吉，凶者终凶。」又曰：「凶中有吉，吉中有凶。」各分所主之。吉凶更论有气无气、得令不得令、制迫不制迫，所以要视加临之地位生克归何耳。休门，休者，美也。得天一生水之义，坎为本宫，在冬得令，在春则休，在夏则囚，在秋则相，在四季月各旺十八日，则受气克无气，在本宫则曰伏吟，临艮则受克，临震则泄气，临巽而入墓，临离则返吟，临坤为长生，临未则受克而被伤，一宫之中，有纯疵之不同也，临兑为败气，在干则得生，在亥而有助。死门，死者，不能生息之象也，坤为本宫，在四季各旺十八日为得令，在秋则休，在冬则囚，在夏则相，在春则死，在本宫则伏吟，临兑沐浴也，临干泄气，临坎门迫，临艮返吟，临震受克，临巽为墓，临离为胎而有生息。伤门，伤者，残也，万物盛极而反伤，震为本宫，在春则得令，在夏则休，在秋则死，在冬则相，在四季则囚，在本宫则为伏吟，临巽为得地，临离为死，临坤木之墓地，又为门迫，临兑受克，又为返吟，临干为长生，临坎受生，临艮为门迫，临震为帝旺。杜门，杜者，闭也，主万物有杜塞不通之象，巽为本宫，干为返吟，于同伤门。开门，开者，启也，道路坦夷，通利关津，干为本宫，在秋则得令，在冬则休，在春则囚，在四季则相，在夏则死，在本宫则伏吟，临坎则无气，临艮为墓地，临震门迫，临巽坤兑系长生官旺之乡为有气，临离为受克。惊门，惊者，动也，惶惑忧疑之象，兑为本宫，在秋得令，在冬则休，在春则囚，在四季则相，在夏则死，在本宫为伏吟，临干衰病之地，临坎无气之乡，临艮为墓地，临震为门迫，临巽为长生之地，临离受克，临坤为冠带得地。生门，生者，养也，万物至此而化育成材之象，艮为本宫，在四季月为有气，在本宫为伏吟，在夏为相，在秋则休，在冬则囚，在春则死，临震为受克，临巽为墓地，临离为有气，临坤干坎系长生冠带临官帝旺之乡为有气，临兑乃败气也。景门，景者，明也，丽明于天中，万象蒸舒之象，离为本宫，在夏得令，在春为相，在四季为休，在秋则囚，在冬则死，在本宫为伏吟，临坤衰病之地，临兑火至而光熄矣，临干为墓，临坎为克，又为返吟，临艮为长生之地为有气，临震为沐浴，亦为得气，临巽为旺气始生之地也。
>
>
> ● 蓬任冲辅禽阳星，英芮柱心阴宿名。辅禽心星为上吉，冲任小吉未全亨，大凶逢芮不堪使，小凶英柱不精明。大凶无气变为吉，小凶无气亦同评。吉宿更能逢旺相。百事为之必有成﹔若遇休囚并废没，劝君不必进前程。
>
>
> 此言九星之吉凶也。经云：「时下得辅禽心为上吉，冲任为次吉，蓬芮为大凶，柱英为小凶。」更以五行生旺言之，若大凶之星，得休囚无气，则小凶也﹔小凶之星，得休囚无气，亦不足忧也﹔若上吉、次吉之星无气，亦不甚吉也。
>
>
> ● 要识九星配五行，各随八卦考羲经。芮禽任坤中艮土，坎蓬属水火离英，干兑为金心柱会，震冲巽辅木相因。吉凶自有元妙诀，旺相休囚与重轻。与我同行即为旺，我生之月诚为相，废于父母休于财，囚于鬼兮真不妄。假令水宿号天蓬，旺在初冬与仲冬，相居正二休三四，其余仿此类推同。
>
>
> 此言九星配五行生克休囚之理也。经云：「我生之月为相，同类之月为旺，生我之月为废，我克之月为休，克我之月为囚。」如天蓬水星，旺于亥子月，水同类也﹔相于寅卯月，水生木也﹔废于申酉月，金生水也﹔休于巳午月，水克火也﹔囚于辰戌丑未月，土克水也。天英火星，旺于巳午月，火同类也﹔相于辰戌丑未月，火生土也﹔废于寅卯月，木生火也﹔休于申酉月，火克金也﹔囚于亥子月，水克火也。天冲天辅木星，旺于寅卯月，木同类也﹔相于巳午月，木生火也﹔废于亥子月，水生木也﹔休于辰戌丑未月，木克土也﹔囚于申酉月，金克木也。天心天柱金星，旺于申酉月，金同类也﹔相于亥子月，金生水也﹔废于辰戌丑未月，土生金也﹔休于寅卯月，金克木也﹔囚于巳午月，火克金也。天芮天禽天任土星，旺于辰戌丑未月，土同类也﹔相于申酉月，土生金也﹔废于巳午月，火生土也﹔休于亥子月，土克水也﹔囚于寅卯月，木克土也。
>
>
> ● 急则从神缓从门，三五反复天道亨。
>
>
> 急者，临事于危难之际，不容稍缓，出入抵向，不利于方位，则有从神之法。神者，天上直符所居之方，从此而趋驰之，自得神灵之护佑也。三者，开休生也。五者，死伤杜惊景也。三五反复者，三吉能凶，五凶能吉，随时变迁，神其用而趋向之，则天道亨通矣。
>
>
> ● 十干加伏若加错，入库伏囚吉事危。
>
>
> 吉凶之枢机皆在于十干加伏，随直使以转运，若宫分加伏有错，则入墓休囚，事之应吉反危矣。
>
>
> 时加六甲，一开一阖，上下交接，又云：「甲为天福，又为青龙，阳开利客，阴开利主，阖则固守，开则扬兵。」阳星合孟甲，内开外阖﹔合仲甲，半开阖﹔合季甲，内外俱开。阴星合孟甲，大阖﹔合仲甲，内阖外开﹔合季甲，外大开内半阖。三甲者，甲子、甲午为孟甲，宜静﹔甲寅、甲申为仲甲，宜潜藏，不可外出﹔甲辰、甲戌为季甲，凡百谋为大吉。诀云：「时加六甲为开阖，六甲虽同用不同。阳星加开移徙吉，阴星加阖所为凶。」
>
>
> 时加六乙，往来恍惚，与神俱出。又云：「时加六乙，诸事皆吉，利生百倍。」，又云：「六乙为天德，言乙与日奇，凡有往来，从天上乙奇而出，如有神助，不可测也。」
>
>
> 时加六丙，道路清宁，所愿皆遂，又云 ：「威德之时，利于为主，不利为客。」又曰：「明堂之下，利于安营。」又云：「六丙天威无不利，敌人亡败莫争功。」丙为月奇，从天上六丙方出，可以制伏兵矣。
>
>
> 时加六丁，出幽入冥，至老不刑，刀虽加颈，犹然不惊。又云：「时加六丁，做事康宁。」丁为星奇，从天上六丁而出，随星奇挟玉女入阴中，则人不见鬼不知，敌人不敢侵，将兵主胜。
>
>
> 时加六戊，乘龙万里，不之呵止。又云：「时加六戊，凶神不遇。」又戊为天门，又为天武，若远行当从天上六戊之下而出，挟天武而出天门，虽万里凶恶，不敢危害，扬兵必获大胜。
>
>
> 时加六己，如神所使，不知六己，出被凶咎。又云：「时加六己明堂，宜秘密潜踪。」己为六合，又为地户，凡隐匿偷营劫寨，当从天上六己之下而出，如神不能见其形，故曰如神所使。
>
>
> 时加六庚，抱木而行，强有出者，必见斗争。又云：「前有凶恶，定主虚惊。」，又云：「庚为天狱，事相触犯，必遭刑狱。」此时强有出者，必迫刑宪，惟宜自守。此时将兵利主，不利客。
>
>
> 时加六辛，行遇死人，强有出者，罪罚缠身，又时加六辛，逢着鬼神，求之不遂，横祸来侵。又云：「辛为天庭，宜行刑决狱。」若强有出者，斧钺在前，必遭刑罪。
>
>
> 时加六壬，为吏所禁，强有出入，飞祸将临。又云：「六壬为天牢，又为天贼，宜囚禁罪恶。」若远行出入，必遭罪杜。将兵强欲出入，反被遭擒。
>
> 时加六癸，众人莫视，不知六癸，出门即死。又云：「时加六癸，为天网，惟利逃亡。」又癸为华盖、天藏，利于伏匿。又云：「六癸之下利于伏兵隐形。」
>
>
> 总论十干加临之法，非执着一处，盖遁甲之所重者在于故，视今日之时得何干，天上所用之时临于地盘得何干，不入库休囚，吉者终吉矣。
>
>
> ● 十精为使用为贵，起宫天乙无须溃。
>
>
> 使者，直使之门也。其直使十时一易，主宰祸福之权衡，贵在察时按宫精而用之。天乙者，直符，即六甲之旬首，统领三奇六仪，加诸时干，到处为之起宫，不可溃乱于用也。
>
>
> ● 天为客兮地为主，六甲推之无差理， 劝君默识此元机，洞澈九宫扶明主。
>
>
> 天者，天盘也。客者，用也。地者，地盘也。主者，体也。从奇仪顺逆相推体用，合其理默识者不出口，与心颖悟此中之元妙，纵横九宫，了然于指掌之中也。
>
>
> ● 宫制其门不为迫，门制其宫门迫凶。吉门被迫吉减去，凶遇门迫凶更凶。宫若生门则为义，最吉日合门主宫。
>
>
> 宫迫者，谓开惊两门临离宫，火克金也﹔休门临坤艮二宫，土克水也﹔生死两门临震巽二宫，木克土也﹔伤杜两门临干兑二宫，金克木也﹔景门临坎宫，水克火也，此宫克门也。凡宫迫门者，为主克客也。门迫者，开惊二门临震巽二宫，金克木也﹔休门临离宫，水克火也﹔生死二门临坎宫，土克水也﹔伤杜二门临坤艮二宫，木克土也﹔景门临干兑二宫，火克金也，此门克宫也。盖迫者，逼也，急切受制或门受制于宫，或宫受制于门，彼此相抗，扼抑不容，故吉门受制，吉则减吉，凶门受制，凶则愈凶矣。凡门克宫者，为客克主也。
>
> 宫生门者，义也，开惊二门临坤艮宫，土生金也﹔休门临干兑二宫，金生水也﹔生死二门临离宫，火生土也﹔伤杜二门临坎宫，水生木也﹔景门临震巽二宫，木生火也，此宫生门也。凡生门者为主生客也。
>
>
> 门生宫者，相也，惊开二门临坎宫，金生水也﹔休门临震巽二宫，水生木也﹔生死二门临干兑二宫，土生金也﹔伤杜二门临离宫，木生火也﹔景门临坤艮二宫，火生土也，此门生宫也。凡门生宫者，为客生主也。
>
>
> 门宫比和者，如金见金，木见木，土见土，水见水，火见火。合三奇吉格者为上吉，诸事大利，需要分别吉凶四时旺相休咎，断之可也。
>
>
> ● 天网四张无走路，一二底纹有路通，三至四宫行人墓，八九高强任西东。
>
>
> 此言时不得六癸也。六癸属阴，乃十干气尽之时也。犯之者，如入网中，幽暗难出，奇神有高下，审定所用之时加诸六癸在何宫。若在坎一宫则高一尺，在坤二宫则高两尺，随宫言高下也。天网一二尺者，遇之可跨而出，倘高在三尺以上，则不可逃矣，此之时可偃旗息鼓，弃甲衔枚匍匐而脱，或吾军陷入敌军或从天门而出，或从玉女而去，或从三奇斩擒，以见血光，臂横刀刃，呼天辅之神号，扬旗擂鼓，举喊震声，并力突出而网破矣。若敌人来追，则身投网内，可回军奋击，后军必慌忙失措，破阵丧师，或敌人入吾所布之网，敌人作法而奔我军，慎不可追，追则我军投入网中矣。故诀云：「天网四张，万物尽伤，高用匍匐，低用声扬也。」
>
>
> ● 节气推移时候定，阴阳顺逆要精通，三元积数成六纪，天地都成一理中。
>
>
> 此言遁甲之理，反复究详之意。二十四气之转移，皆在七十二候上中下三元也，所以有超接之法，期以节候符合轮转，以为遁甲之妙用。以二至而分阴阳两遁，定元布局不可差谬，故须精通。
>
>
> ● 遁甲此书为正轨，节气准的无过此，请观歌里精微诀，非是贤人莫传与。
>
>
> 此言遁甲奇门惟此书为天时节气之正宗，非壬遁等术之可比，故戒妄传。此赋字字珠玑，精研玩味，岂愚昧者所能测识哉？

## 基础

### 二十四节气

> ****
>
> **春雨惊春清谷天，夏满芒夏暑相连**
>
> **秋处露秋寒霜降，冬雪雪冬小大寒**
>
> --------------------------------------
>
> ***立春,雨水,惊蛰,春分,清明,谷雨;***
>
> ***立夏,小满,芒种,夏至,小暑,大暑;***
>
> ***立秋,处暑,白露,秋分,寒露;***
>
> ***立冬,小雪,大雪,冬至,小寒,大寒***

------------------------------------------------------------

### 三奇六仪

> ***奇:乙,丙,丁***
>
> ***门:休、死、伤、杜、开、惊、生、景***
>
> ***甲:主帅***

-----------------------------------------------------------------------------------------

### 八门,九星,洛书,干支,九宫,八神

> ***九星:一天蓬，二天芮，三天冲，四天辅，五天禽，六天心，七天柱，八天任，九天英***
>
> ***天干:甲,乙,丙,丁,戊,己,庚,辛,壬,癸***
>
> ***地支:子,丑,寅,卯,辰,巳,午,未,申,酉,戌,亥***
>
> ***洛书数:戴九履一, 三右七,二四为肩,六八为足***
>
> ***九宫:坎一,坤二,震三,巽四,中五,乾六,兑七,艮八,离九***
>
> ***上元日干:子午卯酉;中元日干:寅申巳亥;下元日干:辰戌丑未***
>
> ***八神:直符,腾蛇,太阴,六合,白虎(勾陈),玄武(朱雀),九地,九天***

### 阴阳遁

> ***阳遁是奇门遁甲里的节气，指从冬至开始到芒种结束。***
>
> ***阳遁:***
>
> ***冬至,惊蛰一七四,小寒二八五***
>
> ***大寒,春分三九六,芒种六三九***
>
> ***谷雨,小满五二八,立春八五二***
>
> ***立夏,清明四一七,雨水九六三***
>
> ***阴遁：*** 
>
> ***夏至、白露九三六，小暑八二五，*** 
>
> ***大暑、秋分七一四，立秋二五八，*** 
>
> ***霜降、小雪五八二，大雪四七一。***
>
> ***寒露、立冬六九三，处暑一四七，*** 
>
> ***即冬至、惊蛰的上元为阳遁一局，中元为阳遁七局，下元为阳遁四局***

### **超接置闰法**

> **超神者，谓节气未至而甲子、己卯、甲午、己酉四上元之符头先到，则从符头而行节气之先上元  。如正月初一日立春，而上年十二月二十五日即是甲子。此符头先至，即以此二十五日甲子作立春上元，至正月初一日乃行中元，故谓之超也。接气者，谓甲子、己卯、甲午、 己酉四上元之符头未到而节气先到，则候符头先日方行节气。如正月初一日立春，而初五方是甲子，此符 头未到，  却以初一至初四仍行大寒下元，至初五方行立春上元。故谓之接也。 超有旬日止五日，余仿此**
>
> ***译文:超神者是指当节气未到时，甲子、己卯、甲午、己酉四个上元符头先到，就以符头上元作为节气上元。例如，正月初一日是立春，而上一年的十二月二十五日是甲子，这时符头先到，就以这个甲子作为立春上元，正月初一日才行中元，所以叫做超。接气者是指当节气已到，但甲子、己卯、甲午、己酉四个上元符头还未到，就等到符头先到的日子才行节气。例如，正月初一日是立春，但初五才是甲子，这时符头未到，所以初一至初四仍行大寒下元，到初五才行立春上元，所以叫做接。超和接的时间都是旬日至五日。***

>  **直符到处加时干，直使顺逆随宫行。**
>
> ***此遁甲奇门之用法，最要认得真切。直符者，系用时之旬甲，乃六仪也，直符所到之处加于所用时干之宫。直使者，八门也，盖门逐符行。假如一局甲子旬，直符在坎一宫，则直使应在休门，占时得甲子时，则甲子直符加甲干应到一宫，直使即在一宫﹔如乙丑时，直符加乙应到九宫，则直使应在二宫﹔丙寅时，直符加丙应到八宫，直使应在三宫。是直使分顺逆随宫而行，直符随时干而行。***
>
> **六甲原号六仪名。**
>
> ***六甲者，甲子、甲戌、甲申、甲午、甲辰、甲寅也。其甲子隐戊，甲戌隐己，甲申隐庚，甲午隐辛，甲辰隐壬，甲寅隐癸。受甲为仪，谓之六仪也。****

### **八门应诀**

> ***欲求财利往生方,葬猎须知死路强***
>
> ***远行征战开门吉,休门见贵最为良***
>
> ***惊门官讼是非多,杜门无事好逃藏***
>
> ***伤门搏斗能捉贼,景门饮酒好思量***

### 五行

#### 十天干

> ***甲乙东方木,丙丁南方火,戊己中央土,庚辛西方金,壬癸北方水***

#### 四墓(四库)

> ***辰:壬水,辛金之墓***
>
> ***戌:丙火,戊土,乙木之墓***
>
> ***丑:庚金,丁火,己土之墓***
>
> ***未:甲木,癸水之墓***

#### 十二地支

> ***子水鼠,丑土牛,寅木虎,卯木兔,辰土龙,巳火蛇,午火马,未土羊,申金猴,西金鸡,戌土狗,亥水猪***

> | 五行   | 阳五行   | 阴五行   |
> | ------ | -------- | -------- |
> | **土** | **辰戌** | **丑未** |
> | **木** | **寅**   | **卯**   |
> | **火** | **午**   | **巳**   |
> | **水** | **子**   | **亥**   |
> | **金** | **申**   | **酉**   |

#### 八门

> ***休(坎水),生(艮土),伤(震木),杜(巽木),景(离火),死(坤土),惊(兑金),开(乾金)***

#### 八神

> ***值符:东方青龙甲木***
>
> ***螣蛇:南方火***
>
> ***太阴:西方阴金***
>
> ***六合:东方木***
>
> ***白虎(勾陈):西方金***
>
> ***玄武(朱雀):北方水***
>
> ***九地:坤土***
>
> ***九天:乾金***

#### 九星

> ***天蓬星(贪狼星):坎水***
>
> ***天芮星(巨门星):坤土***
>
> ***天冲星(禄存星):震木***
>
> ***天辅星(文曲星):巽木***
>
> ***天禽星(廉贞星):中土***
>
> ***天心星(武曲星):乾金***
>
> ***天柱星(破军星):兑金***
>
> ***天任星(左辅星):艮土***
>
> ***天英星(右弼星):离火***

### 八门

#### 旺相休囚死

***(待补充)***

### 九星

#### 旺相休囚

***(待补充)***

### 十天干

#### 生旺死墓绝

***(待补充)***

### 十二地支

#### 刑冲害化合

(***待补充***)

## 吉凶格

### 常用吉格

(***待补充***)

### 常用凶格

(***待补充***)











