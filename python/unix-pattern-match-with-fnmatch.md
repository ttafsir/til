# Unix filename Pattern matching with fnmatch

The `fnmatch` module provides support for Unix shell-style wildcards, which are not the same as regular expressions (which are documented in the re module). - [Documentation](https://docs.python.org/3/library/fnmatch.html)


Examples:

`fnmatch.fnmatch(filename, pattern)`

Test whether the filename string matches the pattern string, returning True or False.

```python
import fnmatch
import os

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*.txt'):
        print(file)
```

> `fnmatch.fnmatchcase(filename, pattern)` is a case-sensitive version of fnmatch.fnmatch(). Also, It does not apply `os.path.normcase()`

`fnmatch.filter(names, pattern)`
Construct a list from those elements of the iterable names that match pattern. It is the same as `[n for n in names if fnmatch(n, pattern)]`, but implemented more efficiently.

```python
import fnmatch
import os

fnmatch.filter(os.listdir('./data/common'), "*.yaml")
```

`fnmatch.translate(pattern)`

Return the shell-style pattern converted to a regular expression for using with re.match().

```python
import fnmatch, re

regex = fnmatch.translate('*.txt')
regex

reobj = re.compile(regex)
reobj.match('foobar.txt')
```
