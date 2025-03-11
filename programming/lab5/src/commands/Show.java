package commands;

import java.util.TreeSet;

import data.LabWork;
import utils.Collection;
import utils.Console;

/**
 * Command to show collection elements.
 */
public class Show extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS

    public Show(Console console, Collection collection) {
        super(
            "show", 
            new String[0], 
            "Show all elements of the collection"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");

        TreeSet<LabWork> labWorks = collection.asTreeSet();
        if (labWorks.size() == 0) {
            console.println("Collection is empty!");
            return;
        }

        long i = 1;
        console.println("The collection contains " + labWorks.size() + " element(s):");
        for (LabWork lw : labWorks) {
            console.println((i++) + ". " + lw);
        }
    }
}
