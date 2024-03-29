from src.common.Singleton import Singleton
from src.common.enum import LanguageType
from src.model.project import ConfigCustomFileType

__java_testing_packages = [
    'junit.framework.Test',
    'junit.framework.TestCase',
    'org.junit.Test',
    'android.test.AndroidTestCase',
    'android.test.InstrumentationTestCase',
    'android.test.ActivityInstrumentationTestCase2',
    'org.junit.Assert',
    'org.junit.jupiter.api.Test',
    'org.junit.rules.TestRule',
    'org.junit.runner.Description',
    'org.junit.runners.model.Statement',
    'org.junit.jupiter.api.BeforeEach',
    'org.mockito.Mockito',
    'org.assertj.core.api.Assertions.assertThat'
]

__csharp_testing_packages = [
    'Microsoft.VisualStudio.TestTools.UnitTesting',
    'Microsoft.VisualStudio.QualityTools.UnitTesting.Framework',
    'NUnit.Tests',
    'NUnit.Framework',
    'Xunit',
    'Xunit.Abstractions'
]

__java_null_check_test_methods = [
    'assertNotNull',
    'assertNull'
]

__csharp_null_check_test_methods = [
    'IsNull',
    'IsNotNull'
]

__java_test_method_annotation = [
    'Test'
]

__csharp_test_method_annotation = [
    'TestMethod',
    'Test',
    'TestCase'
    'Fact',
    'Theory'
]


def __get_java_test_method_annotations(project):
    annotations = []
    annotations.extend(__java_test_method_annotation)
    custom_annotations = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'java_custom_test_method_annotation')
    if custom_annotations is not None:
        annotations.extend(custom_annotations)
    return annotations


def __get_csharp_test_method_annotations(project):
    annotations = []
    annotations.extend(__csharp_test_method_annotation)
    custom_annotations = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'csharp_custom_test_method_annotation')
    if custom_annotations is not None:
        annotations.extend(custom_annotations)
    return annotations


def __get_java_testing_packages(project):
    packages = []
    packages.extend(__java_testing_packages)
    custom_package = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'java_custom_testing_packages')
    if custom_package is not None:
        packages.extend(custom_package)
    return packages


def __get_csharp_testing_packages(project):
    packages = []
    packages.extend(__csharp_testing_packages)
    custom_package = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'csharp_custom_testing_packages')
    if custom_package is not None:
        packages.extend(custom_package)
    return packages


def __get_java_null_check_test_methods(project):
    code = []
    code.extend(__java_null_check_test_methods)
    custom_code = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'java_custom_null_check_test_methods')
    if custom_code is not None:
        code.extend(custom_code)
    return code


def __get_csharp_null_check_test_methods(project):
    code = []
    code.extend(__csharp_null_check_test_methods)
    custom_code = project.get_config_value(ConfigCustomFileType.Code, 'Test', 'csharp_custom_null_check_test_methods')
    if custom_code is not None:
        code.extend(custom_code)
    return code


def get_null_check_test_method(project, language):
    if language == LanguageType.Java:
        return __get_java_null_check_test_methods(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_null_check_test_methods(project)
    else:
        return None


def get_testing_packages(project, language):
    if project is None:
        project = TestingPackage().project
    if language == LanguageType.Java:
        return __get_java_testing_packages(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_testing_packages(project)
    else:
        return None


def get_test_method_annotations(project, language):
    if language == LanguageType.Java:
        return __get_java_test_method_annotations(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_test_method_annotations(project)
    else:
        return None

class TestingPackage(metaclass=Singleton):
    def __init__(self):
        self.project = None

    def set_project(self, project):
        self.project = project
