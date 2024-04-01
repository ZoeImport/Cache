#include <arpa/inet.h>
#include <asm-generic/errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (fd == -1) {
    perror("socket");
    return -1;
  }
  sockaddr_in saddr;
  saddr.sin_family = AF_INET;
  saddr.sin_port = htons(9999);
  saddr.sin_addr.s_addr = INADDR_ANY;
  auto ret = bind(fd, (struct sockaddr *)&saddr, sizeof(saddr));
  if (ret == -1) {
    perror("bind");
    return -1;
  }
  ret = listen(fd, 20);
  if (ret == -1) {
    perror("listen");
    return -1;
  }
  struct sockaddr_in caddr;
  socklen_t addrlen = sizeof(caddr);
  int cfd = accept(fd, (struct sockaddr *)&caddr, &addrlen);
  if (cfd == -1) {
    perror("accept");
    return -1;
  }
  char ip[32];
  printf("client ip: %s,port: %d\n",
         inet_ntop(AF_INET, &caddr.sin_addr.s_addr, ip, sizeof(ip)),
         ntohs(caddr.sin_port));
  while (1) {
    char buffer[1024];
    int len = recv(cfd, buffer, sizeof(buffer), 0);
    if (len) {
      printf("client say: %s\n", buffer);
      send(cfd, buffer, sizeof(buffer), 0);
    } else if (len == 0) {
      printf("client close ... \n ");
      break;
    } else {
      perror("recv");
      break;
    }
  }
  close(fd);
  close(cfd);
}