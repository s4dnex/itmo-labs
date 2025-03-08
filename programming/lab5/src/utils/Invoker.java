package utils;

import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;

import commands.Add;
import commands.AddIfMax;
import commands.Clear;
import commands.Command;
import commands.Exit;
import commands.Help;
import commands.History;
import commands.Info;
import commands.PrintFieldAscendingDifficulty;
import commands.PrintFieldDescendingAuthor;
import commands.RemoveById;
import commands.RemoveLower;
import commands.Show;
import commands.SumOfMinimalPoint;
import commands.Update;

public class Invoker {
    private final Console console;
    private final Collection collection;
    private final Queue<Command> executedCommands;
    private final Map<String, Command> commands;
    private final DataBuilder dataBuilder;

    // CONSTRUCTORS

    public Invoker(Console console, Collection collection) {
        this.console = console;
        this.collection = collection;
        executedCommands = new LinkedList<Command>();
        commands = new HashMap<String, Command>();
        dataBuilder = new DataBuilder(console, collection);

        registerCommand(new Help(console, commands));
        registerCommand(new Info(console, collection));
        registerCommand(new Show(console, collection));
        registerCommand(new Add(console, collection, dataBuilder));
        registerCommand(new Update(console, collection, dataBuilder));
        registerCommand(new RemoveById(console, collection));
        registerCommand(new Clear(console, collection));
        registerCommand(new Exit(console));
        registerCommand(new AddIfMax(console, collection, dataBuilder));
        registerCommand(new RemoveLower(console, collection, dataBuilder));
        registerCommand(new History(console, executedCommands));
        registerCommand(new SumOfMinimalPoint(console, collection));
        registerCommand(new PrintFieldAscendingDifficulty(console, collection));
        registerCommand(new PrintFieldDescendingAuthor(console, collection));
    }

    // METHODS

    private void registerCommand(Command command) {
        commands.put(command.getName(), command);
    }

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
                    executedCommands.poll();
                
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
