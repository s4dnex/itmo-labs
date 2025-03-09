package data;

import json.JsonHandler;

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

    public static boolean validateName(String name) {
        if (name == null || name.isBlank())
            return false;
        return true;
    }

    public static boolean validateWeight(float weight) {
        if (weight <= 0)
            return false;
        return true;
    }

    public static boolean validateEyeColor(EyeColor eyeColor) {   
        return true;
    }

    public static boolean validateHairColor(HairColor hairColor) {
        if (hairColor == null)
            return false;
        return true;
    }

    public static boolean validateLocation(Location location) {
        if (location == null)
            return false;
        return true;
    }

    @Override
    public int compareTo(Person person) {
        return name.compareTo(person.getName());
    }

    @Override
    public String toString() {
        return JsonHandler.getGson().toJson(this);
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
            if (validateName(name)) {
                this.name = name;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setWeight(float weight) {
            if (validateWeight(weight)) {
                this.weight = weight;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setEyeColor(EyeColor eyeColor) {
            if (validateEyeColor(eyeColor)) {
                this.eyeColor = eyeColor;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setHairColor(HairColor hairColor) {
            if (validateHairColor(hairColor)) {
                this.hairColor = hairColor;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Builder setLocation(Location location) {
            if (validateLocation(location)) {
                this.location = location;
                return this;
            }
            throw new IllegalArgumentException();
        }

        public Person build() {
            if (validateName(name) && 
                validateWeight(weight) &&
                validateHairColor(hairColor) && 
                validateLocation(location)
            )
                return new Person(this);
            else throw new IllegalArgumentException("Invalid Person parameters");
        }
    }
}