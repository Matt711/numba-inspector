def load_ipython_extension(ip):
    # A special IPython function that allows users to load the
    # the numba extension as `%load_ext numba` to access the 
    # Jupyter magic commmands
    from .ipython_magic import NumbaMagics
    ip.register_magics(NumbaMagics)