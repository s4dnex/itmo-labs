package adventure;

import java.util.ArrayList;

import characters.Adventurer;
import characters.He;
import characters.Character;
import containers.Container;
import exceptions.EndOfRoadException;
import exceptions.NoFoodInHandException;
import roads.Road;
import roads.RoadPart;
import roads.RoadType;
import transport.Transport;

@SuppressWarnings("rawtypes")
public class Adventure {
    protected ArrayList<Character> persons;
    protected Road road;
    protected Transport transport;
    protected Container container;

    public Adventure(Character persons, Road road, Transport transport, Container container) {
        this.persons = new ArrayList<Character>();
        this.persons.add(persons);
        this.road = road;
        this.transport = transport;
        this.container = container;
    }

    public Adventure(Iterable<Character> persons, Road road, Transport transport, Container container) {
        this.persons = new ArrayList<Character>();
        for (Character person : persons) {
            this.persons.add(person);
        }
        this.road = road;
        this.transport = transport;
        this.container = container;
    }

    public void start() {
        if (!road.isRoadLeft())
            road = Road.getRandomRoad();

        for (Character person : persons) {
            if (!(person instanceof He)) continue;
            try {
                He he = (He) person;
                he.say();
                he.hand.takeFrom(container);
                he.eat();
            }
            catch (NoFoodInHandException e) {
                System.out.println(e.getMessage());
            }
            catch (IllegalArgumentException e) {
                System.out.println(person + " could not take an item from " + container + " because it was empty.");
            }
        }

        while (true) {
            try {
                RoadPart currentRoadPart = road.getNextPart();
                RoadType currentRoadType = currentRoadPart.roadType();

                System.out.printf("Current part of road is %s.\n", currentRoadPart);
                transport.move(currentRoadType);

                for (Character person : persons) {
                    if (person instanceof Adventurer) {
                        ((Adventurer) person).think(currentRoadType);
                    }
                }
            }
            catch (EndOfRoadException e) {
                break;
            }
        }
    }
}
