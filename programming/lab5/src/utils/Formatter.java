package utils;

import java.time.format.DateTimeFormatter;
import java.time.format.FormatStyle;

public class Formatter {
    public static int STRING_INDENTATION_COUNT = 0;
    public final static DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.MEDIUM);

    public static String getIndentation(int count) {
        return " ".repeat(count);
    }

    public static String getStringsWithIndent(String... strings) {
        if (strings == null || strings.length == 0)
            return "";

        if (strings.length == 1) {
            return strings[0] + "\n";
        }

        String indent = Formatter.getIndentation(++Formatter.STRING_INDENTATION_COUNT);
        String result = strings[0] + "\n";

        for (int i = 1; i < (strings.length - 1); i++)
            result += indent + strings[i] + "\n";

        indent = Formatter.getIndentation(--Formatter.STRING_INDENTATION_COUNT);        
        result += indent + strings[strings.length - 1] + "\n";

        return result;
    }

    public static String getColumnStringFormat(int numberOfColumns, int minColumnWidth) {
        String columnFormat = "%-" + minColumnWidth + "s\t";
        
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < numberOfColumns; i++)
            sb.append(columnFormat);
        
        sb.append("\n");

        return sb.toString();
    }
}
