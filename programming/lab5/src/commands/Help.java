package commands;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Map;
import java.util.List;

import utils.Console;
import utils.Formatter;

public class Help extends Command {
    private final Console console;
    private final Map<String, Command> commands;
    
    public Help(Console console, Map<String, Command> commands) {
        super(
            "help", 
            new String[0],
            "Display available commands"
        );

        this.console = console;
        this.commands = commands;
    }

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        int minColumnWidth = 11;
        for (Command command : commands.values())
            minColumnWidth = Math.max(minColumnWidth, command.getName().length());

        String format = Formatter.getColumnStringFormat(3, minColumnWidth);
        console.printf(format, "Command", "Arguments", "Description");

        List<Command> sortedCommands = new ArrayList<Command>(commands.values());
        sortedCommands.sort(Comparator.naturalOrder());

        for (Command command : sortedCommands) {
            console.printf(
                format, 
                command.getName(), 
                String.join(", ", command.getArgs()), 
                command.getDescription()
            );
        }   
    }
}
