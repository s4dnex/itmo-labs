package moves;

import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.SpecialMove;

public class MagicalLeaf extends SpecialMove {
    public MagicalLeaf() {
        super(
            Type.GRASS, // type
            60,  // power
            1 // accuracy
        );
    }

    @Override
    protected String describe() {
        return "uses Magical Leaf";
    }
}
