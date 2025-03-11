package io;

public interface OutputHandler extends AutoCloseable {
    /**
     * Prints object.
     * @param obj object to print
     */
    public void print(Object obj);

    /**
     * Prints object and moves to next line.
     * @param obj object to print
     */
    public void println(Object obj);

    /**
     * Print object(s) with given format.
     * @param format Format in form of {@link String} (check {@link java.util.Formatter})
     * @param args Object(s) to print
     */
    public void printf(String format, Object... args);
}
