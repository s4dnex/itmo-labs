package data;

public enum Difficulty {
    VERY_EASY,
    EASY,
    NORMAL,
    HARD;

    public static String[] getValues() {
        String[] values = new String[Difficulty.values().length];
        for (int i = 0; i < Difficulty.values().length; i++) {
            values[i] = Difficulty.values()[i].toString();
        }
        return values;
    }
}
