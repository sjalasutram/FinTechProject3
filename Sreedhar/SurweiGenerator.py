import pandas as pd
from pathlib import Path
from web3 import Web3
import os
from dotenv import load_dotenv
import json
# import streamlit as st

# load the environment variables by calling the load_dotenv function
load_dotenv()

surwei_admin_address = os.getenv('SURWEI_ADMIN_ADDRESS')
# Create an instance of Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# @st.cache(allow_output_mutation=True)
def load_contract(admin_account):
    with open(Path('./contracts/SurveyDeployer.json')) as f:
        deployer_certificate_abi = json.load(f)
    deployer_contract_address = os.getenv("SURWEI_DEPLOYER_ADDRESS")
    with open(Path('./contracts/Survey.json')) as s:
        survey_abi = json.load(s)



    # survey information
    # will be from the excel file later on
    surwei_name = "Color v5"
    surwei_questions = ["Favorite color", "Pick one hair color", "Steak cooking choice"]  
    surwei_responses = [
        ['Blue','Green','Red','White']
        ,['Blonde','Brunette','Short','Caucasian']
        ,['Rare','Medium','Medium Rare','Well Done']
    ]

    # using the SurveyDeployer.json, create a contract object
    deployer_contract = w3.eth.contract(address=deployer_contract_address,abi=deployer_certificate_abi)
    survey_address = deployer_contract.functions.createNewSurvey(surwei_name,surwei_questions,surwei_responses).transact({'from':admin_account, 'gas':3000000})
    print(f"address of the new contract is {survey_address}")
    #survey_contract = w3.eth.contract(address=survey_address,abi=survey_abi)
    #survey_contract.functions.addSurveyresponse(['C','C','D']).transact({'from':admin_account, 'gas':3000000})

if __name__ == '__main__':
    #accounts = w3.eth.accounts
    #account =  accounts[1]
    #admin_account = st.selectbox("Select Admin Account", options=accounts)
    load_contract(surwei_admin_address)

