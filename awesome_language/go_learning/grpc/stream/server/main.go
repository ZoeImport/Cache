package main

import (
	"context"
	"fmt"
	pb "gogrpc/stream/proto"
	"google.golang.org/grpc"
	"log"
	"net"
	"sync"
	"time"
)

type server struct {
	pb.UnimplementedGreeterServer
}

// GetStream server send a stream to client [Get]
func (s *server) GetStream(req *pb.StreamReq, stream grpc.ServerStreamingServer[pb.StreamResp]) error {
	var i uint = 10
	for {
		_ = stream.Send(&pb.StreamResp{
			Data: fmt.Sprintf("%v", time.Now().Unix()),
		})
		i++
		time.Sleep(time.Second)
		if i > 20 {
			break
		}
	}
	return nil
}

// PutStream client send a stream to server [Put]
func (s *server) PutStream(stream grpc.ClientStreamingServer[pb.StreamReq, pb.StreamResp]) error {
	for {
		if msg, err := stream.Recv(); err != nil {
			log.Fatalf("put stream recv error :%v", err)
		} else {
			fmt.Printf("data: %v \n", msg.Data)
		}
	}
	return nil
}

// AllStream client and server send or receive each other
func (s *server) AllStream(stream grpc.BidiStreamingServer[pb.StreamReq, pb.StreamResp]) error {
	waitGroup := sync.WaitGroup{}
	waitGroup.Add(2)
	// close context
	ctx, cancelFunc := context.WithCancel(context.Background())

	//server recv goroutine
	go func() {
		defer waitGroup.Done()
		for {
			select {
			case <-ctx.Done():
				return
			default:
				if recvMsg, err := stream.Recv(); err != nil {
					log.Fatalf("all stream server recv error: %v, mgs: %v", err, recvMsg)
				} else {
					fmt.Printf("server recv: %v \n", recvMsg)
				}
			}
		}
	}()
	//server send goroutine
	go func() {
		defer waitGroup.Done()
		var i uint = 0
		for {
			select {
			case <-ctx.Done():
				return
			default:
				if err := stream.Send(&pb.StreamResp{
					Data: fmt.Sprintf("server send : %v", time.Now().Unix()),
				}); err != nil {
					log.Fatalf("all stream server send error :%v", err)
				}
				time.Sleep(time.Second)
				i++
				if i > 5 {
					cancelFunc()
					return
				}
			}
		}
	}()
	waitGroup.Wait()
	return nil
}
func main() {
	conn, err := net.Listen("tcp", "127.0.0.1:9091")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	grpcServer := grpc.NewServer()
	pb.RegisterGreeterServer(grpcServer, &server{})

	err = grpcServer.Serve(conn)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
