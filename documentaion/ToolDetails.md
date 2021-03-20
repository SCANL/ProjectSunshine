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
  - XX rules for test methods, defined by  Wu and Clause [2].
  - XX rules for test methods, defined by Peruma et al [3].



## Technical Details

- The tool is implemented in Python (v3.7).
- The tool utilizes srcML v1.0.0 [4] to parse source code files.
- The tool utilizes the following key external Python packages:
  - XML parsing - lxml (v4.6.2)
  - Term splitting - spiral (v1.1.0)
  - Natural language processing - nltk (v3.5)





## References

[1] Arnaoudova, V., Di Penta, M., & Antoniol, G. (2016). Linguistic antipatterns: What they are and how developers
perceive them. Empirical Software Engineering, 21(1), 104-158.

 [2] J. Wu and J. Clause, “A pattern-based approach to detect and improve non-descriptive test names,” Journal of Systems and Software, vol. 168, p. 110639, 2020.

[3] Peruma, A., Hu, E., Chen, J., Alomar, E. A., Mkaouer, M. W., & Newman, C. D. (2021). Using Grammar Patterns to Interpret Test Method Name Evolution. In Proceedings of the 29th International Conference on Program Comprehension.

[4] M. L. Collard, M. J. Decker and J. I. Maletic, "srcML: An Infrastructure for the Exploration, Analysis, and Manipulation of Source Code: A Tool Demonstration," 2013 IEEE International Conference on Software Maintenance, Eindhoven, Netherlands, 2013, pp. 516-519, doi: 10.1109/ICSM.2013.85.