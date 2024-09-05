package go_answer

import "math"

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
