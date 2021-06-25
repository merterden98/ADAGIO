#!/usr/bin/env python
from t_map.garbanzo.edgelist import EdgeListGarbanzo


def test_edgelist():
    # testing for side effect
    EdgeListGarbanzo(
        graph_path="./tests/data/unweighted_edge.list", gene_path="")
