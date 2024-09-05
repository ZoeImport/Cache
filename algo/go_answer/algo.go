package go_answer

import (
	"math"
	"strconv"
	"strings"
	"unicode"
)

// addDigits
func addDigits(num int) int {
	for num >= 10 {
		sum := 0
		for num > 0 {
			// get units
			sum += num % 10
			// get tens
			num /= 10
		}
		num = sum
	}
	return num
}

func addDigits2(num int) int {
	if num == 0 {
		return 0
	} else if num%9 == 0 {
		return 9
	} else {
		return num % 9
	}
}

// clearDigits
func clearDigits(s string) string {
	var res []byte
	for _, b := range s {
		if unicode.IsDigit(b) {
			res = res[:len(res)-1]
		} else {
			res = append(res, byte(b))
		}
	}

	return string(res)
}

// countGoodTriplets
func countGoodTriplets(arr []int, a int, b int, c int) int {
	length := len(arr)
	ans := 0
	for i := 0; i < length; i++ {
		for j := i + 1; j < length; j++ {
			for k := j + 1; k < length; k++ {
				if math.Abs(float64(arr[i]-arr[j])) <= float64(a) && math.Abs(float64(arr[j]-arr[k])) <= float64(b) && math.Abs(float64(arr[i]-arr[k])) <= float64(c) {
					ans++
				}
			}

		}
	}
	return ans
}

var valueSymbols = []struct {
	value  int
	symbol string
}{
	{1000, "M"},
	{900, "CM"},
	{500, "D"},
	{400, "CD"},
	{100, "C"},
	{90, "XC"},
	{50, "L"},
	{40, "XL"},
	{10, "X"},
	{9, "IX"},
	{5, "V"},
	{4, "IV"},
	{1, "I"},
}

func IntToRoman(num int) string {
	var ans []byte
	for _, v := range valueSymbols {
		for num >= v.value {
			num -= v.value
			ans = append(ans, v.symbol...)
		}
		if num == 0 {
			break
		}
	}
	return string(ans)
}

func IsPalindromeNumber(num int) bool {
	if num < 0 {
		return false
	}
	if num/10 == 0 {
		return true
	}
	strNum := strconv.Itoa(num)
	strLen := len(strNum)
	head := 0
	tail := strLen - 1
	for i := 0; i < strLen; i++ {
		if strNum[head] != strNum[tail] {
			return false
		}
		head++
		tail--
	}
	return true
}

func IsPalindromeNumberMoreQuick(num int) bool {
	cp := num
	reverseNum := 0
	for cp > 0 {
		temp := cp % 10
		reverseNum = reverseNum*10 + temp
		cp = cp / 10
	}
	return reverseNum == num
}

func isPowerOfFour(n int) bool {
	return n > 0 && (n&(n-1)) == 0 && n%3 == 1
}

func isPowerOfThree(n int) bool {
	for n > 0 && (n%3 == 0) {
		n /= 3
	}
	return n == 1
}

func isPowerOfTwo(n int) bool {
	return n > 0 && (n&(n-1)) == 0
}

func isUgly(n int) bool {
	if n == 1 {
		return true
	}
	if n < 1 {
		return false
	}
	ugly := []int{2, 3, 5}
	for _, u := range ugly {
		for n%u == 0 {
			n /= u
		}
	}
	return n == 1
}

func isUgly2(n int) bool {

	if n < 1 {
		return false
	}
	for n > 1 {
		if n%2 == 0 {
			n = n / 2
		} else if n%3 == 0 {
			n = n / 3
		} else if n%5 == 0 {
			n = n / 5
		} else {
			return false
		}
	}

	return true

}

// MyAtoi .
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
			ans = ans*10 + int(withoutSpace[currentBit]-'0')
			currentBit++
		}

	}
	if withoutSpace[0] == '-' {
		ans *= -1
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

func shuffle(nums []int, n int) []int {
	x := 0
	y := n
	ans := make([]int, 0, 2*n)

	for x < n {
		ans = append(ans, nums[x], nums[y])
		x++
		y++
	}
	return ans
}

// SubtractProductAndSum .
func SubtractProductAndSum(n int) int {
	product := 1
	sum := 0
	for n > 0 {
		sum += n % 10
		product *= n % 10
		n /= 10
	}

	return product - sum
}

func toLowerCase(s string) string {
	return strings.ToLower(s)
}
