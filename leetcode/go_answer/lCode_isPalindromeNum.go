package go_answer

import (
	"strconv"
)

func IsPalindromeNumber(num int) bool {
	if num < 0 {
		return false
	}
	if num/10 == 0 {
		return true
	}
	str_num := strconv.Itoa(num)
	str_len := len(str_num)
	head := 0
	tail := str_len - 1
	for i := 0; i < str_len; i++ {
		if str_num[head] != str_num[tail] {
			return false
		}
		head++
		tail--
	}
	return true
}

func IsPalindromeNumberMoreQuick(num int) bool {
	cp := num
	reverse_num := 0
	for cp > 0 {
		temp := cp % 10
		reverse_num = reverse_num*10 + temp
		cp = cp / 10
	}
	return reverse_num == num
}
