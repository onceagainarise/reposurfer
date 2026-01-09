import json
from pathlib import Path
from reposurfer.core.retrieval.retriever import RepoRetriever
from reposurfer.core.embeddings.vector_store import VectorStore
from reposurfer.core.embeddings.embedding_generator import EmbeddingGenerator
from reposurfer.core.reasoning.llm_client import LLMClient
from reposurfer.core.reasoning.investigation import InvestigationPlanner
from reposurfer.core.reasoning.conversation_memory import ConversationMemory
from reposurfer.core.reasoning.repo_qa import RepoQA

def run_phase3(repo_path: str, query: str, mode: str = "investigate"):
    """
    Enhanced Phase 3 with multiple modes and memory support
    
    Args:
        repo_path: Path to the repository
        query: User's question or issue
        mode: "investigate" for detailed analysis, "qa" for general questions
    """
    print(repo_path)
    
    # Load repository data
    with open(f"{repo_path}/symbol_graph.json") as f:
        symbol_graph = json.load(f)
    
    # Load repository metadata if available
    repo_metadata = {}
    metadata_file = Path(repo_path) / "repo_metadata.json"
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            repo_metadata = json.load(f)

    repo_name = repo_path.split("/")[-1]

    # Initialize components
    embedder = EmbeddingGenerator()
    store = VectorStore(collection_name=repo_name)
    retriever = RepoRetriever(store, symbol_graph, embedder)
    llm = LLMClient()
    memory = ConversationMemory(repo_path)
    
    # Determine if this is a general Q&A question or investigation
    qa_system = RepoQA(llm, memory)
    
    # Check if we should use Q&A mode or investigation mode
    if mode == "qa" or qa_system._classify_question(query) in ["general_repo", "how_to_fix", "coding_help"]:
        print("🤔 Processing general question...")
        
        # Retrieve relevant symbols for context (even for Q&A)
        print("🔍 Finding relevant code context...")
        retrieved = retriever.query(query, top_k=3)  # Get fewer for Q&A
        
        # Debug info
        print(f"📊 Retrieved {len(retrieved)} symbols")
        if retrieved:
            print(f"📝 Top result: {retrieved[0].get('file', 'Unknown')} - {retrieved[0].get('id', 'Unknown')}")
        
        # Get basic repository context
        repo_context = {
            'name': repo_metadata.get('name', repo_name),
            'description': repo_metadata.get('description', ''),
            'language': repo_metadata.get('language', 'Unknown'),
            'file_count': len(symbol_graph.get('symbols', [])),
            'retrieved_symbols': retrieved  # Add retrieved symbols for context
        }
        
        answer = qa_system.answer_question(query, repo_context)
        memory.add_exchange(query, answer, retrieved)
        
        print(f"\n💬 Answer:\n{answer}")
        return
    
    # Original investigation flow
    print("🔍 Retrieving relevant symbols...")
    retrieved = retriever.query(query, top_k=5)

    planner = InvestigationPlanner(llm)

    print("\n🧠 Generating detailed analysis...\n")
    plan = planner.generate_plan(query, retrieved)
    
    # Store in memory
    memory.add_exchange(query, plan, retrieved)
    
    print(plan)
    
    # Show conversation summary
    summary = memory.get_summary()
    print(f"\n💾 {summary}")

def run_interactive_mode(repo_path: str):
    """Interactive mode for follow-up questions"""
    print(f"🚀 RepoSurfer Interactive Mode - {repo_path}")
    print("Type 'exit' to quit, 'clear' to clear memory, 'help' for commands")
    
    while True:
        try:
            query = input("\n❓ Ask about the repository: ").strip()
            
            if query.lower() == 'exit':
                break
            elif query.lower() == 'clear':
                memory = ConversationMemory(repo_path)
                memory.clear_memory()
                print("🗑️  Memory cleared")
                continue
            elif query.lower() == 'help':
                print("""
Available commands:
- Any question about the repository
- 'exit' to quit
- 'clear' to clear conversation memory
- 'investigate <issue>' for detailed analysis
                """)
                continue
            elif query.lower().startswith('investigate'):
                issue = query[11:].strip()
                run_phase3(repo_path, issue, mode="investigate")
            else:
                run_phase3(repo_path, query, mode="qa")
                
        except KeyboardInterrupt:
            break
    
    print("\n👋 Goodbye!")


"""if __name__ == "__main__":
    run_phase3(
        "storage/repos/psf__requests",
        "Unable to override cookie policy in Session.prepare_request ",
    )
"""