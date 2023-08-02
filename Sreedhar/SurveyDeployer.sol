pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

import "./Survey.sol";

contract SurveyDeployer {

    uint survey_id;

    struct SurveyStruct{
        uint id;
        string name;
        string[] question;
        string[] choices;
    }

    SurveyStruct survey;

    mapping(uint => address) published_surveys;
    
    function generateSurvey(string memory survey_name
                           ,string[] memory survey_question
                           ,string[0][2] memory survey_responses) public {

        survey_id += 1;
        
        survey = SurveyStruct(survey_id, survey_name, survey_question,survey_responses);

    }

    function viewSurvey(uint survey_id_val) external view returns(string memory, string memory, string memory){
        return (survey.name, survey.question[0], survey.choices[0]);
    }

}