package utils;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.TreeSet;

import data.Difficulty;
import data.LabWork;
import data.Person;

public class Collection {
    private TreeSet<LabWork> labWorks;
    private final LocalDateTime creationDate; 

    // CONSTRUCTORS

    public Collection() {
        labWorks = new TreeSet<LabWork>();
        creationDate = LocalDateTime.now();
    }

    // GETTERS

    public String getType() {
        return labWorks.getClass().toString();
    }

    public LocalDateTime getCreationDate() {
        return creationDate;
    }

    public int getSize() {
        return labWorks.size();
    }

    // METHODS

    public ArrayList<LabWork> asArrayList() {
        return new ArrayList<LabWork>(labWorks);
    }

    public void add(LabWork labWork) {
        labWorks.add(labWork);
    }

    public void update(Long id, LabWork labWork) {
        if (!labWorks.removeIf(lw -> lw.getId().equals(id)))
            throw new IllegalArgumentException("No LabWork with such ID"); 
        labWorks.add(labWork);
    }

    public void remove(Long id) {
        if (!labWorks.removeIf(lw -> lw.getId().equals(id)))
            throw new IllegalArgumentException("No LabWork with such ID");
    }

    public void clear() {
        labWorks.clear();
    }

    public void save() {
        // TODO: Implement method
    }

    public void addIfMax(LabWork labWork) {
        LabWork maxLabWork = labWorks.getFirst();
        for (LabWork lw : labWorks) {
            if (lw.compareTo(maxLabWork) > 0)
                maxLabWork = lw;
        }

        if (labWork.compareTo(maxLabWork) > 0)
            labWorks.add(labWork);
    }

    public void removeIfLower(LabWork labWork) {
        labWorks.removeIf(lw -> lw.compareTo(labWork) < 0);
    }

    public long sumOfMinimalPoint() {
        long sum = 0;
        for (LabWork lw : labWorks) {
            sum += lw.getMinimalPoint();
        }
        return sum;
    }

    public List<Difficulty> getAscendingDifficulty() {
        ArrayList<Difficulty> difficulties = new ArrayList<Difficulty>();
        for (LabWork lw : labWorks) {
            difficulties.add(lw.getDifficulty());
        }
        difficulties.sort(Comparator.naturalOrder());
        return difficulties;
    }

    public List<Person> getDescendingAuthor() {
        ArrayList<Person> authors = new ArrayList<Person>();
        for (LabWork lw : labWorks) {
            authors.add(lw.getAuthor());
        }
        authors.sort(Comparator.reverseOrder());
        return authors;
    }
}
