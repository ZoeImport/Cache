# 👋Welcome🎉

:star:[**仓库链接**](https://github.com/zzll37/QingShu):heart:

## 📇目录

### 💻<a href="#linux">Linux</a>

- <a href="#shell">***Shell***</a>
- <a href="#archLinux">***ArchLinux***</a>
- <a href="#baseLinux">***基本操作***</a>
- <a href="#baseTool">***基本工具***</a>
- <a href="#awesomeTool">***有趣的拓展工具***</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/9/96/Farm-Fresh_database_yellow.png" alt="Database" style="zoom:90%;" /><a href="#database">Database</a>

- <a href="#mysql">***mysql***</a>

### <img src="https://golang.org/doc/gopher/frontpage.png" alt="Gopher" style="zoom:8%;" /><a href="#go">**GO**</a>

- <a href="#baseGrammer-go">***Base Grammer***</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/1/18/ISO_C%2B%2B_Logo.svg" alt="C++" style="zoom:8%;" /><a href="#c++">C++</a>

- <a href="#baseGrammer-c++">***Base Grammer***</a>
- <a href="#compiler-c++">***Compiler***</a>
- <a href="#build-c++">***Build***</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Cloud-icon.svg" alt="cloud" style="zoom:5%;" /><a href="#cloud">Cloud</a>

- <a href="#docker">***Docker***</a>
- <a href="#minikube">***Minikube***</a>
- <a href="#kubectl">**Kubectl**</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/1/1c/Avatar_toolbox.png" style="zoom:10%;" /><a href="#toolbox">ToolBox</a>

- <a href="#git">***Git***</a>
- <a href="#make">***Make***</a>
- <a href="#gdb">***GDB***</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Font_Awesome_5_solid_gift.svg/240px-Font_Awesome_5_solid_gift.svg.png" style="zoom:12%;" /><a href="#awesomeLanguage">Awesome Lanage</a>

- <a href="#python">***Python***</a>

### <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Ancient-columns_-_Delapouite_-_game-icons.svg/240px-Ancient-columns_-_Delapouite_-_game-icons.svg.png" style="zoom:15%;" /><a href="#ancientScience">Ancient Science</a>

- <a href="#zhouyi">***周易***</a>
- <a href="#qimendunjia">***奇门遁甲***</a>

## :walking:Bye bye:smile:													👆give me a star ?✅ 

------



# <a id="Linux">Linux</a>

## <a id="shell">Shell</a>

### 数值计算方式

| 计算方法                        | 实例                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| declare定义整数型，直接进行运算 | declare两个整数型a，b，c=a+b                                 |
| expr或；let                     | expr 整数运算表达式  let 整数运算表达式，其中let可以运算多个表达式，expr除了可以运算计算表达式之外，还可以对字符串进行操作 |
| $(()) 或者 $[]                  | $(( 计算表达式 )) 或者 $[ 计算表达式 ]                       |
| bc 计算                         | bc可以对文件中的计算式进行计算，同时也可以进行管道计算 "计算表达式 \| bc [ options ]"，其中可以进行进制转换，内置数学函数调用等操作 |

### 数值比较方式

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

### 字符串比较方式

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

### 逻辑运算符

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

### cut工具（字符串及文件操作）

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

### 字符串截取操作

#### ***cut工具操作：使用方法转上***

##### ***常见字符串截取格式：***

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

## <a id="archLinux">Arch Linux</a>

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



### yay (aur)包管理器

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



## <a id="baseLinux">基础命令与权限控制</a>

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

## <a id="baseTool">基础工具</a>

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





## <a id="awesomeTool">有趣的拓展工具</a>



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

***描述：类似于firewalld的防火墙服务***

> ```bash
>  iptables [-t 表名] 管理选项 [链名] [匹配条件] [-j 控制类型]
> ```
>
> ***使用方式：***
>
> ```bash
> iptables 管理选项
>  -A:在指定链的末尾添加一条新的规则
>  -D:删除指定链中的某一条规则，可删除指定序号或具体内容
>  -I:在指定链中插入一条新规则，未指定序号时默认作为第一条规则
>  -R:修改、替换指定链中的某一条规则，可指定规则序号或具体内容
>  -L:列出指定链中所有的规则，未指定链名，则列出表中的所有链
>  -F:清空指定链中所有的规则，未指定链名，则清空表中的所有链
>  -P:设置指定链的默认策略
>  -n:使用数字形式显示输出结果
>  -v:查看规则列表时显示详细的信息
>  -h:查看命令帮助信息
>  --line-numbers:查看规则列表时，同时显示规则在链中的顺序号
> ```
>
> **例如:**
>
> ```bash
> iptables -t filter -A INPUT -p tcp -s 192.168.100.100 --dport 80 -j REJECT 
> #对filter表APPEND一个新的规则 对于源192.168.100.100 访问本机80端口的tcp协议包都进行拒绝
> ```
>
> ***iptable机制：***
>
> ***iptables维护着四张记录表和五道数据包传递链***
>
> **四表：** 
>
> ​	*filter:* 用于对数据包进行过滤，具体的规则要求决定如何处理某一个包，包含(INPUT FORWARD OUTPUT )
>
> ​	*nat:* 用于网络地址转换，使用待补充,包含(PREROUTING POSTROUTING OUTPUT)
>
> ​	*magle:*为数据包设置标记，包含五链(PREROUTING INPUT FORWARD OUTPUT POSTROUTING)
>
> ​	*raw:* 确定是否对该数据包进行状态跟踪,包含(PREROUTING OUTPUT)
>
> **五链:**
>
> ​	*PREROUTING:*
>
> ​		预路由链，数据包到达路由前，在此链中，数据包的目的地址可能会被修改，NAT
>
> ​	*POSTROUTING:* 
>
> ​		路由后链，当数据包离开路由后，会通过 POSTROUTING 链，在此链中，数据包的源地址可能会被修改，NAT
>
> ​	*INPUT:* 
>
> ​		输入链，数据包进入网络堆栈后，首先通过 INPUT 链。如果数据包是目的地址是本地系统的，就会在此链中进行处理，输		入链中的规则决定了是否接受、拒绝或进一步处理数据包
>
> ​	*FORWARD:* 
>
> ​		转发链，当数据包经过本地系统但不是目的地时，其将被转发到另一台主机，会通过 FORWARD 链，用于控制通过本地系		统的数据包是否转发到其他主机
>
> ​	*OUTPUT:*
>
> ​		输出链，当数据包从本地系统发出时，它首先经过 OUTPUT 链。此链中，规则用于控制本地系统生成的数据包的处理方式
>
> **数据包匹配流程:**
>
> ​	*规则表顺序:*
>
> ​		*raw=>mangle=>nat=>filter*
>
> ​	*规则链顺序:*
>
> ​		*入站：PREROUTING=>INPUT*
>
> ​		*出站：OUTPUT=>POSTROUTING*
>
> ​		*转发：PREROUTING=>FORWARD=>POSTROUTING*
>
> 
>
> ​		

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

# <a id="database">Database</a>

## <a id="mysql">mysql</a>

### 数据类型

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

### 条件运算符

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

### 聚合函数

| 函数  | 功能     |
| ----- | -------- |
| count | 统计数量 |
| max   | 最大值   |
| min   | 最小值   |
| avg   | 平均值   |
| sum   | 求和     |

### DDL语句（数据定义语言）

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

### DML语句（数据操作语言）

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

### DQL语句（数据查询语言）

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

### DCL（数据控制语言）

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

### 函数

#### 字符串函数

| 函数                     | 功能                                                      |
| ------------------------ | --------------------------------------------------------- |
| concat(s1,s2,s3,...)     | 自负床链接，将s1，s2，s3拼接成一个字符串                  |
| lower(str)               | 将字符串全部转为小写                                      |
| upper(str)               | 将字符串转换为大写                                        |
| lpad(str,n,pad)          | 左填充，用字符串pad对str的左边进行填充，达到n个字符长度   |
| rpad(str,n,pad)          | 右填充，用字符串pad对str的右边进行填充，达到n个字符串长度 |
| trim(str)                | 去掉字符串头和尾部的空格                                  |
| substring(str,start,len) | 返回字符串str从start位置起的len个长度的字符串             |

#### 数值函数

| 函数       | 功能                               |
| ---------- | ---------------------------------- |
| ceil(x)    | 向上取整                           |
| floor(x)   | 向下取整                           |
| mod(x,y)   | 返回x/y的模                        |
| rand()     | 返回0~1内的随机数                  |
| round(x,y) | 求参数x的四舍五入的值，保留y位小数 |

#### 日期函数

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

#### 流程函数

| 函数                                                      | 功能                                                     |
| :-------------------------------------------------------- | :------------------------------------------------------- |
| if(value,t,f)                                             | 如果value为true，则返回t，否则返回f                      |
| ifnull(value1,value2)                                     | 如果value不为空，返回value1，否则返回value2              |
| case when [val1] then [res1] ...else [default] end        | 如果value为true，返回res1，...否则返回default默认值      |
| case [expr] when [val1] then [res1] ...else [default] end | 如果expr的值等于val1，返回res1，...否则返回default默认值 |

### 约束

| 约束     | 关键字      |
| -------- | ----------- |
| 非空约束 | NOT NULL    |
| 唯一约束 | UNIQUE      |
| 主键约束 | PRIMARY KEY |
| 默认约束 | DEFAULT     |
| 检查约束 | CHECK       |
| 外键约束 | FOREIGN KEY |

***Ps:作用于字段，为字段添加约束***

#### 示例

```mysql
create table employ(
    id int primary key auto_increment comment 'primary key' 
    name varchar(10) not null unique comment 'name',
    age int check ( age>0&&age<=120 ),
    status char(1) default 1,
    gender char(1)
)comment 'employ table';
```

#### 外键的添加，删除

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

### 多表查询

#### 多表关系

##### 一对一

***在一方加入外键同时设置为unique***

##### 一对多，多对一

***在多的一方设置外键关联另一方的主键***

##### 多对多

***建立中间的表，中间表包含两个外键，关联两张表的主键***

***笛卡尔积：A，B集合的所有组合情况***

***多表查询需要消除无效的笛卡尔积***

```mysql
select * from a,b where a.id = b.id;
```

#### 内连接

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

#### 外连接

***左外连接：查询左表和交集***

```mysql
select * from a left outer join b on a.id = b.id;
```

***右外连接：右表和交集***

```mysql
select * from a right outer join b on a.id = b.id;
```

***Ps:outer可以省略***

#### 自连接

```mysql
select * from U u,dept d where u.id = d.id;
```

### 联合查询

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



### 事务

***一组操作的集合，要么同时成功，要么同时失败***

#### 事务操作

##### 查看/设置事务的提交方式

```mysql
select @@autocommit;
#1为自动提交，0为手动提交
set @@autocommit=0;
```

##### 提交事务

```mysql
commit；
```

##### 回滚事务

```mysql
rollback;
#在报错时需要使用rollback进行数据回滚
```

##### 开启事务

```mysql
start transaction；
#或
begin;
```

##### 四大特性

***A原子性：不可分割***

***C一致性：事务完成需要保证数据是一致状态***

***I隔离性：保证各个事务是独立环境运行***

***D持久性：事务一旦提交，对数据的改变是永久的***

##### 并发事务问题

***脏读：读取到另一个事务未提交的数据***

***不可重复读：对一条记录进行两次读取，但两次读取数据不同***

***幻读：查询数据时未查询到，但在插入时又发现该数据已存在***

##### 事务的隔离级别

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



# <a id="go">Go</a>

## <a id="baseGrammer-go">BaseCrammer</a>

### 变量

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

### 数据类型

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

### 包的使用

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





# <a id="c++">C++</a>

## <a id="baseGrammer-c++">BaseGrammer</a>

### C++11

#### 值的类别

> ***左值：***
>
> ​	  能够用&取地址的表达式是左值表达式。
>
> ​	举例
>
> 		函数名和变量名（实际上是函数指针和具名变量，具名变量如std::cin
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
> 	1）返回右值引用的函数的调用表达式
> 	  2）转换为右值引用的转换函数的调用表达式
>
> 会问：这与“将亡”有什么关系？
> 在C++11中，我们用左值去初始化一个对象或为一个已有对象赋值时，会调用拷贝构造函数或拷贝赋值运算符来拷贝资源（所谓资源，就是指new出来的东西），而当我们用一个右值（包括纯右值和将亡值）来初始化或赋值时，会调用移动构造函数或移动赋值运算符⑤来移动资源，从而避免拷贝，提高效率（关于这些知识，在后续文章讲移动语义时，会详细介绍）。当该右值完成初始化或赋值的任务时，它的资源已经移动给了被初始化者或被赋值者，同时该右值也将会马上被销毁（析构）。也就是说，当一个右值准备完成初始化或赋值任务时，它已经“将亡”了。而上面1）和2）两种表达式的结果都是不具名的右值引用，它们属于右值（关于“不具名的右值引用是右值”这一点，后面还会详细解释）。又因为
> 	 1）这种右值是与C++11新生事物——“右值引用”相关的“新右值”
> 	  2）这种右值常用来完成移动构造或移动赋值的特殊任务，扮演着“将亡”的角色
>  所以C++11给这类右值起了一个新的名字——将亡值。
>
> 关于“三值”：
>
> 1）字符串字面值是左值。
>
> 不是所有的字面值都是纯右值，字符串字面值是唯一例外。
> 早期C++将字符串字面值实现为char型数组，实实在在地为每个字符都分配了空间并且允许程序员对其进行操作，所以类似
>
> ```c++
> cout<<&("abc")<<endl;
> char *p_char="abc";//注意不是char *p_char=&("abc");
> ```
>
> 这样的代码都是可以编译通过的。
>  注意上面代码中的注释，"abc"可以直接初始化指针p_char，p_char的值为字符串"abc"的首字符a的地址。而&("abc")被编译器编译为const的指向数组的指针const char (*) [4]（之所以是4，是因为编译器会在"abc"后自动加上一个'\0'），它不能初始化char *类型，即使是const  char *也不行。另外，对于char  *p_char="abc";，在GCC编译器上,GCC4.9(C++14)及以前的版本会给出警告，在GCC5.3(C++14)及以后的版本则直接报错：ISO C++ forbids converting a string constant to 'char*'（ISO  C++禁止string常量向char*转换）。但这并不影响“字符串字面值是左值”这一结论的正确性，因为cout<<&("abc")<<endl;一句在各个版本的编译器上都能编译通过，没有警告和错误。
>
> ​    2)具名的右值引用是左值，不具名的右值引用是右值。
>
> 见下例（例一）
>
> ```c++
> void foo(X&& x)
> {
>  X anotherX = x;
> //后面还可以访问x
> }
> ```
>
> 上面X是自定义类，并且，其有一个指针成员p指向了在堆中分配的内存；参数x是X的右值引用。如果将x视为右值，那么，X  anotherX=x;一句将调用X类的移动构造函数，而我们知道，这个移动构造函数的主要工作就是将x的p指针的值赋给anotherX的p指针，然后将x的p指针置为nullptr。（后续文章讲移动构造函数时会详细说明）。而在后面，我们还可以访问x，也就是可以访问x.p，而此时x.p已经变成了nullptr，这就可能发生意想不到的错误。 
>
> 又如下例（例二）
>
> ```c++
> X& foo(X&& x)
> {
>   //对x进行一些操作
>   return x;
> }
> 
> //调用
> foo(get_a_X());//get_a_X()是返回类X的右值引用的函数
> ```
>
> 上例中，foo的调用以右值（确切说是将亡值）get_a_X()为实参，调用类X的移动构造函数构造出形参x，然后在函数体内对x进行一些操作，最后return  X，这样的代码很常见，也很符合我们的编写思路。注意foo函数的返回类型定义为X的引用，如果x为右值，那么，一个右值是不能绑定到左值引用上去的。 
> 为避免这种情况的出现，C++规定：具名的右值引用是左值。这样一来，例一中X anotherX = x;一句将调用X的拷贝构造函数，执行后x不发生变化，继续访问x不会出问题；例二中，return x也将得到允许。
>   例二中，get_a_X返回一个不具名右值引用，这个不具名右值引用的唯一作用就是初始化形参x，在后面的代码中，我们不会也无法访问这个不具名的右值引用。C++将其归为右值，是合理的，一方面，可以使用移动构造函数，提高效率；另一方面，这样做不会出问题。

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

