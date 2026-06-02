import heapq

def dijkstra(graph, start, end, stop_penalty=0):
    pq = [(0.0, 0.0, 0, start, [])]
    best_seen = {}

    while pq:
        priority, real_cost, hops, node, path = heapq.heappop(pq)
        if node in best_seen and best_seen[node] <= priority:
            continue
        best_seen[node] = priority
        path = path + [node]
        if node == end:
            return real_cost, path
        for next_node, weight in graph.get(node, {}).items():
            new_real = real_cost + weight
            new_hops = hops + 1
            penalty_scale = 0.01
            new_priority = new_real + new_hops * stop_penalty * penalty_scale
            if next_node in best_seen and best_seen[next_node] <= new_priority:
                continue
            heapq.heappush(pq, (new_priority, new_real, new_hops, next_node, path))
    return float('inf'), []

# Graph where there is a direct A->D (10) and a two-hop A->B->D (5+5=10)
graph = {
    'A': {'B': 5, 'D': 10},
    'B': {'D': 5},
    'D': {}
}

print('No penalty:')
cost0, path0 = dijkstra(graph, 'A', 'D', stop_penalty=0)
print('cost=', cost0, 'path=', path0)

print('\nWith penalty=2:')
cost1, path1 = dijkstra(graph, 'A', 'D', stop_penalty=2)
print('cost=', cost1, 'path=', path1)

print('\nWith penalty=5:')
cost2, path2 = dijkstra(graph, 'A', 'D', stop_penalty=5)
print('cost=', cost2, 'path=', path2)
