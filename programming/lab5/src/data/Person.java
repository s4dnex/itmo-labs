package data;

import utils.Formatter;

public class Person implements Comparable<Person> {
    private String name; // != null, != empty
    private float weight; // > 0
    private EyeColor eyeColor; 
    private HairColor hairColor; // != null
    private Location location; // != null

    // CONSTRUCTORS

    public Person(Person.Builder builder) {
        this.name = builder.name;
        this.weight = builder.weight;
        this.eyeColor = builder.eyeColor;
        this.hairColor = builder.hairColor;
        this.location = builder.location;
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

    // METHODS

    public static Response validateName(String name) {
        if (name == null || name.isBlank())
            return new Response(false, "Name can't be null or empty");
        return new Response(true);
    }

    public static Response validateWeight(float weight) {
        if (weight <= 0)
            return new Response(false, "Weight must be greater than 0");
        return new Response(true);
    }

    public static Response validateEyeColor(EyeColor eyeColor) {   
        return new Response(true);
    }

    public static Response validateHairColor(HairColor hairColor) {
        if (hairColor == null)
            return new Response(false, "Hair color can't be null");
        return new Response(true);
    }

    public static Response validateLocation(Location location) {
        if (location == null)
            return new Response(false, "Location can't be null");
        return new Response(true);
    }

    @Override
    public int compareTo(Person person) {
        return name.compareTo(person.getName());
    }

    @Override
    public String toString() {
        return Formatter.getStringsWithIndent(
            "Person {",
            " name: " + name,
            " weight: " + weight,
            " eyeColor: " + eyeColor,
            " hairColor: " + hairColor,
            " location: " + location,
            "}"            
        );
    }

    // INNER CLASSES

    public static class Builder {
        private String name;
        private float weight;
        private EyeColor eyeColor;
        private HairColor hairColor;
        private Location location;

        // METHODS

        public Builder setName(String name) {
            Response response = validateName(name);
            if (response.getStatus()) {
                this.name = name;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setWeight(float weight) {
            Response response = validateWeight(weight);
            if (response.getStatus()) {
                this.weight = weight;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setEyeColor(EyeColor eyeColor) {
            Response response = validateEyeColor(eyeColor);
            if (response.getStatus()) {
                this.eyeColor = eyeColor;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setHairColor(HairColor hairColor) {
            Response response = validateHairColor(hairColor);
            if (response.getStatus()) {
                this.hairColor = hairColor;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setLocation(Location location) {
            Response response = validateLocation(location);
            if (response.getStatus()) {
                this.location = location;
                return this;
            }
            else throw new IllegalArgumentException(response.getMessage());
        }

        public Person build() {
            if (validateName(name).getStatus() && 
                validateWeight(weight).getStatus() &&
                validateHairColor(hairColor).getStatus() && 
                validateLocation(location).getStatus()
            )
                return new Person(this);
            else throw new IllegalArgumentException("Invalid Person parameters");
        }
    }
}