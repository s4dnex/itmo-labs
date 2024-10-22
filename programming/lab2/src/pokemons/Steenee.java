package pokemons;

import moves.status.PlayNice;

public class Steenee extends Bounsweet{
    public Steenee(String name, int level) {
        super(name, level);
        addMove(
            new PlayNice()
        );
        setStats(
            52, // hp
            40, // attack
            48, // defense
            40, // speed attack
            48, // speed defense
            62 // speed
        );
    }
}
