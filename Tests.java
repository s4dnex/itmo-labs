import java.math.BigInteger;
import java.math.BigDecimal;

public class Tests {
    final static String ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    final static double GOLDEN_RATIO = (1 + Math.sqrt(5)) / 2;

    public static void main(String[] args) {
        System.out.println(convertFromNBase("EDCBA9876543210", 15));
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
                    .multiply(base.pow(number.indexOf(",") - i))
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

        if (isNegative) decimal.negate();

        return decimal;
    }
}
