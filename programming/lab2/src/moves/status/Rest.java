package moves.status;

import ru.ifmo.se.pokemon.Effect;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Stat;
import ru.ifmo.se.pokemon.Status;
import ru.ifmo.se.pokemon.StatusMove;
import ru.ifmo.se.pokemon.Type;

public class Rest extends StatusMove {
    public Rest() {
        super(
            Type.PSYCHIC, // type
            0, // power
            1 // accuracy
        );
    }

    @Override
    protected void applySelfEffects(Pokemon self) {
        if (self.getCondition() == Status.SLEEP) return;
        
        self.setMod(
            Stat.HP, 
            (int) -(self.getStat(Stat.HP) - self.getHP())
        ); // fully restore current HP
        
        self.addEffect(
            new Effect()
            .condition(Status.SLEEP)
            .attack(0)
            .turns(2)
        );
    }

    @Override
    protected String describe() {
        return "is using Rest";
    }
}
