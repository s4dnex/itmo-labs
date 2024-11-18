import java.util.Arrays;

import food.Flavor;
import food.Icecream;
import roads.Road;
import transport.Car;
import adventure.Adventure;
import characters.Adventurer;
import characters.Person;
import containers.FoodContainer;
import containers.Color;

public class Main {
    public static void main(String[] args) {
        Person he = new Person("He");
        Adventurer adventurer1 = new Adventurer("Adventurer #1");
        Adventurer adventurer2 = new Adventurer("Adventurer #2");

        Road road = new Road();

        Car car = new Car("M-B", "W212", 100);

        FoodContainer foodContainer = new FoodContainer(
            Arrays.asList(new Icecream(Flavor.getRandomFlavor()), 
                          new Icecream(Flavor.getRandomFlavor())), 
            Color.BLUE
        );
        
        Adventure adventure = new Adventure(
            Arrays.asList(he, adventurer1, adventurer2), 
            road, 
            car, 
            foodContainer
        );

        for (int i = 0; i < 3; i++) {
            adventure.start();
            System.out.println();          
        }
    }
}