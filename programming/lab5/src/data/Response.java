package data;

public class Response {
    private boolean status;
    private String message;

    // CONSTRUCTORS

    public Response(boolean status) {
        this.status = status;
        this.message = null;
    }

    public Response(boolean status, String message) {
        this.status = status;
        this.message = message;
    }

    // GETTERS

    public boolean getStatus() {
        return status;
    }

    public String getMessage() {
        return message;
    }
}
