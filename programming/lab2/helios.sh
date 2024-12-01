javac -d ./ -cp lib/Pokemon.jar -sourcepath src ./src/Main.java
echo "Class-Path: lib/Pokemon.jar" > manifest
jar -c -f MyPokemons.jar -e Main -m manifest Main.class pokemons/*.class moves/*/*.class
