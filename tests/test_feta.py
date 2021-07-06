from t_map.feta.randomwalk import PreComputeRWR, RandomWalkWithRestart
from t_map.garbanzo.edgelist import EdgeListGarbanzo


def test_rwr():
    data = EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list",
        gene_path="./tests/data/gene.list")

    model = RandomWalkWithRestart()
    model(data.get(0), data.graph)
    model([data.get(0), data.get(1)], data.graph)

    precompute = PreComputeRWR()
    precompute(data.get(0), data.graph)
    precompute([data.get(0), data.get(3)], data.graph)
