# pickle-jar


Pickle Jar is a small utility to used to locally store intermediate results of time consuming functions.


## Usage

```python
from pickle_jar import pickle_jar


@pickle_jar()
def time_consuming_function():
    import time
    time.sleep(5)
    return {'results': 'any kind of results'}

result = time_consuming_function() # Takes ~5 seconds
result2 = time_consuming_function() # Takes less than 1 second
assert result == result2

```

### Detects Changes in Arguments (and Function Source Code)
```python
@pickle_jar()
def function_with_args(result_string):
    import time
    time.sleep(3)
    return {'results': result_string}


result = function_with_args('result') # Takes ~3 seconds
result2 = function_with_args('result') # Takes less than 1 second
assert result == result2
result3 = function_with_args('a different result') # Takes ~3 seconds
result4 = function_with_args('a different result') # Takes less than 1 second
assert result3 == result4
assert result2 != result3
result5 = function_with_args('result') # Still cached, takes less than 1 second
assert result == result5
assert result3 != result5

```

### Clear The Cache (Empty the Pickle Jar)
```python
pickle_jar().clear_cache('time_consuming_function')
```