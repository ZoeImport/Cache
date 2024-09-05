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
