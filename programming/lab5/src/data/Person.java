package data;

public class Person {
    private String name; // != null, != empty
    private float weight; // > 0
    private EyeColor eyeColor; 
    private HairColor hairColor; // != null
    private Location location; // != null

    // CONSTRUCTORS

    public Person(String name, float weight, EyeColor eyeColor, HairColor hairColor, Location location) {
        setName(name);
        setWeight(weight);
        setEyeColor(eyeColor);
        setHairColor(hairColor);
        setLocation(location);
    }

    // GETTERS

    public String getName() {
        return name;
    }

    public float getWeight() {
        return weight;
    }

    public EyeColor getEyeColor() {
        return eyeColor;
    }

    public HairColor getHairColor() {
        return hairColor;
    }

    public Location getLocation() {
        return location;
    }

    // SETTERS

    protected void setName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be null or empty");
        }
        this.name = name;
    }

    protected void setWeight(float weight) {
        if (weight <= 0) {
            throw new IllegalArgumentException("Weight must be greater than 0");
        }
        this.weight = weight;
    }

    protected void setEyeColor(EyeColor eyeColor) {   
        this.eyeColor = eyeColor;
    }

    protected void setHairColor(HairColor hairColor) {
        if (hairColor == null) {
            throw new IllegalArgumentException("Hair color cannot be null");
        }
        this.hairColor = hairColor;
    }

    protected void setLocation(Location location) {
        if (location == null) {
            throw new IllegalArgumentException("Location cannot be null");
        }
        this.location = location;
    }
}