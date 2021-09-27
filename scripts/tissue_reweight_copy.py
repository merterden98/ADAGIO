import glob
import argparse
import matplotlib.pyplot as plt
import networkx as nx
from t_map.garbanzo.huri import Huri
from t_map.hummus.hummus import Hummus
from t_map.hummus.hummus_score import HummusScore, ScoreTypes
from t_map.feta.randomwalk import RandomWalkWithRestart
from t_map.garbanzo.stringdb import StringDB
from t_map.garbanzo.merge import merge
from t_map.feta.glide import Glider
from t_map.feta.dada import Dada
from t_map.feta.feta import PreComputeFeta

parser = argparse.ArgumentParser(description='Tissue reweight by algs')
parser.add_argument('-t', '--tissue-path', type=str, required=True,
                    help='Path to folder that contains tissue presence data')
parser.add_argument('-a', '--algorithms',
                    choices=['all', 'rwr', 'glider', 'dada', 'glider+dada'])
parser.add_argument('-g', '--gene-set', type=str,
                    required=True, help="path to genesets")
parser.add_argument('-th', '--thresholds', type=list,
                    default=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

models = {
    'rwr': RandomWalkWithRestart,
    'glider': Glider,
    'dada': Dada,
    'glider+dada': lambda: Glider(with_dada=True)
}


def reweight_graph_by_tissue(graph: nx.Graph,
                             file_path: str,
                             weight: float = 0.001) -> nx.Graph:
    """
    Given a network `graph` of ppi interactions, and a file path to containing data
    as to where or not a gene is expressed in a given tissue:
        ENSEMBL_ID   Gene       [0-1]
    where 0 indicates low expression and 1 indicates high expression. The function
    reweights the graph by multiplying the weight of each edge by w' = w * weight^{2 - n}
    where n is the number of highly expressed genes in the tissue.


    Parameters
    ----------
    graph : nx.Graph
        A networkx graph object representing the ppi network.
    file_path : str
        A string representing the path to the tissue gene file.
    weight : float, optional
        The weight to assign to each edge in the new graph.

    Returns
    -------
    nx.Graph
        A new networkx graph object with the same nodes and edges as the input
        graph, but with each edge weighted by the tissue-specific interaction
        frequency.
    """

    is_expressed = dict()
    # Read in the tissue-specific interaction file.
    with open(file_path, 'r') as f:
        for line in f:
            _, gene, is_expressed_str = line.split('\t')
            is_expressed[gene] = int(is_expressed_str)

    # Create a new graph with the same nodes and edges as the input graph.
    new_graph = nx.Graph()
    new_graph.add_nodes_from(graph.nodes())
    new_graph.add_edges_from(graph.edges())

    # Iterate through each edge in the new graph.
    for edge in new_graph.edges():
	try:
        	new_graph[edge[0]][edge[1]]['weight'] = graph[edge[0]][edge[1]]['weight'] * \
            		(weight ** (2 - is_expressed[edge[0]] - is_expressed[edge[1]]))
	except:
        	new_graph[edge[0]][edge[1]]['weight'] = graph[edge[0]][edge[1]]['weight'] 

    return new_graph



def main(args: argparse.Namespace):
    # Using glob get all of the tissue files.
    tissue_files = glob.glob(args.tissue_path + '/*.tsv')
    if args.algorithms == 'all':
        algs = ['rwr', 'glider', 'dada', 'glider+dada']
    else:
        algs = [args.algorithms]

    for tissue_file in tissue_files:
        huri = Huri(args.gene_set, with_hugo=True)
        stringdb = StringDB(args.gene_set)
        merged = merge([huri, stringdb])
        merged.graph = reweight_graph_by_tissue(merged.graph, tissue_file)
        for alg in algs:
            model = models[alg]()
            if isinstance(model, PreComputeFeta):
                model.setup(merged.graph)

            scoring = HummusScore(score_type=ScoreTypes.TOP_K)
            runner = Hummus(merged, with_scoring=scoring)
            for i, test_runner in enumerate(runner.with_cv(k_fold="LOO")):
                with test_runner as (disease_genes, graph, fn):
                    predictions = model(disease_genes, graph)
                    fn(predictions)

            # This is how we get the gene set predictions without LOO cross
            # validation.
            gene_list = model(merged.disease_genes, merged.graph)
            # TODO: Figure out how to score this gdamn thing.
            scoring.compute_roc()
            for threshold in args.thresholds:
                scoring.auc_roc(threshold)

            true_pos = [x[0] for x in scoring._roc]
            print(true_pos)

            print(scoring._roc)


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
