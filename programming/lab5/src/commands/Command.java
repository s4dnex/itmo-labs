package commands;

import json.JsonHandler;

public abstract class Command implements Comparable<Command> {
    protected final String name;
    protected final String[] args;
    protected final String description;

    // CONSTRUCTORS

    public Command(String name, String[] args, String description) {
        this.name = name;
        this.args = args;
        this.description = description;
    }

    // GETTERS

    public String getName() {
        return name;
    }

    public String[] getArgs() {
        return args;
    }

    public String getDescription() {
        return description;
    }
    
    // METHODS

    public abstract void execute(String[] args);

    @Override
    public int compareTo(Command command) {
        return name.compareTo(command.getName());
    }

    @Override
    public String toString() {
        return "Command " + JsonHandler.getGson().toJson(this);
    }
}
