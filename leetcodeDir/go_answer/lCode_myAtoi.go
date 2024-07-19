package go_answer

import (
	"math"
	"strings"
	"unicode"
)

func MyAtoi(str string) (ans int) {
	length := len(str)
	if length == 0 {
		return 0
	}
	currentBit := 0
	ans = 0
	withoutSpace := strings.TrimLeft(str, " ")
	if withoutSpace[0] == '-' || withoutSpace[0] == '+' || unicode.IsDigit(rune(withoutSpace[0])) {

		if withoutSpace[0] == '+' || withoutSpace[0] == '-' {
			currentBit = 1
		}
		for (withoutSpace[currentBit] - '0') == 0 {
			currentBit++
		}
		for currentBit < length && unicode.IsDigit(rune(withoutSpace[currentBit])) {
			ans = ans*10 + int((withoutSpace[currentBit] - '0'))
			currentBit++
		}

	}
	if withoutSpace[0] == '-' {
		ans *= (-1)
	}
	if ans >= math.MaxInt32 {
		ans = math.MaxInt32
		return
	}
	if ans <= math.MinInt32 {
		ans = math.MinInt32
		return
	}
	return

}

func MyAtoiQuick(str string) int {
	ans, abs, sign, index, length := 0, 0, 1, 0, len(str)
	if length == 0 {
		return 0
	}
	for index < length && str[index] == ' ' {
		index++
	}
	if index == length {
		return ans
	}
	switch str[index] {
	case '+':
		index++
	case '-':
		sign = -1
		index++
	}
	for index < length && (str[index] >= '0' && str[index] <= '9') {
		abs = abs*10 + int(str[index]-'0')
		ans = sign * abs
		if ans <= math.MinInt32 {
			ans = math.MinInt32
			return ans
		} else if ans >= math.MaxInt32 {
			ans = math.MaxInt32
			return ans
		}
		index++
	}
	return ans
}
