# file-util
The utility to manuplate one file, or manage a structure of source folder parsed with keywords.

## The environment
python 3.7+(recommended)

## Installation

```bash
git clone https://github.com/stevencychuang/file-util.git
cd file-util
pip install .
```

## Usage
Please refer [example.ipynb](example.ipynb).
You can parse the structure of specific directory with the keyword
```python
from fileutil import FileParser
parser = FileParser(r"tmp", "*.py")
print("The dictionary:\r\n", parser.get_dict())
```
Besides, you can copy the parsed structure to another destination
```python
# The simple way
parser.cp2dst("tmp1")

# Advanced way to preprocess the destination and then to copy
parser.det_dst("tmp3")
parser.replace_dst({"directory": "directory1", ".py": ".txt"})
parser.cp2dst()
```
