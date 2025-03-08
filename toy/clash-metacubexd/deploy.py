# this script for deploy for clash-metacubexd [docker compose]
# author: zoe
import os
import subprocess as sp
import sys
import logging as log


docker_version_cmd=["docker","compose","--version"]

release_dir="/etc/os-release"

docker_keyring_gpg_url="https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg"
docker_deb_url="https://mirrors.aliyun.com/docker-ce/linux/ubuntu"
docker_compose_mirror_url="https://gitee.com/smilezgy/compose/releases/download/v2.20.2/docker-compose-linux-x86_64"

# check install pkg
def installed_pkgs_check(release_name,pkgs):
    if release_name == "ubuntu":
        check_process_p1=sp.Popen(["apt","list","--installed"],stdout=sp.PIPE,stderr=sp.PIPE)
        check_process_p2=sp.Popen(["grep",[pkgs]],stdin=check_process_p1.stdout,stdout=sp.PIPE,stderr=sp.PIPE)
        check_process_p1.stdout.close()
        output=check_process_p2.stdout.read().decode("utf-8")
        if len(output)!=0:
            return True
        else:
            return False


# get system release
def get_release():
    try:
        with open(release_dir,'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("ID="):
                    return line.strip().split()[1].lower()
    except FileNotFoundError as e:
        log.error("No release file found: %v",)

def install_docker(release_version):
    if release_version == "ubuntu":
        os.system(
rf"""
curl -fsSL ${docker_keyring_gpg_url} | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg;
sudo apt update;
echo deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] ${docker_deb_url} $(lsb_release -cs) stable"| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null1 ;
sudo apt update;
sudo apt install ca-certificates curl gnupg lsb-release -y;
sudo apt install docker-ce docker-ce-cli containerd.io -y;
sudo systemctl enable docker.service --now;
sudo curl -SL ${docker_compose_mirror_url}  -o /usr/local/bin/docker-compose ;
chmod +x /usr/local/bin/docker-compose;
""")
        test_process=sp.run(docker_version_cmd)
        if test_process.check_returncode():
            log.error(test_process.stderr)
            sys.exit(test_process.returncode)
    else:
        log.error("Unknown release version: %s",release_version)

def main():

    # docker env check
    try:
        # completed_process = sp.run(docker_version_cmd, capture_output=True, text=True)

        # check if error
        if installed_pkgs_check("ubuntu","docker"):
            judge_continue = input("docker compose doesn't find,continue install[y/n]:")

            # do not continue
            if judge_continue.lower() != "y":
                sys.exit(127)

            # continue
            else:
                install_docker(get_release())


    except FileNotFoundError as e:
        log.error(e)
        sys.exit(e.errno)

    except sp.CalledProcessError as e:
        log.error(docker_version_cmd.__str__()+" command not found,errcode=%d",e.returncode)
        sys.exit(e.returncode)


if __name__ == '__main__':
    main()

