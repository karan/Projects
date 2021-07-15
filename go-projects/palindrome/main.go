/*

Check if Palindrome - Checks if the string entered by the user is a palindrome. That is that it reads the same forwards as backwards like “racecar”
*/

package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func main() {

	r := bufio.NewReader(os.Stdin)
	fmt.Printf("String: ")
	input, err := r.ReadString('\n')
	if err != nil {
		log.Println(err)
	}

	if checkPalindrome(input) {
		fmt.Println("The string", strings.Trim(input, "\n"), "is a palindrome")
	} else {
		fmt.Println("The string", strings.Trim(input, "\n"), "is not a palindrome")
	}

}

func checkPalindrome(s string) bool {

	reversed := reverseString(s)

	if strings.Trim(s, "\n") == strings.Trim(reversed, "\n") {
		return true
	}
	return false
}

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
