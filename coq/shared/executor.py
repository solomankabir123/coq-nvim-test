from concurrent.futures import Executor, Future, InvalidStateError
from contextlib import suppress
from queue import SimpleQueue
from typing import Any, Callable, TypeVar, cast

T = TypeVar("T")


class SingleThreadExecutor:
    def __init__(self, pool: Executor) -> None:
        self._q: SimpleQueue = SimpleQueue()
        pool.submit(self._forever)

    def _forever(self) -> None:
        while True:
            f = self._q.get()
            f()

    def submit(self, f: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        fut: Future = Future()

        def cont() -> None:
            try:
                ret = f(*args, **kwargs)
            except Exception as e:
                with suppress(InvalidStateError):
                    fut.set_exception(e)
            else:
                with suppress(InvalidStateError):
                    fut.set_result(ret)

        self._q.put(cont)
        return cast(T, fut.result())
