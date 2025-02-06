package data;

public class Coordinates {
    private int x;
    private float y;

    // CONSTRUCTORS

    public Coordinates(int x, float y) {
        setX(x);
        setY(y);
    }

    // GETTERS

    public int getX() {
        return x;
    }

    public float getY() {
        return y;
    }

    // SETTERS

    protected void setX(int x) {
        this.x = x;
    }

    protected void setY(float y) {
        this.y = y;
    }
}
