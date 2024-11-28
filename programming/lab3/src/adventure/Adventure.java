package adventure;

import java.util.ArrayList;

import characters.CanEat;
import characters.CanSay;
import characters.CanThink;
import characters.Character;
import characters.HasHand;
import containers.Container;
import exceptions.EndOfRoadException;
import exceptions.NoFoodAvailableException;
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
            if (person instanceof CanSay) {
                ((CanSay) person).say();
            }
            
            if (person instanceof HasHand && person instanceof CanEat)
                try {
                    ((HasHand) person).takeFrom(container);
                    ((CanEat) person).eat();
                }
                catch (NoFoodAvailableException e) {
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
                    if (person instanceof CanThink) {
                        ((CanThink) person).thinkAbout(currentRoadType);
                    }
                }
            }
            catch (EndOfRoadException e) {
                break;
            }
        }
    }
}
