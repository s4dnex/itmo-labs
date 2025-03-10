package utils;

public class CommandReader {
    private final Console console;
    private final Invoker invoker;

    // CONSTRUCTORS

    public CommandReader(Console console, Invoker invoker) {
        this.console = console;
        this.invoker = invoker;
    }

    // METHODS

    public static String[] parse(String command) {
        if (command == null || command.isBlank()) {
            return new String[] {""};
        }

        String[] commandParts = command.trim().split("\s+");
        return commandParts;
    }

    public void enable() {
        console.setInteractiveMode();

        while (true) {
            console.print("> ");
            invoker.execute(console.readln());
        }
    }
}
