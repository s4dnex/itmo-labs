package commands;

import utils.Collection;
import utils.Console;

/**
 * Command to print sum of minimal points of every element.
 */
public class SumOfMinimalPoint extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS

    public SumOfMinimalPoint(Console console, Collection collection) {
        super(
            "sum_of_minimal_point", 
            new String[0], 
            "Print the sum of the minimal point of all elements in the collection"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        console.println("Sum of the minimal points: " + collection.sumOfMinimalPoint());
    }

}
