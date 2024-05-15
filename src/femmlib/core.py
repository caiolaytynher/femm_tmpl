import time
from collections.abc import Iterator
from contextlib import contextmanager

import femm


@contextmanager
def open_femm(*, delay: int = 0) -> Iterator[None]:
    try:
        femm.openfemm()
        if delay > 0:
            time.sleep(delay)
        yield
    finally:
        femm.closefemm()
