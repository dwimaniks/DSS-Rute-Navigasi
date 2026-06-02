import heapq

graph = {
    "Kuta": {"Sanur": 10, "Ubud": 35, "Denpasar": 6, "Badung Regency": 5, "Legian": 3, "Seminyak": 4, "Tuban": 3, "Kedonganan": 4},
    "Sanur": {"Kuta": 10, "Ubud": 20, "Tanah Lot": 30, "Denpasar": 4, "Gianyar Regency": 25},
    "Ubud": {"Kuta": 35, "Sanur": 20, "GWK": 40, "Gianyar Regency": 5, "Klungkung Regency": 35, "Karangasem Regency": 90, "Mengwi": 18},
    "Tanah Lot": {"Sanur": 30, "GWK": 25, "Tabanan Regency": 15, "Buleleng Regency": 45},
    "GWK": {"Ubud": 40, "Tanah Lot": 25},
    "Denpasar": {"Kuta": 6, "Sanur": 4, "Badung Regency": 8},
    "Badung Regency": {"Kuta": 5, "Denpasar": 8, "Tabanan Regency": 15, "Abiansemal": 10, "Mengwi": 10, "Petang": 12},
    "Tabanan Regency": {"Badung Regency": 15, "Tanah Lot": 15, "Jembrana Regency": 60},
    "Jembrana Regency": {"Tabanan Regency": 60},
    "Buleleng Regency": {"Tanah Lot": 45},
    "Bangli Regency": {"Gianyar Regency": 10, "Ubud": 30},
    "Karangasem Regency": {"Ubud": 90},
    "Klungkung Regency": {"Ubud": 35},
    "Gianyar Regency": {"Sanur": 25, "Ubud": 5, "Bangli Regency": 10},
    "Legian": {"Kuta": 3},
    "Seminyak": {"Kuta": 4},
    "Tuban": {"Kuta": 3},
    "Kedonganan": {"Kuta": 4},
    "Abiansemal": {"Badung Regency": 10},
    "Mengwi": {"Badung Regency": 10, "Sempidi": 6, "Ubud": 18},
    "Sempidi": {"Mengwi": 6},
    "Petang": {"Badung Regency": 12, "Carangsari": 8, "Belok Sidan": 9},
    "Carangsari": {"Petang": 8},
    "Belok Sidan": {"Petang": 9}
}


def dijkstra(graph, start, end, stop_penalty=0):
    pq = [(0.0, 0.0, 0, start, [])]
    best_seen = {}
    penalty_scale = 0.01

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
            new_priority = new_real + new_hops * stop_penalty * penalty_scale
            if next_node in best_seen and best_seen[next_node] <= new_priority:
                continue
            heapq.heappush(pq, (new_priority, new_real, new_hops, next_node, path))
    return float('inf'), []

if __name__ == '__main__':
    for sp in (0, 2, 5):
        cost, path = dijkstra(graph, 'Mengwi', 'Klungkung Regency', stop_penalty=sp)
        print(f'stop_penalty={sp} -> cost={cost}, path={path}')
