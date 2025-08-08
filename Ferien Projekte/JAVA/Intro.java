import java.util.Arrays;
import java.util.Scanner;

public class Intro {
    public static void main(String[] args) {
           // System.out.println("Hello, World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");

        


//        //Scanner scanner = new Scanner(System.in);
  //      System.out.println("Please enter your Age now and you will get it in 10 years:");
   //     String eingabe = scanner.nextLine();
    //    int ten = 10;
     //   int age = Integer.parseInt(eingabe);
      //  age = age + ten;
       // System.out.println("In 10 years you will be: " + age);
        //scanner.close();




        Scanner scanner2 = new Scanner(System.in);
        
        String qwertz = scanner2.nextLine();
        int alter = Integer.parseInt(qwertz);
        int[] jahre = new int[alter + 1];
        for (int i = 0; i <= alter; i++) {
            jahre[i] = i;

    

        }
        System.out.println("Your age in years is: "+Arrays.toString(jahre));


        scanner2.close();



    }
}


