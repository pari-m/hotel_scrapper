## About

 
This Python script allows you to scrape hotel details from a leading ariliners Hotels API based on the provided CSV file containing hotel IDs, check-in, and check-out dates.

  

## Prerequisites

- Python 3.x

  

## Running the code

-Clone the repo

  
  

- Create a Virtual Environment using

  

```bash

sudo pip  install  virtualenv

virtualenv venv

```

  

- Activate the virtualenv

  

```bash

source /venv/bin/activate

```

  

- Install dependencies

  

```bash

pip install  -r  requirements.txt

```

  

- To run the script

  

copy your csv file to the raw_files directory

  

python3 extract_rates.py

  

## Todo

  

- [ ] Refactor the write_rates_to_csv method. The current method is too clunky

- [ ] Validate the csv before initialization the object
