package go_answer

import "unicode"

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
