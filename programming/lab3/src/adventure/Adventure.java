package adventure;

import java.util.ArrayList;

import characters.Adventurer;
import characters.Person;
import containers.Container;
import exceptions.EndOfRoadException;
import exceptions.NoFoodInHandException;
import roads.Road;
import roads.RoadPart;
import roads.RoadType;
import transport.Transport;

@SuppressWarnings("rawtypes")
public class Adventure {
    protected ArrayList<Person> persons;
    protected Road road;
    protected Transport transport;
    protected Container container;

    public Adventure(Person persons, Road road, Transport transport, Container container) {
        this.persons = new ArrayList<Person>();
        this.persons.add(persons);
        this.road = road;
        this.transport = transport;
        this.container = container;
    }

    public Adventure(Iterable<Person> persons, Road road, Transport transport, Container container) {
        this.persons = new ArrayList<Person>();
        for (Person person : persons) {
            this.persons.add(person);
        }
        this.road = road;
        this.transport = transport;
        this.container = container;
    }

    public void start() {
        road.reset();

        for (Person person : persons) {
            if (person instanceof Adventurer) continue;
            try {
                person.say();
                person.hand.takeFrom(container);
                person.eat();
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

                for (Person person : persons) {
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
