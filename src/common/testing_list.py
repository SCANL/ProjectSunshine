from typing import Any, List, Optional
from src.common.Singleton import Singleton
from src.common.enum import LanguageType
from src.model.project import ConfigCustomFileType, Project

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


def __get_java_test_method_annotations(project: Project) -> List[Any]:
    """
        Get a list of Java test method annotations.

        Args:
            project (Project): The project for which annotations are retrieved.

        Returns:
            List[Any]: A list of Java test method annotations.
    """
    annotations = []
    annotations.extend(__java_test_method_annotation)
    custom_annotations = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'java_custom_test_method_annotation')
    if custom_annotations is not None:
        annotations.extend(custom_annotations)
    return annotations


def __get_csharp_test_method_annotations(project: Project) -> List[Any]:
    """
        Get a list of C# test method annotations.

        Args:
            project (Project): The project for which annotations are retrieved.

        Returns:
            List[Any]: A list of C# test method annotations.
    """
    annotations = []
    annotations.extend(__csharp_test_method_annotation)
    custom_annotations = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'csharp_custom_test_method_annotation')
    if custom_annotations is not None:
        annotations.extend(custom_annotations)
    return annotations


def __get_java_testing_packages(project: Project) -> List[Any]:
    """
        Get a list of Java testing packages.

        Args:
            project (Project): The project for which testing packages are retrieved.

        Returns:
            List[Any]: A list of Java testing packages.
    """
    packages = []
    packages.extend(__java_testing_packages)
    custom_package = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'java_custom_testing_packages')
    if custom_package is not None:
        packages.extend(custom_package)
    return packages


def __get_csharp_testing_packages(project: Project) -> List[Any]:
    """
        Get a list of C# testing packages.

        Args:
            project (Project): The project for which testing packages are retrieved.

        Returns:
            List[Any]: A list of C# testing packages.
    """
    packages = []
    packages.extend(__csharp_testing_packages)
    custom_package = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'csharp_custom_testing_packages')

    packages = []
    packages.extend(__csharp_testing_packages)
    custom_package = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'csharp_custom_testing_packages')
    if custom_package is not None:
        packages.extend(custom_package)
    return packages


def __get_java_null_check_test_methods(project: Project) -> List[Any]:
    """
        Get a list of Java null check test methods.

        Args:
            project (Project): The project for which null check test methods are retrieved.

        Returns:
            List[Any]: A list of Java null check test methods.
    """
    code = []
    code.extend(__java_null_check_test_methods)
    custom_code = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'java_custom_null_check_test_methods')
    if custom_code is not None:
        code.extend(custom_code)
    return code


def __get_csharp_null_check_test_methods(project: Project) -> List[Any]:
    """
        Get a list of C# null check test methods.

        Args:
            project (Project): The project for which null check test methods are retrieved.

        Returns:
            List[Any]: A list of C# null check test methods.
    """
    code = []
    code.extend(__csharp_null_check_test_methods)
    custom_code = project.get_config_value(
        ConfigCustomFileType.Code, 'Test', 'csharp_custom_null_check_test_methods')
    if custom_code is not None:
        code.extend(custom_code)
    return code


def get_null_check_test_method(project: Project, language: LanguageType) -> Optional[List[Any]]:
    """
        Get null check test methods for a specific programming language.

        Args:
            project (Project): The project for which null check test methods are retrieved.
            language (LanguageType): The programming language for which null check test methods are requested.

        Returns:
            Optional[List[Any]]: A list of null check test methods for the specified language,
            or None if the language is not recognized.
    """
    if language == LanguageType.Java:
        return __get_java_null_check_test_methods(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_null_check_test_methods(project)
    else:
        return None


def get_testing_packages(project: Project, language: LanguageType) -> Optional[List[Any]]:
    """
        Get testing packages for a specific programming language.

        Args:
            project (Project): The project for which testing packages are retrieved. If None, the function uses the default project from TestingPackage.
            language (LanguageType): The programming language for which testing packages are requested.

        Returns:
            Optional[List[Any]]: A list of testing packages for the specified language, 
            or None if the language is not recognized.
    """
    if project is None:
        project = TestingPackage().project
    if language == LanguageType.Java:
        return __get_java_testing_packages(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_testing_packages(project)
    else:
        return None


def get_test_method_annotations(project: Project, language: LanguageType) -> Optional[List[Any]]:
    """
        Get test method annotations for a specific programming language.

        Args:
            project (Project): The project for which test method annotations are retrieved.
            language (LanguageType): The programming language for which test method annotations are requested.

        Returns:
            Optional[List[Any]]: A list of test method annotations for the specified language, 
            or None if the language is not recognized.
    """
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
