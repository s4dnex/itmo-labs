package roads;

import java.util.Random;

public enum RoadType {
    UPHILL(0.5),
    DOWNHILL(2),
    STRAIGHT(1);

    private final double speedMultiplier;

    RoadType(double speedMultiplier) {
        this.speedMultiplier = speedMultiplier;
    }

    public static RoadType getRandomRoadType() {
        return values()[new Random().nextInt(values().length)];
    }

    public double getSpeedMultiplier() {
        return speedMultiplier;
    }
}
