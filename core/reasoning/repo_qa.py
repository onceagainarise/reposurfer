from reposurfer.core.reasoning.llm_client import LLMClient
from reposurfer.core.reasoning.conversation_memory import ConversationMemory

class RepoQA:
    """Enhanced Q&A system for general repository questions"""
    
    def __init__(self, llm: LLMClient, memory: ConversationMemory):
        self.llm = llm
        self.memory = memory
    
    def answer_question(self, query: str, repo_context: dict = None) -> str:
        """Answer general questions about the repository"""
        
        # Determine question type
        question_type = self._classify_question(query)
        
        if question_type == "general_repo":
            return self._answer_general_repo_question(query, repo_context)
        elif question_type == "how_to_fix":
            return self._provide_fix_guidance(query, repo_context)
        elif question_type == "coding_help":
            return self._provide_coding_help(query, repo_context)
        else:
            return self._answer_general_question(query, repo_context)
    
    def _classify_question(self, query: str) -> str:
        """Classify the type of question"""
        query_lower = query.lower()
        
        # General repo questions
        if any(word in query_lower for word in ['what is', 'what does', 'purpose', 'about', 'overview', 'describe']):
            return "general_repo"
        
        # Fix guidance questions
        if any(word in query_lower for word in ['how to fix', 'fix this', 'solve this', 'resolve', 'how do i']):
            return "how_to_fix"
        
        # Coding help questions
        if any(word in query_lower for word in ['how to', 'code', 'implement', 'example', 'snippet']):
            return "coding_help"
        
        return "general_question"
    
    def _answer_general_repo_question(self, query: str, repo_context: dict) -> str:
        """Answer questions about repository purpose and structure"""
        
        context = self.memory.get_context_for_query(query)
        
        prompt = f"""
Context: {context}

Question: {query}

Repository Information:
- Name: {repo_context.get('name', 'Unknown') if repo_context else 'Unknown'}
- Description: {repo_context.get('description', 'No description available') if repo_context else 'No description available'}
- Main Language: {repo_context.get('language', 'Unknown') if repo_context else 'Unknown'}
- Files: {repo_context.get('file_count', 'Unknown') if repo_context else 'Unknown'} files

Instructions:
1. Provide a clear, concise answer about the repository
2. Focus on the main purpose and functionality
3. Mention key components or features if relevant
4. Do not generate code unless specifically asked
5. If information is insufficient, say so explicitly
"""
        
        return self.llm.explain(prompt)
    
    def _provide_fix_guidance(self, query: str, repo_context: dict) -> str:
        """Provide guidance on how to approach fixing issues"""
        
        context = self.memory.get_context_for_query(query)
        
        prompt = f"""
Context: {context}

Issue: {query}

Instructions:
1. Provide step-by-step guidance on how to approach fixing this issue
2. Suggest debugging strategies and investigation methods
3. Mention relevant files or areas to focus on (based on context)
4. Do NOT provide complete code solutions
5. Provide small code snippets only if absolutely necessary for illustration
6. Focus on the methodology and approach
7. If more information is needed, specify what to look for

Format:
## Approach Strategy
[Step-by-step methodology]

## Areas to Investigate
[List specific files/components to check]

## Debugging Tips
[Specific suggestions for debugging]
"""
        
        return self.llm.explain(prompt)
    
    def _provide_coding_help(self, query: str, repo_context: dict) -> str:
        """Provide coding help and small examples"""
        
        context = self.memory.get_context_for_query(query)
        
        prompt = f"""
Context: {context}

Coding Question: {query}

Instructions:
1. Provide clear guidance on how to implement the requested functionality
2. Include small, relevant code snippets (2-10 lines max) if helpful
3. Explain the concepts and approach
4. Reference relevant files or functions from the repository if applicable
5. Do NOT provide complete solutions or large code blocks
6. Focus on teaching the approach and concepts

Format:
## Approach
[Explanation of the method]

## Key Concepts
[Important concepts to understand]

## Example Snippet
[Small code example if applicable]

## Relevant Areas
[Files/functions to reference in the repo]
"""
        
        return self.llm.explain(prompt)
    
    def _answer_general_question(self, query: str, repo_context: dict) -> str:
        """Answer general questions about the codebase"""
        
        context = self.memory.get_context_for_query(query)
        
        prompt = f"""
Context: {context}

Question: {query}

Instructions:
1. Answer based on the available context and repository information
2. Be helpful and informative
3. If the question requires more specific code analysis, suggest using the investigation feature
4. Do not hallucinate information
5. If you don't have enough information, say so explicitly
"""
        
        return self.llm.explain(prompt)
