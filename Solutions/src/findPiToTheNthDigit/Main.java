package findPiToTheNthDigit;

import java.util.Scanner;

public class Main {


	public static void main(String[] args) {
		String Pi = Double.toString(Math.PI);
		Scanner keyboard = new Scanner(System.in);
        int piDigits = 0;
        boolean tooManyDigits;
        do {
            System.out.println("Enter the desired number of digits for PI from 0 to 15");
            piDigits = keyboard.nextInt();
            tooManyDigits = piDigits > Pi.length() - 2;
            if (tooManyDigits){
                System.out.println("unable to compute that many digits");
            }
        }
        while(tooManyDigits);
		Pi = Pi.substring(0, piDigits+2);
		System.out.println("PI = "+Pi);
	}

}


