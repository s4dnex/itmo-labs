package data;

public enum HairColor {
    RED,
    ORANGE,
    BROWN;

    public static String[] getValues() {
        String[] values = new String[HairColor.values().length];
        for (int i = 0; i < HairColor.values().length; i++) {
            values[i] = HairColor.values()[i].toString();
        }
        return values;
    }
}
