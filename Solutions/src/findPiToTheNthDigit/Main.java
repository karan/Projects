package findPiToTheNthDigit;

import java.util.Scanner;

public class Main {


	public static void main(String[] args) {
		String Pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652";
		Scanner keyboard = new Scanner(System.in);
        int piDigits = 0;
        do {
            System.out.println("Enter the desired number of digits for PI");
            piDigits = keyboard.nextInt();
            if (piDigits > Pi.length()-3){
                System.out.println("unable to compute that many digits");
            }
        }
        while(piDigits > Pi.length()-3);
		Pi = Pi.substring(0, piDigits+2);
		System.out.println("PI = "+Pi);
	}

}