### c++20

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

## <a id="compiler-c++">Compiler</a>

### gcc/g++

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

### 预编译指令

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

## <a id="build-c++">Build</a>

### Cmake(跨平台构建工具)

***跨平台自动生成makefile,不需要手动编写makefile***

#### BaseGrammer

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

# <a id="cloud">Cloud</a>

## <a id="docker">Docker</a>

***介绍：Docker 是一个开源平台，支持开发人员构建、部署、运行、更新和管理*容器*，这些容器是标准化的可执行组件，结合了应用源代码以及在任何环境中运行该代码所需的操作系统 (OS) 库和依赖项。***

### BaseGrammer

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



## <a id="minikube">Minikube</a>

***desc:适用于学习以及开发环境的小型kubernet集群***

**启动minikube**

```shell
minikube start --driver=docker --container-runtime=docker
#配置驱动以及容器运行时环境
```

**基本概念**

> **Node:**对于minikube来说Node只有自己,但其实对于一个kubernetes来说会有主节点(master) 工作节点(work) 
>
> **service:** service控制了容器内部网络以及集群与外部的网络结构
>
> **ingress:**作为路由对**Node**的网络进行路由
>
> **deployment:**自动对多个pod的生命进行弹性伸缩控制,拥有滚动更新的特性
>
> **pod:**pod中的多个容器共享一个ip与端口空间
>
> **container:**docker中的基本容器概念

