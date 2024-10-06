package moves.status;

import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Type;

public class PlayNice extends StatusMove{
    public PlayNice() {
        super(
            Type.NORMAL, // type
            0, // power
            1 // accuracy
        );
    }

    @Override
    protected void applyOppEffects(Pokemon opp) {
        opp.setMod(Stat.ATTACK, -1);
    }

    @Override
    protected String describe() {
        return "uses Play Nice";
    }
}
