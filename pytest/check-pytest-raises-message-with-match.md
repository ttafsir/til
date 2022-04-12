# Check pytest.raises exception message with match

Another gem from the [Python testing with Pytest](https://pythontest.com/pytest-book/) I learned is that you can check the message raised by an exception using regular expressions.

Here's an example of what I was doing before. I was using an additional assert outside the `with` context manager to check the message.

```python
@pytest.mark.parametrize("filename", ["tower_payload_schema.json"])
def test_uat_environment_wo_change_record_fails(self, schema):
    data = _load_json(Path("uat_env_wo_crfield_f_fails.json"))
    with pytest.raises(ValidationError) as error:
        assert_valid_schema(data, schema)
    expected = "is a required property"
    assert expected in str(error)
```

Now, I simply pass a regular expression pattern to the `match` argument.

```python
@pytest.mark.parametrize("filename", ["tower_payload_schema.json"])
def test_uat_environment_wo_change_record_fails(self, schema):
    data = _load_json(Path("uat_env_wo_crfield_f_fails.json"))
    match_re = ".* is a required property"
    with pytest.raises(ValidationError, match=match_re):
        assert_valid_schema(data, schema)
```

I prefer this approach because it's more readable, and I don't have to worry about the exact message!
