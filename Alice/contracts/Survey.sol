pragma solidity >=0.8.1;
pragma experimental ABIEncoderV2;
//USE SPDX-License-Identifier: MIT;

contract Survey {
   
    // this modifier will be used to ensure that the responses are recorded before the survey is expired
    modifier isactiveSurvey(){
        require(hasSurveyExpired() == false);
        _;
    }

    uint _survey_id; // a running sequence of the surveys generated
    string _survey_name; // a user identified survey name
    string[] _survey_questions; // a list of survey questions, stored in an array of string
    string[][] _survey_q_choices; // list of responses for each survey question. assumed to be index consistent with questions

    uint public deployDate;

    function hasSurveyExpired() public view returns(bool){
        return (block.timestamp > (deployDate + 100 minutes));
    }

    constructor(uint survey_id
               ,string memory survey_name
               ,string[] memory survey_q
               ,string[][] memory survey_q_choices)  payable{
        deployDate = block.timestamp;
        _survey_id = survey_id;
        _survey_name = survey_name;
        _survey_questions = survey_q;
        _survey_q_choices = survey_q_choices;
    }

    // enum _response_option_indexes{A,B,C,D}
    // _response_option_indexes response; 

    // function to return the Survey information
    function getSurvey() public view returns (string memory, string[] memory, string[][] memory){
        return (_survey_name,_survey_questions,_survey_q_choices);
    }

    // the mapping will ensure that the respondent can submit the survey only once
    mapping(address => string[]) public _survey_responses;
    address[] public _responder_address;

    function numSurveyResponses() external view returns(uint){
        return _responder_address.length;
    }

    // the function returns the responses that were recorded on the survey
    function getSurveyResponseAtIndex(uint _index) external view returns (string[] memory){
        return (_survey_responses[_responder_address[_index]]);
    }

    // the function returns the responder address at a specific index that were recorded on the survey
    function getSurveyResponderAtIndex(uint _index) external view returns (address) {
        return _responder_address[_index];
    }

    // responses on the contract will be recorded using this function
    // the function uses a modifier to ensure that the survey responses are recorded on the survey
    // within the the time the survey is allocated to be active
    function addSurveyresponse(string[] memory responses) public isactiveSurvey{
        _survey_responses[msg.sender] = responses;
        _responder_address.push(msg.sender);
    }

    // callback function
    receive() external payable {}

}
