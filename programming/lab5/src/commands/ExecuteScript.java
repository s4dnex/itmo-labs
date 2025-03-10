package commands;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Queue;
import java.util.Set;

import io.DefaultFileHandler;
import utils.Console;
import utils.Invoker;

public class ExecuteScript extends Command {
    private final Console console;
    private final Invoker invoker;
    private final Set<Path> executedScripts = new HashSet<Path>();

    // CONSTUCTORS

    public ExecuteScript(Console console, Invoker invoker) {
        super(
            "execute_script",
            new String[] {"filePath"},
            "Read and execute the script from the specified file"
        );

        this.console = console;
        this.invoker = invoker;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 1) 
            throw new IllegalArgumentException("Unexpected arguments occurred");

        Path path = Path.of(args[0]);
        if (Files.notExists(path)) {
            throw new IllegalArgumentException("File with such name does not exist.");
        }

        try {
            if (executedScripts.contains(path)) {
                throw new IllegalArgumentException("Recursion detected.");
            }
            executedScripts.add(path);
            Queue<String> script = new DefaultFileHandler(path).readLines();
            console.setScriptMode(script);
            while (!script.isEmpty()) {
                String command = script.poll();
                // console.println(command);
                invoker.execute(command);
            }
        } catch (Exception e) {
            console.println("Failed to execute the script: " + e.getMessage());
        } finally {
            executedScripts.remove(path);
            console.setInteractiveMode();
        }
    }
}
