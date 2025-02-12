package data;

import utils.Formatter;

public class Location {
    private Double x; // != null
    private Double y; // != null
    private Double z; // != null
    private String name; // != null, != empty

    // CONSTRUCTORS

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

    public static Response validateX(Double x) {
        if (x == null)
            return new Response(false, "X can't be null");
        return new Response(true);
    }

    public static Response validateY(Double y) {
        if (y == null)
            return new Response(false, "Y can't be null");
        return new Response(true);
    }

    public static Response validateZ(Double z) {
        if (z == null)
            return new Response(false, "Z can't be null");
        return new Response(true);
    }

    public static Response validateName(String name) {
        if (name == null || name.isBlank())
            return new Response(false, "Name can't be null or empty");
        return new Response(true);
    }

    @Override
    public String toString() {
        String indent = Formatter.getIndentation(++Formatter.STRING_INDENTATION_COUNT);

        String result = "Location {\n" +
               indent + " x: " + x + "\n" +
               indent + " y: " + y + "\n" +
               indent + " z: " + z + "\n" +
               indent + " name: " + name + "\n";

        indent = Formatter.getIndentation(--Formatter.STRING_INDENTATION_COUNT);
        result += indent + "}";

        return result;
    }

    // INNER CLASSES

    public static class Builder {
        private Double x;
        private Double y;
        private Double z;
        private String name;

        public Builder setX(Double x) {
            Response response = validateX(x);
            if (response.getStatus()) {
                this.x = x;
                return this;
            }
            else
                throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setY(Double y) {
            Response response = validateY(y);
            if (response.getStatus()) {
                this.y = y;
                return this;
            }
            else
                throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setZ(Double z) {
            Response response = validateZ(z);
            if (response.getStatus()) {
                this.z = z;
                return this;
            }
            else
                throw new IllegalArgumentException(response.getMessage());
        }

        public Builder setName(String name) {
            Response response = validateName(name);
            if (response.getStatus()) {
                this.name = name;
                return this;
            }
            else
                throw new IllegalArgumentException(response.getMessage());
        }

        public Location build() {
            if (validateX(x).getStatus() && 
                validateY(y).getStatus() && 
                validateZ(z).getStatus() && 
                validateName(name).getStatus()
            )
                return new Location(this);
            else
                throw new IllegalArgumentException("Invalid Location parameters");
        }
    }
}
