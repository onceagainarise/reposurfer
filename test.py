from phase0.tree_builder import FileTreeBuilder

builder = FileTreeBuilder()
tree = builder.build_tree("storage/repos/psf_requests/source")

print(len(tree))
print(tree[:10])
