/*

Count Vowels - Enter a string and the program counts the number of vowels in the text.
For added complexity have it report a sum of each vowel found.

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
	c, vC := countVowel(input)
	fmt.Println("The string", strings.TrimRight(input, "\n"), "contains", c, "vowels")
	fmt.Println("Vowel counter:")
	fmt.Println("_____________")
	for k, v := range vC {
		fmt.Println(k, v)
	}

}

func countVowel(s string) (int, map[string]int) {
	var counter int
	vowels := []string{"a", "e", "i", "o", "u"}
	vowelsCount := make(map[string]int)
	for _, vowel := range vowels {
		vowelsCount[vowel] = 0 // initiating vowel count map
	}

	for _, letter := range s {
		for _, vowel := range vowels {
			if strings.Contains(string(letter), vowel) {
				counter++
				vowelsCount[vowel]++
				break
			}
		}

	}
	return counter, vowelsCount

}
