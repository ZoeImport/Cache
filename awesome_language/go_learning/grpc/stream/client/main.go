package main

import (
	"context"
	"fmt"
	pb "gogrpc/stream/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"log"
	"sync"
	"time"
)

// serverStream .
func serverStream(conn *grpc.ClientConn) {
	client := pb.NewGreeterClient(conn)
	resp, err := client.GetStream(context.Background(), &pb.StreamReq{
		Data: "zoeImport",
	})
	if err != nil {
		log.Fatal("client send err:", err)
	}
	for {
		msg, err := resp.Recv()
		if err != nil {
			log.Fatal("client receive err:", err)
		}
		fmt.Printf("data:%v \n", msg.Data)
	}
}

// clientStream .
func clientStream(conn *grpc.ClientConn) {
	client := pb.NewGreeterClient(conn)

	stream, err := client.PutStream(context.Background())
	if err != nil {
		log.Fatal("client err:", err)
	}
	var i uint = 0
	for {
		if err := stream.Send(&pb.StreamReq{Data: fmt.Sprintf("the %dth data", i)}); err != nil {
			log.Fatalf("stream send err: %v", err)
			return
		}
		i++
		if i > 10 {
			break
		}
		time.Sleep(time.Second)

	}

}

func allStream(conn *grpc.ClientConn) {
	client := pb.NewGreeterClient(conn)
	ctx, cancelFunc := context.WithCancel(context.Background())
	stream, err := client.AllStream(ctx)
	if err != nil {
		log.Fatalf("all stream client err: %v", err)
	}
	waitGroup := sync.WaitGroup{}
	waitGroup.Add(2)

	//client send goroutine
	go func() {
		defer waitGroup.Done()
		var i uint = 0
		for {
			select {
			case <-ctx.Done():
				return
			default:
				if err := stream.Send(&pb.StreamReq{
					Data: fmt.Sprintf("client send : %v", time.Now().Unix()),
				}); err != nil {
					log.Fatalf("all stream client send err: %v", err)
				}
				i++
				time.Sleep(time.Second)
				if i > 5 {
					cancelFunc()
					return
				}
			}
		}
	}()
	//client recv goroutine
	go func() {
		defer waitGroup.Done()
		for {
			select {
			case <-ctx.Done():
				return
			default:
				if recvMsg, err := stream.Recv(); err != nil {
					log.Fatalf("all stream client recv err: %v, msg: %v", err, recvMsg)
				} else {
					fmt.Printf("client recv: %v \n", recvMsg)
				}
			}
		}
	}()
	waitGroup.Wait()
}

func main() {
	conn, err := grpc.NewClient("127.0.0.1:9091", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal("grpc conn err:", err)
		return
	}
	defer func(conn *grpc.ClientConn) {
		err := conn.Close()
		if err != nil {
			log.Fatal("grpc conn close err:", err)
		}
	}(conn)

	allStream(conn)

}
