package main

import (
	"context"
	"errors"
	"fmt"
	pb "gogrpc/hello/hello-server/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/metadata"
	"log"
	"net"
)

type server struct {
	pb.UnimplementedSayHiServer
}

func (s *server) SayHi(ctx context.Context, req *pb.HelloRequest) (*pb.HelloResponse, error) {
	incomingContext, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, errors.New("nil token")
	}

	var appid string
	if v, ok := incomingContext["appid"]; ok {
		appid = v[0]
	}
	if appid != "123" {
		return nil, errors.New("invalid appid")
	}

	return &pb.HelloResponse{ResponseName: "thank you " + req.RequestName}, nil
}

func main() {

	creds, err := credentials.NewServerTLSFromFile("/home/zoe/CodeSpace/QingShu/awesome_language/go_learning/grpc/key/test.pem", "/home/zoe/CodeSpace/QingShu/awesome_language/go_learning/grpc/key/test.key")

	if err != nil {
		log.Fatal("credentials failed", err)
	}

	listen, err := net.Listen("tcp", ":9090")
	if err != nil {
		panic(err)
	}
	// create server service
	grpcServer := grpc.NewServer(grpc.Creds(creds))
	// register service
	pb.RegisterSayHiServer(grpcServer, &server{})
	// start server
	err = grpcServer.Serve(listen)
	if err != nil {
		fmt.Printf("failed to serve: %v", err)
		panic(err)
	}
}
