package json;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.time.LocalDateTime;


public class JsonHandler {
    private static final Gson gson = new GsonBuilder()
                                         .setPrettyPrinting()
                                         .registerTypeAdapter(LocalDateTime.class, new LocalDateTimeTypeAdapter())
                                         .create();


    // CONSTRUCTORS

    private JsonHandler() {

    }

    // METHODS

    public static Gson getGson() {
        return gson;
    }
}
