import java.util.Scanner;
import java.util.TreeSet;

import com.google.gson.JsonElement;
import com.google.gson.JsonParser;

import data.LabWork;

import java.nio.file.Files;
import java.nio.file.Path;

import io.FileHandler;
import io.InputHandler;
import io.OutputHandler;
import io.ScannerInput;
import io.SystemOutput;
import json.JsonHandler;
import utils.Collection;
import utils.Console;
import utils.Invoker;

public class App {
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Pass file name as argument.");
            System.exit(1);
        }

        try {
            Path path = Path.of(args[0]);
            if (Files.notExists(path)) {
                System.err.println("File with such name does not exist.");
                System.exit(1);
            }

            InputHandler inputHandler = new ScannerInput(new Scanner(System.in));
            OutputHandler outputHandler = new SystemOutput();        
            Console console = new Console(inputHandler, outputHandler);
    
            FileHandler fileHandler = new FileHandler(path);
            
            TreeSet<LabWork> labWorks = new TreeSet<LabWork>();
            for (JsonElement item : JsonParser.parseString(fileHandler.read()).getAsJsonArray()) {
                labWorks.add(JsonHandler.getGson().fromJson(item, LabWork.class));
            }
            
            Collection collection = new Collection(labWorks);
            
            Invoker invoker = new Invoker(console, fileHandler, collection);
    
            while (true) {
                console.print("> ");
                invoker.execute(console.readln());
            }
        } catch (Exception e) {
            System.err.println(e.getClass() + ": " + e.getMessage());
            System.exit(1);
        }
    }
}
