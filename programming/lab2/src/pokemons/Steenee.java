package pokemons;

import moves.PlayNice;

public class Steenee extends Bounsweet{
    public Steenee(String name, int level) {
        super(name, level);
        addMove(
            new PlayNice()
        );
    }
}
