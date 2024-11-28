package characters;

import containers.Container;

@SuppressWarnings("rawtypes")
public interface HasHand {
    public void takeFrom(Container container);

    public class Hand {
        Object item;

        public void takeFrom(Container container) {
            item = container.getRandomItem();
        }
    }
}
