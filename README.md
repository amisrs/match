# Course Match Backend

All backend processes are covered by this repo. This readme will clarify the purpose of each of the scripts.
If you want to run this yourself you just need to install Python and all the dependencies (and also have
your own database server to write to, instead of mine).


## Scraping
How-to: Run the scrapers for each uni, and then write the json output into your database.
1. Scraping a list of partner universities for UNSW.
	- partner-scrape.py

2. Scraping the course outlines from partner universities.
	- [university].py

3. Writing scraped course outlines (with metadata) to the database.
	- unis-to-mysql.py
	- json-to-mysql.py
	- json-to-mysql-duplicates.py


## Training
How-to: Automatically done when classifier.py is used.
1. We manually labelled a bunch of sentences for use as training data, and
stored it in a directory structure.
	- csv_to_dir.py
	- outline_sentences/

2. classifier.py uses this directory to train.


## Processing
How-to: Run breaker.py
The entry point is breaker.py. I should have split it into more files, because
breaker.py does more than just breaking now (but with time constraints I lived with it)

1. Breaking the course outlines into sentences.
	- breaker.py
  	At this point the sentences are in the database ready to be classified.

2. Classifying the sentences into the categories.
	- classifier.py

3. Extracting keywords from classified sentences.
	- breaker.py
	- keyword_cleaner.py
	- unsw_keyword_updater.py

4. Calculating similarity score
	- cosine2.py *

5. Extracting email addresses from outlines.
	- regex_emails.py

The results of all of these scripts are written to the database. From there, the [front-end](https://github.com/imjeremyhi/ExchangeCourseMatcher)
reads the database and displays the information.

* You will need to download the enwiki_dbow model before running this script, and extract it to processor/

## Requirements
[glove.6B.zip](https://nlp.stanford.edu/projects/glove/) - Pretrained model based on Wikipedia used for vectorizing.

[enwiki_dbow/](https://github.com/jhlau/doc2vec) - Another pretrained model based on Wikipedia used for vectorizing.

mysql.txt - credentials to access the database (I'm not putting it on github)

### Python
Ideally run this on Python 2.7.


beautifulsoup4==4.5.3

gensim==2.3.0

nltk==3.2.4

numpy==1.13.1

pandas==0.20.3

PyPDF2==1.26.0

rake-nltk==1.0.1

scikit-learn==0.19.0

scipy==0.19.1

selenium==3.5.0

textract==1.6.1




