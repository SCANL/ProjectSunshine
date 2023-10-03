from typing import List, cast
from src.classifier.predict import Predicter
from src.common.enum import GreetIssueType, LanguageType
from src.model.greet.greet_attribute import GreetAttribute
from src.model.greet.greet_entity import AbstractGreetEntity
from src.model.greet.greet_function import GreetFunction
from src.model.greet.greet_issue import GreetIssue
from src.model.input import Input
from src.rule.linguistic_antipattern.contains_only_special_characters import ContainsOnlySpecialCharacters
from src.rule.linguistic_antipattern.starts_with_special_character import StartsWithSpecialCharacter
from src.rule.linguistic_antipattern.attribute_name_type_opposite import AttributeNameTypeOpposite
from src.rule.linguistic_antipattern.attribute_signature_comment_opposite import AttributeSignatureCommentOpposite
from src.rule.linguistic_antipattern.expecting_not_getting_collection import ExpectingNotGettingCollection
from src.rule.linguistic_antipattern.expecting_not_getting_single import ExpectingNotGettingSingle
from src.rule.linguistic_antipattern.get_more_than_accessor import GetMoreThanAccessor
from src.rule.linguistic_antipattern.get_no_return import GetNoReturn
from src.rule.linguistic_antipattern.is_no_return_bool import IsNoReturnBool
from src.rule.linguistic_antipattern.method_name_return_opposite import MethodNameReturnOpposite
from src.rule.linguistic_antipattern.method_signature_comment_opposite import MethodSignatureCommentOpposite
from src.rule.linguistic_antipattern.name_suggest_boolean_type_not import NameSuggestBooleanTypeNot
from src.rule.linguistic_antipattern.not_answered_question import NotAnsweredQuestion
from src.rule.linguistic_antipattern.not_implemented_condition import NotImplementedCondition
from src.rule.linguistic_antipattern.says_many_contains_one import SaysManyContainsOne
from src.rule.linguistic_antipattern.says_one_contains_many import SaysOneContainsMany
from src.rule.linguistic_antipattern.set_returns import SetReturns
from src.rule.linguistic_antipattern.transform_not_return import TransformNotReturn
from src.rule.linguistic_antipattern.validate_not_confirm import ValidateNotConfirm
from src.service.factory import EntityFactory
from src.service.parser import PythonParser


class Analyzer:

    def __init__(self, project, file: Input):
        self.project = project
        self.file_path = file.path
        self.file_type = file.type
        self.file_language = file.language
        self.junit = None
        self.rules = [
            ###### arnaoudova ######
            MethodSignatureCommentOpposite(),
            AttributeSignatureCommentOpposite(),
            AttributeNameTypeOpposite(),
            MethodNameReturnOpposite(),
            TransformNotReturn(),
            NotAnsweredQuestion(),
            NotImplementedCondition(),
            ValidateNotConfirm(),
            SaysManyContainsOne(),
            SaysOneContainsMany(),
            ExpectingNotGettingCollection(),
            ExpectingNotGettingSingle(),
            NameSuggestBooleanTypeNot(),
            SetReturns(),
            GetMoreThanAccessor(),
            IsNoReturnBool(),
            GetNoReturn(),
            ###### peruma ######
            # TestAnnotationTest(),
            # TestAnnotationSetup(),
            # TestAnnotationTeardown(),
            # TestNonVerbStarting(),
            # TestMissingNullCheck(),
            StartsWithSpecialCharacter(),
            ContainsOnlySpecialCharacters()
        ]
        self.issues = []

    def __process_python_file(self):
        with open(self.file_path, 'r') as file:
            source = file.read()
            __python_parser = PythonParser(source)
            __predictor = Predicter()

            __python_parser.parse_file()
            attributes = cast(List[GreetAttribute],
                              __python_parser.get_attributes()) or []
            functions = cast(List[GreetFunction],
                             __python_parser.get_functions()) or []
            entities: List[AbstractGreetEntity] = [*attributes, *functions]

            for entity in entities:
                result = __predictor.predict(entity)

                if GreetIssueType(result) != GreetIssueType.CLEAR:
                    g_issue = []
                    g_issue.append(GreetIssue(
                        entity, GreetIssueType(result), self.file_path))
                    self.issues.append(g_issue)

    def analyze(self):
        if self.file_language == LanguageType.Python:
            self.__process_python_file()
        else:
            entity = EntityFactory().construct_model(
                self.file_path, self.file_type, self.junit)
            if entity is None:
                return []

            for rule in self.rules:
                issue_list = rule.analyze(self.project, entity)
                if issue_list is not None:
                    self.issues.append(issue_list)

        concat_issues = [j for i in self.issues for j in i]

        return concat_issues
