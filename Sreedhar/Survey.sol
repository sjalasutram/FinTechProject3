pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

contract Survey {

    constructor (uint _num_questions, string memory _survey_name) public {
    }

    uint public _survey_end_time;
    
    enum _response_option_indexes{A,B,C,D}
    _response_option_indexes response; 

    /*
    survey question structure is identified by a question index and
    the question. all survey questions start with index value of 1.
    a survey cannot have more than 10 questions
    */
    // struct _question {
    //     uint q_index;
    //     string question;
    // }

    // struct _choice {
    //     _response_option_indexes choice_index;
    //     string choice_text;
    //     //bool _selected; // indicates if this choice was selected; needed?
    // }
    
    // struct survey {
    //     uint _survey_id;
    //     string _survey_name;
    //     _question[] question;
    //     _choice[] choice;
    // }

    string[][7] survey;

    // the mapping will ensure that the respondent can submit the survey only once
    mapping(address => string[]) _survey_responses;

    function listSurveyResults() external view returns (string[] memory, string[] memory, string[] memory) {

    }

    function addSurveyresponse(string[] memory responses) public payable{
        _survey_responses[msg.sender] = responses;

    }

    function() external payable{}

}
