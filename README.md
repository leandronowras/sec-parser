## Parser Structure

folders with what it is expected to have:

## /sec_parser
### /parsing_engine/
* Abstract class with the methods for each implementations
* Concrete implementation

obs: missing sec_parser abstract class??

### /parsing_plugin/
* orquestration of engines
* logic of how engines should interact

### /semantic_elements/
* Abstract class with the methods for each semantic_element
* Concrete implementation

### /semantic_tree_transformation/
* rules.py
    - how the hierarchy should behave
* semantic_tree.py
    - class of the semantic tree
* tree_builder.py
    - builder for the three
* tree_node.py
    - class of the tree's nodes

### TODO:
- [ ] better definition of what a semantic_element is

