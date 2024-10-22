package pokemons;

import moves.special.MagicalLeaf;

public class Tsareena extends Steenee{
    public Tsareena(String name, int level) {
        super(name, level);
        addMove(
            new MagicalLeaf()
        );
        setStats(
            72, // hp
            120, // attack
            98, // defense
            50, // speed attack
            98, // speed defense
            72 // speed
        );
    }
}
