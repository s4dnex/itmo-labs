package utils;

import java.util.LinkedList;
import java.util.Queue;

import io.InputHandler;
import io.OutputHandler;

public class Console implements InputHandler, OutputHandler {
    private boolean isInteractiveMode;
    private final InputHandler inputHandler;
    private final OutputHandler outputHandler;
    private Queue<String> script = new LinkedList<String>();

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
        script.clear();
        isInteractiveMode = true;
    }

    public void setScriptMode(Queue<String> script) {
        isInteractiveMode = false;
        script.addAll(this.script);
        this.script = script;
    }

    @Override
    public void print(Object obj) {
        outputHandler.print(obj);
    }

    @Override
    public void println(Object obj) {
        outputHandler.println(obj);
    }

    @Override
    public void printf(String format, Object... args) {
        outputHandler.printf(format, args);
    }

    @Override
    public String readln() {
        if (!isInteractiveMode)
            return script.poll();
        else
            return inputHandler.readln();
    }

    @Override
    public void close() {
        inputHandler.close();
        outputHandler.close();
    }
}
