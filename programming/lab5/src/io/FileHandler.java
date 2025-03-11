package io;

import java.io.File;
import java.nio.file.Path;
import java.util.Queue;

/**
 * Class to work with files.
 */
public abstract class FileHandler {
    protected final Path path;

    // CONSTRUCTORS 

    /**
     * @param path path to file
     */
    public FileHandler(Path path) {
        this.path = path;
        File file = path.toFile();

        if (!file.isFile())
            throw new IllegalArgumentException("Path does not lead to file.");
        if (!file.canRead() || !file.canWrite())
            throw new IllegalArgumentException("Does not have enough permission to work with the file.");
    }

    // METHODS

    /**
     * Write content to file.
     * @param content data to write
     */
    public abstract void write(String content);

    /**
     * Reads file and returns it as {@link String}.
     * @return data from file
     */
    public abstract String read();

    /**
     * Reads file and returns it as {@link Queue} of {@link String}.
     * @return lines in order
     */
    public abstract Queue<String> readLines();
}
