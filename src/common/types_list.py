from typing import List, Optional
from src.common.enum import LanguageType
from src.model.project import ConfigCustomFileType, Project

__cplusplus_primitive_data_types = ['int', 'unsigned int', 'signed int', 'short', 'short int', 'unsigned short', 'long',
                                    'long double', 'unsigned long', 'float', 'double', 'char', 'unsigned char',
                                    'signed char', 'bool']

# https://www.cplusplus.com/reference/stl/
__cplusplus_collection_data_types = [
    'array',
    'vector',
    'deque',
    'forward_list',
    'list',
    'stack',
    'queue',
    'priority_queue',
    'set',
    'multiset',
    'map',
    'multimap',
    'unordered_set',
    'unordered_multiset',
    'unordered_map',
    'unordered_multimap'
]

# https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/built-in-types
__csharp_primitive_data_types = ['bool', 'byte', 'sbyte', 'char', 'decimal', 'double', 'float', 'int', 'uint', 'long',
                                 'ulong', 'short', 'ushort', 'object', 'string', 'dynamic']

__csharp_numeric_data_types = ['byte', 'sbyte',  'decimal', 'double',
                               'float', 'int', 'uint', 'long', 'ulong', 'short', 'ushort']

# https://docs.microsoft.com/en-us/dotnet/standard/collections/commonly-used-collection-types
__csharp_collection_data_types = [
    'Dictionary',
    'List',
    'Queue',
    'Stack',
    'LinkedList',
    'ObservableCollection',
    'SortedList',
    'HashSet',
    'SortedSet',
    'Hashtable',
    'Array',
    'ArrayList',
    'ConcurrentDictionary',
    'BitArray',
    'BlockingCollection',
    'ConcurrentQueue',
    'ConcurrentStack',
    'ConcurrentBag',
    'ICollection',
    'IComparer',
    'IDictionary',
    'IDictionaryEnumerator',
    'IEnumerable',
    'IEnumerator',
    'IEqualityComparer',
    'IHashCodeProvider',
    'IList',
    'IStructuralComparable',
    'IStructuralEquatable',
    'Collection',
    'ReadOnlyObservableCollection',
    'KeyedCollection',
    'ReadOnlyCollection',
    'ReadOnlyDictionary'
]

# https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html
__java_primitive_data_types = [
    'byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']

__java_numeric_data_types = ['byte', 'short', 'int', 'long', 'float',
                             'double', 'Byte', 'Float', 'Integer', 'Long', 'Number', 'Short']

# https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html
__java_collection_data_types = [
    'ArrayBlockingQueue',
    'ArrayDeque',
    'ArrayList',
    'BlockingDeque',
    'BlockingQueue',
    'Collection',
    'ConcurrentHashMap',
    'ConcurrentMap',
    'ConcurrentNavigableMap',
    'ConcurrentSkipListMap',
    'ConcurrentSkipListSet',
    'CopyOnWriteArrayList',
    'CopyOnWriteArraySet',
    'DelayQueue',
    'Deque',
    'HashMap',
    'HashSet',
    'Hashtable',
    'Iterator ',
    'LinkedBlockingDeque',
    'LinkedBlockingQueue',
    'LinkedHashMap',
    'LinkedHashSet',
    'LinkedList',
    'LinkedTransferQueue',
    'List',
    'ListIterator',
    'Map',
    'NavigableMap',
    'NavigableSet',
    'PriorityBlockingQueue',
    'PriorityQueue',
    'Queue',
    'Set',
    'SortedMap',
    'SortedSet',
    'SynchronousQueue',
    'TransferQueue',
    'TreeMap',
    'TreeSet',
    'Vector',
    'BitSet'
]


def __get_cplusplus_collection_data_types() -> List[str]:
    """
        Get a list of C++ collection data types.

        Args:
            project: The project (not used in this function).

        Returns:
            List[str]: A list of C++ collection data types.
    """
    return __cplusplus_collection_data_types


def __get_cplusplus_primitive_data_types() -> List[str]:
    """
        Get a list of C++ primitive data types.

        Returns:
            List[str]: A list of C++ primitive data types.
    """
    return __cplusplus_primitive_data_types


