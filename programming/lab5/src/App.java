import java.util.Scanner;

import utils.Collection;
import utils.Console;
import utils.Invoker;
import utils.OutputHandler;
import utils.InputHandler;
import utils.ScannerInput;
import utils.SystemOutput;

public class App {
    public static void main(String[] args) {
        Collection collection = new Collection();
        InputHandler inputHandler = new ScannerInput(new Scanner(System.in));
        OutputHandler outputHandler = new SystemOutput();
        Console console = new Console(inputHandler, outputHandler);
        Invoker invoker = new Invoker(console, collection);

        while (true) {
            console.print("> ");
            invoker.execute(console.readln());
        }
    }
}
