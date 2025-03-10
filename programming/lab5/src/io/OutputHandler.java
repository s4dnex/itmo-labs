package io;

public interface OutputHandler extends AutoCloseable {
    public void print(Object obj);
    public void println(Object obj);
    public void printf(String format, Object... args);
}