def __get_java_primitive_data_types() -> List[str]:
    """
        Get a list of Java primitive data types.

        Returns:
            List[str]: A list of Java primitive data types.
    """
    return __java_primitive_data_types


def __get_csharp_primitive_data_types() -> List[str]:
    """
        Get a list of C# primitive data types.

        Returns:
            List[str]: A list of C# primitive data types.
    """
    return __csharp_primitive_data_types


def __get_java_numeric_data_types() -> List[str]:
    """
        Get a list of Java numeric data types.

        Returns:
            List[str]: A list of Java numeric data types.
    """
    return __java_numeric_data_types


def __get_csharp_numeric_data_types() -> List[str]:
    """
        Get a list of C# numeric data types.

        Returns:
            List[str]: A list of C# numeric data types.
    """
    return __csharp_numeric_data_types


def __get_csharp_collection_data_types(project: Project) -> List[str]:
    """
        Get a list of C# collection data types.

        Args:
            project (Project): The project instance containing project-specific configuration.

        Returns:
            List[str]: A list of C# collection data types, including custom types if defined in the project configuration.
    """
    types = []
    types.extend(__csharp_collection_data_types)
    custom_types = project.get_config_value(
        ConfigCustomFileType.Code, 'DataTypes', 'csharp_custom_collection_data_types')
    if custom_types is not None:
        types.extend(custom_types)
    return types


def __get_java_collection_data_types(project: Project):
    """
        Get a list of Java collection data types.

        Args:
            project (Project): The project instance containing project-specific configuration.

        Returns:
            List[str]: A list of Java collection data types, including custom types if defined in the project configuration.
    """
    types = []
    types.extend(__java_collection_data_types)
    custom_types = project.get_config_value(
        ConfigCustomFileType.Code, 'DataTypes', 'java_custom_collection_data_types')
    if custom_types is not None:
        types.extend(custom_types)
    return types


def get_collection_types(project: Project, language: LanguageType) -> Optional[List[str]]:
    """
        Get collection data types for a specific programming language.

        Args:
            project (Project): The project instance containing project-specific configuration.
            language (LanguageType): The programming language for which collection data types are requested.

        Returns:
            List[str] or None: A list of collection data types for the specified language, including custom types if defined in the project configuration, 
            or None if the language is not recognized.
    """
    if language == LanguageType.Java:
        return __get_java_collection_data_types(project)
    elif language == LanguageType.CPP:
        return __get_cplusplus_collection_data_types()
    elif language == LanguageType.CSharp:
        return __get_csharp_collection_data_types(project)
    else:
        return None


def get_primitive_types(language: LanguageType) -> Optional[List[str]]:
    """
        Get primitive data types for a specific programming language.

        Args:
            language (LanguageType): The programming language for which primitive data types are requested.

        Returns:
            List[str] or None: A list of primitive data types for the specified language, 
            or None if the language is not recognized.
    """
    if language == LanguageType.Java:
        return __get_java_primitive_data_types()
    elif language == LanguageType.CPP:
        return __get_cplusplus_primitive_data_types()
    elif language == LanguageType.CSharp:
        return __get_csharp_primitive_data_types()
    else:
        return None


def get_numeric_types(language: LanguageType) -> Optional[List[str]]:
    """
        Get numeric data types for a specific programming language.

        Args:
            language (LanguageType): The programming language for which numeric data types are requested.

        Returns:
            List[str] or None: A list of numeric data types for the specified language, 
            or None if the language is not recognized.
    """
    if language == LanguageType.Java:
        return __get_java_numeric_data_types()
    elif language == LanguageType.CSharp:
        return __get_csharp_numeric_data_types()
    else:
        return None


def get_bool_types(language: LanguageType) -> Optional[List[str]]:
    """
        Get boolean data types for a specific programming language.

        Args:
            language (LanguageType): The programming language for which boolean data types are requested.

        Returns:
            List[str] or None: A list of boolean data types for the specified language, 
            or None if the language is not recognized.
    """
    if language == LanguageType.Java:
        return ['boolean', 'Boolean', 'Predicate']
    elif language == LanguageType.CSharp:
        return ['bool', 'Boolean', 'Predicate']
    else:
        return None
