package pokemons;

import moves.special.MagicalLeaf;
import moves.status.Rest;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Bounsweet extends Pokemon {

    public Bounsweet(String name, int level) {
        super(name, level);
        setType(Type.GRASS);
        setMove(
            new Rest(), 
            new MagicalLeaf()
        );
        setStats(
            42, // hp
            30, // attack
            38, // defense
            30, // speed attack
            38, // speed defense
            32 // speed
        );
    }
}
