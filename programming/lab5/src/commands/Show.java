package commands;

import java.util.ArrayList;

import data.LabWork;
import utils.Collection;
import utils.Console;

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

        ArrayList<LabWork> labWorks = collection.asArrayList();
        if (labWorks.size() == 0) {
            console.println("The collection is empty");
            return;
        }

        for (LabWork lw : labWorks)
            console.println(lw);
            console.println("");
    }
}
