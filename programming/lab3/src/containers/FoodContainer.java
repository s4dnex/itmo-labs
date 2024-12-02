package containers;

import food.Edible;
import other.Color;

public class FoodContainer extends Container<Edible> {
    public FoodContainer() {
        super();
    }
    
    public FoodContainer(Edible item) {
        super(item);
    }

    public FoodContainer(Edible item, Color color) {
        super(item, color);
    }

    public FoodContainer(Iterable<Edible> items) {
        super(items);
    }

    public FoodContainer(Iterable<Edible> items, Color color) {
        super(items, color);
    }

    @Override
    public String toString() {
        return super.toString() + " for food";
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        FoodContainer foodContainer = (FoodContainer) obj;
        return super.equals(foodContainer);
    }

    @Override
    public int hashCode() {
        return super.hashCode();
    }
}
