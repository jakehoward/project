from tasks.hello import hello


def test_hello() -> None:
    assert hello() == "Hello from tasks!"
