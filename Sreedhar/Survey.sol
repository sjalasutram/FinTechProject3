pragma solidity >=0.8.1;
pragma experimental ABIEncoderV2;
//USE SPDX-License-Identifier: MIT;
import "@openzeppelin/contracts/utils/Counters.sol";

contract Survey {
    using Counters for Counters.Counter;

    modifier isactiveSurvey(){
        require(hasSurveyExpired() == false);
        _;
    }

    Counters.Counter survey_counter;

    string[4][] survey;
    string[7][] survey_questions;

    uint deployDate;

    function hasSurveyExpired() public view returns(bool){
        return (block.timestamp > (deployDate + 1 minutes));
    }

    constructor(){
        deployDate = block.timestamp;
        survey_counter.increment();
    }


    enum _response_option_indexes{A,B,C,D}
    _response_option_indexes response; 

    // the mapping will ensure that the respondent can submit the survey only once
    mapping(address => string[]) _survey_responses;
    address[] _responder_address;

    function numSurveyResponses() external view returns(uint){
        return _responder_address.length;
    }

    function getSurveyResponseAtIndex(uint _index) external view returns (address, string[] memory){
        return (_responder_address[_index], _survey_responses[_responder_address[_index]]);
    }

    function addSurveyresponse(string[] memory responses) public payable isactiveSurvey{
        _survey_responses[msg.sender] = responses;
        _responder_address[_responder_address.length] = msg.sender;

    }

    receive() external payable {}

}
