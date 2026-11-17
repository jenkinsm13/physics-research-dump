"""Basic test to verify that dividebyzero import works."""

import numpy as np
import sys

try:
    import dividebyzero as dbz
    from dividebyzero.array import DimensionalArray
    from dividebyzero.exceptions import DimensionalError
    print("Successfully imported dividebyzero modules!")
    
    # Test creating an array
    a = dbz.array([1, 2, 3])
    print(f"Created array with shape {a.shape}")
    
    # Test basic operations
    b = a * 2
    print(f"a * 2 = {b.array}")
    
    c = a + 1
    print(f"a + 1 = {c.array}")
    
    # Test division by zero
    d = a / 0
    print(f"a / 0 created an array with shape {d.shape}")
    
    # Test elevation
    e = d.elevate()
    print(f"After elevation back to shape {e.shape}, values: {e.array}")
    
    print("All basic tests passed!")
except ImportError as e:
    print(f"Error importing: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)