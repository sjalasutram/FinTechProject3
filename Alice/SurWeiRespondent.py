# This python file contains the logic to invoke a Smart Contract on the (local) blockchain and perform transactions,
# and verify that the transactions were executed successfully, by calling functions on the smart contract
import pandas as pd
from pathlib import Path
from web3 import Web3
import os
from dotenv import load_dotenv
import json
from typing import List
from eth_abi import abi
from random import choices
from random import randint


# load the environment variables by calling the load_dotenv function
#
load_dotenv()

#
# surwei_admin_address will hold the Ganache Account that is used to transact on the smart contract
#
surwei_admin_address = os.getenv('SURWEI_ADMIN_ADDRESS')
#print(f"surwei_admin_address is {surwei_admin_address}")

#
# deployer_contract_address stores the address of the deployer contract on the blockchain
# deployer contract is responsible for generating surveys when the CreateNewSurvey function is invoked
#
deployer_contract_address = os.getenv("SURWEI_DEPLOYER_ADDRESS")

#
# In this version of the Survey Administration, the surveys are loaded using an Excel spreadsheet
# The spreadsheet contains pre-defined surveys with responses
# _excel_file_path contains the folder path (relative to this python file) where the Excel file 
# is located
#
_excel_file_path=os.getenv('EXCEL_FILE_LOCATION')

#
# create an instance of Web3
# WEB3_PROVIDER_URI holds the URI from the Ganache application
#
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# get responder_address returns a random address from the Ganache
def get_responder_address():
    accounts = w3.eth.accounts
    # print(f"accounts: {accounts}")
    random_value = randint(1,5)
    return accounts[random_value]

#
# get_survey_deployer_abi returns the application binary interface of
# the survey_deployer from the SurveyDeployer.json file
#
def get_survey_deployer_abi():
    with open(Path('./contracts/SurveyDeployer.json')) as f:
        deployer_json = json.load(f)
        # from the json object get the value of the abi key
        deployer_abi = deployer_json['abi']
    return deployer_abi

#
# get_survey_deployer_abi returns the application binary interface of
# the survey from the Survey.json file
#
def get_survey_abi():
    with open(Path('./contracts/Survey.json')) as f:
        survey_json = json.load(f)
        survey_abi = survey_json['abi']
    return survey_abi

#
# get_survey_deployer_contract returns the web3 contract object
# this function uses the get_survey_deployer_abi function
#
def get_survey_deployer_contract():
    survey_deployer_abi = get_survey_deployer_abi()
    return w3.eth.contract(address=deployer_contract_address,abi=survey_deployer_abi)

#
# get_survey_contract returns the web3 contract object
# this function uses the get_survey_abi function
#
def get_survey_contract(survey_address):
    survey_abi = get_survey_abi()
    return w3.eth.contract(address=survey_address,abi=survey_abi)


#
# get_surveys_generated function returns the number of surveys generated by the survey_deployer contract
#
def get_surveys_generated(survey_deployer_contract):
    return survey_deployer_contract.functions.getTotalSurveys().call()

#
# generate_surveys function invokes the survey_deployer contract and generates
# one survey for each title in the SurveyQuestions.xls file
#
def generate_surveys(admin_account):
    # read the SurveyQuestions.xls file into a pandas dataframe
    df = pd.read_excel(Path(f"{_excel_file_path}/SurveyQuestions.xls"),index_col=None)        
    # each unique title from the pandas dataframe is assigned to survey_name
    unique_surveys = df['Title'].unique()

    # assign survey_name, survey_questions and survey_choices from the dataframe
    for surwei in unique_surveys:
        surwei_name = surwei
        surwei_questions = df.loc[df['Title']==surwei,'Question'].tolist()
        survey_choices = df.loc[df['Title']==surwei,['Choice_A','Choice_B','Choice_C','Choice_D']]
        survey_choices: List[List[str]] = survey_choices.values.tolist()
        survey_choices = [[str(s) for s in l] for l in survey_choices]

        deployer_contract = get_survey_deployer_contract()
        # createNewSurvey function call creates a new Survey contract and stores the address of the contract on the survey deployer contract
        deployer_contract.functions.createNewSurvey(surwei_name,surwei_questions,survey_choices).transact({'from':admin_account, 'gas':3000000})
    
    #
    # invoke the getTotalSurveys function on the deployer contract to verify that number of surveys
    # agree with the number of titles in the excel file
    #
    total_surveys_generated = get_surveys_generated(deployer_contract)
    #print(f"Total number of surveys generated {total_surveys_generated}" )
    return total_surveys_generated
    # return total_surveys_generated

#
# function respond_to_surveys mimics as though other users on the blockchain are responding to the survey
# the function injects fictitious responses to the survey, generating 4 random choices from a list - A, B, C or D
#
def respond_to_surveys(num_surveys_generated):
    #print(f"num_surveys_generated {num_surveys_generated}")
    survey_deployer_contract = get_survey_deployer_contract()
    response_options_list = ['A','B','C','D']
    responder_address = get_responder_address()
    for i in range(num_surveys_generated):
        survey_address = survey_deployer_contract.functions.getSurveyAddressAtIndex(i).call()
        survey_contract = get_survey_contract(survey_address)
        # generate about 10 responses on every survey
        # the number of responses is controlled by a randint function
        for i in range(randint(1,10)):
            choice_list = choices(response_options_list,k=4)
            print(f"survey_address: {survey_address} {choice_list} {responder_address}")
            survey_contract.functions.addSurveyresponse(choice_list).transact({'from':responder_address, 'gas':3000000})
            
           
#
# function list_surveys_and_responses
#
def surveys_and_responses_report(survey_deployer_contract):
    num_surveys_generated = get_surveys_generated(survey_deployer_contract)
    for i in range(num_surveys_generated):
        survey_address = survey_deployer_contract.functions.getSurveyAddressAtIndex(i).call()
       #print(f"survey_address: {survey_address}")
        if(survey_address != '0x0000000000000000000000000000000000000000'):
            survey_contract = get_survey_contract(survey_address)
            val = survey_contract.functions.getSurvey().call()
            #print(val)
            num_responses = survey_contract.functions.numSurveyResponses().call()
            for i in range(num_responses):
                responder = survey_contract.functions.getSurveyResponderAtIndex(i).call() 
                response = survey_contract.functions.getSurveyResponseAtIndex(i).call()
               # print(f"responder: {responder}, response: {response}")

if __name__ == '__main__':
    # objective 1: generate surveys
    num_surveys_generated = generate_surveys(surwei_admin_address)
    # objective 2: add responses to surveys
    respond_to_surveys(num_surveys_generated)
    # objective 3: show survey and responses
    surveys_and_responses_report(get_survey_deployer_contract())
