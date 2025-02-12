package utils;

public class Console {
    private InputHandler inputHandler;
    private OutputHandler outputHandler;

    // CONSTRUCTORS 

    public Console(InputHandler inputHandler, OutputHandler outputHandler) {
        this.inputHandler = inputHandler;
        this.outputHandler = outputHandler;
    }

    // METHODS

    public void print(Object obj) {
        outputHandler.print(obj);
    }

    public void println(Object obj) {
        outputHandler.println(obj);
    }

    public void printf(String format, Object... args) {
        outputHandler.printf(format, args);
    }
    
    public String readln() {
        return inputHandler.readln();
    }

    public void close() {
        inputHandler.close();
        outputHandler.close();
    }
}
