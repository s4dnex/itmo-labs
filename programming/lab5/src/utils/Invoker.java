package utils;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Stack;

import commands.*;

public class Invoker {
    private final Console console;
    private final Collection collection;
    private final Stack<Command> executedCommands;
    private final Map<String, Command> commands;

    // CONSTRUCTORS

    public Invoker(Console console, Collection collection) {
        this.console = console;
        this.collection = collection;
        executedCommands = new Stack<Command>();
        commands = new HashMap<String, Command>();

        commands.put("help", new Help(console, commands));
        commands.put("add", new Add(console, collection));
        commands.put("show", new Show(console, collection));
        commands.put("exit", new Exit(console));  
    }

    // METHODS

    public void execute(String command) {
        if (command == null || command.isBlank()) {
            console.println("Command not found. Type 'help' to see available commands.");
            return;
        }

        String[] commandParts = command.trim().split("\s+");
        command = commandParts[0];
        String[] args = (commandParts.length > 1) ?  Arrays.copyOfRange(commandParts, 1, commandParts.length) : new String[0];

        if (commands.containsKey(command)) {
            try {
                commands.get(command).execute(args);
            
                if (executedCommands.size() > 15) 
                    executedCommands.pop();
                executedCommands.add(commands.get(command));    
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }
        else
            console.println("Command not found. Type 'help' to see available commands.");
    }
}
