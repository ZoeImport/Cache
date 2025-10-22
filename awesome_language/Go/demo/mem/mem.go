package main

// To returns a pointer to the given value.
func To[T any](v T) *T {
	return &v
}

// ➜  mem git:(master) ✗ go run -gcflags="-m" mem.go
// # command-line-arguments
// ./mem.go:4:6: can inline To[go.shape.int]
// ./mem.go:8:6: can inline main
// ./mem.go:4:6: can inline To[int]
// ./mem.go:10:11: inlining call to To[go.shape.int]
// ./mem.go:4:6: inlining call to To[go.shape.int]
// ./mem.go:4:16: moved to heap: v
// ./mem.go:4:6: moved to heap: v
func main() {
	i := 42
	ptr := To(i)
	_ = ptr
}
