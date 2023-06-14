# Crawler and Page Rank calculations

This application will crawl the given url and will calculate the page rank using neo4j library
## Installation

Use the requirements.txt to install foobar.


```bash
pip install -r requirements.txt
```

## Neo4j Installation

Make sure there are correct versions of DBMS and Graph data science library
1. DBMS version - 5.5.0
2. Graph data science library version - 2.3.2

- Create a new DBMS with user <USERNAME> and password <PASSWORD>
- Next in DBMS goto plugin section and install Graph data science library
- Start the DBMS and Open it
- You will get a connection url
- Update all 3 values(user, password, connectionUrl) in config.ini in the project


## Usage
Finally run the main file and page rank will be displayed
```python
python main.py

## Results will be
<Record name='Page 4' score=1.2981276232326968>
<Record name='Page 51' score=1.2446889144558029>
<Record name='Page 6' score=1.199268670399495>
<Record name='Page 3' score=0.48518406594746616>
<Record name='Page 2' score=0.39434357783485113>
<Record name='Page 1' score=0.287466160281063>
<Record name='Page 7' score=0.287466160281063>
