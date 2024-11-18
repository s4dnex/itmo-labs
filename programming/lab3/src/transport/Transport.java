package transport;

import java.util.Objects;

import roads.RoadType;

public abstract class Transport {
    protected double speed;

    public Transport(double speed) {
        this.speed = speed;
    }

    public double getSpeed() {
        return speed;
    }

    public abstract void move(RoadType roadType);

    @Override
    public String toString() {
        return "transport";
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Transport transport = (Transport) obj;
        return this.speed == transport.speed;
    }

    @Override
    public int hashCode() {
        return Objects.hash(speed);
    }
}
