package commands;

import utils.Console;
import utils.Collection;
import io.FileHandler;
import json.JsonHandler;


public class Save extends Command {
    private final Console console;
    private final FileHandler fileHandler;
    private final Collection collection;

    // CONSTRUCTORS

    public Save(Console console, FileHandler fileHandler, Collection collection) {
        super(
            "save", 
            new String[0], 
            "Save the collection to the file"
        );

        this.console = console;
        this.fileHandler = fileHandler;
        this.collection = collection;
    }

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");
        
        try {
            fileHandler.write(
                JsonHandler.getGson().toJson(collection.asTreeSet())
            );      
        } catch (Exception e) {
            console.println("Failed to save to the file: " + e.getMessage());
        }

        if (console.isInteractiveMode())
            console.println("Collection has been saved!");
    }
}
