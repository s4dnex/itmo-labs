import java.math.BigInteger;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.math.MathContext;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Converter {
    final static String INVALID_NUMBER_MSG = "Invalid number";
    final static String INVALID_FROM_BASE_MSG = "Invalid base to convert from";
    final static String INVALID_TO_BASE_MSG = "Invalid base to convert to";

    final static String FACT_NUM_REGEX = "-?[0-9]+";
    final static String FIB_NUM_REGEX = "-?[0-1]+";
    final static String BERG_NUM_REGEX = "-?[0-1]+([,]?[0-1]+)?";
    final static String NEGA_NUM_REGEX = "[0-9A-Z]+";
    final static String N_NUM_REGEX = "-?[0-9A-Z]+([,]?[0-9A-Z]+)?";

    final static String SYM_BASE_REGEX = "[0-9]*[13579]+[S]{1}";
    final static String N_BASE_REGEX = "-?[0-9]+";

    final static int FRACTION_DIGITS = 5;
    final static MathContext MATH_CONTEXT = new MathContext(50, RoundingMode.HALF_UP);
    final static String ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    final static BigDecimal GOLDEN_RATIO = (BigDecimal.ONE
                                            .add(BigDecimal.valueOf(5).sqrt(MATH_CONTEXT)))
                                            .divide(BigDecimal.valueOf(2));
    
    private final static Scanner SCANNER = new Scanner(System.in);
    private static String response = "";

    public static void main(String[] args) {
        String[][] tasks = {};
        String number, fromBase, toBase, result;

        do {
            System.out.println("Numeral system converter by Nikita \"sadnex\" Ryazanov");
            System.out.println("Available modes:");
            System.out.println("1. Variant №20");
            System.out.println("2. Console input");
            System.out.print("Enter a corresponding number: ");
            response = SCANNER.nextLine();
        } while (!response.equals("1") && !response.equals("2"));
        
        switch (response) {
            case "1":
                tasks = new String[][] {
                    // Variant №20
                    {"68981", "10", "7"}, // 405053
                    {"40403", "5", "10"}, // 2603
                    {"B9235", "15", "5"}, // 122302000
                    {"58,88", "10", "2"}, // 111010,11100
                    {"BA,12", "16", "2"}, // 10111010,00010
                    {"34,43", "8", "2"}, // 11100,10001
                    {"0,111101", "2", "16"}, // 0,F4
                    {"0,100001", "2", "10"}, // 0,51562
                    {"52,A1", "16", "10"}, // 82,62890
                    {"613301", "Fact", "10"}, // 4531
                    {"229", "10", "Fib"}, // 10101010001
                    {"10100000", "Fib", "10"}, // 47
                    {"100010,001001", "Berg", "10"} // 13
                    
                    // tests
                    ,{"-310", "fact", "10"} // -20
                    ,{"310", "Fact", "10"} // 20
                    ,{"4120", "Fact", "10"} // 106
                    ,{"-4120", "fact", "10"} // -106
                    ,{"20", "10", "Fact"} // 310
                    ,{"-20", "10", "fact"} // -310
                    ,{"106", "10", "Fact"} // 4120
                    ,{"-106", "10", "fact"} // -4120
                    ,{"100100", "Fib", "10"} // 16
                    ,{"-100100", "Fib", "10"} // -16
                    ,{"100,01", "Berg", "10"} // 3
                    ,{"-100,01", "Berg", "10"} // -3
                    ,{"3", "10", "Berg"} // 100,01
                    ,{"-3", "10", "Berg"} // -100,01
                    ,{"7", "10", "Berg"} // 10000,0001
                    ,{"-7", "10", "Berg"} // -10000,0001
                    ,{"16", "10", "Berg"} // 101000,100001
                    ,{"-16", "10", "Berg"} // -101000,100001
                    ,{"10000,0001", "Berg", "10"} // 7
                    ,{"-10000,0001", "Berg", "10"} // -7
                    ,{"101000,100001", "Berg", "10"} // 16
                    ,{"-101000,100001", "Berg", "10"} // -16
                    ,{"20^210", "5S", "10"} // 1205
                    ,{"^202^10", "5S", "10"} // -1205
                    ,{"33^200", "7S", "10"} // 8134
                    ,{"8134", "10", "7S"} // 33^200
                    ,{"10^2^12", "5S", "10"} // 572
                    ,{"572", "10", "5S"} // 10^2^12
                    ,{"^1021^2", "5s", "10"} // -572
                    ,{"-572", "10", "5s"} // ^1021^2
                    ,{"-1205", "10", "5s"} // ^202^10
                    ,{"1937", "10", "-10"} // 18077
                    ,{"18077", "-10", "10"} // 1937
                    ,{"123", "-10", "10"} // 83
                    ,{"58", "-10", "10"} // -42
                    ,{"-42", "10", "-10"} // 58
                    ,{"83", "10", "-10"} // 123
                     
                };
                break;
        
            case "2":
                do {
                    System.out.print("Enter a number to convert: ");
                    response = SCANNER.nextLine();
                } while (response.isBlank());
                number = response;

                do {
                    System.out.print("Enter a base of the number: ");
                    response = SCANNER.nextLine();
                } while (response.isBlank());
                fromBase = response;

                do {
                    System.out.print("Enter a base to convert to: ");
                    response = SCANNER.nextLine();
                } while (response.isBlank());
                toBase = response;

                tasks = new String[][] { {number, fromBase, toBase} };
                break;
        }
        
        System.out.println();
        System.out.printf("%-4s %-15s %-12s %-10s %s%n", "№", "NUMBER", "FROM BASE", "TO BASE", "RESULT");

        for (int i = 0; i < tasks.length; i++) {
            number = tasks[i][0].toUpperCase();
            fromBase = tasks[i][1].toUpperCase(); 
            toBase = tasks[i][2].toUpperCase();
            result = convert(number, fromBase, toBase).toUpperCase();

            if (number.length() > 15) number = number.substring(0, 12) + "...";

            System.out.printf("%-4d %-15s %-12s %-10s %s%n", i + 1, number, fromBase, toBase, result);
        }
    }

    public static String convert(String number, String fromBase, String toBase) {
        String result = "";
        BigDecimal decimal = BigDecimal.ZERO;

        switch(fromBase) {
            case "FACT":
                if (!Pattern.matches(FACT_NUM_REGEX, number))
                    return INVALID_NUMBER_MSG;

                for (int i = 0; i < number.replace("-", "").length(); i++) {
                    if (ALPHABET.indexOf(number.replace("-", "").charAt(i)) > (number.replace("-", "").length() - i))
                        return INVALID_NUMBER_MSG;
                }
                
                decimal = convertFromFact(number);
                break;
            
            case "FIB":
                if (!Pattern.matches(FIB_NUM_REGEX, number))
                    return INVALID_NUMBER_MSG;
                
                decimal = convertFromFib(number);
                break;
            
            case "BERG":
                if (!Pattern.matches(BERG_NUM_REGEX, number)) 
                    return INVALID_NUMBER_MSG;
                
                decimal = convertFromBerg(number);
                break;

            default:
                if (Pattern.matches(SYM_BASE_REGEX, fromBase)) {
                    int base = Integer.parseInt(fromBase.substring(0, fromBase.length() - 1));
                    
                    if (!(1 <= base && base <= 71)) return INVALID_FROM_BASE_MSG;

                    for (int i = 0; i < number.length(); i++) {
                        if (number.charAt(i) == '^') continue;

                        if (ALPHABET.indexOf(number.charAt(i)) < 0 || (ALPHABET.indexOf(number.charAt(i)) > (base / 2))) 
                            return INVALID_NUMBER_MSG;
                    }
                    
                    decimal = convertFromSymmetric(number, base);
                }
                else if (Pattern.matches(N_BASE_REGEX, fromBase)) {
                    int base = Integer.parseInt(fromBase);
                    if (!(1 <= Math.abs(base) && Math.abs(base) <= 36)) 
                        return INVALID_FROM_BASE_MSG;
                    
                    if (!Pattern.matches(base < 0 ? NEGA_NUM_REGEX : N_NUM_REGEX, number))
                        return INVALID_NUMBER_MSG;

                    for (int i = 0; i < number.length(); i++) {
                        if (number.charAt(i) == '-' || number.charAt(i) == ',') continue;

                        if (ALPHABET.indexOf(number.charAt(i)) < 0 || (ALPHABET.indexOf(number.charAt(i)) >= Math.abs(base))) 
                            return INVALID_NUMBER_MSG;
                    }

                    if (base < 0) decimal = convertFromNegaBase(number, base);
                    else decimal = convertFromNBase(number, base);
                }
                else return INVALID_FROM_BASE_MSG;
                break;
        }

        switch(toBase) {
            case "FACT":
                if (decimal.remainder(BigDecimal.ONE).compareTo(BigDecimal.ZERO) != 0)
                    return INVALID_NUMBER_MSG;
                result = String.valueOf(convertToFact(decimal));
                break;
            
            case "FIB":
                if (decimal.remainder(BigDecimal.ONE).compareTo(BigDecimal.ZERO) != 0)
                    return INVALID_NUMBER_MSG;
                result = String.valueOf(convertToFib(decimal));
                break;

            case "BERG":
                result = String.valueOf(convertToBerg(decimal));
                break;

            default:
                if (Pattern.matches(SYM_BASE_REGEX, toBase)) {
                    int base = Integer.parseInt(toBase.substring(0, toBase.length() - 1));
                    if (!(1 <= base && base <= 71)) return INVALID_TO_BASE_MSG;

                    if ((decimal.remainder(BigDecimal.ONE).compareTo(BigDecimal.ZERO) != 0)) 
                        return INVALID_NUMBER_MSG;

                    result = convertToSymmetric(decimal, base);
                }
                else if (Pattern.matches(N_BASE_REGEX, toBase)) {
                    int base = Integer.parseInt(toBase);
                    if (!(1 <= Math.abs(base) && Math.abs(base) <= 36)) 
                        return INVALID_FROM_BASE_MSG;

                    if (base < 0 && (decimal.remainder(BigDecimal.ONE).compareTo(BigDecimal.ZERO) != 0)) 
                        return INVALID_NUMBER_MSG;
                    
                    if (base < 0) result = String.valueOf(convertToNegaBase(decimal, base));
                    else result = String.valueOf(convertToNBase(decimal, base));
                }
                else return INVALID_TO_BASE_MSG;
                break;
        }

        return result.replace(".", ",");
    }

    private static BigDecimal convertFromNBase(String number, int fromBase) {
        boolean isNegative = false;
        BigDecimal base = BigDecimal.valueOf(fromBase);
        BigDecimal decimal = BigDecimal.ZERO;

        if (number.startsWith("-")) {
            isNegative = true;
            number = number.substring(1);
        }

        if (number.contains(",")) {
            BigDecimal integer = BigDecimal.ZERO;
            BigDecimal fraction = BigDecimal.ZERO;

            for (int i = 0; i < number.indexOf(","); i++) {
                integer = integer.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(base.pow(number.indexOf(",") - 1 - i))
                );
            }
            for (int i = number.indexOf(",") + 1; i < number.length(); i++) {
                fraction = fraction.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(base.pow(number.indexOf(",") - i, MATH_CONTEXT))
                );
            }

            decimal = fraction.add(integer);
        }
        else {
            for (int i = 0; i < number.length(); i++) {
                decimal = decimal.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(base.pow(number.length() - 1 - i))
                );
            }
        }

        if (isNegative) decimal = decimal.negate();

        return decimal;
    }

    private static String convertToNBase(BigDecimal decimal, int toBase) {
        String result = decimal.compareTo(BigDecimal.ZERO) == -1 ? "-" : "", resultInteger = "", resultFraction = "";
        decimal = decimal.abs();
        BigDecimal base = BigDecimal.valueOf(toBase);
        BigDecimal integer = decimal.setScale(0, RoundingMode.DOWN);
        BigDecimal fraction = decimal.remainder(BigDecimal.ONE);
        
        while (integer.compareTo(BigDecimal.ZERO) != 0) {
            int remainder = integer.remainder(base).intValue();
            integer = integer.divideToIntegralValue(base);
            resultInteger = ALPHABET.charAt(remainder) + resultInteger;
        }
        while (fraction.compareTo(BigDecimal.ZERO) != 0 && resultFraction.length() < FRACTION_DIGITS) {
            int remainder = fraction.multiply(base).intValue();
            fraction = fraction.multiply(base).remainder(BigDecimal.ONE);
            resultFraction += ALPHABET.charAt(remainder);
        }
        
        if (resultInteger.length() > 0) result += resultInteger;
        else result = "0";
        if (resultFraction.length() > 0) result += "," + resultFraction;

        return result;
    }

    private static BigDecimal convertFromNegaBase(String number, int fromBase) {
        BigDecimal base = BigDecimal.valueOf(fromBase);
        BigDecimal decimal = BigDecimal.ZERO;


        for (int i = 0; i < number.length(); i++) {
            decimal = decimal.add(
                BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                .multiply(base.pow(number.length() - 1 - i))
            );
        }

        return decimal;
    }

    private static String convertToNegaBase(BigDecimal decimal, int toBase) {
        String result = "", resultInteger = "";
        BigDecimal base = BigDecimal.valueOf(toBase);
        BigDecimal integer = decimal.setScale(0, RoundingMode.DOWN);
        
        while (integer.compareTo(BigDecimal.ZERO) != 0) {
            int remainder = integer.remainder(base).intValue();
            if (remainder < 0) remainder += Math.abs(toBase);
            integer = integer.divide(base, MATH_CONTEXT).setScale(0, RoundingMode.CEILING);
            resultInteger = ALPHABET.charAt(remainder) + resultInteger;
        }
        
        if (resultInteger.length() > 0) result += resultInteger;
        else result = "0";

        return result;
    }

    private static BigDecimal convertFromFact(String number) {
        boolean isNegative = false;
        BigDecimal decimal = BigDecimal.ZERO;
        
        if (number.startsWith("-")) {
            isNegative = true;
            number = number.substring(1);
        }

        for (int i = 0; i < number.length(); i++) {
            decimal = decimal.add(
                BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                .multiply(getFactorial(number.length() - i))
            );
        }
        
        if (isNegative) decimal = decimal.negate();

        return decimal;
    }

    private static String convertToFact(BigDecimal decimal) {
        boolean isNegative = false;
        String result = "";


        if (decimal.compareTo(BigDecimal.ZERO) < 0) {
            isNegative = true;
            decimal = decimal.negate();
        }

        for (int i = 2; decimal.compareTo(BigDecimal.ZERO) > 0; i++) {
            result = ALPHABET.charAt((decimal.remainder(BigDecimal.valueOf(i)).intValue())) + result;
            decimal = decimal.divideToIntegralValue(BigDecimal.valueOf(i));
        }

        if (isNegative) result = "-" + result;

        return result;
    }

    private static BigDecimal getFactorial(int n) {
        BigDecimal result = BigDecimal.ONE;
        for (int i = 1; i <= n; i++) {
            result = result.multiply(BigDecimal.valueOf(i));
        }
        return result;
    }

    private static BigDecimal convertFromFib(String number) {
        boolean isNegative = false;
        BigDecimal decimal = BigDecimal.ZERO;
        
        if (number.startsWith("-")) {
            isNegative = true;
            number = number.substring(1);
        }

        for (int i = 0; i < number.length(); i++) {
            decimal = decimal.add(
                BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                .multiply(getFibonacci(number.length() - i + 1))
            );
        }
        
        if (isNegative) decimal = decimal.negate();

        return decimal;
    }

    private static BigDecimal convertToFib(BigDecimal decimal) {
        if (decimal.compareTo(BigDecimal.ZERO) == 0) return BigDecimal.ZERO;

        boolean isNegative = false;
        BigDecimal result;
        int i = 2;

        if (decimal.compareTo(BigDecimal.ZERO) < 0) {
            isNegative = true;
            decimal = decimal.negate();
        }

        while (decimal.compareTo(getFibonacci(i + 1)) > 0) {
            i++;
        }

        result = BigDecimal.TEN.pow(i - 2)
                .add(convertToFib(decimal.subtract(getFibonacci(i))));

        if (isNegative) result = result.negate();

        return result.setScale(0, RoundingMode.DOWN);
    }

    private static BigDecimal getFibonacci(int n) {
        // Binet's formula
        return (GOLDEN_RATIO.pow(n)
                .subtract(GOLDEN_RATIO.negate().pow(-n, MATH_CONTEXT)))
                .divide(GOLDEN_RATIO.multiply(BigDecimal.valueOf(2)).subtract(BigDecimal.ONE), MATH_CONTEXT)
                .setScale(0, RoundingMode.HALF_UP);
    }

    private static BigDecimal convertFromBerg(String number) {
        boolean isNegative = false;
        BigDecimal decimal = BigDecimal.ZERO;

        if (number.startsWith("-")) {
            isNegative = true;
            number = number.substring(1);
        }

        if (number.contains(",")) {
            BigDecimal integer = BigDecimal.ZERO;
            BigDecimal fraction = BigDecimal.ZERO;

            for (int i = 0; i < number.indexOf(","); i++) {
                integer = integer.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(GOLDEN_RATIO.pow(number.indexOf(",") - 1 - i))
                );
            }
            for (int i = number.indexOf(",") + 1; i < number.length(); i++) {
                fraction = fraction.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(GOLDEN_RATIO.pow(number.indexOf(",") - i, MATH_CONTEXT))
                );
            }

            decimal = fraction.add(integer);
        }
        else {
            for (int i = 0; i < number.length(); i++) {
                decimal = decimal.add(
                    BigDecimal.valueOf(ALPHABET.indexOf(number.charAt(i)))
                    .multiply(GOLDEN_RATIO.pow(number.length() - 1 - i))
                );
            }
        }
        
        decimal = decimal.setScale(5, RoundingMode.HALF_UP);

        if (isNegative) decimal = decimal.negate();

        return decimal;
    }

    private static BigDecimal convertToBerg(BigDecimal decimal) {
        long precision = (long) Math.pow(10, 10);

        if (decimal.multiply(BigDecimal.TEN.multiply(BigDecimal.valueOf(precision)))
            .abs().toBigInteger().compareTo(BigInteger.ZERO) == 0) 
            return BigDecimal.ZERO;

        boolean isNegative = false;
        BigDecimal result = BigDecimal.ZERO;

        if (decimal.compareTo(BigDecimal.ZERO) < 0) {
            isNegative = true;
            decimal = decimal.negate();
        }

        int power = (int) Math.round(Math.log(decimal.longValue()) / Math.log(GOLDEN_RATIO.doubleValue()));

        while (decimal.subtract(GOLDEN_RATIO.pow(power, MATH_CONTEXT))
                .multiply(BigDecimal.valueOf(precision))
                .setScale(0, RoundingMode.DOWN)
                .compareTo(BigDecimal.ZERO) < 0) {
            power--;
        }
        while (decimal.subtract(GOLDEN_RATIO.pow(power + 1, MATH_CONTEXT))
                .multiply(BigDecimal.valueOf(precision))
                .setScale(0, RoundingMode.DOWN)
                .compareTo(BigDecimal.ZERO) > 0) {
            power++;
        }

        result = BigDecimal.valueOf(Math.pow(10, power))
                .add(convertToBerg(decimal.subtract(GOLDEN_RATIO.pow(power, MATH_CONTEXT))));

        if (isNegative) result = result.negate();

        return result;
    }

    private static BigDecimal convertFromSymmetric(String number, int fromBase) {
        BigDecimal decimal = BigDecimal.ZERO;
        BigDecimal base = BigDecimal.valueOf(fromBase);
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
                decimal = decimal.add(
                    BigDecimal.valueOf((isNegative ? -1 : 1) * ALPHABET.indexOf(number.charAt(i)))
                    .multiply(base.pow(number.length() - 1 - i - amountOfNegatives + notDigits, MATH_CONTEXT))
                );
                isNegative = false;
            }
        }        

        return decimal;
    }

    private static String convertToSymmetric(BigDecimal decimal, int toBase) {
        String result = "";
        BigDecimal remainder = BigDecimal.ZERO;
        BigDecimal maxDigit = BigDecimal.valueOf(toBase / 2);
        BigDecimal base = BigDecimal.valueOf(toBase);

        while (decimal.compareTo(BigDecimal.ZERO) != 0) {
            remainder = decimal.remainder(base);
            
            if (remainder.compareTo(BigDecimal.ZERO) < 0) remainder = remainder.add(base);
            decimal = decimal.divide(base, RoundingMode.FLOOR);
            

            if (remainder.compareTo(maxDigit) <= 0) {
                result = ALPHABET.charAt(remainder.intValue()) + result;
            }
            else {
                result = "^" + remainder.subtract(base).abs() + result;
                decimal = decimal.add(BigDecimal.ONE); 
            }
        }

        return result;
    }
}
