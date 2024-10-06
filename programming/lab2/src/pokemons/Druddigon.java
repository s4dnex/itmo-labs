package pokemons;

import moves.physical.CrushClaw;
import moves.physical.Scratch;
import moves.physical.ThunderFang;
import moves.status.Swagger;
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
