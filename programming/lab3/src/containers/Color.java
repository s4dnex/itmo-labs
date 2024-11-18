package containers;

import java.util.Random;

public enum Color {
    RED("red"),
    GREEN("green"),
    BLUE("blue");

    private final String name;

    Color(String name) {
        this.name = name;
    }

    public static Color getRandomColor() {
        return values()[new Random().nextInt(values().length)];
    }

    @Override
    public String toString() {
        return name;
    }
}
