import configparser
import logging
import os

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


# https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html
java_primitive_data_types = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']

# https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html
java_collection_data_types = [
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
