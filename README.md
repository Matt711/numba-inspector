# numba-inspector
Visualize and Debug Numba compiled code in Jupyter

## Quickstart

### Installation

Install the package:
```console
pip install numba-inspector
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
![View the bytecode of a jitted function (CPUDispatcher object)](https://raw.githubusercontent.com/Matt711/numba-inspector/main/examples/cpu_dispatcher_control_flow.png)


Install the cudatoolkit:
```console
conda install cudatoolkit
```

```python
%%numba --ptx

from numba import cuda
import numpy as np

@cuda.jit(lineinfo=True)
def increment_by_one(an_array):
    # Thread id in a 1D block
    tx = cuda.threadIdx.x
    # Block id in a 1D grid
    ty = cuda.blockIdx.x
    # Block width, i.e. number of threads per block
    bw = cuda.blockDim.x
    # Compute flattened index inside the array
    pos = tx + ty * bw
    if pos < an_array.size:  # Check array boundaries
        an_array[pos] += 1
        
a = np.arange(4096,dtype=np.float32)
d_a = cuda.to_device(a)
blocks = 32
threads = 128
increment_by_one[blocks, threads](d_a)
cuda.synchronize()
d_a.copy_to_host()
```
![View the PTX of CUDA kernel (CPUDispatcher object example)](https://raw.githubusercontent.com/Matt711/numba-inspector/main/examples/cuda_dispatcher.png)
