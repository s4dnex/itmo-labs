package json;

import java.lang.reflect.Type;
import java.time.LocalDateTime;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import utils.Formatter;

/**
 * Class to adapt {@link LocalDateTime} to/from JSON.
 */
public class LocalDateTimeTypeAdapter implements JsonSerializer<LocalDateTime>, JsonDeserializer<LocalDateTime> {
    @Override
    public JsonElement serialize(LocalDateTime localDateTime, Type srcType, JsonSerializationContext context) {
      return new JsonPrimitive(localDateTime.format(Formatter.DATE_FORMAT));
    }
    
    @Override
    public LocalDateTime deserialize(JsonElement json, Type typeOfT, JsonDeserializationContext context) throws JsonParseException {
      return LocalDateTime.parse(json.getAsString(), Formatter.DATE_FORMAT);
    }
}