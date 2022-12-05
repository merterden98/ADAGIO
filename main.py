import argparse
from t_map.garbanzo.edgelist import EdgeListGarbanzo
from t_map.garbanzo.transforms.tissue_reweight import reweight_graph_by_tissue
from t_map.feta.glide import ADAGIO
parser = argparse.ArgumentParser()
parser.add_argument('--network', '-n', type=str, required=True, help="Path to edgelist, assumes tab separated.")
parser.add_argument('--genelist', '-g', type=str, required=True, help="Path to genelist, assumes genes are newline separated and in the network.")
parser.add_argument('--out', '-o', type=str, default="adagio.out",help="Path to output results")
parser.add_argument('--tissue_path', '-t', type=str, default="None", help="Path to tissue files for optional reweighting")


def main(network_path: str, genelist_path: str, out_path: str, tissue_path: str):
        # Initialize an instance of a Garbanzo EdgeList. Contains class variables
        # for graph path, (disease) gene path, list of genes, networkx graph
        graph = EdgeListGarbanzo(network_path, genelist_path)
        
        # Load the ADAGIO model - model.setup method reweights the graph with GLIDE
        model = ADAGIO()
        model.setup(graph.graph)
        
        # Reweight graph AFTER initial reweighting with GLIDE
        if tissue_path != "None":
                reweight_graph_by_tissue(graph.graph, tissue_path)

        # Run RWR, produce output
        predictions = sorted(list(model.prioritize(graph.genes, graph.graph)), key=lambda x: x[1], reverse=True)
        
        with open(out_path, "w") as f:
                for gene, score in predictions:
                        f.write(f"{gene.name}\t{score}\n")
        

if __name__ == "__main__":
        args = parser.parse_args()
        main(args.network, args.genelist, args.out, args.tissue_path)
        