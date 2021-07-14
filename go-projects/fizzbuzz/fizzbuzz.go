/*
Fizz Buzz - Write a program that prints the numbers from 1 to 100.
But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”.
For numbers which are multiples of both three and five print “FizzBuzz”.
*/

package fizzbuzz

import (
	"fmt"

	"github.com/fatih/color"
)

func Printer(x int) {

	if x%3 == 0 && x%5 == 0 {
		color.Red("FizzBuzz")
	} else if x%3 == 0 {
		color.Blue("Fizz")
	} else if x%5 == 0 {
		color.Blue("Buzz")
	} else {
		fmt.Println(x)
	}

}
