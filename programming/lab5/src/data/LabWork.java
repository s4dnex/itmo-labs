package data;

import java.time.LocalDateTime;

import json.JsonHandler;

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

    public static boolean validateName(String name) {
        if (name == null || name.isBlank())
            return false;
        return true;
    }

    public static boolean validateCoordinates(Coordinates coordinates) {
        if (coordinates == null)
            return false;
        return true;
    }

    public static boolean validateMinimalPoint(Long minimalPoint) {
        if (minimalPoint != null && minimalPoint <= 0)
            return false;
        return true;
    }

    public static boolean validateDifficulty(Difficulty difficulty) {
        if (difficulty == null)
            return false;
        return true;
    }

    public static boolean validateAuthor(Person author) {
        return true;
    }

    @Override
    public int compareTo(LabWork labWork) {
        return this.difficulty == labWork.difficulty ?
                this.minimalPoint.compareTo(labWork.minimalPoint) :
                this.difficulty.compareTo(labWork.difficulty);

    }

    @Override
    public String toString() {      
        return "LabWork " + JsonHandler.getGson().toJson(this);
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
            if (validateName(name)) {
                this.name = name;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setCoordinates(Coordinates coordinates) {
            if (validateCoordinates(coordinates)) {
                this.coordinates = coordinates;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setMinimalPoint(Long minimalPoint) {
            if (validateMinimalPoint(minimalPoint)) {
                this.minimalPoint = minimalPoint;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setDifficulty(Difficulty difficulty) {
            if (validateDifficulty(difficulty)) {
                this.difficulty = difficulty;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setAuthor(Person author) {
            if (validateAuthor(author)) {
                this.author = author;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public LabWork build() {
            if (validateName(name) &&
                validateCoordinates(coordinates) &&
                validateMinimalPoint(minimalPoint) &&
                validateDifficulty(difficulty) &&
                validateAuthor(author)
            )
                return new LabWork(this);
            throw new IllegalArgumentException("Invalid LabWork parameters");
        }
    }
}
