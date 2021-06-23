## Document Purpose

This document provides details (functional and technical) around our linguistic anti-pattern detection tool.



## Functional Requirements

- Supported programming languages: Java and C#
- Analyze one or more source code files
  - The tool can either accept the path to a directory or a source code file.
  - If a directory is provided, the tool will analyze all source code files within the directory and its subdirectories recursively.
  - The user can specify if the file or (files in the directory) are test or non-test files. If the type is not specified, the tool will automatically determine the file type based on the import/using statements present in the file.

- The tool will detect and analyze the following identifiers in a file: classes, class variables (i.e., attributes), methods, method parameters, and method variables. Note: constants fall under attributes/variables.
- The detected violations are saved in a CSV file. The details include the violating identifier and the type of violation.
- The tool checks for the presence of:
  - 17 linguistic anti-patterns, defined by  Arnaoudova et al [1].
    - The original definitions of the anti-patterns apply to methods and attributes. Our implementation includes applying specific anti-patterns to method variables and method parameters.
  - 1 rule for test methods.
  - 1 rule for identifier names in C#



## Technical Details

- The tool is implemented in Python (v3.7).
- The tool utilizes srcML v1.0.0 to parse source code files.
- The tool utilizes the following key external Python packages:
  - XML parsing - lxml (v4.6.2)
  - Term splitting - spiral (v1.1.0)
  - Natural language processing - nltk (v3.5)
  - Part-of-Speech tagging - Stanford tagger (4.2.0)


## References

[1] Arnaoudova, V., Di Penta, M., & Antoniol, G. (2016). Linguistic antipatterns: What they are and how developers
perceive them. Empirical Software Engineering, 21(1), 104-158.


##### [Back To ReadMe](../README.md)