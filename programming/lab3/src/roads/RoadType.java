package roads;

public enum RoadType {
    UPHILL(0.5),
    DOWNHILL(2),
    STRAIGHT(1);

    private final double speedMultiplier;

    RoadType(double speedMultiplier) {
        this.speedMultiplier = speedMultiplier;
    }

    public double getSpeedMultiplier() {
        return speedMultiplier;
    }
}
