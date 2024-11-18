package exceptions;

public class NoFoodInHandException extends Exception {
    private final String message;
    private final Object item;
    
    public NoFoodInHandException(String message, Object item) {
        super(message);
        this.message = message;
        this.item = item;
    }

    @Override
    public String getMessage() {
        return message + " Current item in hand is " + (item.toString() != null ? item.toString() : "null");
    }
}
