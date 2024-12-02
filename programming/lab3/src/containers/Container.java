package containers;

import java.util.ArrayList;
import java.util.Objects;
import java.util.Random;

import other.Color;

public abstract class Container<T> {
    protected ArrayList<T> items;
    protected Color color;

    public Container() {
        this.items = new ArrayList<T>();
        this.color = Color.getRandomColor();
    }

    public Container(T item) {
        this();
        this.items.add(item);
    }

    public Container(T item, Color color) {
        this(item);
        this.color = color;
    }

    public Container(Iterable<T> items) {
        this();
        for (T item : items) {
            this.items.add(item);
        }
    }

    public Container(Iterable<T> items, Color color) {
        this(items);
        this.color = color;
    }

    public T getRandomItem() throws IndexOutOfBoundsException{
        try {
            int index = new Random().nextInt(items.size());
            T item = items.get(index);
            items.remove(index);
            return item;    
        }
        catch (Exception e) {
            throw new IndexOutOfBoundsException();
        }
    }

    public void add(T item) {
        this.items.add(item);
    }
    
    @Override
    public String toString() {
        return color.toString() + " container";
    }

    @Override
    @SuppressWarnings("rawtypes")
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Container container = (Container) obj;
        return this.items.equals(container.items) &&
               this.color.equals(container.color);
    }

    @Override
    public int hashCode() {
        return Objects.hash(items, color);
    }
}
