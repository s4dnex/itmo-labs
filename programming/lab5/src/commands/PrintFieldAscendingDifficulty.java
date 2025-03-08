package commands;

import utils.Collection;
import utils.Console;

public class PrintFieldAscendingDifficulty extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS

    public PrintFieldAscendingDifficulty(Console console, Collection collection) {
        super(
            "print_field_ascending_difficulty", 
            new String[0], 
            "Print the 'difficulty' field of all elements in ascending order"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        var fields = collection.getAscendingDifficulty();

        if (fields.isEmpty()) {
            console.println("Collection is empty!");
        }
        else {
            console.println("Difficulties in ascending order:");
            for (var field : fields) {
                console.println(field);
            }
        }
    }
}
