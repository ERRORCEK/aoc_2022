import collections
import heapq
from typing import Any


def parse_input(filename) -> list[dict]:
    valves, tunnels = {}, {}
    with open(filename, encoding='utf-8') as _:
        for line in _.read().split('\n'):
            valve = line[6:8]
            flow_rate = int(line.split('=')[1].split(';')[0])
            new_tunnels = [x.strip()
                           for x in line.split('valve')[1][1:].split(',')]
            valves[valve] = flow_rate
            tunnels[valve] = new_tunnels
    return [valves, tunnels]


def calc_distances(valves, tunnels) -> dict[Any, dict[Any, int]]:
    """ Floyd-Warshall """
    dist = {a: {b: 1000 for b in valves} for a in valves}
    for x in valves:
        dist[x][x] = 0
        for y in tunnels[x]:
            dist[x][y] = 1
    for k in valves:
        for i in valves:
            for j in valves:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


State = collections.namedtuple("State", "flow,p1,t1,p2,t2,closed")
State.time = lambda s: min(s.t1, s.t2)


def generate_new_human_states(valves, dist, _s) -> list:
    if _s.time() != _s.t1:
        return [_s]

    if valves[_s.p1] and _s.p1 in _s.closed:
        return [_s._replace(
            flow=_s.flow - (29 - _s.time()) * valves[_s.p1],
            t1=_s.t1 + 1,
            closed=_s.closed - {_s.p1})]

    new_states = [_s._replace(p1=dest, t1=_s.t1 + dist[_s.p1][dest])
                  for dest in _s.closed]

    if not new_states:
        return [_s._replace(t1=30)]
    return new_states


def generate_new_elephant_states(valves, dist, states) -> list:
    new_states = []
    for _s in states:
        if _s.time() != _s.t2:
            new_states.append(_s)
        elif valves[_s.p2] and _s.p2 in _s.closed:
            new_states.append(_s._replace(
                flow=_s.flow - (29 - _s.time()) * valves[_s.p2],
                t2=_s.t2 + 1,
                closed=_s.closed - {_s.p2}))
        else:
            new_states.extend(
                [_s._replace(p2=dest, t2=_s.t2 + dist[_s.p2][dest]) for dest in _s.closed])

    if not new_states:
        return [s._replace(t2=30) for s in states]
    return new_states


def part1(valves, dist) -> int:
    _pq = []
    heapq.heappush(_pq, State(0, 'AA', 0, 'AA', 30, {
                   k for k, v in valves.items() if v}))

    best, best_for_time = 0, collections.defaultdict(int)
    while _pq:
        cur = heapq.heappop(_pq)
        best = min(cur.flow, best)
        best_for_time[cur.time()] = min(best_for_time[cur.time()], cur.flow)
        if (cur.time() < 30 and cur.closed and
                (cur.time() < 10 or 1.5 * cur.flow <= best_for_time[cur.time()])):
            for _s in generate_new_human_states(valves, dist, cur):
                heapq.heappush(_pq, _s)

    return -best


def part2(valves, dist) -> int:
    _pq = []
    heapq.heappush(_pq, State(0, 'AA', 4, 'AA', 4, set(
        k for k, v in valves.items() if v)))
    best, best_for_time = 0, collections.defaultdict(int)
    while _pq:
        cur = heapq.heappop(_pq)
        best = min(cur.flow, best)
        best_for_time[cur.time()] = min(best_for_time[cur.time()], cur.flow)
        if cur.time() < 30 and cur.closed:
            if cur.time() < 12 or 1.25 * cur.flow <= best_for_time[cur.time()]:
                h_states = generate_new_human_states(valves, dist, cur)
                e_states = generate_new_elephant_states(valves, dist, h_states)
                for _s in e_states:
                    heapq.heappush(_pq, _s)
    return -best


if __name__ == '__main__':
    i_valves, i_tunnels = parse_input('input.txt')
    i_dist = calc_distances(i_valves, i_tunnels)
    print(part1(i_valves, i_dist))
    print(part2(i_valves, i_dist))
