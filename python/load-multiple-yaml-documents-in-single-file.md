# Load Multiple YAML documents from single file

I've known that it was possible to have multiple documents in a single YAML file, but I hadn't had an actual use case that required it until recently.

You can use `pyYAML` to parse and load the file to do so.

```python
from pathlib import Path
import yaml

stream = Path("test.yaml").read_text()
documents = yaml.load_all(stream, Loader=yaml.Loader)

for doc in documents:
    print(doc)
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
