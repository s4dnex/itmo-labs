package moves.physical;

import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.PhysicalMove;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.Type;

public class CrushClaw extends PhysicalMove {
    public CrushClaw() {
        super(
            Type.NORMAL, // type
            75, // power
            0.95 // accuracy
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        opp.addEffect(
            new Effect()
            .stat(Stat.DEFENSE, -1)
            .chance(0.5)
        );
    }

    @Override
    protected String describe() {
        return "uses Crush Claw";
    }
}
