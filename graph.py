import pandas as pd
import networkx as nx

links= pd.read_csv("Data/links.csv")

# Creating a directed graph
graph= nx.DiGraph()

for _, row in links.iterrows():

    graph.add_edge(
        row["source"],
        row["target"],
        anchor_text=row["anchor_text"]
    )

print("Number of pages:", graph.number_of_nodes())
print("Number of internal links:",graph.number_of_edges())

print("\n Pages and their outgoing links:")

for page in graph.nodes:
    targets=list(
        graph.successors(page)
    )
    print(page,"->",targets)

# To find Orphan like pages

print("\n Potential orphan-like pages:")

for page in graph.nodes:

    incoming_links=graph.in_degree(page)
    if incoming_links ==0:
        print(page)