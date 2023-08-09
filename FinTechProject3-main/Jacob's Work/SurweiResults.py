from web3 import Web3
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import json
from typing import List
from eth_abi import abi
from random import choices
from random import randint

#load the env file to allow the addresses to be used
load_dotenv()

#setup the ability to call the admin addresses
surwei_admin_address = os.getenv('SURWEI_ADMIN_ADDRESS')

#setup the ability to call the deployer address
deployer_contract_address = os.getenv("SURWEI_DEPLOYER_ADDRESS")

#setup the ability to call the example excel file
_excel_file_path=os.getenv('EXCEL_FILE_LOCATION')

#setup the Web provider call
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB_PROVIDER_URI")))

# Contract interfaces
CONTRACTS = {}

with open("Survey.json") as f:
  CONTRACTS["Survey"] = json.load(f)

# Deployed contract addresses
SURVEY_ADDRESS = "0x..." 

# Survey contract instance
survey_contract = w3.eth.contract(address=SURVEY_ADDRESS, abi=CONTRACTS["Survey"]["abi"])

# Authorized accounts
AUTHORIZED_USERS = ["0x6be0613661a5CF3a6788112758AFC41C0233Dbca", "0xd7befC0F9AEdF9514A3f7715c1fB9F8B843a5e98"]

# Get survey results
def get_survey_results(survey_address, sender):

  # Check authorization
  if sender not in AUTHORIZED_USERS:
    raise Exception("Unauthorized")
    
  num_responses = survey_contract.functions.numSurveyResponses().call()

  results = []

  for i in range(num_responses):
    responder = survey_contract.functions.getSurveyResponderAtIndex(i).call()
    response = survey_contract.functions.getSurveyResponseAtIndex(i).call() 
    results.append((responder, response))

  return results

# Print results  
def print_survey_results(survey_address, sender):

  results = get_survey_results(survey_address, sender)

  print(f"Results for {survey_address}:")

  for result in results:
    print(result)

# Example call  
sender = w3.eth.accounts[0]
print_survey_results(SURVEY_ADDRESS, sender)
