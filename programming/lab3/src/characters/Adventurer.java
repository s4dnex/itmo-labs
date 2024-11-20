package characters;

import java.util.Objects;

import roads.RoadType;

public class Adventurer extends Character implements Thinkable {
    public Adventurer() {
        this.name = "Unknown adventurer";
    }

    public Adventurer(String name) {
        super(name);
    }

    public void think(RoadType roadType) {
        if (roadType == RoadType.UPHILL) {
            System.out.println(name + " thinks that he/she is on the edge of the world now.");
        }
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Adventurer adventurer = (Adventurer) obj;
        return this.name.equals(adventurer.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
