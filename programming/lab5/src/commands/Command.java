package commands;

import json.JsonHandler;

/**
 * Abstract class for commands
 */
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

    /**
     * Returns name of {@link Command}.
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * Returns array of required for {@link Command} arguments.
     * @return array of arguments
     */
    public String[] getArgs() {
        return args;
    }

    /**
     * Returns description of {@link Command}
     * @return description
     */
    public String getDescription() {
        return description;
    }
    
    // METHODS

    /**
     * Method to execute command with given arguments.
     * @param args arguments
     */
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