**代理问题：**

> **问题场景：**
>
> 在minikube启动时提醒忽略代理同时在deployment拉取镜像时失败,配置docker的systemd 的http-proxy.conf设置docker的代理
>
> ```shell
>  #新建如下文件并新增如下条目
>  cat /etc/systemd/system/docker.service.d/http-proxy.conf
> [Service]
> Environment="HTTP_PROXY=http://127.0.0.1:7897"
> Environment="HTTPS_PROXY=http://127.0.0.1:7897"
> ```
>
> **手动拉取镜像并Load进minikube**
>
> ```shell
> docker pull <image-name>
> minikube image load <image-name>
> ```
>
> *ps:所以其实对于deployment的代理问题并没有得到解决,只是手动下载并添加*
>
> 😭

## <a id="kubectl">Kubectl</a>

***desc:kubenetes的控制工具***

### BaseGrammer

#### concept

> **action:**get | delete | describe |exec 
>
> **workLoad:**pod | deployment | service | endpoint  | context | namespaces

#### deployment

> **prober:**探针概念
>
> **label:**标签概念(标识键值对)
>
> **selector:**选择器(依据条件选择满足条件的标签)

#### service

> 控制集群内部或集群内外的网络连接

#### ingress

> 对进入节点的网络进行路由

# <a id="toolbox">Toolbox</a>

