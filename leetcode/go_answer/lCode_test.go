package go_answer_test

import (
	"fmt"
	go_answer "leetcode_answer_go"
	"testing"
)

func TestPrintfndromeNumber(t *testing.T) {
	for i := 0; i < 100000000; i++ {
		_ = go_answer.IsPalindromeNumber(1000021)
	}
}

func TestPrintfndromeNumberQuick(t *testing.T) {
	fmt.Println(go_answer.IsPalindromeNumberMoreQuick(1000021))
}

func TestMyAtoi(t *testing.T) {
	// fmt.Println(go_answer.MyAtoi(" -1943kk"))
	// fmt.Println(go_answer.MyAtoi(" -1-943kk"))
	// fmt.Println(go_answer.MyAtoi("    +1943kk"))
	// fmt.Println(go_answer.MyAtoi("    +01943kk"))
	// fmt.Println(go_answer.MyAtoi(" sss1943kk"))
	// fmt.Println(go_answer.MyAtoi("   "))
	fmt.Println(go_answer.MyAtoi(" -91283472332aa"))
	fmt.Println(go_answer.MyAtoi("13c3ccc0d3"))
	fmt.Println(go_answer.MyAtoi(""))
	fmt.Println(go_answer.MyAtoiQuick(" -91283472332aa"))
	fmt.Println(go_answer.MyAtoiQuick("13c3ccc0d3"))
	fmt.Println(go_answer.MyAtoiQuick(""))
	fmt.Println(go_answer.MyAtoiQuick(" "))

}

func TestIntToRoman(t *testing.T) {
	fmt.Println(go_answer.IntToRoamn(3749))
}
