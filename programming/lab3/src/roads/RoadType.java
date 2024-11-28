package roads;

import java.util.Random;

import other.Thinkable;

public enum RoadType implements Thinkable {
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

    @Override
    public String getThought() {
        switch (this) {
            case UPHILL:
                return "this is the edge of the world";

            case DOWNHILL:
                return "this road is going to be easy";
            
            case STRAIGHT:
                return "this is just a straight road";
            
            default:
                return "this is a completely unknown road";
        }
    }

    public double getSpeedMultiplier() {
        return speedMultiplier;
    }


}
