package data;

import java.util.Objects;

import json.JsonHandler;

public class Location {
    private Double x; // != null
    private Double y; // != null
    private Double z; // != null
    private String name; // != null, != empty

    // CONSTRUCTORS

    /**
     * @param builder {@link Builder}
     */
    public Location(Location.Builder builder) {
        this.x = builder.x;
        this.y = builder.y;
        this.z = builder.z;
        this.name = builder.name;
    }

    // GETTERS

    public Double getX() {
        return x;
    }

    public Double getY() {
        return y;
    }

    public Double getZ() {
        return z;
    }

    public String getName() {
        return name;
    }

    // METHODS

    public static boolean validateX(Double x) {
        if (x == null)
            return false;
        return true;
    }

    public static boolean validateY(Double y) {
        if (y == null)
            return false;
        return true;
    }

    public static boolean validateZ(Double z) {
        if (z == null)
            return false;
        return true;
    }

    public static boolean validateName(String name) {
        if (name == null || name.isBlank())
            return false;
        return true;
    }

    @Override
    public String toString() {
        return "Location " + JsonHandler.getGson().toJson(this);
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass())
            return false;
        
        Location loc = (Location) obj;
        return this.x.equals(loc.x) &&
               this.y.equals(loc.y) &&
               this.z.equals(loc.z) &&
               this.name.equals(loc.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y, z, name);
    }

    // INNER CLASSES

    /**
     * Class to build {@link Location}.
     */
    public static class Builder {
        private Double x;
        private Double y;
        private Double z;
        private String name;


        /**
         * Sets value of field {@code x}.
         * @param x coordinate
         * @return {@link Builder} instance
         */
        public Builder setX(Double x) {
            if (validateX(x)) {
                this.x = x;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code y}.
         * @param y coordinate
         * @return {@link Builder} instance
         */
        public Builder setY(Double y) {
            if (validateY(y)) {
                this.y = y;
                return this;
            }
            throw new IllegalArgumentException();
        }

        /**
         * Sets value of field {@code z}.
         * @param z coordinate
         * @return {@link Builder} instance
         */
        public Builder setZ(Double z) {
            if (validateZ(z)) {
                this.z = z;
                return this;
            }
            throw new IllegalArgumentException();
        }

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
         * Returns new {@link Location} instance with set fields.
         * @return {@link Location} 
         */
        public Location build() {
            if (validateX(x) && 
                validateY(y) && 
                validateZ(z) && 
                validateName(name)
            )
                return new Location(this);
            else
                throw new IllegalArgumentException("Invalid Location parameters");
        }
    }
}
