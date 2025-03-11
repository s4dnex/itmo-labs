package utils;

import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;

import commands.*;
import io.FileHandler;

/**
 * Class to register commands and invoke their execution.
 */
public class Invoker {
    private final Console console;
    private final FileHandler fileHandler;
    private final Collection collection;
    private final Queue<Command> executedCommands;
    private final Map<String, Command> commands;
    private final DataBuilder dataBuilder;

    // CONSTRUCTORS

    /**
     * @param console Class to handle input and output
     * @param fileHandler Class to handle files
     * @param collection Class to store and work with data
     */
    public Invoker(Console console, FileHandler fileHandler, Collection collection) {
        this.console = console;
        this.fileHandler = fileHandler;
        this.collection = collection;
        executedCommands = new LinkedList<Command>();
        commands = new HashMap<String, Command>();
        dataBuilder = new DataBuilder(console);

        registerCommand(new Help(console, commands));
        registerCommand(new Info(console, collection));
        registerCommand(new Show(console, collection));
        registerCommand(new Add(console, collection, dataBuilder));
        registerCommand(new Update(console, collection, dataBuilder));
        registerCommand(new RemoveById(console, collection));
        registerCommand(new Clear(console, collection));
        registerCommand(new Save(console, fileHandler, collection));
        registerCommand(new ExecuteScript(console, this));
        registerCommand(new Exit(console));
        registerCommand(new AddIfMax(console, collection, dataBuilder));
        registerCommand(new RemoveLower(console, collection, dataBuilder));
        registerCommand(new History(console, executedCommands));
        registerCommand(new SumOfMinimalPoint(console, collection));
        registerCommand(new PrintFieldAscendingDifficulty(console, collection));
        registerCommand(new PrintFieldDescendingAuthor(console, collection));
    }

    // METHODS

    /**
     * Method to register command to allow further execution
     * @param command Command to register
     */
    private void registerCommand(Command command) {
        commands.put(command.getName(), command);
    }

    /**
     * Method that parses command from String and executes it
     * @param command Command to execute
     */
    public void execute(String command) {
        String[] commandParts = CommandReader.parse(command);
        command = commandParts[0];
        String[] args = (commandParts.length > 1) ?  Arrays.copyOfRange(commandParts, 1, commandParts.length) : new String[0];

        if (commands.containsKey(command)) {
            try {
                commands.get(command).execute(args);

                if (executedCommands.size() > 15)
                    executedCommands.poll();
                
                executedCommands.add(commands.get(command));    
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }
        else {
            String msg = "Command not found. Type 'help' to see available commands.";
            if (console.isInteractiveMode())
                console.println(msg);
            else throw new RuntimeException(msg);
        }
    }
}
