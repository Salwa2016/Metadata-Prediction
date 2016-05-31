import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
 
public class LabelsPreprocessing {

public static void CreateFiles(String FileName)
{
try { 
                String FileName2=FileName+".txt";
                FileName=FileName+".csv";
               
                File dir = new File(".");
		String source = File.separator + "/home/ahmariss/Desktop/CBRC_PROJECT/Labels/"+FileName2;
		String dest =  File.separator +"/home/ahmariss/Desktop/CBRC_PROJECT/Word2Vec_Model/Ontologies/Ontologies_Labels/"+"Edited_"+FileName;
		File fin = new File(source);
		FileInputStream fis = new FileInputStream(fin);
		BufferedReader in = new BufferedReader(new InputStreamReader(fis));
		FileWriter fstream = new FileWriter(dest, false);
		BufferedWriter out = new BufferedWriter(fstream);
		String aLine ;
                String new_line;
		while ((aLine = in.readLine()) != null) {
//Process each line and add output to Dest.txt file
 new_line= aLine.replaceAll("_", "\n");
 new_line= new_line.replaceAll("\\[","\n");
 new_line= new_line.replace("]","\n");
 new_line= new_line.replace(" ","\n");
 new_line= new_line.replace(")","\n");
 new_line= new_line.replace("(","\n");
 new_line= new_line.replace("\\/"," \n");
 new_line= new_line.replace("/","\n ");
 new_line= new_line.replaceAll("\\*", "\n");
 new_line= new_line.replaceAll("[0-9]+", "\n");
 new_line= new_line.replace("\"","\n");
 new_line= new_line.replaceAll(",","\n");
 new_line= new_line.replaceAll("'","\n");
 new_line= new_line.replaceAll("\\.","\n");
 new_line= new_line.replaceAll("-", "\n");
 new_line= new_line.replaceAll(" ", "\n");
 new_line= new_line.replaceAll("\n\n", "");

			out.write(new_line);
			//out.newLine();
		}
 // do not forget to close the buffer reader
		in.close();
 
		// close buffer writer
                out.flush();
		out.close();
	
	}catch (Exception e) { System.out.println(e); }
            	
	}



	public static  void main(String[] args) throws IOException {
          File dir = new File(".");
          String source = dir.getCanonicalPath() + File.separator + "ListOfOntologies.txt";      
	  File fin = new File(source);
	  FileInputStream fis = new FileInputStream(fin);
	  BufferedReader in = new BufferedReader(new InputStreamReader(fis));
          String aLine ;
while (( aLine= in.readLine()) != null) {
System.out.println( aLine);
CreateFiles( aLine);
}

}
}
