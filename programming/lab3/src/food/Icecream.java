package food;

public record Icecream(Flavor flavour) implements Edible {
    @Override
    public String toString() {
        return flavour.toString() + " ice cream";
    }
}
