from rule.linguistic_antipattern.attribute_name_type_opposite import AttributeNameTypeOpposite
from rule.linguistic_antipattern.attribute_signature_comment_opposite import AttributeSignatureCommentOpposite
from rule.linguistic_antipattern.expecting_not_getting_collection import ExpectingNotGettingCollection
from rule.linguistic_antipattern.expecting_not_getting_single import ExpectingNotGettingSingle
from rule.linguistic_antipattern.get_more_than_accessor import GetMoreThanAccessor
from rule.linguistic_antipattern.get_no_return import GetNoReturn
from rule.linguistic_antipattern.is_no_return_bool import IsNoReturnBool
from rule.linguistic_antipattern.method_name_return_opposite import MethodNameReturnOpposite
from rule.linguistic_antipattern.method_signature_comment_opposite import MethodSignatureCommentOpposite
from rule.linguistic_antipattern.name_suggest_boolean_type_not import NameSuggestBooleanTypeNot
from rule.linguistic_antipattern.not_answered_question import NotAnsweredQuestion
from rule.linguistic_antipattern.not_implemented_condition import NotImplementedCondition
from rule.linguistic_antipattern.says_many_contains_one import SaysManyContainsOne
from rule.linguistic_antipattern.says_one_contains_many import SaysOneContainsMany
from rule.linguistic_antipattern.set_returns import SetReturns
from rule.linguistic_antipattern.transform_not_return import TransformNotReturn
from rule.linguistic_antipattern.validate_not_confirm import ValidateNotConfirm
from rule.test.annotation_setup import AnnotationSetup
from rule.test.annotation_teardown import AnnotationTeardown
from rule.test.annotation_test import AnnotationTest
from rule.test.nonverb_starting import NonVerbStarting
from service.factory import EntityFactory


class Analyzer:

    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.junit = None
        self.rules = [
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
            # AnnotationTest(),
            # AnnotationSetup(),
            # AnnotationTeardown(),
            # NonVerbStarting()
        ]
        self.issues = []

    def analyze(self):
        entity = EntityFactory().construct_model(self.file_path, self.file_type, self.junit)


        for rule in self.rules:
            issue_list = rule.analyze(entity)
            if issue_list is not None:
                self.issues.append(issue_list)

        concat_issues = [j for i in self.issues for j in i]
        return concat_issues
