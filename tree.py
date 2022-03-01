#!/usr/bin/python3
import os
import sys
import ast
import subprocess
from anytree.importer import DictImporter
from anytree.exporter import DictExporter
import anytree
import os

args = list(sys.argv)

# Import filesystem tree file in this function
def import_tree_file(treename):
    treefile = open(treename,"r")
    tree = ast.literal_eval(treefile.readline())
    return(tree)

# Print out tree with descriptions
def print_tree(tree):
    for pre, fill, node in anytree.RenderTree(tree):
        if os.path.isfile(f"/root/images/{node.name}-desc"):
            descfile = open(f"/root/images/{node.name}-desc","r")
            desc = descfile.readline()
            descfile.close()
        else:
            desc = ""
        print("%s%s - %s" % (pre, node.name, desc))

# Add to root tree
def append_base_tree(tree,val):
    add = anytree.Node(val, parent=tree.root)

# Add child to node
def add_node_to_parent(tree, id, val):
    par = (anytree.find(tree, filter_=lambda node: (str(node.name)+"x") in (str(id)+"x")))
    add = anytree.Node(val, parent=par)
    
def add_node_to_level(tree,id, val): # Broken, likely useless, probably remove later
    par = (anytree.find(tree, filter_=lambda node: (str(node.name) + "x") in (str(id) + "x")))
    spar = str(par).split("/")
    nspar = (spar[len(spar)-2])
    npar = (anytree.find(tree, filter_=lambda node: (str(node.name) + "x") in (str(nspar) + "x")))
    add = anytree.Node(val, parent=npar)

# Remove node from tree
def remove_node(tree, id):
    par = (anytree.find(tree, filter_=lambda node: (str(node.name)+"x") in (str(id)+"x")))
    par.parent = None

# Save tree to file
def write_tree(tree):
    exporter = DictExporter()
    to_write = exporter.export(tree)
    fsfile = open(fstreepath,"w")
    fsfile.write(str(to_write))

# Return list of children for node
def return_children(tree, id):
    children = []
    par = (anytree.find(tree, filter_=lambda node: (str(node.name)+"x") in (str(id)+"x")))
    for child in anytree.PreOrderIter(par):
        children.append(child.name)
    return (children)

def tree_crawl(treename):
    children = [node.name for node in anytree.LevelOrderIter(treename)]
    for child in children: # This runs for the tree itself, fix later (doesn't cause issues)
        par = (anytree.find(treename, filter_=lambda node: (str(node.name) + "x") in (str(child) + "x")))
        spar = str(par).split("/")
        nspar = (spar[len(spar)-2])
        npar = (anytree.find(treename, filter_=lambda node: (str(node.name) + "x") in (str(nspar) + "x"))) # Maybe works
        print(npar,child)


# Main function
def main(args):
    importer = DictImporter() # Dict importer
    exporter = DictExporter() # And exporter
    global fstree # Currently these are global variables, fix sometime
    global fstreepath # ---
    fstreepath = str("tree.txt") # Path to fstree file
    fstree = importer.import_(import_tree_file(fstreepath)) # Import fstree file
    append_base_tree(fstree, "test")
    add_node_to_parent(fstree, "test", "test2")
    add_node_to_parent(fstree, "test", "test3")
    add_node_to_parent(fstree, "test2", "test6")
    add_node_to_parent(fstree, "test2", "test5")
    append_base_tree(fstree, "test10")
    add_node_to_parent(fstree, "test10", "test8")
    print_tree(fstree)
    tree_crawl(fstree)
    print(return_children(fstree,"root"))
    # Recognize argument and call appropriate function

main(args)
