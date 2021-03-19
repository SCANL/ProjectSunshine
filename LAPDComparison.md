## LAPD (Linguistic Anti-Pattern Detector)

Tool initially developed by Arnaoudova et al.[1] and extended in [2].

### Tool Comparison

| LAPD                                                       | SCANL                                                        |
| :--------------------------------------------------------- | :----------------------------------------------------------- |
| Tool/Source code is not available                          | ***Source code available on GitHub***                        |
| Analyzes methods and attributes                            | ***Analyzes methods, attributes, method variables, and method parameters; supports analysis of class names*** |
| Utilizes srcML based                                       | Utilizes srcML based                                         |
| Supports C++ and Java                                      | ***Supports C++, Java, and C#***                             |
| Utilizes WordNet and Stanford tagger                       | Utilizes WordNet and Stanford tagger                         |
| Unknown                                                    | ***Supports custom linguistic terms in rule analysis***      |
| C++ is offline; ***Java is an Eclipse Checkstyle plugin*** | Completely offline                                           |
|                                                            |                                                              |
|                                                            |                                                              |
|                                                            |                                                              |

### Open Items

- Need the dataset analyzed by LDAP -- identifiers that exhibited anti-patterns. Use this to compare the correctness of our tool.
- Can we combine some rules (e.g., C1 & F1, C2 & F2)?
- Clarification on B4 & A2.



### References

- [1] Arnaoudova V, Di Penta M, Antoniol G, Gu´eh´eneuc YG (2013) A new family of software anti-patterns: Linguistic
  anti-patterns. In: Proceedings of the European Conference on Software Maintenance and Reengineering (CSMR), pp 187–196
- [2] Arnaoudova, V., Di Penta, M., & Antoniol, G. (2016). Linguistic antipatterns: What they are and how developers
  perceive them. Empirical Software Engineering, 21(1), 104-158.