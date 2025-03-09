package data;

import json.JsonHandler;

public class Coordinates {
    private int x;
    private float y;

    // CONSTRUCTORS

    public Coordinates(Coordinates.Builder builder) {
        this.x = builder.x;
        this.y = builder.y;
    }

    // GETTERS

    public int getX() {
        return x;
    }

    public float getY() {
        return y;
    }

    // METHODS

    @Override
    public String toString() {
        return JsonHandler.getGson().toJson(this);
    }

    // INNER CLASSES

    public static class Builder {
        private int x;
        private float y;

        public Builder setX(int x) {
            this.x = x;
            return this;
        }

        public Builder setY(float y) {
            this.y = y;
            return this;
        }

        public Coordinates build() {
            return new Coordinates(this);
        }
    }
}
