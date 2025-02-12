package utils;

public interface OutputHandler {
    public void print(Object obj);
    public void println(Object obj);
    public void printf(String format, Object... args);
    public void close();
}
