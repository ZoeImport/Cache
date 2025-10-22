package tests

import (
	"fmt"
	"testing"
	"time"
)

const (
	MillSecondsTemplate = "2006-01-02 15:04:05.000"
)

func TestTime(t *testing.T) {
	lastT, err := time.ParseInLocation(MillSecondsTemplate, "2025-10-11 12:00:16.496", time.Local)
	if err != nil {
		t.Fatal(err)
	}

	now := time.Now()
	if now.Before(lastT) {
		fmt.Println("now before lastT:", now)
	}
	fmt.Println(now)
	fmt.Println(lastT)
}
