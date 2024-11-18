package food;

import java.util.Random;

public enum Flavor {
    VANILLA("vanilla"),
    CHOCOLATE("chocolate"),
    CARAMEL("caramel"),
    FRUIT("fruit"),
    BERRY("berry");

    private final String name;

    Flavor(String name) {
        this.name = name;
    }

    public static Flavor getRandomFlavor() {
        return values()[new Random().nextInt(values().length)];
    }

    @Override
    public String toString() {
        return name;
    }
}
