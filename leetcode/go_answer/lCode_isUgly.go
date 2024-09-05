package go_answer

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
