# RepoSurfer 🏄‍♂️

**Semantic Codebase Understanding for Large Repositories**

RepoSurfer is an experimental system that helps developers understand, navigate, and reason about large codebases using symbol graphs, embeddings, and LLM-based reasoning.

Instead of reading files manually or relying only on runtime errors, RepoSurfer builds a semantic map of a repository and uses it to answer questions like:

- Where is this issue likely coming from?
- Which classes, methods, or files are related to this bug?
- What parts of the codebase should I inspect first?

---

## 🚀 What RepoSurfer Does (High Level)

1. **Clones a repository**
2. **Extracts code structure** (files, classes, functions, methods)
3. **Builds a symbol graph** representing relationships in the code
4. **Generates embeddings** for symbols (code-aware chunks)
5. **Performs hybrid retrieval** (vector similarity + graph expansion)
6. **Uses an LLM** to reason over retrieved code and propose investigation paths

RepoSurfer is **language-aware**, **repository-aware**, and **context-driven**.

---

## ✅ Current Progress (Completed Phases)

### Phase 0 – Repository Ingestion
- ✔ Clone GitHub repositories
- ✔ Fetch metadata (commits, issues, PRs, branches, tags)
- ✔ Build file tree structure

### Phase 1 – Static Code Understanding
- ✔ Language detection
- ✔ AST-based parsing (Python)
- ✔ Symbol extraction (files, classes, methods, functions)
- ✔ Symbol graph construction

### Phase 2 – Semantic Retrieval Engine
- ✔ Symbol-level chunking
- ✔ Embedding generation
- ✔ Vector storage using Qdrant
- ✔ Hybrid retrieval (vector similarity + graph neighbors)
- ✔ Ranked, explainable retrieval results

### Phase 3 – LLM Reasoning (Initial)
- ✔ LLM-powered investigation planning
- ✔ Reasoning over retrieved symbols
- ✔ Issue-to-code mapping (manual issue input)

📌 **At this stage, the full RepoSurfer pipeline is functional and validated end-to-end.**

---

## 🧪 What RepoSurfer Is Not

- ❌ A runtime debugger
- ❌ A replacement for stack traces
- ❌ A test runner

RepoSurfer is designed for **semantic understanding** and **codebase exploration**, especially when:

- The repo is large
- You're unfamiliar with the code
- The bug is architectural or historical
- Context is scattered across files

---

## 🛠️ Current Usage (Developer Mode)

RepoSurfer currently runs as a backend research pipeline using Python modules and runners.

**Typical flow:**
```
Repo → Symbols → Graph → Embeddings → Retrieval → LLM Reasoning
```

> **Note:** User-facing interfaces (CLI / library API) are not yet finalized.

---

## 🧭 What's Coming Next (Planned Phases)

### Phase 4 – MVP Productization
- Python library API
- CLI interface (`reposurfer analyze <repo> --issue "<text>"`)
- Structured, user-friendly outputs

### Phase 5 – Issue-Aware Reasoning
- Automatic GitHub issue ingestion
- Patch / PR context awareness
- Historical fix reasoning
- Issue-to-commit linking

### Phase 6 – Advanced Semantics
- Improved embeddings (symbol + context + dependency aware)
- Cross-file and cross-module reasoning
- Multi-hop graph reasoning
- Better handling of large, complex repositories

---

## 🎯 Project Goal

The goal of RepoSurfer is to evolve into a **practical AI assistant** for understanding real-world codebases, not just answering surface-level questions.

RepoSurfer prioritizes:

- **Explainability**
- **Precision**
- **Code structure awareness**
- **Scalability** to large repos

---

## ⚠️ Status

🟡 **Active development**  
🧪 **Research-driven**  
🚧 **APIs may change**

---

## 🙌 Why RepoSurfer Exists

Modern repositories are too large to understand file-by-file. RepoSurfer explores a better abstraction:

> **Understand the codebase as a graph of meaning, not a pile of files.**

---

## 📦 Installation

*Coming soon – Phase 4*
```bash
# Planned installation (not yet available)
pip install reposurfer
```

---

## 🚀 Quick Start

*Coming soon – Phase 4*
```bash
# Planned CLI usage (not yet available)
reposurfer analyze <github-repo-url> --issue "Bug in authentication flow"
```

---

**Built with 🧠 for developers who want to understand code, not just read it.**


### Author Note
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

with this commit we have started building the phase2 we first designed a symbol_chunk_loader file in order to convert all symbols(classes , method and functions) into chunks before generating the embeddings.

i have used qdrant database to store the embeddings generated using sentence transformers all-mini-l6-v2 . as of now the embeddings are not being stored permanently until phase3 so lets go!

made some changes to over the embedded data and retrieve it . there are some issues but will be solved with the later commits .

sovled the issues related to the retrival and now I AM able to retrieve the embeddings along with the confidence score so that's good.
and with the latest commit which take in account of both graph and semantic comparision in giving the confidence score i am done with the phase2 which was one of the most important phase and now will move onto to the llm reasoning stage. the BRAIN.


with this commit i have started building the phase3 of the project of integrating the llm for reasoning .


As of now i have completed the basic pipeline of repo-surfer and now we would try to create a user interface for it using the cli and access it using cli commands and for that we would require to resturcture the folder sturcture a little bit as shown in this commit

As of right now the main pipeline for the whole process has been completed and from now on the main challenge would start.
repo surfer currently only performs surface level reasoning which is good for small repos but for complex architecture it would fail so we would now work on imporving the creation of graph, symbol tree, embedding and optimizing the retreival process and also provide a ui for user to use the repo surfer since as of now it is only an engine without an outside body of car to drive it.

now with this i have made the basic structure of how the orchestrator should look like and now i would change each modules by removing individual runners and combining the small funcitons into a single class to make the code more modular.

i have done some changes and for now most of the commits would be related to the structural changes since these are done for long term and in th development of the mvp.recreated the whole architecture and moving the files in their proper desiginated places.

with that i am done with completing the command line interface for the reposurfer so that any one cna use it by cloning the repo. it still consists of some minor issue which i would solve in the later issue and then we can begin with optimizing and improving the reposurfer to make it more efficient , reliable and durable.

DONE WITH SOLVING ALL THE ISSUES , WOULD UPDATE THE README TO GIVE USER GUIDE TO REPO SURFER.

now will work on improving it!!!!

BACK AGAIN !

Now will start woking with upgrading it and taking it to the next level and creating the mvp.

the main concerns regarding the mvp are four which are as follows:
1) Enhance LLM reasoning to provide detailed, specific responses with exact locations and root cause analysis.

2) Implement contextual memory system for follow-up questions and conversation continuity.

3) Expand Q&A capabilities to handle general repo questions and guidance without code generation.

4) Simplify CLI interface and commands for better user experience.

expanded the q&a capablities of the reposurfer and added the contextual memory along with more detailed explainiations.
and now we would start contverting this into a library to enhance its cli interface

