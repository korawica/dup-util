from collections import defaultdict
from functools import partial
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
)

T = TypeVar("T")


def ordered(value: Any) -> Any:
    """Order an object by ``sorted``.

    Examples:
        >>> ordered([[11], [2], [4, 1]])
        [[1, 4], [2], [11]]
    """
    if isinstance(value, dict):
        return sorted((k, ordered(v)) for k, v in value.items())
    elif isinstance(value, list):
        return sorted(ordered(x) for x in value)
    return value


def sort_list_by_priority(
    values: Union[Iterable, List[T]],
    priority: List[T],
    reverse: bool = False,
    mode: Optional[str] = None,
) -> List[T]:
    """Sorts an iterable according to a list of priority items.

    Examples:
        >>> sort_list_by_priority(values=[1, 2, 2, 3], priority=[2, 3, 1])
        [2, 2, 3, 1]
        >>> sort_list_by_priority(values={1, 2, 3}, priority=[2,3])
        [2, 3, 1]
    """
    _mode: str = mode or "default"

    def _enumerate(_values, _priority, _reverse):
        priority_dict = {k: i for i, k in enumerate(_priority)}

        def priority_getter(value):
            return priority_dict.get(value, len(_values))

        return sorted(_values, key=priority_getter, reverse=_reverse)

    def default(_values, _priority, _reverse):
        priority_dict = defaultdict(
            lambda: len(_priority),
            zip(
                _priority,
                range(len(_priority)),
            ),
        )
        priority_getter = priority_dict.__getitem__  # dict.get(key)
        return sorted(_values, key=priority_getter, reverse=_reverse)

    switcher: Dict[str, partial] = {
        "chain": partial(default, values, priority, reverse),
        "enumerate": partial(_enumerate, values, priority, reverse),
    }

    func = switcher.get(_mode, lambda: [])
    return func()
