# this script for deploy for clash-metacubexd [docker compose]
# author: zoe
import os
import subprocess as sp
import sys
import logging as log

# log = log.getLogger(__name__)



docker_version_cmd=["docker-compose","--version"]

release_dir="/etc/os-release"

docker_keyring_gpg_url="https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg"
docker_deb_url="https://mirrors.aliyun.com/docker-ce/linux/ubuntu"
docker_compose_mirror_url="https://gitee.com/smilezgy/compose/releases/download/v2.20.2/docker-compose-linux-x86_64"

install_str=rf"""
curl -fsSL {docker_keyring_gpg_url} | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
sudo apt update  && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] {docker_deb_url} $(lsb_release -cs) stable"| sudo tee /etc/apt/sources.list.d/docker.list > /dev/null1  && \
sudo apt update  && \
sudo apt install ca-certificates curl gnupg lsb-release -y  && \
sudo apt install docker-ce docker-ce-cli containerd.io -y  && \
sudo systemctl enable docker.service --now  && \
sudo curl -SL {docker_compose_mirror_url}  -o /usr/local/bin/docker-compose  && \
chmod +x /usr/local/bin/docker-compose
"""

prompt=\
r"""
==========================================================
=make sure u have a valid clash config then press y [y/n]=
=========================================================="""

docker_compose_yaml="clash-metacubexd-compose.yml"

def uninstall_docker():
    if input("uninstall docker and its keyring? [y/n]").strip().lower()!="y":
        log.warning("stopped to remove older docker and service")
        return 0
    installed_docker_process=sp.Popen(["apt","list","--installed"],
                                      stdout=sp.PIPE,
                                      stderr=sp.PIPE,
                                      text=True)
    stdout_proc, stderr_proc = installed_docker_process.communicate()
    if installed_docker_process.returncode!=0:
        log.error(f"list docker pkgs failed :{stderr_proc}")
        sys.exit(121)

    grep_process=sp.Popen(["grep","docker"],
                          stdin=sp.PIPE,
                          stdout=sp.PIPE,
                          stderr=sp.PIPE,
                          text=True)
    stdout_proc, stderr_proc=grep_process.communicate(input=stdout_proc)
    if grep_process.returncode not in (0,1):
        log.error(f"grep docker pkgs failed {stderr_proc}")
        sys.exit(120)

    pkg_list=[
        line.split("/")[0].strip()
        for line in stdout_proc.splitlines()
        if line.strip()
    ]

    if not pkg_list:
        log.info("No Docker packages found")
        return 0
    else:
        print(f"All docker packages found: {pkg_list},they will be removed")
    remove_pkg_process=sp.Popen(["apt","purge","-y"]+pkg_list,
                                stdout=sys.stdout,
                                stderr=sp.PIPE,
                                text=True)
    stdout_proc, stderr_proc = remove_pkg_process.communicate()
    if remove_pkg_process.returncode!=0:
        log.error(f"Failed to remove packages: {stderr_proc}")
        sys.exit(119)
    log.info(f"Removed packages:\n{stdout_proc}")

    sp.run([ "rm", "-rf", "/var/lib/docker", "/etc/docker","/usr/local/bin/docker-compose"], check=False)
    sp.run([ "systemctl", "disable", "docker.service"], check=False)
    return 0

def deploy_clashmetacubexd():
    # print(prompt)
    begin_sig=input(prompt)
    if begin_sig.strip().lower()=="y":
        deploy_subprocess=os.system(rf"docker-compose -f {docker_compose_yaml} up -d")
        if deploy_subprocess!=0:
            log.error("Failed to deploy clashmetacubexd")
            sys.exit(125)
        else:
            print("Successfully deploy metecubexd service")
    return 0


# check install pkg
def installed_pkgs_check(release_name,pkgs):
    if release_name == "ubuntu":
        check_process_p1=sp.Popen(["apt","list","--installed"],stdout=sp.PIPE,stderr=sp.PIPE)
        check_process_p2=sp.Popen(["grep",pkgs],stdin=check_process_p1.stdout,stdout=sp.PIPE,stderr=sp.PIPE)
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
                    return line.strip().split('=')[1].lower()
    except FileNotFoundError as e:
        log.error("No release file found: %s",e)

def install_docker(release_version):
    if release_version == "ubuntu":
        os.system(install_str)
        test_process=sp.run(docker_version_cmd)
        if test_process.check_returncode():
            log.error(test_process.stderr)
            log.error(test_process.stdout)
            log.error(test_process.returncode)
            return 118
        return 0
    else:
        log.error("Unknown release version: %s",release_version)

def main():
    # test_process=sp.run(docker_version_cmd)
    # if test_process.check_returncode():
    #     log.error(test_process.stderr)
    #     log.error(test_process.stdout)
    #     log.error(test_process.returncode)
    #     return 118



    try:
        uninstall_docker()
        # print(install_str)
        # docker env check
        # completed_process = sp.run(docker_version_cmd, capture_output=True, text=True)
        # check if error
        if not installed_pkgs_check("ubuntu","docker"):
            # do not continue
            if input("docker compose doesn't find,continue install[y/n]:").lower() != "y":
                sys.exit(127)
            # continue
            else:
                if not install_docker(get_release()):
                    deploy_clashmetacubexd()
                else:
                    log.error("Failed to install docker")
                    sys.exit(126)
        else:
            print("detect docker-compose")
            deploy_clashmetacubexd()


    except FileNotFoundError as e:
        log.error(e)
        sys.exit(124)

    except sp.CalledProcessError as e:
        log.error(docker_version_cmd.__str__()+" command not found,errcode=%d",e.returncode)
        sys.exit(123)


if __name__ == '__main__':
    main()

