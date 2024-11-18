package roads;

public record RoadPart(String description, RoadType roadType) {
    @Override
    public String toString() {
        return description;
    }
}
