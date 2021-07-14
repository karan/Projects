package main

import (
	"fmt"
	"runtime"
)

func main() {

	c := make(chan int, 1)

	go func() {

		c <- 4141
	}()
	fmt.Println(runtime.NumGoroutine())

	fmt.Printf("%T\n", c)
	fmt.Println(<-c)

}
