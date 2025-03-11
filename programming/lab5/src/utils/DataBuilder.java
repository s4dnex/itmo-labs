package utils;

import data.*;

/**
 * Class to build data for collection.
 */
public class DataBuilder {
    private final Console console;
    
    // CONSTRUCTORS

    /**
     * @param console Class to handle input and output
     */
    public DataBuilder(Console console) {
        this.console = console;
    }

    // METHODS

    /**
     * Method to set fields and build {@link LabWork}.
     * @return LabWork instance
     */
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

    /**
     * Method to set fields and build {@link Coordinates}.
     * @return Coordinates instance
     */
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

    /**
     * Method to set fields and build {@link Location}.
     * @return Location instance
     */
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

    /**
     * Method to set fields and build {@link Person}.
     * @return Person instance
     */
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

    /**
     * Method to receive {@link String} from input.
     * @param prompt Text to request field
     * @return {@link String} (or {@code null})
     */
    public String getString(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        return console.readln();
    }

    /**
     * Method to receive {@link Integer} from input.
     * @param prompt Text to request field
     * @return {@link Integer} (or {@code null})
     */
    public Integer getInt(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null) 
            return null;
        return Integer.parseInt(line);
    }

    /**
     * Method to receive {@link Long} from input.
     * @param prompt Text to request field
     * @return {@link Long} (or {@code null})
     */
    public Long getLong(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null) 
            return null;
        return Long.parseLong(line);
    }

    /**
     * Method to receive {@link Float} from input.
     * @param prompt Text to request field
     * @return {@link Float} (or {@code null})
     */
    public Float getFloat(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null)
            return null;
        return Float.parseFloat(line);
    }

    /**
     * Method to receive {@link Double} from input.
     * @param prompt Text to request field
     * @return {@link Double} (or {@code null})
     */
    public Double getDouble(String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);

        String line = console.readln();
        if (line == null)
            return null;
        return Double.parseDouble(line);
    }

    /**
     * Method to receive one of {@link Enum} values from input.
     * @param prompt Text to request field
     * @return One of {@link Enum} values (or {@code null})
     */
    public <T extends Enum<T>> T getEnum(Class<T> enumType, String prompt) {
        if (console.isInteractiveMode())
            console.print(prompt);
        
        String line = console.readln();
        if (line == null || line.isBlank()) 
            return null;
        else 
            return Enum.valueOf(enumType, line.toUpperCase());
    }

    /**
     * Method to handle exception with given message. Prints message to console if {@link Console} in interactive mode, throws {@link RuntimeException} if {@link Console} in script mode.
     * @param msg Message from exception
     */
    private void handleException(String msg) {
        if (console.isInteractiveMode()) 
            console.println(msg);
        else throw new RuntimeException(msg);
    }
}
