package commands;

import utils.Collection;
import utils.Console;
import utils.DataBuilder;

/**
 * Command to build element and add it to collection if it is greater than any other.
 */
public class AddIfMax extends Command {
    private final Console console;
    private final Collection collection;
    private final DataBuilder dataBuilder;
    
    // CONSTRUCTORS

    public AddIfMax(Console console, Collection collection, DataBuilder dataBuilder) {
        super(
            "add_if_max", 
            new String[0], 
            "Add a new element to the collection if its value is greater than the greatest element of this collection"
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
        
        if (console.isInteractiveMode())
            if (collection.addIfMax(dataBuilder.buildLabWork()))
                console.println("Element has been added!");
            else
                console.println("Element has NOT been added!");
    }

}
