import pokemons.*;
import ru.ifmo.se.pokemon.Battle;


public class Main {
    public static void main(String[] args) {
        Battle b = new Battle();

        Druddigon druddigon = new Druddigon("Дракошка", 100);
        Silvally silvally = new Silvally("Сир Свали", 100);
        Minior minior = new Minior("Миньон", 100);
        Bounsweet bounsweet = new Bounsweet("Свекла", 100);
        Steenee steenee = new Steenee("Стини", 100);
        Tsareena tsareena = new Tsareena("Царица", 100);

        b.addAlly(druddigon);
        b.addFoe(silvally);
        b.addAlly(minior);
        b.addFoe(bounsweet);
        b.addAlly(steenee);
        b.addFoe(tsareena);

        b.go();
    } 
}
