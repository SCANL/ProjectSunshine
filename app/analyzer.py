from app.rule.linguistic_antipattern.contains_only_special_characters import ContainsOnlySpecialCharacters
from app.rule.linguistic_antipattern.starts_with_special_character import StartsWithSpecialCharacter
from app.rule.linguistic_antipattern.attribute_name_type_opposite import AttributeNameTypeOpposite
from app.rule.linguistic_antipattern.attribute_signature_comment_opposite import AttributeSignatureCommentOpposite
from app.rule.linguistic_antipattern.expecting_not_getting_collection import ExpectingNotGettingCollection
from app.rule.linguistic_antipattern.expecting_not_getting_single import ExpectingNotGettingSingle
from app.rule.linguistic_antipattern.get_more_than_accessor import GetMoreThanAccessor
from app.rule.linguistic_antipattern.get_no_return import GetNoReturn
from app.rule.linguistic_antipattern.is_no_return_bool import IsNoReturnBool
from app.rule.linguistic_antipattern.method_name_return_opposite import MethodNameReturnOpposite
from app.rule.linguistic_antipattern.method_signature_comment_opposite import MethodSignatureCommentOpposite
from app.rule.linguistic_antipattern.name_suggest_boolean_type_not import NameSuggestBooleanTypeNot
from app.rule.linguistic_antipattern.not_answered_question import NotAnsweredQuestion
from app.rule.linguistic_antipattern.not_implemented_condition import NotImplementedCondition
from app.rule.linguistic_antipattern.says_many_contains_one import SaysManyContainsOne
from app.rule.linguistic_antipattern.says_one_contains_many import SaysOneContainsMany
from app.rule.linguistic_antipattern.set_returns import SetReturns
from app.rule.linguistic_antipattern.test_annotation_setup import TestAnnotationSetup
from app.rule.linguistic_antipattern.test_annotation_teardown import TestAnnotationTeardown
from app.rule.linguistic_antipattern.test_annotation_test import TestAnnotationTest
from app.rule.linguistic_antipattern.test_missing_null_check import TestMissingNullCheck
from app.rule.linguistic_antipattern.test_nonverb_starting import TestNonVerbStarting
from app.rule.linguistic_antipattern.transform_not_return import TransformNotReturn
from app.rule.linguistic_antipattern.validate_not_confirm import ValidateNotConfirm
from app.service.factory import EntityFactory


class Analyzer:

    def __init__(self, project, file_path, file_type):
        self.project = project
        self.file_path = file_path
        self.file_type = file_type
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
            TestAnnotationTest(),
            TestAnnotationSetup(),
            TestAnnotationTeardown(),
            TestNonVerbStarting(),
            TestMissingNullCheck(),
            StartsWithSpecialCharacter(),
            ContainsOnlySpecialCharacters()
        ]
        self.issues = []

    def analyze(self):
        entity = EntityFactory().construct_model(self.file_path, self.file_type, self.junit)

        for rule in self.rules:
            issue_list = rule.analyze(self.project, entity)
            if issue_list is not None:
                self.issues.append(issue_list)

        concat_issues = [j for i in self.issues for j in i]
        return concat_issues
