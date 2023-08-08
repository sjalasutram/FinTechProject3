import pandas as pd
from pathlib import Path
from web3 import Web3
import os
from dotenv import load_dotenv
import json
from typing import List
from eth_abi import abi

# load the environment variables by calling the load_dotenv function
load_dotenv()

surwei_admin_address = os.getenv('SURWEI_ADMIN_ADDRESS')
_excel_file_path=os.getenv('EXCEL_FILE_LOCATION')

# Create an instance of Web3
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

def load_contract(admin_account):
    with open(Path('./contracts/SurveyDeployer.json')) as f:
        deployer_certificate_json = json.load(f)
        deployer_certificate_abi = deployer_certificate_json['abi']
        # print(f"deployer_certificate_abi: {deployer_certificate_abi}")
    deployer_contract_address = os.getenv("SURWEI_DEPLOYER_ADDRESS")
    with open(Path('./contracts/Survey.json')) as s:
        survey_json = json.load(s)
        survey_abi = survey_json['abi']

    df = pd.read_excel(Path(f"{_excel_file_path}/SurveyQuestions.xls"),index_col=None)        
    unique_surveys = df['Title'].unique()

    for surwei in unique_surveys:
        surwei_name = surwei
        surwei_questions = df.loc[df['Title']==surwei,'Question'].tolist()
        surwei_responses = df.loc[df['Title']==surwei,['Choice_A','Choice_B','Choice_C','Choice_D']]
        surwei_responses: List[List[str]] = surwei_responses.values.tolist()
        #print(f"surwei_responses {type(surwei_responses)}")
        #surwei_responses = [[]]
        # [s.encode("utf-8").decode("utf-8") for s in l for l in surwei_responses]
        surwei_responses = [[str(s) for s in l] for l in surwei_responses]


    # survey information
    # will be from the excel file later on
     #surwei_name = "Color v5"
     #surwei_questions = ["Favorite color", "Pick one hair color", "Steak cooking choice"]  
        surwei_responses_c = [
            ['Blue','Green','Red','White']
            ,['Blonde','Brunette','Short','Caucasian']
            ,['Rare','Medium','Medium Rare','Well Done']
        ]

        # using the SurveyDeployer.json, create a contract object
        deployer_contract = w3.eth.contract(address=deployer_contract_address,abi=deployer_certificate_abi)
        #response_data = deployer_contract.functions.createNewSurvey(surwei_name,surwei_questions,surwei_responses).transact({'from':admin_account, 'gas':3000000})
        #decodedABI = abi.decode(['address', 'uint'], response_data)
        #print(decodedABI)
        deployer_contract.functions.createNewSurvey(surwei_name,surwei_questions,surwei_responses).transact({'from':admin_account, 'gas':3000000})
        total_surveys_generated = deployer_contract.functions.getTotalSurveys().call()
        print(type(total_surveys_generated))


    #for i in total_surveys_generated[1]:
    survey_address = deployer_contract.functions.getSurveyAddressAtIndex(1).call()
    # print(f"{survey_address}")
    survey_contract = w3.eth.contract(address=survey_address,abi=survey_abi)
    survey_contract.functions.addSurveyresponse(["A","D","C","D"]).transact({'from':admin_account, 'gas':3000000})
    num_survey_responses = survey_contract.functions.numSurveyResponses().call()        
    print(f"{survey_address} {num_survey_responses}")

        #print(f"address of the new contract is {survey_address}")        
    #survey_contract = w3.eth.contract(address=survey_address,abi=survey_abi)
    #survey_contract.functions.addSurveyresponse(['C','C','D']).transact({'from':admin_account, 'gas':3000000})

if __name__ == '__main__':
    load_contract(surwei_admin_address)
