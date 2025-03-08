package data;

public enum EyeColor {
    GREEN,
    RED,
    BLACK,
    WHITE,
    BROWN;

    public static String[] getValues() {
        String[] values = new String[EyeColor.values().length];
        for (int i = 0; i < EyeColor.values().length; i++) {
            values[i] = EyeColor.values()[i].toString();
        }
        return values;
    }
}
