package utils;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.TreeSet;

import data.Difficulty;
import data.LabWork;
import data.Person;

/**
 * Class to work with collection.
 */
public class Collection {
    private static long lastId = 0L;
    private TreeSet<LabWork> labWorks;
    private final LocalDateTime creationDate; 

    // CONSTRUCTORS

    public Collection() {
        labWorks = new TreeSet<LabWork>();
        creationDate = LocalDateTime.now();
    }

    public Collection(TreeSet<LabWork> labWorks) {
        this();
        
        for (LabWork lw : labWorks)
            add(lw);
    }

    // GETTERS

    /**
     * Returns id for next {@link LabWork} instance.
     * @return id
     */
    public long getNextId() {
        return ++lastId;
    }

    /**
     * Returns type (class) of collection as String.
     * @return class of collection
     */
    public String getType() {
        return labWorks.getClass().getSimpleName();
    }

    /**
     * Returns creation date of collection.
     * @return creation date
     */
    public LocalDateTime getCreationDate() {
        return creationDate;
    }

    /**
     * Returns current size of collection.
     * @return collection size
     */
    public int getSize() {
        return labWorks.size();
    }

    // METHODS

    /**
     * Returns collection as {@link TreeSet}
     * @return collection
     */
    public TreeSet<LabWork> asTreeSet() {
        return labWorks;
    }

    /**
     * Checks if element with given id is in collection.
     * @param id id to check
     * @return {@code true} if element with such id is in collection, otherwise {@code false}
     */
    public boolean contains(long id) {
        for (LabWork lw : labWorks) {
            if (lw.getId().equals(id))
                return true;
        }
        return false;
    }

    /**
     * Adds element to collection.
     * @param labWork element to add
     */
    public void add(LabWork labWork) {
        if (labWork.getId() == null)
            labWork.setId(getNextId());
        
        if (labWorks.add(labWork)) {
            lastId = Math.max(labWork.getId(), lastId);
        }
    }

    /**
     * Updates element with given id.
     * @param id id of element to update
     * @param labWork new element
     */
    public void update(Long id, LabWork labWork) {
        labWork.setId(id);
        
        if (!labWorks.removeIf(lw -> lw.getId().equals(id)))
            throw new IllegalArgumentException("No LabWork with such ID");
        labWorks.add(labWork);
    }

    /**
     * Removes element with given id.
     * @param id id of element to remove
     */
    public void remove(Long id) {
        if (!labWorks.removeIf(lw -> lw.getId().equals(id)))
            throw new IllegalArgumentException("No LabWork with such ID");
    }

    /**
     * Clears the collection.
     */
    public void clear() {
        labWorks.clear();
    }

    /**
     * Adds element to collection if it is greater than any other element.
     * @param labWork element to add
     * @return {@code true} if element has been added, otherwise {@code false}
     */
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

    /**
     * Removes every element that is lower than given.
     * @param labWork element for comparison
     * @return number of elements that have been removed
     */
    public long removeLower(LabWork labWork) {
        long count = 0;
        for (LabWork lw : labWorks) {
            if (lw.compareTo(labWork) < 0) {
                count++;
            }
        }
        labWorks.removeIf(lw -> lw.compareTo(labWork) < 0);
        return count;
    }

    /**
     * Return sum of minimal points from all elements.
     * @return sum of minimal points
     */
    public long sumOfMinimalPoint() {
        long sum = 0;
        for (LabWork lw : labWorks) {
            Long mp = lw.getMinimalPoint();
            
            if (mp != null)
                sum += mp;
        }
        return sum;
    }

    /**
     * Returns list of all elements difficulties sorted in ascending order.
     * @return list of difficulties
     */
    public List<Difficulty> getAscendingDifficulty() {
        List<Difficulty> difficulties = new ArrayList<Difficulty>();
        for (LabWork lw : labWorks) {
            difficulties.add(lw.getDifficulty());
        }
        difficulties.sort(Comparator.naturalOrder());
        return difficulties;
    }

    /**
     * Returns list of all elements persons sorted in descending order.
     * @return list of persons
     */
    public List<Person> getDescendingAuthor() {
        List<Person> authors = new ArrayList<Person>();
        for (LabWork lw : labWorks) {
            Person author = lw.getAuthor();
            
            if (author != null)
                authors.add(lw.getAuthor());
        }
        authors.sort(Comparator.reverseOrder());
        return authors;
    }
}
