package moves.special;

import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.SpecialMove;
import ru.ifmo.se.pokemon.Type;

public class AirSlash extends SpecialMove {
    public AirSlash() {
        super(
            Type.FLYING, // type
            75, // power
            0.95 // accuracy
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        if (Math.random() < 0.3) {
            Effect.flinch(opp);
        }
    }

    @Override
    protected String describe() {
        return "is using Air Slash";
    }
}
