package utils;

import data.*;

public class DataBuilder {
    private final Console console;
    private final Collection collection;
    
    // CONSTRUCTORS

    public DataBuilder(Console console, Collection collection) {
        this.console = console;
        this.collection = collection;
    }

    // METHODS

    public LabWork buildLabWork() {
        LabWork.Builder lwBuilder = new LabWork.Builder();
        
        while (true) {
            try {
                lwBuilder.setName(
                    getString("Enter the name: ")
                );
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                lwBuilder.setMinimalPoint(
                    getLong("Enter the minimal point: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Minimal point must be an integer");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                lwBuilder.setDifficulty(
                    getEnum(Difficulty.class, "Enter the difficulty (" + String.join(", ", Difficulty.getValues()) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        return lwBuilder.setCoordinates(buildCoordinates())
                        .setAuthor(buildPerson())
                        .build();
    }

    public Coordinates buildCoordinates() {
        Coordinates.Builder coordsBuilder = new Coordinates.Builder();

        while (true) {
            try {
                coordsBuilder.setX(
                    getInt("Enter the X coordinate: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("X coordinate must be an integer");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                coordsBuilder.setY(
                    getFloat("Enter the Y coordinate: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Y coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        return coordsBuilder.build();
    }

    public Location buildLocation() {
        Location.Builder locationBuilder = new Location.Builder();

        while (true) {
            try {
                locationBuilder.setName(
                    getString("Enter the location's name: ")
                );
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }


        while (true) {
            try {
                locationBuilder.setX(
                    getDouble("Enter the location's X coordinate: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("X coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                locationBuilder.setY(
                    getDouble("Enter the location's Y coordinate: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Y coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                locationBuilder.setZ(
                    getDouble("Enter the location's Z coordinate: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Z coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        return locationBuilder.build();
    }

    public Person buildPerson() {
        Person.Builder personBuilder = new Person.Builder();

        while (true) {
            try {
                personBuilder.setName(
                    getString("Enter the person's name: ")
                );
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                personBuilder.setWeight(
                    getFloat("Enter the person's weight: ")
                );
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Weight must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                personBuilder.setEyeColor(
                    getEnum(EyeColor.class, "Enter the person's eye color (" + String.join(", ", EyeColor.getValues()) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                personBuilder.setHairColor(
                    getEnum(HairColor.class, "Enter the person's hair color (" + String.join(", ", HairColor.getValues()) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        return personBuilder.setLocation(buildLocation())
                            .build();

    }

    public String getString(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return console.readln();
    }

    public int getInt(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return Integer.parseInt(console.readln());
    }

    public long getLong(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return Long.parseLong(console.readln());
    }

    public float getFloat(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return Float.parseFloat(console.readln());
    }

    public double getDouble(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return Double.parseDouble(console.readln());
    }

    public <T extends Enum<T>> T getEnum(Class<T> enumType, String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return Enum.valueOf(enumType, console.readln().toUpperCase());
    }
}
