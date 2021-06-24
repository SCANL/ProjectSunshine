# IDEAL Architecture

Implemented as a command-line/console-based tool in Python, IDEAL integrates with some well-known open-source libraries and tools in analyzing source code to detect identifier name violations. Depicted in the below figure is a view of the conceptual architecture of IDEAL. Broadly, IDEAL is composed of three layers-- Platform, Modules, and Interface. It utilizes well-known tools and libraries used for natural language and static analysis, including Spiral, NLTK, Wordnet, Stanford POS tagging, and srcML.

<img src="images\other\architecture.png" alt="architecture" style="zoom:50%;" />

## Platform 

The Platform layer consists of the underlying technology and libraries that IDEAL depends on, such as:

- **srcML** - A multi-language parsing tool that converts source code into an XML format. By utilizing srcML, IDEAL does not rely on multiple technology-dependent parsers to analyze C\# and Java source code. Furthermore, the incorporation of additional programming languages in future releases of IDEAL becomes less complicated.
- **Stanford POS Tagger** - A part-of-speech tagger utilized by IDEAL to determine the parts of speech (based on the Penn Treebank tag set) of words in an identifier's name.
- **NLTK** - The The Natural Language Toolkit is a collection of python-based natural language processing modules.
- **WordNet** - A lexical database for the English language. IDEAL utilizes WordNet to determine relationships between terms, such as synonyms and antonyms. 
- **Spiral** - A Python package that provides several different functions for splitting identifiers found in source code.

## Modules

Contained in this layer are the modules that provide the core functionality of detecting naming violations:  

- **srcML Parser** - This module aims to parse the srcML output and construct the identifier hierarchy for a class. Furthermore, using heuristics, such as namespaces and annotations, the module identifies unit test files and test methods.
- **Project Customizations** - With this module, the linguistic anti-patterns can account for project-specific data types and terminology associated with identifiers, thereby reducing the volume of reported false positives. Developers set the customizations in structured text files and associate these files with each execution of IDEAL.
- **Linguistic Anti-Patterns** - IDEAL appraises an identifier's name based on a set of linguistic anti-patterns. Each evaluation rule is implemented and executes independently of the others. This design construct ensures that failures of a single rule will not impact the IDEAL's overall execution. Furthermore, it also permits the seamless addition and removal of rules.
- **Results Reporting** -  On completion of execution, IDEAL saves the results into a Comma-Separated Values (CSV) file. For each detected violation, IDEAL saves the path of the file containing the identifier, the name and line number of the identifier, the issue type, and additional details around the issue in the CSV file. The CSV file can be easily imported into a spreadsheet or storage database for further analysis. 

## Interface

As a console application, IDEAL permits developers and build systems to perform offline analysis of the source code. IDEAL requires an input file that contains the list of files (or directories containing files) for analysis along with project-specific configurations and customizations such as custom types and terms.