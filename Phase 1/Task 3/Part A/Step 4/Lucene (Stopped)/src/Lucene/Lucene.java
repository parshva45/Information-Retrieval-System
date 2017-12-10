package Lucene;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

public class Lucene {
	private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {

		String indexLocation = null;
		String s = "Indexes";
		Arrays.stream(new File(s).listFiles()).forEach(File::delete);
		Lucene indexer = null;
		try {
		    indexLocation = s;
		    indexer = new Lucene(s);
		} catch (Exception ex) {
		    System.out.println("Cannot create index..." + ex.getMessage());
		    System.exit(-1);
		}

	    try {
	    s = "../../Step 1/Stopped Tokenizer Output";
		if (s.equalsIgnoreCase("q")) {
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		indexer.closeIndex();

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
			indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);

		System.out.println();
		s = "";
		
		PrintWriter writer = new PrintWriter("Stopped_Lucene_Top100_Pages.txt", "UTF-8");			
		PrintWriter writer1 = new PrintWriter("Stopped_Lucene_Top5_Docs.txt", "UTF-8");
		PrintWriter writer2 = new PrintWriter("Stopped_Lucene_Top100_Docs.txt", "UTF-8");
		writer.println("Ranking (Top 100) for the queries in Cleaned_queries.txt in the format:");
		writer.println("query_id Q0 doc_id rank Lucene_score system_name");
		
	    try {
	    	String contents = new String(Files.readAllBytes(Paths.get("../../Step 3/Cleaned_Queries_Stopped.txt")));
	    	for(String str:contents.split("\r\n")){
	    		if(str != "")
	    		{
	    			String q_id = str.split("\t")[0];
	    			s = str.split("\t")[1];
	    			writer.println();
	    			writer.println("For query: "+s);
	    			writer.println();
	    			TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
				
		    
	    			Query q = new QueryParser(Version.LUCENE_47, "contents",
					analyzer).parse(s);
	    			searcher.search(q, collector);
	    			ScoreDoc[] hits = collector.topDocs().scoreDocs;
		
	    			for (int i = 0; i < hits.length; ++i) {
	    				int docId = hits[i].doc;
	    				Document d = searcher.doc(docId);
	    				int pos = d.get("path").lastIndexOf('\\')+1;
	    				int tot = d.get("path").length();
	    				writer.println(q_id+" Q0 "+d.get("path").substring(pos,tot-4)+" "+(i+1)+" "+hits[i].score+" LuceneStopNoStem");
	    				writer2.println(d.get("path").substring(pos,tot-4));
	    				if(i < 5)
	    					writer1.println(d.get("path").substring(pos,tot-4));
	    			}
	    			System.out.println("Generated: Results for the query '"+s+"'");
				
	    		}
	    	}

	    } catch (Exception e) {
		System.out.println("Error searching " + s + " : "
			+ e.getMessage());
	    }
	    writer.close();
	    writer1.close();
	    writer2.close();

    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    Lucene(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		analyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

		writer.addDocument(doc);
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
}
