package commands;

import utils.Collection;
import utils.Console;
import utils.DataBuilder;

/**
 * Command to build element and add it to collection.
 */
public class Add extends Command {
    private final Console console;
    private final Collection collection;
    private final DataBuilder dataBuilder;

    // CONSTRUCTORS
    
    public Add(Console console, Collection collection, DataBuilder dataBuilder) {
        super(
            "add", 
            new String[0], 
            "Add a new element to the collection"
        );

        this.console = console;
        this.collection = collection;
        this.dataBuilder = dataBuilder;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        collection.add(
            dataBuilder.buildLabWork()
        );

        if (console.isInteractiveMode())
            console.println("Element has been added!");
    }
}
