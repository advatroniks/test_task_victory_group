from collections import defaultdict, deque


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def create_nodes_in_graph(data_dict: dict):
    nodes = []
    links_with_price = []
    for key, value in data_dict.items():
        nodes.append(key)
        if isinstance(value, dict):
            for w, d in value.items():
                links_with_price.append([key, w, d[0]])
                nodes.append(w)
    return nodes, links_with_price


def run_algorithm(
        data_dict: dict,
        arr_airport: str,
        dep_airport: str,
):
    """
    Функция, которая запускает Алгоритм Дейкстры для поиска самой дешевой связки билетов.
    example for data_dict >>>  {
    "USPP": {
        "UNNT": [4056, "2023-12-04T05:01:36.440052"]
    },
    "UNNT": {
        "UUDD": [4457, "2023-12-04T16:04:21.998287"],
        "XHSO": [6313, "2023-12-04T15:13:32.598047"],
        "UUOL": [4426, "2023-12-04T21:37:32.909848"],
        "UUUQ": [3885, "2023-12-04T10:23:29.142713"],
        "UHNK": [4000, "2023-12-04T13:30:57.117000"],
        "ULML": [3942, "2023-12-04T10:54:02.331461"],
        "ULMQ": [3794, "2023-12-04T12:26:42.074165"]
    }
    }

    :param data_dict: dict
    :param arr_airport: Аэропорт, ОТПРАВЛЕНИЯ
    :param dep_airport: Аэропорт ПРИЛЕТА
    :return: tuple(total_flight_price, [DepartureAirportCode, Point, ... , ArrivalAirportCode])
    """
    graph = Graph()

    list_nodes, edges = create_nodes_in_graph(data_dict=data_dict)

    for node in list_nodes:
        graph.add_node(node)

    for list_with_values in edges:
        graph.add_edge(*list_with_values)

    return shortest_path(
        graph,
        origin=dep_airport,
        destination=arr_airport
    )


