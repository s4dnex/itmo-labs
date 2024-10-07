package moves.physical;

import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;

public class Scratch extends PhysicalMove {
    public Scratch() {
        super(
            Type.NORMAL, // type
            40, // power
            1 // accuracy
        );
    }

    @Override
    protected String describe() {
        return "is using Scratch";
    }
}
