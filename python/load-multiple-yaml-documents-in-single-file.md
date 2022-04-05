# Load Multiple YAML documents from single file

I've known that it was possible to have multiple documents in a single YAML file, but I hadn't had an actual use case that required it until recently.  In YAML, a new document starts with a `---` marker. Then, you delimit each using the same marker as shown below to combine multiple documents.

```yaml
---
name: document 1

---
name: document 2

---
name: document 3
```

You can then use `pyYAML` to load the file and parse the documents.

```python
>>> from pathlib import Path
>>> import yaml
>>> 
>>> stream = Path("test.yaml").read_text()
>>> documents = yaml.load_all(stream, Loader=yaml.Loader)
>>> 
>>> for doc in documents:
...     print(doc)
... 
{'name': 'document 1'}
{'name': 'document 2'}
{'name': 'document 3'}
```

I was a little frustrated that following the documented way to load the documents led to failures. I'm currently using version `6.0`, which has now deprecated the use of `yaml.load_all()` without specifying `Loader=Loader.` However, the [Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation) still showed the deprecated method.

Here's the version of the failing code.

```python
from pathlib import Path
import yaml

stream = Path("test.yaml").read_text()
documents = yaml.load_all(stream)

for doc in documents:
    print(doc)
```

Below is the error.

```sh
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: load_all() missing 1 required positional argument: 'Loader'
```

Here's the link to a pinned discussion regarding the issue: https://github.com/yaml/pyyaml/issues/576. There have been deprecation notices for three years before the breaking change.
