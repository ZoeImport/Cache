#include <arpa/inet.h>
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <netinet/in.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

int main() {
  int fd = socket(AF_INET, SOCK_STREAM, 0);
  if (!fd) {
    perror("socket");
    return -1;
  }
  struct sockaddr_in saddr;
  saddr.sin_family = AF_INET;
  inet_pton(AF_INET, "127.0.0.1", &saddr.sin_addr.s_addr);
  saddr.sin_port = ntohs(9999);
  int ret = connect(fd, (struct sockaddr *)&saddr, sizeof(saddr));
  if (ret==-1) {
    perror("ret");
    return -1;
  }
  while (1) {
    char buffer[1024];
    std::cin>>buffer;
    send(fd, buffer, strlen(buffer) + 1, 0);
    memset(buffer, 0, sizeof(buffer));
    int len = recv(fd, buffer, sizeof(buffer), 0);
    if (len) {
      printf("server say: %s\n", buffer);
    } else if (len == 0) {
      printf("server close ...");
      break;
    } else {
      perror("recv");
      break;
    }
    sleep(2);
  }
  close(fd);
}