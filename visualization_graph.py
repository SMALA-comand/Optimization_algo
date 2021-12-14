import matplotlib.pyplot as plt
import networkx as nx
from simulated_annealing import simulated_annealing


def get_tuples(matrix):
    plan = []
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != '*':
                elem = (i+1, j+1, matrix[i][j])
                plan.append(elem)
    return plan


def get_set(path, tuples):
    good_tuples = [(path[i]+1, path[i+1]+1) for i in range(0, len(path)-1)]
    last_el = (path[-1]+1, path[0]+1)
    good_tuples.append(last_el)

    bad_tuples = [i for i in tuples if i not in good_tuples]

    return good_tuples, bad_tuples


def create_visual(matrix=None):
    ans = simulated_annealing(matrix=matrix)
    matrix = ans[3]
    path = ans[0]

    tuples = get_tuples(matrix)

    MG = nx.MultiDiGraph()
    MG.add_weighted_edges_from(tuples)
    pos = nx.spring_layout(MG, seed=63)
    options = {
        "node_color": "blue",
        "edge_color": 'gray',
        "width": 1,
        "edge_cmap": plt.cm.Blues,
        "with_labels": True,
    }
    subax1 = plt.subplot(121)
    nx.draw(MG, pos, **options)
    nx.draw_networkx_edges(
        MG,
        pos,
        edgelist=get_set(path, tuples)[1],
        width=1,
        alpha=0.2,
        edge_color="gray",
    )
    nx.draw_networkx_edges(
        MG,
        pos,
        edgelist=get_set(path, tuples)[0],
        width=6,
        alpha=1,
        edge_color="tab:red",
    )

    plt.show()


if __name__ == '__main__':
    matr = [['*', 40.0, 1.0, 16.0, 8.0],
            [7.0, '*', 1.0, 7.0, 20.0],
            [10.0, 10.0, '*', 5.0, 3.0],
            [7.0, 9.0, 7.0, '*', 2.0],
            [1.0, 9.0, 2.0, 18.0, '*']]

    create_visual(matrix=matr)
