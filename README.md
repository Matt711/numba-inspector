# numba-inspector
View Numba compiled code in Jupyter

## Quickstart

### Installation

```console
$ pip install numba_inspector
```

### %%numba magic command

```python
%load_ext numba_inspector
```

```python
%%numba --bytecode

from numba import njit

@njit
def func(x,y):
    if x:
        x=x+1
        if y:
            y=y+1
        else:
            y=y-1
    else:
        x=x-1
        if y:
            y=y+1
        else:
            y=y-1
    return x+y

func(1,2)
```
