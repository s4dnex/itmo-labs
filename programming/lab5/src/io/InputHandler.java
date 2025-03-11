package io;

public interface InputHandler extends AutoCloseable {
    /**
     * Reads line and returns it.
     * @return line as {@link String}
     */
    public String readln();
}
