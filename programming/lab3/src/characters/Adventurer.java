package characters;

import java.util.Objects;

import other.Thinkable;


public class Adventurer extends Character implements CanThink {
    public Adventurer() {
        this.name = "Unknown adventurer";
    }

    public Adventurer(String name) {
        super(name);
    }

    @Override
    public void thinkAbout(Thinkable obj) {
        System.out.printf("%s thinks that %s.\n", name, obj.getThought());
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Adventurer adventurer = (Adventurer) obj;
        return this.name.equals(adventurer.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
