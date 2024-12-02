package characters;

import java.util.Objects;

import containers.Container;
import exceptions.NoFoodAvailableException;
import food.Edible;

public class He extends Character implements CanSay, HasHand, CanEat {
    protected Hand hand = new Hand();

    public He() {
        super("He");
    }

    public void say() {
        System.out.printf("%s said something.\n", name);
    }

    public void say(String words) {
        System.out.printf("%s said: \"%s\".\n", name, words);
    }
    
    @Override
    @SuppressWarnings("rawtypes")
    public void takeFrom(Container container) throws IllegalArgumentException {
        hand.takeFrom(container);
        System.out.printf("%s took out %s from %s.\n", name, hand.item.toString(), container.toString());
    }

    public void eat() throws NoFoodAvailableException {
        if (hand.item != null && hand.item instanceof Edible)
            System.out.printf("%s ate %s.\n", name, hand.item.toString());
        else
            throw new NoFoodAvailableException(name + " does not have any food in his/her hand.", hand.item);
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        He he = (He) obj;
        return this.name.equals(he.name) &&
                this.hand.equals(he.hand);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name, hand);
    }
}
