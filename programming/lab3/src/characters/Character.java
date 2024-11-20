package characters;

import java.util.Objects;

public abstract class Character {
    protected String name;

    public Character() {
        this.name = "Unknown";
    }
    
    public Character(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Character person = (Character) obj;
        return this.name.equals(person.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
