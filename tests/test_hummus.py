import networkx as nx

from t_map.gene.gene import Gene
from t_map.garbanzo.edgelist import EdgeListGarbanzo
from t_map.hummus.hummus import Hummus


def test_train():
    data = EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list",
        gene_path="./tests/data/gene.list")

    runner = Hummus(data=data)
    for (d, g) in runner.train():
        assert isinstance(d, Gene)
        assert isinstance(g, nx.Graph)
