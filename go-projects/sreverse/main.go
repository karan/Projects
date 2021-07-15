/*

Reverse a String - Enter a string and the program will reverse it and print it out.

*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func reverseString(s string) string {
	if len(s) == 1 {
		return s
	}
	reversed := make([]byte, len(s))

	for i := len(s) - 1; i >= 0; i-- {
		reversed = append(reversed, s[i])
	}

	return string(reversed)

}

func main() {

	r := bufio.NewReader(os.Stdin)
	fmt.Printf("String: ")
	input, err := r.ReadString('\n')
	if err != nil {
		log.Println(err)
	}

	fmt.Println(reverseString(input))

}
