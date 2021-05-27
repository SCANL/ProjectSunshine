from src.common.enum import LanguageType
from src.model.project import ConfigCustomFileType

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
    'ConcurrentBag'
]

# https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html
__java_primitive_data_types = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']

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
    'Vector'
]


def __get_cplusplus_collection_data_types(project):
    return __cplusplus_collection_data_types


def __get_cplusplus_primitive_data_types():
    return __cplusplus_primitive_data_types


def __get_java_primitive_data_types():
    return __java_primitive_data_types


def __get_csharp_primitive_data_types():
    return __csharp_primitive_data_types


def __get_csharp_collection_data_types(project):
    types = []
    types.extend(__csharp_collection_data_types)
    custom_types = project.get_config_value(ConfigCustomFileType.Code, 'DataTypes', 'csharp_custom_collection_data_types')
    if custom_types is not None:
        types.extend(custom_types)
    return types


def __get_java_collection_data_types(project):
    types = []
    types.extend(__java_collection_data_types)
    custom_types = project.get_config_value(ConfigCustomFileType.Code, 'DataTypes', 'java_custom_collection_data_types')
    if custom_types is not None:
        types.extend(custom_types)
    return types


def get_collection_types(project, language):
    if language == LanguageType.Java:
        return __get_java_collection_data_types(project)
    elif language == LanguageType.CPP:
        return __get_cplusplus_collection_data_types(project)
    elif language == LanguageType.CSharp:
        return __get_csharp_collection_data_types(project)
    else:
        return None


def get_primitive_types(language):
    if language == LanguageType.Java:
        return __get_java_primitive_data_types()
    elif language == LanguageType.CPP:
        return __get_cplusplus_primitive_data_types()
    elif language == LanguageType.CSharp:
        return __get_csharp_primitive_data_types()
    else:
        return None
