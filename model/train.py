import os
import re
from time import time
import multiprocessing
import psycopg2
from psycopg2.extras import DictCursor
from gensim.models.doc2vec import Doc2Vec, TaggedDocument, logger


class DocIterator(object):
    """
    gensim documentation calls this "streaming a corpus", which
    lets us train without holding entire corpus in memory.
    It needs to be an object so gensim can make multiple passes over data.
    Here, we stream from a postgres database.
    """

    def __init__(self, conn, content=False):
        self.conn = conn
        self.content = content
        self.excluded_list = []
	self.count = 0

    def __iter__(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM articles;")
            for article in cur:
		        if self.count % 100000 == 0:
		            print 'Current count: ', self.count
                body = ''
                try:
                    body += article['abstract'].replace('\n', ' ').strip()
                except:
                    print 'Missing Abstract for ', article['abstract']
                try:
                    body += str(' ' + article['title'] + '. ')
                except:
		            pass
                    #print 'Title missing for ', article['arxiv_id']
                if self.content:
                    try:
                        body += str(article['content'] + '. ')
                    except:
                        print 'Content missing for ', article['arxiv_id']

                if len(body) < 250:  # exclude articles which have too little content (heuristically)
                    self.excluded_list.append(article['arxiv_id'])
                    continue
                removed_nums = re.sub(r'[0-9.,_{}><()\-\|\$]{3,}', ' ', body)
                removed_specials = re.sub(
                    r'[{}><()\|\$\\\*\^\%\#\@]', '', body)
                words = re.findall(r"[\w']+|[.,!?;]", removed_specials)
                words = [word.lower() for word in words]
                tags = [article['arxiv_id'], article['subject_id']]

		        self.count+=1
                yield TaggedDocument(words, tags)


if __name__ == '__main__':
    print 'Starting'
    full_content = True
    hidden_layer_size = 100
    print 'Content Setting: ', full_content
    n_cpus = multiprocessing.cpu_count()
    print 'Connecting to DB'
    with psycopg2.connect(host='arxivpsql.cctwpem6z3bt.us-east-1.rds.amazonaws.com',
                          user='root', password='1873', database='arxivpsql') as conn:
        print 'Building doc_iterator'
        doc_iterator = DocIterator(conn, full_content)
        print 'Begin Training'
    	os.system("taskset -p 0xFFFFFFFf %d" % os.getpid())
        time1 = time()
    	model = Doc2Vec(
                documents=doc_iterator,
                workers = n_cpus,
                size=hidden_layer_size)
        time2 = time()
    print 'Training time: ', time2-time1
    print 'Training Complete. Saving...'
    with open('excluded_full.txt', 'w') as f:
        f.write(str(doc_iterator.excluded_list))
    if full_content:
        model.save('full_model')
    else:
        model.save('abstract_model')
