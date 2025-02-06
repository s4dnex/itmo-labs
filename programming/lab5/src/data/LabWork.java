package data;

import java.time.LocalDateTime;

public class LabWork {
    private static long lastId = 0;
    private Long id; // != null, > 0, unique, auto
    private String name; // != null, != empty
    private Coordinates coordinates; // != null
    private LocalDateTime creationDate; // != null, auto
    private Long minimalPoint; // > 0
    private Difficulty difficulty; // != null
    private Person author;

    // CONSTRUCTORS

    public LabWork(String name, Coordinates coordinates, Long minimalPoint, Difficulty difficulty, Person author) {
        setName(name);
        setCoordinates(coordinates);
        setMinimalPoint(minimalPoint);
        setDifficulty(difficulty);
        setAuthor(author);

        // If everything above is OK
        setId();
        setCreationDate();
    }

    // GETTERS

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public LocalDateTime getCreationDate() {
        return creationDate;
    }

    public Long getMinimalPoint() {
        return minimalPoint;
    }

    public Difficulty getDifficulty() {
        return difficulty;
    }

    public Person getAuthor() {
        return author;
    }

    // SETTERS

    private void setId() {
        this.id = ++lastId;
    }

    protected void setName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be null or empty");
        }
        this.name = name;
    }

    protected void setCoordinates(Coordinates coordinates) {
        if (coordinates == null) {
            throw new IllegalArgumentException("Coordinates cannot be null");
        }
        this.coordinates = coordinates;
    }

    private void setCreationDate() {
        this.creationDate = LocalDateTime.now();
    }

    protected void setMinimalPoint(Long minimalPoint) {
        if (minimalPoint != null && minimalPoint <= 0) {
            throw new IllegalArgumentException("Minimal point must be greater than 0");
        }
        this.minimalPoint = minimalPoint;
    }

    protected void setDifficulty(Difficulty difficulty) {
        if (difficulty == null) {
            throw new IllegalArgumentException("Difficulty cannot be null");
        }
        this.difficulty = difficulty;
    }

    protected void setAuthor(Person author) {
        this.author = author;
    }
}
