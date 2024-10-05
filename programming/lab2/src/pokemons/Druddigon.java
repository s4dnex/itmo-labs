package pokemons;

import moves.Swagger;
import moves.CrushClaw;
import moves.Scratch;
import moves.ThunderFang;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Druddigon extends Pokemon {
    public Druddigon (String name, int level) {
        super(name, level);
        setType(Type.DRAGON);
        setMove(
            new Swagger(),
            new CrushClaw(),
            new Scratch(),
            new ThunderFang()
        );
        setStats(
            77, // hp
            120, // attack
            90, // defense
            60, // speed attack
            90, // speed defense
            48 // speed
        );
    }
}
