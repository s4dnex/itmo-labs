package utils;

/**
 * Class to read and parse {@link commands.Command}.
 */
public class CommandReader {
    private final Console console;
    private final Invoker invoker;

    // CONSTRUCTORS

    /**
     * @param console Class to handle input and output
     * @param invoker Class to invoke commands execution
     */
    public CommandReader(Console console, Invoker invoker) {
        this.console = console;
        this.invoker = invoker;
    }

    // METHODS

    /**
     * Parses {@link commands.Command} from {@link String} and returns it as array.
     * @param command Command to parse
     * @return Array with command name and arguments
     */
    public static String[] parse(String command) {
        if (command == null || command.isBlank()) {
            return new String[] {""};
        }

        String[] commandParts = command.trim().split("\s+");
        return commandParts;
    }

    /**
     * Method to enable {@link CommandReader} and pass input to {@link Invoker}.
     */
    public void enable() {
        console.setInteractiveMode();

        while (true) {
            console.print("> ");
            invoker.execute(console.readln());
        }
    }
}
