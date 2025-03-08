package commands;

import utils.Collection;
import utils.Console;
import utils.DataBuilder;

public class RemoveLower extends Command {
    private final Console console;
    private final Collection collection;
    private final DataBuilder dataBuilder;
    
    // CONSTRUCTORS

    public RemoveLower(Console console, Collection collection, DataBuilder dataBuilder) {
        super(
            "remove_lower", 
            new String[0], 
            "Remove all elements from the collection that are less than the specified one"
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
        
        if (collection.getSize() == 0) {
            console.println("Collection is empty!");
            return;
        }

        long amount = collection.removeLower(
            dataBuilder.buildLabWork()
        );

        if (console.isInteractiveMode())
            if (amount > 1)
                console.println(amount + " elements have been removed!");
            else if (amount == 1)
                console.println("1 element has been removed!");
            else
                console.println("No elements have been removed!");
    }
}
