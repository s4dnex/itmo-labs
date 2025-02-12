package utils;

import java.util.NoSuchElementException;
import java.util.Scanner;

public class ScannerInput implements InputHandler {
    private final Scanner scanner;

    // CONSTRUCTORS

    public ScannerInput(Scanner scanner) {
        this.scanner = scanner;
    }

    // METHODS

    @Override
    public String readln() {
        String result;

        try {
            result = scanner.nextLine();
        }
        catch (NoSuchElementException e) {
            return null;
        }

        if (result.isBlank()) return null;

        return result.trim();
    }

    @Override
    public void close() {
        scanner.close();
    }
}
