package transport;

import java.util.Objects;

import roads.RoadType;

public class Car extends Transport {
    protected String manufacturer;
    protected String model;

    public Car(double speed) {
        super(speed);
        this.manufacturer = "unknown manufacturer";
        this.model = "unknown model";
    }

    public Car(String manufacturer, String model, double speed) {
        super(speed);
        this.manufacturer = manufacturer;
        this.model = model;
    }

    @Override
    public void move(RoadType roadType) {
        if (roadType.getSpeedMultiplier() > 1) {
            System.out.println(this + " is driving faster.");
        }
        else if (roadType.getSpeedMultiplier() < 1) {
            System.out.println(this + " is driving slower.");
        }
        else {
            System.out.println(this + " is driving at the same speed.");
        }
    }

    @Override
    public String toString() {
        return manufacturer + " " + model;
    }

    @Override
    public boolean equals(Object obj) {
        if (this.getClass() != obj.getClass()) 
            return false;
        
        Car car = (Car) obj;
        return this.manufacturer.equals(car.manufacturer) && 
               this.model.equals(car.model) && 
               this.speed == car.speed;

    }

    @Override
    public int hashCode() {
        return Objects.hash(manufacturer, model, speed);
    }
}
