package pokemons;

import moves.MagicalLeaf;

public class Tsareena extends Steenee{
    public Tsareena(String name, int level) {
        super(name, level);
        addMove(
                new MagicalLeaf()
        );
    }
}
