package characters;

import exceptions.NoFoodAvailableException;

public interface CanEat {
    public void eat() throws NoFoodAvailableException;
}
