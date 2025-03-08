package data;

import java.time.LocalDateTime;

import utils.Formatter;

public class LabWork implements Comparable<LabWork> {
    private Long id; // != null, > 0, unique, auto
    private String name; // != null, != empty
    private Coordinates coordinates; // != null
    private LocalDateTime creationDate; // != null, auto
    private Long minimalPoint; // > 0
    private Difficulty difficulty; // != null
    private Person author;

    // CONSTRUCTORS

    public LabWork(LabWork.Builder builder) {
        this.name = builder.name;
        this.coordinates = builder.coordinates;
        this.minimalPoint = builder.minimalPoint;
        this.difficulty = builder.difficulty;
        this.author = builder.author;

        this.creationDate = LocalDateTime.now();
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

    public void setId(long id) {
        this.id = id;
    }

    // METHODS

    public static Response validateName(String name) {
        if (name == null || name.isBlank())
            return new Response(false, "Name cannot be null or empty");
        return new Response(true);
    }

    public static Response validateCoordinates(Coordinates coordinates) {
        if (coordinates == null)
            return new Response(false, "Coordinates cannot be null");
        return new Response(true);
    }

    public static Response validateMinimalPoint(Long minimalPoint) {
        if (minimalPoint != null && minimalPoint <= 0)
            return new Response(false, "Minimal point must be greater than 0");
        return new Response(true);
    }

    public static Response validateDifficulty(Difficulty difficulty) {
        if (difficulty == null)
            return new Response(false, "Difficulty cannot be null");
        return new Response(true);
    }

    public static Response validateAuthor(Person author) {
        return new Response(true);
    }

    @Override
    public int compareTo(LabWork labWork) {
        return this.difficulty == labWork.difficulty ?
                this.minimalPoint.compareTo(labWork.minimalPoint) :
                this.difficulty.compareTo(labWork.difficulty);

    }

    @Override
    public String toString() {      
        return Formatter.getStringsWithIndent(
            "LabWork {",
            "id: " + id,
            "name: " + name,
            "coordinates: " + coordinates,
            "creationDate: " + creationDate.format(Formatter.DATE_FORMAT),
            "minimalPoint: " + minimalPoint,
            "difficulty: " + difficulty,
            "author: " + author,
            "}"
        );
    }

    // INNER CLASSES

    public static class Builder {
        private String name;
        private Coordinates coordinates;
        private Long minimalPoint;
        private Difficulty difficulty;
        private Person author;

        // METHODS

        public Builder setName(String name) {
            Response response = validateName(name);
            if (response.getStatus()) {
                this.name = name;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setCoordinates(Coordinates coordinates) {
            Response response = validateCoordinates(coordinates); 
            if (response.getStatus()) {
                this.coordinates = coordinates;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setMinimalPoint(Long minimalPoint) {
            Response response = validateMinimalPoint(minimalPoint);
            if (response.getStatus()) {
                this.minimalPoint = minimalPoint;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setDifficulty(Difficulty difficulty) {
            Response response = validateDifficulty(difficulty);
            if (response.getStatus()) {
                this.difficulty = difficulty;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setAuthor(Person author) {
            Response response = validateAuthor(author);
            if (response.getStatus()) {
                this.author = author;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public LabWork build() {
            if (validateName(name).getStatus() &&
                validateCoordinates(coordinates).getStatus() &&
                validateMinimalPoint(minimalPoint).getStatus() &&
                validateDifficulty(difficulty).getStatus() &&
                validateAuthor(author).getStatus()
            )
                return new LabWork(this);
            throw new IllegalArgumentException("Invalid LabWork parameters");
        }
    }
}
