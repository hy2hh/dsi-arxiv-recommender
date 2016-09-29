# final_project
DSI Final Project

Timeline:
10/3 Monday: Data, Github Ready
10/5 Wednesday: Basic Model Done
10/7 Friday: Analysis Done
10/10 Monday: Presentation Done
Sometime in between: lecture on presentation
10/14 Friday: Code Freeze
10/17 Monday: Practice Presentation with Group
10/18 Tuesday: More Practice (with half of class)
10/19 Wednesday: Practice with next cohort as audience
10/20 (TBD) Thursday: Capstone Presentations
10/21 Friday: Day off
10/24-10/28: Interview prep. Course review. Graduation.

The data-modeling-analysis-presentation loop should be completed ASAP.
No live demo allowed on presentation.
Always do what you set out to do for the day.


9/28/2016:
- Made the decision to try to run Doc2Vec on arXiv corpus (~190 GB of text)
- Setup conda environment and AWS EC2 for mining arXiv metadata
- Worked on script (harvest.py) to take the metadata from arXiv OAI.
- Decided that harvest.py should contain processing before moving the data to S3.

Some comments about harvest.py:
	The purpose of harvest.py is to:
	1. Grab metadata from arXiv OAI
	2. Process the metadata (which is XML). Apply the schema.
	3. Place the metadata on S3 and PostgreSQL server.

9/29/2016:
Goals: DATABASE. PROPOSAL.
- Parse metadata XML into JSON. Store in DB on AWS. (PRIORITY)
- Find out whether it would be possible to match the raw text with the metadata via file name and perm. link.
- Ultimately: Combine the raw text and metadata within a single DB entry
Completed:
- Submitted Final Project Proposal
- 


Notes:
- arXiv changed its identifer scheme on March 2007. See https://arxiv.org/help/arxiv_identifier 
- Since SciExplorer is built on post-2007 papers, its parser only handles the new scheme.
- Therefore we will need to write a parser for the old scheme.


AWS PostgreSQL DB:
psql --host=arxivpsql.cctwpem6z3bt.us-east-1.rds.amazonaws.com --port=5432 --username=root --password --dbname=arxivpsql

ALTER USER "user_name" WITH PASSWORD 'new_password';



Links:
http://docs.aws.amazon.com/quickstart/latest/mongodb/architecture.html

http://www.aclweb.org/anthology/E14-3011

