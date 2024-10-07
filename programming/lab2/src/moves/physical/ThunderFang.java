package moves.physical;

import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Pokemon;

public class ThunderFang extends PhysicalMove {
    public ThunderFang() {
        super(
            Type.ELECTRIC, // type
            65, // power
            0.95 // accuracy
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        if (Math.random() < 0.1) {
            Effect.flinch(opp);
            Effect.paralyze(opp);
        }
    }

    @Override
    protected String describe() {
        return "is using Thunder Fang";
    }
}
