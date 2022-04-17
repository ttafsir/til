# Deciding Fixture Scope Dynamically

A few days ago, I learned that you can dynamically decide the scope of a fixture at runtime to facilitate testing with different scopes.

The examples below are from the [Python Testing with Pytest](https://pythontest.com/pytest-book/), and they show how to use the scope argument to decide the scope of a fixture dynamically.

```python
@pytest.fixture(scope=db_scope)
def db():
    """CardsDB object connected to a temporary database"""
    with TemporaryDirectory() as db_dir:
        db_path = Path(db_dir)
        db = cards.CardsDB(db_path)
        yield db
        db.close()

def db_scope(fixture_name, config):
  if config.getoption("--func-db", None):
    return "function"
  return "session"
```

We're using a function named `db_scope` instead of a specific scope like "function" or "session" because we want to be able to decide the scope of the fixture at runtime dynamically.

In `conftest.py`, we can then set up an option flag to accept a value at the CLI.

```python
def pytest_addoption(parser):
  parser.addoption(
  	"--func-db",
    action="store_true",
    default=False,
    help="use function scope db for each test"
  )
```

Running with test with our `--func-db` flag shows that we're using the function `F` scope.

```sh
➜ pytest --func-db --setup-show test_count.py
====================================== test session starts ================================================================
test_count.py
        SETUP    F db
        SETUP    F cards_db (fixtures used: db)
        ch3/d/test_count.py::test_empty (fixtures used: cards_db, db).
        TEARDOWN F cards_db
        TEARDOWN F db
        SETUP    F db
        SETUP    F cards_db (fixtures used: db)
        ch3/d/test_count.py::test_two (fixtures used: cards_db, db).
        TEARDOWN F cards_db
        TEARDOWN F db

========================================= 2 passed in 0.02s =================================================================
```

Running the test without the flag, shows the session `S` scope.

```sh
➜ pytest --setup-show test_count.py
=========================================== test session starts ================================================================
test_count.py
SETUP    S db
        SETUP    F cards_db (fixtures used: db)
        ch3/d/test_count.py::test_empty (fixtures used: cards_db, db).
        TEARDOWN F cards_db
        SETUP    F cards_db (fixtures used: db)
        ch3/d/test_count.py::test_two (fixtures used: cards_db, db).
        TEARDOWN F cards_db
TEARDOWN S db

=========================================== 2 passed in 0.01s =================================================================
```
