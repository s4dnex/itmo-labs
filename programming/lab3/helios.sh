javac -d bin --source-path src src/Main.java
jar -c -f MyObjectModel.jar -e Main -C bin .
java -jar MyObjectModel.jar