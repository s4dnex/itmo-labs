package utils;

import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;

/**
 * Class to format text and different objects.
 */
public class Formatter {
    public final static DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM);

    /**
     * Returns format (see {@link java.util.Formatter}) of {@link String} to print text with given number of columns with given width.
     * @param numberOfColumns Number of columns
     * @param minColumnWidth Minimum width of columns
     * @return String with needed format
     */
    public static String getColumnStringFormat(int numberOfColumns, int minColumnWidth) {
        String columnFormat = "%-" + minColumnWidth + "s\t";
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < numberOfColumns; i++)
            sb.append(columnFormat);
        
        sb.append("\n");

        return sb.toString();
    }

    /**
     * Returns {@link String} with commas as delimiter with values of given {@link Enum}.
     * @param enumClass Enum to take values from
     * @return String with Enum values
     */
    public static <T extends Enum<T>> String getEnumValues(Class<T> enumClass) {
        T[] values = enumClass.getEnumConstants();
        
        StringBuilder sb = new StringBuilder();
        for (T value : values) {
            sb.append(value.toString());
            sb.append(", ");
        }
        sb.delete(sb.length() - 2, sb.length());
        
        return sb.toString();
    }
}
