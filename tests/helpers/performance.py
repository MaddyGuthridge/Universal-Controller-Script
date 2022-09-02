"""

"""

import os
import functools


@functools.cache
def perfTestsSkipped() -> dict:
    """
    Used to check if we should skip tests which depend on CPU performance.

    This checks for the UCS_PERF_TEST environment variable, which can be set by
    running the following command in your shell.

    ```bash
    export UCS_PERF_TEST="TRUE"
    ```

    You can use this function to skip tests as follows:
    ```py
    @pytest.mark.skipif(**perfTestsSkipped())
    def my_test():
        ...
    ```
    """
    return {
        'condition': os.environ.get('UCS_PERF_TEST', '') == '',
        'reason': 'Performance tests disabled'
    }
