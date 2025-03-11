package json;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import java.time.LocalDateTime;
import java.util.TreeSet;

import data.LabWork;

/**
 * Class to work with JSON
 */
public class JsonHandler {
    private static final Gson gson = new GsonBuilder()
                                         .setPrettyPrinting()
                                         .registerTypeAdapter(LocalDateTime.class, new LocalDateTimeTypeAdapter())
                                         .create();


    // CONSTRUCTORS

    private JsonHandler() {

    }

    // METHODS

    /**
     * Returns {@link Gson} instance.
     * @return
     */
    public static Gson getGson() {
        return gson;
    }

    /**
     * Method to serialize collection to JSON.
     * @param labWorks collection as {@link TreeSet}
     * @return JSON as {@link String}
     */
    public static String serializeCollection(TreeSet<LabWork> labWorks) {
        return JsonHandler.getGson().toJson(labWorks);
    }

    /**
     * Method to deserialize collection from JSON.
     * @param json JSON as {@link String}
     * @return collection as {@link TreeSet}
     */
    public static TreeSet<LabWork> deserializeCollection(String json) {
        try {
            TreeSet<LabWork> labWorks = new TreeSet<LabWork>();
            for (JsonElement item : JsonParser.parseString(json).getAsJsonArray()) {
                labWorks.add(JsonHandler.getGson().fromJson(item, LabWork.class));
            }
            return labWorks;    
        } catch (Exception e) {
            throw new JsonParseException("Couldn't parse the collection from file.");
        }
    }
}
