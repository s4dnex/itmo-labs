package Informatics.Lab1;

import java.math.BigInteger;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Lab1 {
    final static String INVALID_NUMBER = "Invalid number";
    final static String INVALID_FROM_BASE = "Invalid base to convert from";
    final static String INVALID_TO_BASE = "Invalid base to convert to";
    final static String ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    final static double GOLDEN_RATIO = (1 + Math.sqrt(5)) / 2;
    final static Scanner scanner = new Scanner(System.in);
    static String response = "";

    public static void main(String[] args) {
        String[][] tasks = {};
        String number, fromBase, toBase, result;

        do {
            System.out.println("Numeral system converter by Nikita \"sadnex\" Ryazanov");
            System.out.println("Available modes:");
            System.out.println("1. Tasks of variant №20");
            System.out.println("2. Own input");
            System.out.print("Choose a mode: ");
            response = scanner.nextLine();
        } while (!response.equals("1") && !response.equals("2"));
        
        switch (response) {
            case "1":
                tasks = new String[][] {
                    // Variant №20
                    {"68981", "10", "7"},
                    {"40403", "5", "10"},
                    {"B9235", "15", "5"},
                    {"58,88", "10", "2"},
                    {"BA,12", "16", "2"},
                    {"34,43", "8", "2"},
                    {"0,111101", "2", "16"},
                    {"0,100001", "2", "10"},
                    {"52,A1", "16", "10"},
                    {"613301", "Fact", "10"},
                    {"229", "10", "Fib"},
                    {"10100000", "Fib", "10"},
                    {"100010,001001", "Berg", "10"}
                    // tests
                    
                    ,{"310", "Fact", "10"}
                    ,{"4120", "Fact", "10"}
                    ,{"20", "10", "Fact"}
                    ,{"106", "10", "Fact"}
                    ,{"100100", "Fib", "10"}
                    ,{"100,01", "Berg", "10"}
                    ,{"3", "10", "Berg"}
                    ,{"7", "10", "Berg"}
                    ,{"16", "10", "Berg"}
                    ,{"10000,0001", "Berg", "10"}
                    ,{"101000,100001", "Berg", "10"}
                    ,{"20^210", "5S", "10"}
                    ,{"^202^10", "5S", "10"}
                    ,{"33^200", "7S", "10"}
                    ,{"8134", "10", "7S"}
                    ,{"10^2^12", "5S", "10"}
                    ,{"572", "10", "5S"}
                    ,{"^1021^2", "5s", "10"}
                    ,{"-572", "10", "5s"}
                    ,{"-1205", "10", "5s"}
                    
                };
                break;
        
            case "2":
                do {
                    System.out.print("Enter a number to convert: ");
                    response = scanner.nextLine();
                } while (response.isEmpty() || response.isBlank());
                number = response;

                do {
                    System.out.print("Enter a base of the number: ");
                    response = scanner.nextLine();
                } while (response.isEmpty() || response.isBlank());
                fromBase = response;

                do {
                    System.out.print("Enter a base to convert to: ");
                    response = scanner.nextLine();
                } while (response.isEmpty() || response.isBlank());
                toBase = response;

                tasks = new String[][] { {number, fromBase, toBase} };
                break;
        }
        
        System.out.println();
        System.out.printf("%-4s %-15s %-12s %-10s %s%n", "№", "Convert", "From Base", "To Base", "Result");

        for (int i = 0; i < tasks.length; i++) {
            number = tasks[i][0];
            fromBase = tasks[i][1]; 
            toBase = tasks[i][2];
            result = convert(number, fromBase, toBase);
            System.out.printf("%-4d %-15s %-12s %-10s %s%n", i + 1, number, fromBase.toUpperCase(), toBase.toUpperCase(), result);
        }
    }

    public static String convert(String number, String fromBase, String toBase) {
        String result = "";
        double decimal = 0.0;

        switch(fromBase.toUpperCase()) {
            case "FACT":
                if (!Pattern.matches("[0-9]+", number)) {
                    return INVALID_NUMBER; 
                }
                decimal = convertFromFact(number);
                break;
            
            case "FIB":
                if (!Pattern.matches("[0-1]+", number)) {
                    return INVALID_NUMBER;
                }
                decimal = convertFromFib(number);
                break;
            
            case "BERG":
                if (!Pattern.matches("[0-1]+([,]?[0-1]+)?", number)) {
                    return INVALID_NUMBER;
                }
                decimal = convertFromBerg(number);
                break;

            default:
                if (Pattern.matches("[0-9]*[13579]+[sS]{1}", fromBase)) {
                    if (!Pattern.matches("-?[0-9^]+[0-9]+", number)) {
                        return INVALID_NUMBER;
                    }
                    decimal = convertFromSymmetric(number, Integer.parseInt(fromBase.substring(0, fromBase.length() - 1)));
                }
                else if (Pattern.matches("[0-9]+", fromBase)) {
                    if (!Pattern.matches("-?[0-9A-Z]+([,]?[0-9A-Z]+)?", number)) {
                        return INVALID_NUMBER;
                    }
                    decimal = convertFromNBase(number, Integer.parseInt(fromBase));
                }
                else return INVALID_FROM_BASE;
                break;
        }

        switch(toBase.toUpperCase()) {
            case "FACT":
                result = String.valueOf(convertToFact((long) decimal));
                break;
            
            case "FIB":
                result = String.valueOf(convertToFib((long) decimal));
                break;

            case "BERG":
                result = String.valueOf(convertToBerg(decimal));
                break;

            default:
                if (Pattern.matches("[0-9]*[13579]+[sS]{1}", toBase)) {
                    result = convertToSymmetric((int) decimal, Integer.parseInt(toBase.substring(0, toBase.length() - 1)));   
                }
                else if (Pattern.matches("[0-9]+", toBase)) {
                    result = String.valueOf(convertToNBase(decimal, Integer.parseInt(toBase)));
                }
                else return INVALID_TO_BASE;
                break;
        }

        return result.replace(".", ",");
    }

    private static double convertFromNBase(String number, int fromBase) {
        boolean isNegative = false;
        double decimal = 0.0;

        if (number.startsWith("-")) {
            isNegative = true;
            number = number.substring(1);
        }

        if (number.contains(",")) {
            int integer = 0;
            double fraction = 0.0;

            for (int i = 0; i < number.indexOf(","); i++) {
                integer += ALPHABET.indexOf(number.charAt(i)) * Math.pow(fromBase, number.indexOf(",") - 1 - i);
            }
            for (int i = number.indexOf(",") + 1; i < number.length(); i++) {
                fraction += ALPHABET.indexOf(number.charAt(i)) * Math.pow(fromBase, number.indexOf(",") - i);
            }

            decimal = integer + fraction;
        }
        else {
            for (int i = 0; i < number.length(); i++) {
                decimal += ALPHABET.indexOf(number.charAt(i)) * Math.pow(fromBase, number.length() - 1 - i);
            }
        }

        return decimal * (isNegative ? -1 : 1);
    }

    private static String convertToNBase(double decimal, int toBase) {
        String result = decimal < 0 ? "-" : "", resultInteger = "", resultFraction = "";
        decimal = Math.abs(decimal);
        int integer = (int) decimal;
        double fraction = decimal - integer;
        
        while (integer > 0) {
            int remainder = integer % toBase;
            integer /= toBase;
            resultInteger = ALPHABET.charAt(remainder) + resultInteger;
        }
        while (fraction > 0 && resultFraction.length() < 5) {
            int remainder = (int) (fraction * toBase);
            fraction = fraction * toBase - remainder;
            resultFraction += ALPHABET.charAt(remainder);
        }
        
        
        if (resultInteger.length() > 0) {
            result += resultInteger;
        }
        else {
            result += "0";
        }
        if (resultFraction.length() > 0) {
            result += "," + resultFraction;
        }

        return result;
    }

    private static long convertFromFact(String number) {
        long decimal = 0;
        
        for (int i = 0; i < number.length(); i++) {
            decimal += ALPHABET.indexOf(number.charAt(i)) * getFactorial(number.length() - i);
        }
        
        return decimal;
    }

    private static String convertToFact(long decimal) {
        String result = "";

        for (int i = 2; decimal > 0; i++) {
            result = ALPHABET.charAt((int) (decimal % i)) + result;
            decimal /= i;
        }

        return result;
    }

    private static int getFactorial(int f) {
        int result = 1;
        for (int i = 1; i <= f; i++) {
            result = result * i;
        }
        return result;
    }

    private static long convertFromFib(String number) {
        long decimal = 0;

        for (int i = 0; i < number.length(); i++) {
            decimal += ALPHABET.indexOf(number.charAt(i)) * getFibonacci(number.length() - i + 1);
        }
        
        return decimal;
    }

    private static BigInteger convertToFib(long decimal) {
        if (decimal == 0) return BigInteger.ZERO;

        BigInteger result;
        int i = 2;

        while (getFibonacci(i + 1) < decimal) {
            i++;
        }

        result = BigInteger.valueOf((long) Math.pow(10, i - 2)).add(convertToFib(decimal - getFibonacci(i)));

        return result;
    }

    private static long getFibonacci(int n) {
        // Binet's formula
        return (long) ((Math.pow(GOLDEN_RATIO, n) - Math.pow((-GOLDEN_RATIO), -n)) / Math.sqrt(5));
    }

    private static double convertFromBerg(String number) {
        double decimal = 0.0;

        if (number.contains(",")) {
            double integer = 0;
            double fraction = 0.0;

            for (int i = 0; i < number.indexOf(","); i++) {
                integer += ALPHABET.indexOf(number.charAt(i)) * Math.pow(GOLDEN_RATIO, number.indexOf(",") - 1 - i);
            }
            for (int i = number.indexOf(",") + 1; i < number.length(); i++) {
                fraction += ALPHABET.indexOf(number.charAt(i)) * Math.pow(GOLDEN_RATIO, number.indexOf(",") - i);
            }

            decimal = integer + fraction;
        }
        else {
            for (int i = 0; i < number.length(); i++) {
                decimal += ALPHABET.indexOf(number.charAt(i)) * Math.pow(GOLDEN_RATIO, number.length() - 1 - i);
            }
        }
    
        return decimal;
    }

    private static double convertToBerg(double decimal) {
        if (Math.abs((int) (decimal * Math.pow(10, 10))) == 0) return 0.0;

        double result = 0.0;
        int power = (int) Math.round(Math.log(decimal) / Math.log(GOLDEN_RATIO));

        while ((int) ((decimal - Math.pow(GOLDEN_RATIO, power)) * Math.pow(10, 10)) < 0) {
            power--;
        }
        while ((int) ((decimal - Math.pow(GOLDEN_RATIO, power + 1)) * Math.pow(10, 10)) > 0) {
            power++;
        }

        result = Math.pow(10, power) + convertToBerg(decimal - Math.pow(GOLDEN_RATIO, power));

        return result;
    }

    private static int convertFromSymmetric(String number, int fromBase) {
        int decimal = 0;
        int amountOfNegatives = 0;
        int notDigits = 0;
        boolean isNegative = false;

        for (int i = 0; i < number.length(); i++) {
            if (ALPHABET.indexOf(number.charAt(i)) == -1) amountOfNegatives++;
        }

        for (int i = 0; i < number.length(); i++) {
            if (ALPHABET.indexOf(number.charAt(i)) == -1) {
                notDigits++;
                isNegative = true;
            }
            else {
                decimal += ALPHABET.indexOf(number.charAt(i)) * Math.pow(fromBase, number.length() - 1 - i - amountOfNegatives + notDigits) * ((isNegative) ? -1 : 1);
                isNegative = false;
            }
        }        

        return decimal;
    }

    private static String convertToSymmetric(int decimal, int toBase) {
        String result = "";
        int remainder = 0;
        int maxDigit = toBase / 2;

        while (decimal != 0) {
            remainder = decimal % toBase;
            if (remainder < 0) remainder += toBase;
            decimal = (int) Math.floor(Double.parseDouble(String.valueOf(decimal)) / toBase);

            if (remainder <= maxDigit) {
                result = ALPHABET.charAt(remainder) + result;
            }
            else {
                result = "^" + String.valueOf(Math.abs(remainder - toBase)) + result;
                decimal += 1; 
            }
        }

        return result;
    }
}
