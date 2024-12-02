import java.util.Arrays;
import java.util.Random;

import food.Flavor;
import food.Icecream;
import other.Color;
import roads.Road;
import transport.Car;
import adventure.Adventure;
import characters.Adventurer;
import characters.He;
import containers.FoodContainer;

public class Main {
    public static void main(String[] args) {
        He he = new He();
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

        for (int i = 0; i < new Random().nextInt(1, 5); i++) {
            adventure.start();
            adventure.updateRoad();
            System.out.println();         
        }
    }
}