## <a id="git">Git</a>

### BaseGrammer

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

**变基rebase**

```shell
git rebase  -i <commit-id> 
# 即对某次commit后的所有commit进行操作
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

分支管理

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

### Git多人协作

多人协作在同一个分支上进行开发的工作模式：

1. 首先，可以试图用`git push origin <branch-name>`推送自己的修改；
2. 如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
3. 如果合并有冲突，则解决冲突，并在本地提交；
4. 没有冲突或者解决掉冲突后，再用`git push origin <branch-name>`推送就能成功！
5. 如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`。

### git回滚

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

HEAD

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

### commit type

> **feat**: 增加新功能（feature）。
>
> - 示例: `feat: add user login functionality`
>
> **fix**: 修复错误（bug fix）。
>
> - 示例: `fix: correct the typo in the user login page`
>
> **docs**: 仅仅修改文档（documentation）。
>
> - 示例: `docs: update API documentation`
>
> **style**: 代码格式（空格、分号等），不影响代码逻辑。
>
> - 示例: `style: reformat the code in user.js`
>
> **refactor**: 代码重构，既不是新增功能，也不是修复 bug。
>
> - 示例: `refactor: optimize the user authentication module`
>
> **perf**: 提升性能的代码更改（performance improvement）。
>
> - 示例: `perf: improve the query performance in user module`
>
> **test**: 添加测试或修改测试代码。
>
> - 示例: `test: add unit tests for the login function`
>
> **chore**: 杂项任务，不涉及代码更改的功能或修复。
>
> - 示例: `chore: update the dependencies`
>
> **build**: 影响构建系统或外部依赖的更改（例如：webpack、npm）。
>
> - 示例: `build: update the webpack configuration`
>
> **ci**: 持续集成相关的更改（例如：Travis, Circle, GitLab CI）。
>
> - 示例: `ci: add CI configuration for GitHub Actions`
>
> **revert**: 回退先前的提交。
>
> - 示例: `revert: revert commit abc123`
>
> **merge**: 合并分支。
>
> - 示例: `merge: merge branch 'feature-xyz' into 'main'`

