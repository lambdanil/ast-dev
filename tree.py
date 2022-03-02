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

def print_tree(tree):
    for pre, fill, node in anytree.RenderTree(tree):
        print("%s%s" % (pre, node.name))

# Print out tree with descriptions
# Add to root tree
def append_base_tree(tree,val):
    add = anytree.Node(val, parent=tree.root)

# Add child to node
def add_node_to_parent(tree, id, val):
    par = (anytree.find(tree, filter_=lambda node: (str(node.name)+"x") in (str(id)+"x"))) # Not entirely sure how the lambda stuff here works, but it does ¯\_(ツ)_/¯
    add = anytree.Node(val, parent=par)

# Remove node from tree
def remove_node(tree, id):
    par = (anytree.find(tree, filter_=lambda node: (str(node.name)+"x") in (str(id)+"x")))
    par.parent = None
    print(par)

# Save tree to file
def write_tree(tree):
    exporter = DictExporter()
    to_write = exporter.export(tree)
    fsfile = open(fstreepath,"w")
    fsfile.write(str(to_write))

# Return list of children for node
def return_all_children(tree, id):
    children = []
    par = (anytree.find(tree, filter_=lambda node: (str(id)+"x") in (str(node.name)+"x")))
    #print(par.children)
    for child in anytree.PreOrderIter(par):
        children.append(child.name)
    return (children)

def return_children(tree, id):
    children = []
    importer = DictImporter() # Dict importer
    par = (anytree.find(tree, filter_=lambda node: (str(id)+"x") in (str(node.name)+"x")))
    #print(par, par.children)
    children = []
    try:
        cstr = str(par.children)
    except:
        return(children)
    cstr = cstr.replace("(","")
    cstr = cstr[:-1]
    scstr = cstr.split("Node'/root/")
    nscstr = []
    for item in scstr:
        item = item.replace(",", "")
        item = item.replace("')", "")
        sitem = item.split(f"{id}/")
        if item != "" and len(sitem) > 1:
            children.append(sitem[1])
        else:
            item = sitem[0]
            item = item.replace("AnyNodename='","")
            item = item.replace(" ", "")
            if item != "":
                children.append(item)
    return (children)

# Main function
def main(args):
    importer = DictImporter() # Dict importer
    exporter = DictExporter() # And exporter
    global fstree # Currently these are global variables, fix sometime
    global fstreepath # ---
    fstreepath = str("tree.txt") # Path to fstree file
    fstree = (importer.import_(import_tree_file(fstreepath))) # Import fstree file
    add_node_to_parent(fstree,"0", "1")
    add_node_to_parent(fstree, "4", "2")
    add_node_to_parent(fstree, "4", "7")
    add_node_to_parent(fstree, "2", "5")
    add_node_to_parent(fstree, "2", "6")
    print_tree(fstree)
    #print(return_all_children(fstree, "4"))
    print(return_children(fstree, "2"))

main(args)
