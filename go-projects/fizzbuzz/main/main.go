/*
Fizz Buzz - Write a program that prints the numbers from 1 to 100.
But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”.
For numbers which are multiples of both three and five print “FizzBuzz”.
*/

package main

import (
	"github.com/j0rdan0/fizzbuzz"
)

func main() {
	for i := 1; i <= 10000; i++ {
		fizzbuzz.Printer(i)
	}
}
