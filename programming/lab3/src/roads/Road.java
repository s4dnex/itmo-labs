package roads;

import java.util.ArrayList;
import java.util.Objects;
import java.util.Random;

import exceptions.EndOfRoadException;

public class Road {
    protected ArrayList<RoadPart> road;
    protected int currentPosition = -1;

    public Road() {
        this.road = new ArrayList<>();
        road.add(new RoadPart("downhill road", RoadType.DOWNHILL));
        road.add(new RoadPart("uphill road", RoadType.UPHILL));
        road.add(new RoadPart("straight road", RoadType.STRAIGHT));
    }

    public Road(RoadPart roadPart) {
        this();
        this.road.add(roadPart);
    }

    public Road(Iterable<RoadPart> road) {
        this();
        for (RoadPart part : road) {
            this.road.add(part);
        }
    }

    public static Road getRandomRoad() {
        ArrayList<RoadPart> roadParts = new ArrayList<RoadPart>();
        for (int i = 0; i < new Random().nextInt(10); i++) {
            roadParts.add(RoadPart.getRandomRoadPart());
        }
        return new Road(roadParts);
    }

    public RoadPart getCurrentPart() {
        return road.get(currentPosition);
    }

    public boolean isRoadLeft() {
        return (currentPosition + 1) < road.size();
    }

    public RoadPart getNextPart() throws EndOfRoadException {
        if (isRoadLeft()) {
            currentPosition++;
            return getCurrentPart();
        }
        throw new EndOfRoadException(this);
    }

    public void reset() {
        currentPosition = -1;
    }

    @Override
    public String toString() {
        String str = "Road consists of following parts:\n";
        for (int i = 0; i < road.size(); i++) {
            str += road.get(i).toString() + "\n";
        }
        return str;
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Road road = (Road) obj;
        return this.road.equals(road.road);
    }

    @Override
    public int hashCode() {
        return Objects.hash(road);
    }
}
