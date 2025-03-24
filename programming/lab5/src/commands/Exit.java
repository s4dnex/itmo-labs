package commands;

import utils.Console;

/**
 * Command to exit the program.
 */
public class Exit extends Command {
    private final Console console;
    // CONSTRUCTORS

    public Exit(Console console) {
        super(
            "exit", 
            new String[0], 
            "Exit the program"
        );

        this.console = console;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");


        try {
            console.close();
            System.exit(0);
        } catch (Exception e) {
            System.err.println("Couldn't close the console's I/O handlers.");
            System.exit(1);
        }
    }
}
