This is an upgraded version of repo surfer ---> Repo Surfer V2 
our main foucs of making this project is to help users in open source project exploration and contribution.

I divided the project making into many phases.
the phase0 includes desinging the pipline to fetch github repo , clone it ,get details related to its commit history, issues in the present repo using the git token.

with the phase0 i am onto the phase1 and am half way there , there are some issues realted to file path configurations which would be solved with the next commit so stay tuned.

solved the issue related to the file path , it was creating two different directories for cloning and json files which caused issues in the phase1 execution.

and with this commit I are finished building the phase1 of repo surfer, what I achieved:
cloning the repo.
getting the commit , issues , pr and metadata about the repo.
build symbols files to get the info about the function loactions.
build graph to get understanding of how these files connect to each other.

let's move to the phase2 that is chunking , generating embedding and storing it in the database.

