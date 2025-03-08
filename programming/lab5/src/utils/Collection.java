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
    private static long lastId = 0L;
    private TreeSet<LabWork> labWorks;
    private final LocalDateTime creationDate; 

    // CONSTRUCTORS

    public Collection() {
        labWorks = new TreeSet<LabWork>();
        creationDate = LocalDateTime.now();
    }

    // GETTERS

    public long getNextId() {
        return ++lastId;
    }

    public String getType() {
        return labWorks.getClass().getSimpleName();
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

    public boolean contains(long id) {
        for (LabWork lw : labWorks) {
            if (lw.getId().equals(id))
                return true;
        }
        return false;
    }

    public void add(LabWork labWork) {
        if (labWork.getId() == null)
            labWork.setId(getNextId());
        
        if (labWorks.add(labWork)) {
            lastId = Math.max(labWork.getId(), lastId);
        }
    }

    public void update(Long id, LabWork labWork) {
        labWork.setId(id);
        
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

    public boolean addIfMax(LabWork labWork) {
        if (labWorks.size() == 0) {
            labWorks.add(labWork);
            return true;
        }

        LabWork maxLabWork = labWorks.last();
        // for (LabWork lw : labWorks) {
        //     if (lw.compareTo(maxLabWork) > 0)
        //         maxLabWork = lw;
        // }
        
        if (labWork.compareTo(maxLabWork) > 0) {
            labWorks.add(labWork);
            return true;
        }

        return false;
    }

    public long removeLower(LabWork labWork) {
        return labWorks.stream()
            .filter(lw -> lw.compareTo(labWork) < 0)
            .peek(lw -> labWorks.remove(lw))
            .count();
    }

    public long sumOfMinimalPoint() {
        long sum = 0;
        for (LabWork lw : labWorks) {
            sum += lw.getMinimalPoint();
        }
        return sum;
    }

    public List<Difficulty> getAscendingDifficulty() {
        List<Difficulty> difficulties = new ArrayList<Difficulty>();
        for (LabWork lw : labWorks) {
            difficulties.add(lw.getDifficulty());
        }
        difficulties.sort(Comparator.naturalOrder());
        return difficulties;
    }

    public List<Person> getDescendingAuthor() {
        List<Person> authors = new ArrayList<Person>();
        for (LabWork lw : labWorks) {
            authors.add(lw.getAuthor());
        }
        authors.sort(Comparator.reverseOrder());
        return authors;
    }
}
