from t_map.feta.glide import Glider
from t_map.utils.genedise_utils import run_genedise, load_graph
import networkx as nx
from t_map.garbanzo.networkx import Networkx

config = {
    "alpha": 0.85,
    "k": 20,
}

graph = load_graph("../data/cleaned_graph.csv")
model = Glider()
print("Beginning Setup")
model.setup(graph)
print("Beginning Setup")
# model.load("./model3.pkl")

model._get_sorted_similarity_indexes()
model._get_sorted_similarity_indexes(descending=True)
for i in range(0, 50, 5):
    for j in range(0, 50, 5):
        with Glider.with_reset(model) as m:
            print(f"{i}-{j}")
            m.add_new_edges(i / 100, in_place=True)
            m.remove_old_edges(j / 100, in_place=True)
            run_genedise("../data/cleaned_graph.csv", "../genedise_experiments/splits",
                         f"./outputs/add_{i / 100}_remove_{j / 100}", m)
