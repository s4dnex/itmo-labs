package exceptions;

import roads.Road;
import roads.RoadPart;

public class EndOfRoadException extends Exception {
    private static final String message = "This is the end of the road.";
    private final RoadPart currentPart;
    
    public EndOfRoadException(Road road) {
        super(message);
        this.currentPart = road.getCurrentPart();
    }

    @Override
    public String getMessage() {
        return  message + " Current part of road is " + this.currentPart.toString();
    }
}
