import java.io.*;
import java.util.*;
public class InvertedIndex {


        public static class Posting {
            public Posting next = null;
            public int docId;
            public int dtf = 1;    // document term frequency

            public Posting(int docId) {
                this.docId = docId;
            }
        }

        public static class DictEntry {
            public int doc_freq = 0;      // number of documents that contain the term
            public int term_freq = 0;    //number of times the term is mentioned in the collection
            public Posting pList = null;
        }

        public static void main(String[] args) {
            HashMap<String, DictEntry> index = new HashMap<>();
            String[] filenames = {"file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt", "file7.txt", "file8.txt", "file9.txt", "file10.txt"};
            int docId = 0;
            int N = filenames.length;
            double[] scores = new double[N];
            double[] length = new double[N];

            // Read files and build index
            for (String filename : filenames) {
                try {
                    BufferedReader br = new BufferedReader(new FileReader(filename));
                    String line;
                    while ((line = br.readLine()) != null) {
                        String[] words = line.split("\\W+");
                        for (String word : words) {
                            word = word.toLowerCase();
                            if (!index.containsKey(word)) {
                                index.put(word, new DictEntry());
                            }
                            DictEntry entry = index.get(word);
                            entry.term_freq++;
                            if (entry.pList == null || entry.pList.docId != docId) {
                                Posting posting = new Posting(docId);
                                posting.next = entry.pList;
                                entry.pList = posting;
                                entry.doc_freq++;
                            } else {
                                entry.pList.dtf++;
                            }
                        }
                    }
                    br.close();
                    docId++;
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            // Compute cosine similarity between each file and the query
            Scanner input = new Scanner(System.in);
            System.out.print("Enter a query: ");
            String query = input.nextLine().toLowerCase();
            String[] queryTerms = query.split("\\W+");
            for (String term : queryTerms) {
                if (index.containsKey(term)) {
                    DictEntry entry = index.get(term);
                    int tdf = entry.doc_freq;
                    int ttf = entry.term_freq;
                    double idf = Math.log10((double) N / tdf);
                    Posting post = entry.pList;
                    while (post != null) {
                        int docIdForTerm = post.docId;
                        double tfIdf = (1 + Math.log10((double) post.dtf)) * idf;
                        scores[docIdForTerm] += tfIdf;
                        length[docIdForTerm] += Math.pow(tfIdf, 2);
                        post = post.next;
                    }
                }
            }

            // Normalize for the length of the doc
            for (int i = 0; i < N; i++) {
                length[i] = Math.sqrt(length[i]);
                if (length[i] != 0) {
                    scores[i] /= length[i];
                }
            }

            // Rank the 10 files according to the value of the cosine similarity
            List<Integer> rankedDocs = new ArrayList<>();
            for (int i = 0; i < N; i++) {
                rankedDocs.add(i);
            }
            Collections.sort(rankedDocs, (doc1, doc2) -> Double.compare(scores[doc2], scores[doc1]));

            // Return top K components of the ranked list
            int k = 5;
            System.out.println("Top " + k + " documents:");
            for (int i = 0; i < k; i++) {
                int docIdForRank = rankedDocs.get(i);
                double score = scores[docIdForRank];
                System.out.println("  " + filenames[docIdForRank] + ": " + score);
            }
        }

}
