# Writing Assertion Helper Functions

I don't have an actual use case yet, but I learned that I could write _assertion helper_ functions from Brian Okken's [Python Testing with Pytest](https://pythontest.com/pytest-book/).

An _assertion helper_ function is a function that is used to wrap complex assertions.

Here's an example from the book showing an _assertion helper_ function called **assert_identical**:

```python
from cards import Card
import pytest

def assert_identical(c1: Card, c2: Card):
    __tracebackhide__ = True
    assert c1 == c2
    if c1.id != c2.id:
        pytest.fail(f"IDs don't match. {c1} != {c2}")

def test_identical():
    c1 = Card("Foo", id=123)
    c1 = Card("Foo", id=123)
    assert_identical(c1, c2)

def test_identical():
    c1 = Card("Foo", id=123)
    c1 = Card("Foo", id=456)
    assert_identical(c1, c2)
```
