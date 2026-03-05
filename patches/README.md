# Python 3.11+ Compatibility Fix for `aphyt`

The original `aphyt` library contains a syntax error in f-strings that prevents it from running on Python 3.11 or newer. This directory contains instructions and a script to apply the fix.

## The Error
In `aphyt/cip/cip.py`, the `get_message` method uses single quotes for both the f-string and the inner `.decode('utf-8')`, which causes a syntax error in Python 3.11.

## How to fix manually
1. Locate your `aphyt` installation (e.g., in `site-packages/aphyt/cip/cip.py`).
2. Go to the `get_message` method (around line 89).
3. Change the outer quotes of the f-string from `'` to `"`.

## Automatic Patch
You can find the corrected file `cip.py` in this folder. Replace the original one in your Python environment with this version.
