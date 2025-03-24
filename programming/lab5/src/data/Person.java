package data;

import json.JsonHandler;

public class Person implements Comparable<Person> {
    private String name; // != null, != empty
    private float weight; // > 0
    private EyeColor eyeColor; 
    private HairColor hairColor; // != null
    private Location location; // != null

    // CONSTRUCTORS

    /**
     * @param builder {@link Builder}
     */
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
        return "Person " + JsonHandler.getGson().toJson(this);
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass())
            return false;
        
        Person person = (Person) obj;
        return this.name.equals(person.name) &&
               this.weight == person.weight &&
               this.eyeColor.equals(person.eyeColor) &&
               this.hairColor.equals(person.hairColor) &&
               this.location.equals(person.location);
    }

    // INNER CLASSES

    /**
     * Class to build {@link Person}.
     */
    public static class Builder {
        private String name;
        private float weight;
        private EyeColor eyeColor;
        private HairColor hairColor;
        private Location location;

        // METHODS
        
        /**
         * Sets value of field {@code name}.
         * @param name name
         * @return {@link Builder} instance
         */
        public Builder setName(String name) {
            if (validateName(name)) {
                this.name = name;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code weight}.
         * @param weight weight
         * @return {@link Builder} instance
         */
        public Builder setWeight(float weight) {
            if (validateWeight(weight)) {
                this.weight = weight;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code eyeColor}.
         * @param eyeColor {@link EyeColor}
         * @return {@link Builder} instance
         */
        public Builder setEyeColor(EyeColor eyeColor) {
            if (validateEyeColor(eyeColor)) {
                this.eyeColor = eyeColor;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code hairColor}.
         * @param hairColor {@link HairColor}
         * @return {@link Builder} instance
         */
        public Builder setHairColor(HairColor hairColor) {
            if (validateHairColor(hairColor)) {
                this.hairColor = hairColor;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code location}.
         * @param location {@link Location}
         * @return {@link Builder} instance
         */
        public Builder setLocation(Location location) {
            if (validateLocation(location)) {
                this.location = location;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Returns new {@link Person} instance with set fields.
         * @return {@link Person} 
         */
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