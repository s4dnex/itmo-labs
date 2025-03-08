package commands;

import utils.Collection;
import utils.Console;
import utils.DataBuilder;

public class Update extends Command {
    private final Console console;
    private final Collection collection;
    private final DataBuilder dataBuilder;

    // CONSTRUCTORS
    
    public Update(Console console, Collection collection, DataBuilder dataBuilder) {
        super(
            "update", 
            new String[] { "id" }, 
            "Update element in the collection by its ID"
        );

        this.console = console;
        this.collection = collection;
        this.dataBuilder = dataBuilder;
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

        if (!collection.contains(id))
            throw new IllegalArgumentException("No LabWork with such ID");

        collection.update(
            id,
            dataBuilder.buildLabWork()
        );

        if (console.isInteractiveMode())
            console.println("Element with ID " + id + " has been updated!");
    }
}
