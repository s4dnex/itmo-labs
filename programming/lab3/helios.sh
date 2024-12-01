javac -d bin --source-path src src/Main.java
jar -c -f MyObjectModel.java -e Main -C bin .
java -jar MyObjectModel.java