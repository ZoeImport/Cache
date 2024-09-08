package go_answer

import (
	"fmt"
	"os"
	"testing"
)

func TestMain(t *testing.M) {
	fmt.Println("[Test====Main]")
	os.Exit(t.Run())

}

func TestEcho(t *testing.T) {
	fmt.Println("echo")
}

func TestMaxScore(t *testing.T) {
	score := MaxScore("011101")
	//str := "0123"
	fmt.Println(score)

}
