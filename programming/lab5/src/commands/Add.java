package commands;

import data.Coordinates;
import data.Difficulty;
import data.EyeColor;
import data.HairColor;
import data.LabWork;
import data.Location;
import data.Person;
import utils.Collection;
import utils.Console;

public class Add extends Command {
    private final Console console;
    private final Collection collection;

    // CONSTRUCTORS
    
    public Add(Console console, Collection collection) {
        super(
            "add", 
            new String[0], 
            "Add a new element to the collection"
        );

        this.console = console;
        this.collection = collection;
    }

    // METHODS

    @Override
    public void execute(String[] args) {
        if (args.length != 0) 
            throw new IllegalArgumentException("Unexpected arguments occurred");

        String input;
        LabWork.Builder lwBuilder = new LabWork.Builder();
        
        while (true) {
            try {
                console.print("Enter the name: ");
                input = console.readln();
                lwBuilder.setName(input);
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        Coordinates.Builder coordsBuilder = new Coordinates.Builder();

        while (true) {
            try {
                console.print("Enter the X coordinate: ");
                input = console.readln();
                coordsBuilder.setX(Integer.parseInt(input));
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
                console.print("Enter the Y coordinate: ");
                input = console.readln();
                coordsBuilder.setY(Float.parseFloat(input));
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Y coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        lwBuilder.setCoordinates(coordsBuilder.build());

        while (true) {
            try {
                console.print("Enter the minimal point: ");
                input = console.readln();
                lwBuilder.setMinimalPoint(Long.parseLong(input));
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
                console.print("Enter the difficulty (");
                for (int i = 0; i < Difficulty.values().length; i++) {
                    console.print(Difficulty.values()[i].toString());
                    if (i < Difficulty.values().length - 1)
                        console.print(", ");
                }
                console.print("): ");
                input = console.readln();
                lwBuilder.setDifficulty(Difficulty.valueOf(input));
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        Person.Builder personBuilder = new Person.Builder();

        while (true) {
            try {
                console.print("Enter the author's name: ");
                input = console.readln();
                personBuilder.setName(input);
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                console.print("Enter the author's weight: ");
                input = console.readln();
                personBuilder.setWeight(Float.parseFloat(input));
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
                console.print("Enter the author's eye color (");
                for (int i = 0; i < EyeColor.values().length; i++) {
                    console.print(EyeColor.values()[i].toString());
                    if (i < EyeColor.values().length - 1)
                        console.print(", ");
                }
                console.print("): ");
                input = console.readln();
                personBuilder.setEyeColor(EyeColor.valueOf(input));
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                console.print("Enter the author's hair color (");
                for (int i = 0; i < HairColor.values().length; i++) {
                    console.print(HairColor.values()[i].toString());
                    if (i < HairColor.values().length - 1)
                        console.print(", ");
                }
                console.print("): ");
                input = console.readln();
                personBuilder.setHairColor(HairColor.valueOf(input));
                break;
            }
            catch (IllegalArgumentException|NullPointerException e) {
                console.println(e.getMessage());
            }
        }

        Location.Builder locationBuilder = new Location.Builder();

        while (true) {
            try {
                console.print("Enter the location's X coordinate: ");
                input = console.readln();
                locationBuilder.setX(Double.parseDouble(input));
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
                console.print("Enter the location's Y coordinate: ");
                input = console.readln();
                locationBuilder.setY(Double.parseDouble(input));
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
                console.print("Enter the location's Z coordinate: ");
                input = console.readln();
                locationBuilder.setZ(Double.parseDouble(input));
                break;
            }
            catch (NumberFormatException|NullPointerException e) {
                console.println("Z coordinate must be a number");
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        while (true) {
            try {
                console.print("Enter the location's name: ");
                input = console.readln();
                locationBuilder.setName(input);
                break;
            }
            catch (IllegalArgumentException e) {
                console.println(e.getMessage());
            }
        }

        personBuilder.setLocation(locationBuilder.build());

        lwBuilder.setAuthor(personBuilder.build());

        collection.add(lwBuilder.build());
    }
}
