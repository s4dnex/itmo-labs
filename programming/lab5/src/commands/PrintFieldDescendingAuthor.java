package commands;

import utils.Console;
import utils.Collection;

public class PrintFieldDescendingAuthor extends Command {
    private final Console console;
    private final Collection collection;
    
    // CONSTRUCTORS

    public PrintFieldDescendingAuthor(Console console, Collection collection) {
        super(
            "print_field_descending_author", 
            new String[0], 
            "Print the 'author' field of all elements in descending order"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        var fields = collection.getDescendingAuthor();

        if (fields.isEmpty()) {
            console.println("Collection is empty!");
        }
        else {
            console.println("Authors in descending order:");
            for (var field : fields) {
                console.println(field);
            }
        }
    }
}
