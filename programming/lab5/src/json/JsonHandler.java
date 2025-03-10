package json;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonParser;
import java.time.LocalDateTime;
import java.util.TreeSet;

import data.LabWork;


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

    public static String serializeCollection(TreeSet<LabWork> labWorks) {
        return JsonHandler.getGson().toJson(labWorks);
    } 

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
