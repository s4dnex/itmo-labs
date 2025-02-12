package commands;

import utils.Collection;
import utils.Console;
import utils.Formatter;

public class Info extends Command {
    private final Console console;
    private final Collection collection;
    
    // CONSTRUCTORS

    public Info(Console console, Collection collection) {
        super(
            "info", 
            new String[0], 
            "Display information about the collection"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");

        console.println("Type: " + collection.getType());
        console.println("Size: " + collection.getSize());
        console.println("Creation date: " + collection.getCreationDate().format(Formatter.DATE_FORMAT));
    }

}
