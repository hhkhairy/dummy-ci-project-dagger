from demo_ci_project.foo import Bar

def test_bar():
    bar = Bar('test')
    bar.try_something_stupid()
    assert True

def test_try_false():
    bar = Bar('test')
    bar.try_something_stupid()
    assert True