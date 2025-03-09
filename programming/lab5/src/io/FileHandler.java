package io;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class FileHandler {
    private final Path path;

    // CONSTRUCTORS 

    public FileHandler(Path path) {
        this.path = path;
    }

    // METHODS
    
    public void write(String content) {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(path.toFile()))) {
            bw.write(content);
        } catch (IOException e) {

        } 
    }

    public String read() {
        try (Scanner scanner = new Scanner(path)) {
            String result = "";
            while (scanner.hasNextLine()) {
                result += scanner.nextLine();
            }
            return result;
        } catch (IOException e) {
            return null;      
        }
    }

    public Queue<String> readLines() {
        try (Scanner scanner = new Scanner(path)) {
            Queue<String> result = new LinkedList<String>();
            while (scanner.hasNextLine()) {
                result.add(scanner.nextLine());
            }
            return result;
        } catch (IOException e) {
            return null;
        }
    }
}
