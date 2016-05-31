import gensim, logging
import os
import string
import numpy as np
#load model
import os
import string
import gensim, logging
import re

class MySentences(object):
        def __init__(self, dirname):
                self.dirname = dirname

        def __iter__(self):
                for fname in os.listdir(self.dirname):
                        for line in open(os.path.join(self.dirname, fname)):
                                line = " ".join(line.split())
                                line = line.lower()
                                #line = line.translate(None, string.punctuation)
                                line = re.sub(ur"[^\w\d\-\s]+",'',line)
                                line = line.translate(None, string.digits)
                                print line
                                yield line.split()
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = MySentences('/home/ahmariss/Desktop/CBRC_PROJECT/Word2Vec_Model/TheCombinedCorpus') 
model = gensim.models.Word2Vec()
model.build_vocab(sentences)
model = gensim.models.Word2Vec(sentences,min_count=5,size=100,workers=32)
model.save('salwamodel')

