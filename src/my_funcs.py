import sys
import os
import argparse 
import pprint
import json
import time
import math


from sodapy import Socrata
from maps import (mappings as es_mappings, make_key)
from datetime import datetime

from es_helper import (
    ElasticHelperException, 
    insert_doc,
    try_create_index,
)


DATASET_ID = "nc67-uf89"
#DATASET_ID = os.environ.get("DATASET_ID")
ES_USERNAME = os.environ.get("ES_USERNAME")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
APP_TOKEN = os.environ.get("APP_TOKEN")
ES_HOST = os.environ.get("ES_HOST")


client = Socrata(
        "data.cityofnewyork.us",
        APP_TOKEN,
    )
    
# The total number of rows
tot_records =  int(client.get(DATASET_ID, select="COUNT(*)")[0]["COUNT"])
#print("The total number of rows are:",tot_records)
    
# Creates index, pings the api, and then pushes to elasticsearch
def cap_data(page_size, num_pages = None):
    if not num_pages:
        tot_records = int(client.get(DATASET_ID, select="COUNT(*)")[0]["COUNT"])
        num_pages = tot_records // page_size + 1
    
    # STEP 1: try to create an index in elasticsearch
        
    try:
        try_create_index(
            "bigdata1",
            ES_HOST,
            mappings=es_mappings,
            es_user=ES_USERNAME,
            es_pw=ES_PASSWORD,
        )
    except ElasticHelperException as e:
        print("Index already exists! skipping")
        print(f"{e}")
            
            
    # STEP 2: query the data and get rows
        
    success = 0
    fail = 0
    offset = 0
        
        
    for x in range(num_pages):
        offset = x * page_size 
        rows = client.get(DATASET_ID, limit=page_size, offset=offset, order=":id")
        print("The current run:", x + 1)
        print("The current offset:", offset)
        print("The page size:", page_size)
        print("The number of pages :", num_pages)
        print("---------------------------------------------------------------")
        time.sleep(2) # wait for 2 seconds
        pprint.pprint(rows)
            
        # STEP 3: convert the row data into the correct types as needed.
        make_key(rows)
        for row in rows:
            try:
                row['fine_amount'] = float(row['fine_amount'])
                row['penalty_amount'] = float(row['penalty_amount'])
                row['interest_amount'] = float(row['interest_amount'])
                row['reduction_amount'] = float(row['reduction_amount'])
                row['amount_due'] = float(row['amount_due'])
                row['payment_amount'] = float(row['payment_amount'])
                row['summons_number'] = int(row['summons_number'])
                # row['issue_date'] =  str(row['issue_date'])
                # format the date from MM/dd/YYYY to YYYY-MM-dd
                old = row['issue_date']
                datetimeobj = datetime.strptime(old, '%m/%d/%Y')
                new = datetimeobj.strftime('%Y-%m-%d')
                row['issue_date'] = new
                    
            except Exception as e:
                print("SKIPPING! Failed to transform row: {row}. Reason: {e}")
                print(e)
                fail += 1
                print("The total number of failures:",fail)
                continue
                
            # STEP 4: POST this data to elasticsearch
            try:
                # index_name, host, data=None, es_user=None, es_pw=None
                ret = insert_doc(
                    "bigdata1", 
                    ES_HOST,
                    data=row,
                    es_user=ES_USERNAME,
                    es_pw=ES_PASSWORD,
                )
                success += 1
                print("The total number of inserted documents are:", success)
                print(ret)
            except ElasticHelperException as e:
                print(e)
    
#cap_data(3,2)          
