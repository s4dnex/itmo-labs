package data;

public class Location {
    private Double x; // != null
    private Double y; // != null
    private Double z; // != null
    private String name; // != null, != empty

    // CONSTRUCTORS

    public Location(Double x, Double y, Double z, String name) {
        setX(x);
        setY(y);
        setZ(z);
        setName(name);
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

    // SETTERS

    protected void setX(Double x) {
        if (x == null) {
            throw new IllegalArgumentException("X cannot be null");
        }
        this.x = x;
    }

    protected void setY(Double y) {
        if (y == null) {
            throw new IllegalArgumentException("Y cannot be null");
        }
        this.y = y;
    }

    protected void setZ(Double z) {
        if (z == null) {
            throw new IllegalArgumentException("Z cannot be null");
        }
        this.z = z;
    }

    protected void setName(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name cannot be null or empty");
        }
        this.name = name;
    }
}
