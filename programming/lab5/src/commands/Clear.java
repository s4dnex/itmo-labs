package commands;

import utils.Collection;
import utils.Console;

/**
 * Command to clear the collection.
 */
public class Clear extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS

    public Clear(Console console, Collection collection) {
        super(
            "clear", 
            new String[0], 
            "Clear the collection"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        collection.clear();
        
        if (console.isInteractiveMode())
            console.println("Collection has been cleared!");
    }
}
