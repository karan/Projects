package main

import (
	"fmt"
	"runtime"
	"sync"
)

var wg sync.WaitGroup
var mu sync.Mutex

func main() {

	fmt.Println("GOOS ", runtime.GOOS)
	fmt.Println("CPU", runtime.NumCPU())

	wg.Add(100)
	for i := 0; i <= 99; i++ {
		go test_routine()
		fmt.Println("Goroutines", runtime.NumGoroutine())
	}
	wg.Wait()

}

func test_routine() {
	mu.Lock()
	fmt.Println("Done")
	mu.Unlock()
	wg.Done()
}
