package findEToTheNthDigit;

import java.util.Scanner;

/**
 * Created by jigd on 14/09/14.
 */
public class Main {


    public static void main(String[] args){
        String e = Double.toString(Math.E);
        Scanner keyboard = new Scanner(System.in);
        int eDigits = 0;
        boolean tooManyDigits;
        do {
            System.out.println("Enter the desired number of digits for PI from 0 to 15");
            eDigits = keyboard.nextInt();
            tooManyDigits = eDigits > e.length() - 2;
            if (tooManyDigits){
                System.out.println("unable to compute that many digits");
            }
        }
        while(tooManyDigits);
        e = e.substring(0, eDigits+2);
        System.out.println("e = "+e);
    }

}
