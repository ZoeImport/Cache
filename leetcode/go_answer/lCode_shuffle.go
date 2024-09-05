package go_answer

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
