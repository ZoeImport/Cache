FROM archlinux:latest
# ENV

# mirror env 
ENV mirrorlist=https://mirrors.ustc.edu.cn/archlinux/\$repo/os/\$arch
ENV archlinuxcn_mirrior=https://mirrors.ustc.edu.cn/archlinuxcn/\$arch
#sign keyring
ENV signkey=farseerfc@archlinux.org
ENV temp_user_name=noone
ENV temp_user_password=noone

WORKDIR /home
#1st build  
RUN  echo "Server = ${mirrorlist}" >> /etc/pacman.d/mirrorlist  \
    && sed -i "84a\[archlinuxcn]\nServer = ${archlinuxcn_mirrior}" /etc/pacman.conf   \
    && pacman -Sy --noconfirm \
    && pacman-key --init   \
    && pacman-key --lsign-key "${signkey}"   \
    && pacman -S --noconfirm archlinuxcn-keyring   \
    && useradd ${temp_user_name} \
    && echo "${temp_user_name}:${temp_user_password}"\
    && echo "${temp_user_name} ALL=(ALL) NOPASSWD:ALL " >> /etc/sudoers   \
    && pacman -S --noconfirm binutils base-devel sudo cmake make  git  openssh \
    && pacman -S --noconfirm tree vim \
    && touch Readme \
    && echo -e "welcome arch dev image \n temp_user_name:${temp_user_name}\n temp_user_password:${temp_user_password}"> Readme 
