package pokemons;

import moves.AerialAce;
import moves.AirSlash;
import moves.CrushClaw;
import moves.IceFang;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Minior extends Pokemon{
    public Minior(String name, int level) {
        super(name, level);
        setType(Type.ROCK, Type.FLYING);
        setMove(
            new AerialAce(),
            new AirSlash(),
            new CrushClaw(),
            new IceFang()
        );
        setStats(
            60, // hp
            60, // attack
            100, // defense
            60, // speed attack
            100, // speed defense
            60 // speed
        );
    }
}
