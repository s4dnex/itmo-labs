package exceptions;

public class NoFoodAvailableException extends Exception {
    private final String message;
    private final Object item;
    
    public NoFoodAvailableException(String message, Object item) {
        super(message);
        this.message = message;
        this.item = item;
    }

    @Override
    public String getMessage() {
        return message + (item.toString() != null ? 
                            " Current item in hand is " + item.toString() + "." :
                             " There is nothing in hand.");
    }
}
