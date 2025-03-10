package commands;

import java.util.Queue;

import utils.Console;

public class History extends Command {
    private final Console console;
    private final Queue<Command> executedCommands;
    
    public History(Console console, Queue<Command> executedCommands) {
        super(
            "history", 
            new String[0],
            "Display last 15 executed commands"
        );

        this.console = console;
        this.executedCommands = executedCommands;
    }

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        console.println("Last executed commands (up to 15):");

        for (Command command : executedCommands)
            console.println(command.getName());
    }
}
