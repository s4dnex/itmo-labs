package moves.physical;

import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Effect;

public class IceFang extends PhysicalMove {
    public IceFang() {
        super(
            Type.ICE, // type
            65, // power
            0.95 // accuracy
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        if (Math.random() < 0.1) {
            Effect.freeze(opp);
            Effect.flinch(opp);
        }
    }

    @Override 
    protected String describe() {
        return "uses Ice Fang";
    }
}
