/*

Reverse a String - Enter a string and the program will reverse it and print it out.

*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func reverseString(s string) string {
	var sb strings.Builder
	if len(s) == 1 {
		return s
	}
	for i := len(s) - 1; i >= 0; i-- {
		sb.WriteByte(s[i])
	}

	return sb.String()
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
