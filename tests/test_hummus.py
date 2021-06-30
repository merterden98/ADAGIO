import networkx as nx

from t_map.gene.gene import Gene
from t_map.garbanzo.edgelist import EdgeListGarbanzo
from t_map.hummus.hummus import Hummus
from t_map.hummus.hummus_score import HummusScore


def test_train():
    data = EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list",
        gene_path="./tests/data/gene.list")

    runner = Hummus(data=data)
    for (d, g) in runner.train():
        assert isinstance(d, Gene)
        assert isinstance(g, nx.Graph)


def test_score():
    data = EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list",
        gene_path="./tests/data/gene.list")
    score_module = HummusScore()
    runner = Hummus(data, with_scoring=score_module)

    for (d, g, score_fn) in runner.train():
        predicted_genes = list(map(lambda x: Gene(x), g.nodes))
        score_fn(predicted_genes)

    for (d, g, score_fn) in runner.test():
        predicted_genes = list(map(lambda x: Gene(x), g.nodes))
        score_fn(predicted_genes)


def test_cv():
    data = EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list",
        gene_path="./tests/data/gene.list")
    score_module = HummusScore()
    runner = Hummus(data, with_scoring=score_module)

    # Check if we assert gracefully in cv is not set
    try:
        for (trainer, tester) in runner:
            ...
    except AssertionError:
        ...

    for (trainer, tester) in runner.with_cv():
        for (d, g, score_fn) in trainer:
            predicted_genes = list(map(lambda x: Gene(x), g.nodes))
            score_fn(predicted_genes)
        for (d, g, score_fn) in runner.test():
            predicted_genes = list(map(lambda x: Gene(x), g.nodes))
            score_fn(predicted_genes)
