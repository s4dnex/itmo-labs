package moves.status;

import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Type;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.Effect;

public class Swagger extends StatusMove {
    public Swagger() {
        super(
            Type.NORMAL,
            0,
            0.85
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        opp.setMod(Stat.ATTACK, 2);
        Effect.confuse(opp);
    }

    @Override
    protected String describe() {
        return "is using Swagger";
    }
}
