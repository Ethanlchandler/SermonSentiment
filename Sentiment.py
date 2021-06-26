from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
import sparknlp



spark = sparknlp.start()

pipeline = PretrainedPipeline('explain_document_dl', lang='en')

result = pipeline.annotate("The Mona Lisa is a 16th century oil painting created by Leonardo. It's held at the Louvre in Paris.")


list(result.keys())
Output: ['entities', 'stem', 'checked', 'lemma', 'document', 'pos', 'token', 'ner', 'embeddings', 'sentence']

opt_list = ['entities', 'stem', 'checked', 'lemma', 'document', 'pos', 'token', 'ner', 'embeddings', 'sentence']

print(result['sentence'])
