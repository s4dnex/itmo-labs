package commands;

import utils.Collection;
import utils.Console;

public class RemoveById extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS
    
    public RemoveById(Console console, Collection collection) {
        super(
            "remove_by_id", 
            new String[] { "id" }, 
            "Remove element from the collection by its ID"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 1) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        long id;
        
        try {
            id = Long.parseLong(args[0]);
        }
        catch (NumberFormatException e) {
            throw new IllegalArgumentException("ID must be a long integer");
        }

        collection.remove(id);

        if (console.isInteractiveMode())
            console.println("Element with ID " + id + " has been removed!");
    }
}
