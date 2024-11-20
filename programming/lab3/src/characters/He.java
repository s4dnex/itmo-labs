package characters;

import containers.Container;
import exceptions.NoFoodInHandException;
import food.Edible;

public class He extends Character implements Speaks {
    public Hand hand = new Hand();

    public He() {
        super("He");
    }

    public void say() {
        System.out.printf("%s said something.\n", name);
    }

    public void say(String words) {
        System.out.printf("%s said: \"%s\".\n", name, words);
    }
    

    public void eat() throws NoFoodInHandException {
        if (hand.item != null && hand.item instanceof Edible)
            System.out.printf("%s ate %s.\n", name, hand.item.toString());
        else
            throw new NoFoodInHandException(name + " does not have any food in his/her hand.", hand.item);
    }

    public class Hand {
        Object item;

        @SuppressWarnings("rawtypes")
        public void takeFrom(Container container) {
            item = container.getRandomItem();
            System.out.printf("%s took out %s from %s.\n", name, item.toString(), container.toString());
        }
    }
}
