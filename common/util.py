import configparser
import logging
import os

from common.enum import LanguageType

log = logging.getLogger(__name__)


def get_config_setting(section, name):
    directory_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(directory_path, 'config.txt')

    config = configparser.ConfigParser()
    config.read(config_path)
    try:
        return config[section][name]
    except:
        log.exception(msg='Config setting %s not available.' % str(section + name), exc_info=True)


def get_file_name(file_path):
    head, tail = os.path.split(file_path)
    return tail


def remove_list_nestings(l):
    output = []
    for i in l:
        if type(i) == list:
            remove_list_nestings(i)
        else:
            output.append(i)
    return output


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

__java_testing_packages = [
    'junit.framework.Test',
    'junit.framework.TestCase',
    'org.junit.Test',
    'android.test.AndroidTestCase',
    'android.test.InstrumentationTestCase',
    'android.test.ActivityInstrumentationTestCase2',
    'org.junit.Assert'
]

__csharp_testing_packages = [
    'Microsoft.VisualStudio.TestTools.UnitTesting',
    'Microsoft.VisualStudio.QualityTools.UnitTesting.Framework',
    'NUnit.Tests',
    'NUnit.Framework',
    'Xunit',
    'Xunit.Abstractions'
]


def get_testing_packages(language):
    if language == LanguageType.Java:
        return __java_testing_packages
    elif language == LanguageType.CSharp:
        return __csharp_testing_packages
    else:
        return None


def get_collection_types(language):
    if language == LanguageType.Java:
        return __java_collection_data_types
    elif language == LanguageType.CPP:
        return __cplusplus_collection_data_types
    elif language == LanguageType.CSharp:
        return __csharp_collection_data_types
    else:
        return None


def get_primitive_types(language):
    if language == LanguageType.Java:
        return __java_primitive_data_types
    elif language == LanguageType.CPP:
        return __cplusplus_primitive_data_types
    elif language == LanguageType.CSharp:
        return __csharp_primitive_data_types
    else:
        return None


def get_supported_file_extensions():
    return ['.java', '.cs']