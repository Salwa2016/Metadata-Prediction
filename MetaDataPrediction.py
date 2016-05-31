import multiprocessing
import multiprocessing.pool
import logging
from multiprocessing import Pool,Process
import sys
from pprint import pprint
import gensim
from gensim.models.word2vec import Word2Vec
import string
import os.path
import time
import sys
import numpy as np
import nltk
from nltk.cluster import GAAClusterer
import numpy  as np
import csv
from StringIO import StringIO
from numpy import genfromtxt
import sys, traceback
import time
import json

def ExtractTopics():
    with open('Json_Files/results.json') as data_file:    
         data = json.load(data_file)
         items=data.keys()
         AllTopics=[]
         for item in items:
             ontology=item
             data[ontology]['topics']
             topics=list(data[ontology]['topics'])
             for topic in topics:
                 topic[1]=topic[1].replace("'", "")
                 if (topic[1] not in AllTopics):
                     AllTopics.append(str(topic[1])) 
                 else:
    
                      continue
    #print AllTopics
    
    multiprocessing.log_to_stderr(logging.DEBUG)
    for topic in AllTopics: 
        ExtractOntologiesForCertainTopic (topic)
   

def ExtractOntologiesForCertainTopic(ontology_topic):
    counter =0
    poolpp = Pool(5)
    poolnn = Pool(5) 
    with open('Json_Files/results.json') as data_file:    
         data = json.load(data_file)
         items=data.keys()
         AllOntologies=[]
         positive_Ontology=[]
         negative_Ontology=[]
         for item in items:
             ontology=item
             data[ontology]['topics']
             topics=list(data[ontology]['topics'])
             for topic in topics:
                 topic[1]=topic[1].replace("'", "")
                 if (topic[1])==ontology_topic:
                     Label=data[ontology]['ontology'][29:]
                     positive_Ontology.append(str(Label))
             
    for item in items:
        ontology=item
        Label=data[ontology]['ontology'][29:]
        AllOntologies.append(str(Label))
    for ontology in  AllOntologies:
        if ontology not in positive_Ontology:
           counter+=1
           if counter<51:
                negative_Ontology.append(ontology)
    for ontology in positive_Ontology:    
        poolpp.apply_async(RepresentOntologyLabelsAsVector,(ontology,ontology_topic))          
    for ontology in negative_Ontology:    
        poolnn.apply_async(RepresentOntologyLabelsAsVector,(ontology,"Not-"+str(ontology_topic)))
    poolpp.close()              
    poolpp.join()
    poolnn.close()
    poolnn.join()
    #print   positive_Ontology     
    #print   negative_Ontology

def RepresentOntologyLabelsAsVector(ontology,topic):
    #Loading the trained model
    model = Word2Vec.load('salwamodel2') 
    #Intaliz empty array
    LabelsVectors=[]
    words=[]
    LabelsFile = str('Ontologies/Ontologies_Labels/Edited_'+'%s.csv' % ontology)
    WordsFile = str('Ontologies/Ontologies_Words/'+ ontology+'%s.csv' % '_Words')
    VectorsFile = str('Ontologies/Ontologies_Vectors/'+ ontology+'%s.csv' %'_Vectors')
    if os.path.exists(LabelsFile):
       with open(LabelsFile, 'r') as LabelsFile:
            words =LabelsFile.readlines()
            for word in words: 
                word= word.replace('"','')
                word= word.strip()
                word= word.strip('\n')  
                try:
                    WordVector=model[word]
                    LabelsVectors.append(WordVector) 
                    with open( WordsFile , 'a') as LabelsFile:
                         LabelsFile.write(word+'\n')       
                except KeyError:
                         pass
    np.savetxt(VectorsFile,LabelsVectors,delimiter=",")
    Apply_GACC_ClusteringOnOntologyLabels(ontology,topic)
   #Writting the numpy array to .csv file
   #VectorsAsArray= np.asarray(LabelsVectors)
  

def Apply_GACC_ClusteringOnOntologyLabels(ontology,topic):
    
    try:
        VectorsFile = str('Ontologies/Ontologies_Vectors/'+ ontology+"%s.csv" %'_Vectors')
        if (os.path.isdir('Ontologies/Topics_Classifiers/'+topic)):
           ClassifierFile = str('Ontologies/Topics_Classifiers/'+topic+"/"+ontology+"%s.csv" %'_Classifier')
           ClustersAverageFile = str('Ontologies/Topics_Classifiers/'+topic+"/"+ontology+"%s.csv" %'_Average')
        else:
            os.mkdir('Ontologies/Topics_Classifiers/'+topic)
            ClassifierFile = str('Ontologies/Topics_Classifiers/'+topic+"/"+ontology+"%s.csv" %'_Classifier')
            ClustersAverageFile = str('Ontologies/Topics_Classifiers/'+topic+"/"+ontology+"%s.csv" %'_Average')
        word_vectors = genfromtxt(VectorsFile, delimiter=',')
        vectors = [np.array(f) for f in word_vectors]
        if len(vectors) >13000:
           vectors=vectors[0:12000] 
       #  the GAAC clusterer with 3 clusters
        try:
           clusterer = GAAClusterer(3)
           clusters = clusterer.cluster(vectors, True)
        except MemoryError:
           pass
           clusters=[0]
        with open(VectorsFile,'r') as csvinput:
             with open(ClassifierFile, 'w') as csvoutput:
                  writer = csv.writer(csvoutput)
                  i=0
                  for row in csv.reader(csvinput):
                      try:
                         writer.writerow(row+[clusters[i]]+[topic])
                         i=i+1
                      except IndexError:
                            pass
        Average_Clusters(ClassifierFile,ClustersAverageFile)        
        csvinput.close()
        csvoutput.close()
    except AssertionError:
           pass
      

def Average_Clusters(ClassifierFile,ClustersAverageFile):
    first_cluster=[]
    second_cluster=[]
    third_cluster=[]
    with open(ClassifierFile, 'rb') as f:
          for row in csv.reader(f):
              try:
                 if row[100]== '0':
                    first_cluster.append([float(i) for i in row[0:100]])
                 if row[100]== '1':
                     second_cluster.append([float(i) for i in row[0:100]])
                 if row[100]== '2':
                    third_cluster.append([float(i) for i in row[0:100]])
              except IndexError:
                    print "ERRO:"
                    pass
    first_cluster=np.average(np.array(first_cluster), axis=0)
    second_cluster=np.average(np.array(second_cluster), axis=0)
    third_cluster=np.average(np.array(third_cluster), axis=0)
    np.savetxt(ClustersAverageFile,[first_cluster,second_cluster,third_cluster],delimiter=",") 
        

def main(topic):
    #Start time
    start=time.time()
    print "WELCOME"
    try:
       ExtractOntologiesForCertainTopic(topic)
       #ExtractTopics()
       
    except ValueError,MemoryError:
          print 'Memory Or Value ERROR'
    end=time.time()
    elapsed=end-start
    print "Time taken by Pipline:",elapsed,"Seconds." 
#*************************************************************
if __name__ == "__main__":
   main(' '.join(sys.argv[1:]))


