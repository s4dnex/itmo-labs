package utils;

public class Console {
    private boolean isInteractiveMode;
    private final InputHandler inputHandler;
    private final OutputHandler outputHandler;

    // CONSTRUCTORS 

    public Console(InputHandler inputHandler, OutputHandler outputHandler) {
        isInteractiveMode = true;
        this.inputHandler = inputHandler;
        this.outputHandler = outputHandler;
    }

    // METHODS
    
    public boolean isInteractiveMode() {
        return isInteractiveMode;
    }

    public void setInteractiveMode() {
        isInteractiveMode = true;
    }

    public void setScriptMode() {
        isInteractiveMode = false;
    }

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

    public void closeIO() {
        inputHandler.close();
        outputHandler.close();
    }
}
