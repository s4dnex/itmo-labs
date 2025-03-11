import java.util.Scanner;
import java.nio.file.Files;
import java.nio.file.Path;

import io.*;
import json.JsonHandler;
import utils.Collection;
import utils.CommandReader;
import utils.Console;
import utils.Invoker;

public class App {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Pass file path as argument.");
            System.exit(-1);
        }

        try (
            InputHandler inputHandler = new ScannerInput(new Scanner(System.in));
            OutputHandler outputHandler = new SystemOutput()
        ) {
            Path path = Path.of(args[0]);
            if (Files.notExists(path)) {
                System.err.println("File with such name does not exist.");
                System.exit(-1);
            }

            FileHandler fileHandler = new DefaultFileHandler(path);
            Collection collection = new Collection(
                JsonHandler.deserializeCollection(fileHandler.read())
            );

            Console console = new Console(inputHandler, outputHandler);    
            Invoker invoker = new Invoker(console, fileHandler, collection);
            CommandReader commandReader = new CommandReader(console, invoker);
            
            commandReader.enable();
        } catch (Exception e) {
            System.err.println("Unexpected program error (" + e.getClass() + "): " + e.getMessage());
            System.exit(-1);
        }
    }
}
