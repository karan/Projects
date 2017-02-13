import java.util.Scanner; 

public class Fibonacci {
  public static void main (String [] args) {
    new Fibonacci ();
  }
  
  public Fibonacci () {
    Scanner input = new Scanner(System.in);  // Reading from System.in
    System.out.println("How many numbers?");
    int n = input.nextInt();
    
    int a = 0;
    int b = 1;
    int c = 0;
    
    for (int i = 0; i < n; i ++) {
      c = a + b;
      a = b;
      b = c;
      System.out.println(c);
    }
  }
}