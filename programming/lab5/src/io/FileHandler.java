package io;

import java.io.File;
import java.nio.file.Path;
import java.util.Queue;

public abstract class FileHandler {
    protected final Path path;

    // CONSTRUCTORS 

    public FileHandler(Path path) {
        this.path = path;
        File file = path.toFile();

        if (!file.isFile())
            throw new IllegalArgumentException("Path does not lead to file.");
        if (!file.canRead() || !file.canWrite())
            throw new IllegalArgumentException("Does not have enough permission to work with the file.");
    }

    // METHODS
    
    public abstract void write(String content);

    public abstract String read();

    public abstract Queue<String> readLines();
}
