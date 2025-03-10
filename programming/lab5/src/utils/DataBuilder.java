package utils;

import data.*;

public class DataBuilder {
    private final Console console;
    
    // CONSTRUCTORS

    public DataBuilder(Console console) {
        this.console = console;
    }

    // METHODS

    public LabWork buildLabWork() {
        LabWork.Builder lwBuilder = new LabWork.Builder();
        
        while (true) {
            try {
                lwBuilder.setName(
                    getString("Enter the labwork's name: ")
                );
                break;
            }
            catch (Exception e) {
                handleException("Name cannot be null or empty!");
            }
        }

        while (true) {
            try {
                lwBuilder.setMinimalPoint(
                    getLong("Enter the labwork's minimal point: ")
                );
                break;
            }
            catch (NumberFormatException e) {
                handleException("Minimal point must be a long integer greater than 0!");
            }
        }

        while (true) {
            try {
                lwBuilder.setDifficulty(
                    getEnum(Difficulty.class, "Enter the labwork's difficulty (" + Formatter.getEnumValues(Difficulty.class) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("Difficulty must be one if available values!");
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
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("X coordinate must be an integer!");
            }
        }

        while (true) {
            try {
                coordsBuilder.setY(
                    getFloat("Enter the Y coordinate: ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("Y coordinate must be a float number!");
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
                handleException("Name can't be null or empty!");
            }
        }


        while (true) {
            try {
                locationBuilder.setX(
                    getDouble("Enter the location's X coordinate: ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("X coordinate must be a double number!");
            }
        }

        while (true) {
            try {
                locationBuilder.setY(
                    getDouble("Enter the location's Y coordinate: ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("Y coordinate must be a double number!");
            }
        }

        while (true) {
            try {
                locationBuilder.setZ(
                    getDouble("Enter the location's Z coordinate: ")
                );
                break;
            }
            catch (NullPointerException|IllegalArgumentException e) {
                handleException("Z coordinate must be a double number!");
            }
        }

        return locationBuilder.build();
    }

    public Person buildPerson() {
        Person.Builder personBuilder = new Person.Builder();

        while (true) {
            try {
                personBuilder.setName(
                    getString("Enter the person's name (if you want to skip, enter the blank line): ")
                );
                break;
            }
            catch (IllegalArgumentException e) {
                return null;
                // handleException("Name can't be null or empty!");
            }
        }

        while (true) {
            try {
                personBuilder.setWeight(
                    getFloat("Enter the person's weight: ")
                );
                break;
            }
            catch (NullPointerException|IllegalArgumentException e) {
                handleException("Weight must be a float number greater than 0!");
            }
        }

        while (true) {
            try {
                personBuilder.setEyeColor(
                    getEnum(EyeColor.class, "Enter the person's eye color (" + Formatter.getEnumValues(EyeColor.class) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("Eye color must be one of available values or null!");
            }
        }

        while (true) {
            try {
                personBuilder.setHairColor(
                    getEnum(HairColor.class, "Enter the person's hair color (" + Formatter.getEnumValues(HairColor.class) + "): ")
                );
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                handleException("Hair color must be one if available values!");
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

    public Integer getInt(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null) 
            return null;
        return Integer.parseInt(line);
    }

    public Long getLong(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null) 
            return null;
        return Long.parseLong(line);
    }

    public Float getFloat(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null)
            return null;
        return Float.parseFloat(line);
    }

    public Double getDouble(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);

        String line = console.readln();
        if (line == null)
            return null;
        return Double.parseDouble(line);
    }

    public <T extends Enum<T>> T getEnum(Class<T> enumType, String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null || line.isBlank()) 
            return null;
        else 
            return Enum.valueOf(enumType, line.toUpperCase());
    }

    private void handleException(String msg) {
        if (console.isInteractiveMode()) 
            console.println(msg);
        else throw new RuntimeException(msg);
    }
}
