pragma solidity >=0.8.1;
pragma experimental ABIEncoderV2;
//USE SPDX-License-Identifier: MIT;
import "./Survey.sol";

contract SurveyDeployer {
    // survey_id holds a running sequence the deployer is generating
    uint survey_id;

    // all the survey addresses this contract generates are stored in a
    // mapping data structure 
    mapping(uint => address) public published_surveys;

    constructor () {
        survey_id = 0;
    }
    
    // this function create a new survey when invoked, assigns the next available
    // survey_id to it, stores the survey questions and the choice options for each question
    // the function returns the address of the survey
    function createNewSurvey(string memory survey_name
                            ,string[] memory survey_questions
                            ,string[][] memory survey_q_choices
                            ) public payable returns (address, uint) {
        survey_id += 1;                                

        Survey survey = new Survey(survey_id
                                  ,survey_name
                                  ,survey_questions
                                  ,survey_q_choices
                                  );     

       published_surveys[survey_id] = address(survey);

       return (address(survey), survey_id);

    }

    // returns the total number of surveys the deployer contract has generated
    function getTotalSurveys() public view returns(uint){
        return survey_id;
    }

    //
    function getSurveyAddressAtIndex(uint index) public view returns(address){
        return published_surveys[index];
    }

    //fallback function
    receive() external payable {}

}