## <a id="make">Make</a>

***make：利用makefile进行自动化目标生成***

## <a id="gdb">GDB</a>

***描述：开源命令行调试器(GNU debugger)***

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

# <a id="awesomeLanguage">Awesome-Language</a>

## <a id="python">Python</a>

### BaseGrammer

##### 列表，元组，集合，字典

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

文件操作

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

##### 类，对象，成员方法，构造方法，封装，继承，多态

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

变量注解，函数参数注解

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

### 利用爬虫建立IP池

#### 具体流程

***获取网站链接->伪造访问的消息头(检查网站的网络,获取伪造的请求头)->获取网站源代码—>提取IP信息结构特点->利用正则表达式筛选IP端口信息->利用字符串截取将信息整合到列表中再将列表信息变为字典存储->对字典数据进行可用性测试***

#### IP爬虫代码示例

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

#### shell数据二次处理脚本

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

### OpenCv库

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

​    print(h_min, h_max, s_min, s_max, v_min, v_max)

​    lower = np.array([h_min, s_min, v_min])
​    upper = np.array([h_max, s_max, v_max])
​    mask = cv2.inRange(puke_HSV, lower, upper)
​    img_result = cv2.bitwise_or(puke, puke, mask=mask)

​    cv2.imshow("puke source", puke)
​    cv2.imshow("HSV puke", puke_HSV)
​    cv2.imshow("mask", mask)
​    cv2.imshow("result puke ", img_result)
​    cv2.waitKey(1)
```

# <a id="ancientScience">古代科学</a>

## <a id="zhouyi">周易</a>

### 序卦传

#### 64卦

***乾为天,坤为地,水雷屯,山水蒙,水天需,天水讼,地水师,水地比,风天小蓄,天泽履,地天泰,天地否,天火同人,火天大有,地山谦,雷地豫,泽雷随,山风蛊,地泽临,风地观,火雷噬嗑,山火贲,山地剥,地雷复,天雷无妄,山天大蓄,山雷颐,泽风大过,坎为水,离为火***

***泽山咸,雷风恒,天山遁,雷天大壮,火地晋,地火明夷,风火家人,火泽睽,水山蹇,雷水解,山泽损,风雷益,泽天夬,天风姤,泽地萃,地风生,泽水困,水风井,泽火革,火风鼎,震为雷,艮为山,风山渐,雷泽归妹,雷火丰,火山旅,巽为风,兑为泽,风水涣,水泽节,风泽中孚,雷山小过,水火既济,火水未济***

## <a id="qimendunjia">奇门遁甲</a>

### 烟波钓叟赋

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

#### 基础

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

#### 三奇六仪

> ***奇:乙,丙,丁***
>
> ***门:休、死、伤、杜、开、惊、生、景***
>
> ***甲:主帅***

-----------------------------------------------------------------------------------------

#### 八门,九星,洛书,干支,九宫,八神

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

#### 阴阳遁

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

#### **超接置闰法**

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

#### **八门应诀**

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

### 吉凶格

#### 常用吉格

(***待补充***)

#### 常用凶格

(***待补充***)











