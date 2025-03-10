package utils;

import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;

public class Formatter {
    public final static DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM);

    public static String getIndentation(int count) {
        return " ".repeat(count);
    }

    public static String getColumnStringFormat(int numberOfColumns, int minColumnWidth) {
        String columnFormat = "%-" + minColumnWidth + "s\t";
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < numberOfColumns; i++)
            sb.append(columnFormat);
        
        sb.append("\n");

        return sb.toString();
    }

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
