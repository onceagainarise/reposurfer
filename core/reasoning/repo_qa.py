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
    
    def _format_retrieved_symbols(self, retrieved_symbols: list) -> str:
        """Format retrieved symbols for context"""
        if not retrieved_symbols:
            return "No specific code context found."
        
        context_parts = []
        for s in retrieved_symbols[:3]:  # Limit to top 3
            symbol_info = f"""
File: {s.get('file', 'Unknown')}
Symbol: {s.get('id', 'Unknown')}
Type: {s.get('type', 'Unknown')}
Lines: {s.get('start_line', '?')}-{s.get('end_line', '?')}
Code: {s.get('text', '')[:300]}...
"""
            context_parts.append(symbol_info.strip())
        
        return "\n\n".join(context_parts)
    
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
        
        # Get retrieved symbols if available
        retrieved_symbols = repo_context.get('retrieved_symbols', [])
        code_context = self._format_retrieved_symbols(retrieved_symbols)
        
        prompt = f"""
Context: {context}

Question: {query}

Repository Information:
- Name: {repo_context.get('name', 'Unknown') if repo_context else 'Unknown'}
- Description: {repo_context.get('description', 'No description available') if repo_context else 'No description available'}
- Main Language: {repo_context.get('language', 'Unknown') if repo_context else 'Unknown'}
- Files: {repo_context.get('file_count', 'Unknown') if repo_context else 'Unknown'} files

Relevant Code Context:
{code_context}

CRITICAL INSTRUCTIONS:
1. Provide a COMPREHENSIVE overview of this repository based on ALL available information
2. Analyze the code structure, imports, and patterns to understand the repository's purpose
3. Identify the main functionality and key features from the code evidence
4. Explain what problems this repository solves or what it enables users to do
5. Describe the architecture and main components in detail
6. If it's a tool, library, or application, explain its use case
7. Use specific examples from the code to support your analysis
8. Be thorough and detailed - this is likely the user's first interaction with this repo
9. If you can infer the project's domain (e.g., web scraping, data analysis, ML, etc.), state it clearly

Format your response as:
## 🎯 Repository Overview
[Clear, concise summary of what this repository does]

## 🏗️ Architecture & Structure
[Main components and how they work together]

## ⚡ Key Features & Functionality
[What this code enables users to accomplish]

## 📁 Code Analysis
[Insights from the actual code structure and patterns]

## 🔍 Domain & Use Case
[What problem domain this addresses and who would use it]

## 💡 Key Insights
[Important observations about the codebase]
"""
        
        return self.llm.explain(prompt)
    
    def _provide_fix_guidance(self, query: str, repo_context: dict) -> str:
        """Provide guidance on how to approach fixing issues"""
        
        context = self.memory.get_context_for_query(query)
        
        # Get retrieved symbols if available
        retrieved_symbols = repo_context.get('retrieved_symbols', [])
        code_context = self._format_retrieved_symbols(retrieved_symbols)
        
        prompt = f"""
Context: {context}

Issue: {query}

Relevant Code Context:
{code_context}

COMPREHENSIVE GUIDANCE INSTRUCTIONS:
1. Provide DETAILED, step-by-step guidance for addressing this issue
2. Use the code context to identify specific problem areas and patterns
3. Suggest concrete debugging strategies and investigation methods
4. Recommend specific files, functions, or line numbers to examine
5. Explain the technical approach needed to solve this type of issue
6. If this is a common pattern, explain the typical solution approach
7. Provide actionable next steps the user can take immediately
8. Include specific code examples ONLY if absolutely necessary (2-5 lines max)
9. Explain WHY this approach works and the reasoning behind it

Format your response as:
## 🔍 Issue Analysis
[What the issue is and where it likely occurs]

## 🛠️ Step-by-Step Solution Approach
[Detailed methodology to fix the issue]

## 🎯 Investigation Areas
[Specific files/lines to examine based on code context]

## 🧠 Debugging Strategy
[Technical approach to identify and resolve the problem]

## 💡 Pro Tips
[Best practices and common solutions for this type of issue]

## ⚡ Immediate Actions
[Concrete next steps the user can take right now]
"""
        
        return self.llm.explain(prompt)
    
    def _provide_coding_help(self, query: str, repo_context: dict) -> str:
        """Provide coding help and small examples"""
        
        context = self.memory.get_context_for_query(query)
        
        # Get retrieved symbols if available
        retrieved_symbols = repo_context.get('retrieved_symbols', [])
        code_context = self._format_retrieved_symbols(retrieved_symbols)
        
        prompt = f"""
Context: {context}

Coding Question: {query}

Relevant Code Context:
{code_context}

Instructions:
1. Provide clear guidance on how to implement the requested functionality
2. Use the retrieved code context to understand the repository's patterns and conventions
3. Include small, relevant code snippets (2-10 lines max) if helpful
4. Explain the concepts and approach
5. Reference relevant files or functions from the repository if applicable (based on retrieved context)
6. Do NOT provide complete solutions or large code blocks
7. Focus on teaching the approach and concepts

Format:
## Approach
[Explanation of the method based on repository patterns]

## Key Concepts
[Important concepts to understand]

## Example Snippet
[Small code example if applicable]

## Relevant Areas
[Files/functions to reference in the repo based on retrieved context]
"""
        
        return self.llm.explain(prompt)
    
    def _answer_general_question(self, query: str, repo_context: dict) -> str:
        """Answer general questions about the codebase"""
        
        context = self.memory.get_context_for_query(query)
        
        # Get retrieved symbols if available
        retrieved_symbols = repo_context.get('retrieved_symbols', [])
        code_context = self._format_retrieved_symbols(retrieved_symbols)
        
        prompt = f"""
Context: {context}

Question: {query}

Relevant Code Context:
{code_context}

Instructions:
1. Answer based on the available context, repository information, and retrieved code
2. Use the retrieved code context to provide specific, informed answers
3. Be helpful and informative
4. If the question requires more specific code analysis, suggest using the investigation feature
5. Do not hallucinate information
6. If you don't have enough information, say so explicitly
"""
        
        return self.llm.explain(prompt)
