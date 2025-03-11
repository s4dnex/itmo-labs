package utils;

import java.util.LinkedList;
import java.util.Queue;

import io.InputHandler;
import io.OutputHandler;

/**
 * Class that handles input and output.
 */
public class Console implements InputHandler, OutputHandler {
    private boolean isInteractiveMode;
    private final InputHandler inputHandler;
    private final OutputHandler outputHandler;
    private Queue<String> script = new LinkedList<String>();

    // CONSTRUCTORS 

    /**
     * @param inputHandler Class that handles input
     * @param outputHandler Class that handles output
     */
    public Console(InputHandler inputHandler, OutputHandler outputHandler) {
        this.inputHandler = inputHandler;
        this.outputHandler = outputHandler;
    }

    // METHODS

    /**
     * Returns current mode of {@link Console}.
     * @return {@code true} if in interactive mode, {@code false} if in script mode.
     */
    public boolean isInteractiveMode() {
        return isInteractiveMode;
    }

    /**
     * Set mode of {@link Console} to interactive.
     */
    public void setInteractiveMode() {
        script.clear();
        isInteractiveMode = true;
    }

    /**
     * Set mode of {@link Console} to script.
     * @param script Script to execute
     */
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

    /**
     * Read line from input (if in interactive mode) or script (if in script mode).
     * @return line in form of {@link String}
     */
    @Override
    public String readln() {
        if (!isInteractiveMode)
            return script.poll();
        else
            return inputHandler.readln();
    }

    /**
     * Close all IO handlers.
     */
    @Override
    public void close() throws Exception {
        inputHandler.close();
        outputHandler.close();
    }
}
