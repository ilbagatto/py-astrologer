import collections
from operator import attrgetter
from typing import Iterable

from astrologer.aspects.aspects import Aspect, AspectInfo, AspectType
from astrologer.aspects.orbs import ClassicWithAspectRatio, OrbsMethod
from astrologer.objects import ChartObjectInfo
from astropc.mathutils import diff_angle, shortest_arc_deg


def find_closest_aspect(
    source: ChartObjectInfo,
    target: ChartObjectInfo,
    orbs_method: OrbsMethod | None = None,
    type_flags: int = AspectType.MAJOR.value,
) -> AspectInfo | None:
    """Find closest aspect between two objects.

    Args:
        source (ChartObjectInfo): the first object.
        target (ChartObjectInfo): the second object.

    Returns:
        AspectInfo | None: Aspect details, if any.
    """
    if orbs_method is None:
        orbs_method = ClassicWithAspectRatio()

    closest = None
    arc = shortest_arc_deg(source.position.lmbda, target.position.lmbda)
    for asp in Aspect:
        if asp.type.value & type_flags:
            info = orbs_method.is_aspect(source, target, asp, arc)
            if info is None:
                continue
            if closest is None or closest.delta > info.delta:
                closest = info
    return closest


def iter_stelliums(
    objects: Iterable[ChartObjectInfo], gap: float = 10.0
) -> Iterable[tuple[ChartObjectInfo, ...]]:
    """Partition celestial points to stelliums — closely spaced objects.

    Args:
        objects (Iterable[ChartObjectInfo]): celettial bodies
        gap (float, optional): minimal distance between groups. Defaults to 10.0.

    Returns:
        Iterable[tuple[ChartObjectInfo, ...]]: iterator on stelliums

    Yields:
        Iterator[Iterable[tuple[ChartObjectInfo, ...]]]: stellium
    """
    sorted_objs = sorted(objects, key=attrgetter("position.lmbda"))
    deq = collections.deque(sorted_objs)
    for _ in range(len(sorted_objs)):
        first = deq.popleft()
        last = deq.pop()
        if shortest_arc_deg(first.position.lmbda, last.position.lmbda) <= gap:
            deq.insert(0, first)
            deq.insert(0, last)
        else:
            deq.insert(0, first)
            deq.append(last)
            break
    ordered_objs = list(deq)
    last_idx = len(ordered_objs) - 1

    group: list[ChartObjectInfo] | None = None

    for idx, curr_obj in enumerate(ordered_objs):
        if group is None:
            group = []
        group.append(curr_obj)
        if idx < last_idx:
            next_obj = ordered_objs[idx + 1]
            if diff_angle(curr_obj.position.lmbda, next_obj.position.lmbda) > gap:
                yield tuple(group)
                group = None
        else:
            yield tuple(group)
            group = None
