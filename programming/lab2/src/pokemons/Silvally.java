package pokemons;

import moves.AerialAce;
import moves.AirSlash;
import moves.CrushClaw;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Silvally extends Pokemon{
    public Silvally(String name, int level) {
        super(name, level);
        setType(Type.NORMAL);
        setMove(
            new AerialAce(),
            new AirSlash(),
            new CrushClaw()
        );
        setStats(
            95, // hp
            95, // attack
            95, // defense
            95, // speed attack
            95, // speed defense
            95 // speed
        );
    }

}
