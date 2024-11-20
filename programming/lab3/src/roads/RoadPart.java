package roads;

public record RoadPart(String description, RoadType roadType) {
    public static RoadPart getRandomRoadPart() {
        RoadType roadType = RoadType.getRandomRoadType();
        return new RoadPart(roadType.name().toLowerCase() + " road", roadType);
    }

    @Override
    public String toString() {
        return description;
    }
}
