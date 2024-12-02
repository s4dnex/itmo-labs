package characters;

import java.util.Objects;

import containers.Container;

@SuppressWarnings("rawtypes")
public interface HasHand {
    public void takeFrom(Container container);

    public class Hand {
        Object item;

        public void takeFrom(Container container) {
            item = container.getRandomItem();
        }

        @Override
        public String toString() {
            return "Hand with " + item.toString();
        }

        @Override
        public boolean equals(Object obj) {
            if (this.getClass() != obj.getClass()) 
                return false;
            
            Hand hand = (Hand) obj;
            return this.item.equals(hand.item);
        }

        @Override
        public int hashCode() {
            return Objects.hash(item);
        }
    }
}
