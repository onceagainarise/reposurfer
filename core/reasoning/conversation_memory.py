import json
import time
from pathlib import Path
from typing import Dict, List, Any

class ConversationMemory:
    """Manages conversational context for follow-up questions"""
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.memory_file = Path(repo_path) / "conversation_memory.json"
        self.conversation_history: List[Dict[str, Any]] = []
        self.current_context: Dict[str, Any] = {}
        self.load_memory()
    
    def load_memory(self):
        """Load existing conversation memory"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('history', [])
                    self.current_context = data.get('context', {})
            except Exception as e:
                print(f"Warning: Could not load memory file: {e}")
                self.conversation_history = []
                self.current_context = {}
    
    def save_memory(self):
        """Save conversation memory to file"""
        try:
            memory_data = {
                'history': self.conversation_history,
                'context': self.current_context,
                'last_updated': time.time()
            }
            with open(self.memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save memory file: {e}")
    
    def add_exchange(self, query: str, response: str, retrieved_symbols: List[Dict] = None):
        """Add a new query-response exchange to memory"""
        exchange = {
            'timestamp': time.time(),
            'query': query,
            'response': response,
            'retrieved_symbols_count': len(retrieved_symbols) if retrieved_symbols else 0,
            'key_symbols': [s.get('id', '') for s in (retrieved_symbols or [])[:3]]  # Top 3 symbols
        }
        
        self.conversation_history.append(exchange)
        
        # Update context with key information from latest exchange
        if retrieved_symbols:
            self.current_context.update({
                'last_query': query,
                'last_response_summary': response[:200] + "..." if len(response) > 200 else response,
                'key_files': list(set([s.get('file', '') for s in retrieved_symbols])),
                'key_symbols': [s.get('id', '') for s in retrieved_symbols[:5]]
            })
        
        # Keep only last 10 exchanges to avoid memory bloat
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        self.save_memory()
    
    def get_context_for_query(self, current_query: str) -> str:
        """Generate context summary for follow-up questions"""
        if not self.conversation_history:
            return ""
        
        # Check if this might be a follow-up question
        follow_up_indicators = ['follow up', 'more about', 'what about', 'also', 'additionally', 'further']
        is_followup = any(indicator in current_query.lower() for indicator in follow_up_indicators)
        
        if not is_followup and len(self.conversation_history) <= 1:
            return ""
        
        context_parts = []
        
        # Add recent context
        if self.current_context.get('key_files'):
            context_parts.append(f"Recently discussed files: {', '.join(self.current_context['key_files'][:3])}")
        
        if self.current_context.get('key_symbols'):
            context_parts.append(f"Key symbols mentioned: {', '.join(self.current_context['key_symbols'][:3])}")
        
        # Add last query summary if relevant
        last_query = self.current_context.get('last_query', '')
        if last_query and is_followup:
            context_parts.append(f"Previous question: {last_query}")
        
        return "\n".join(context_parts) if context_parts else ""
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.conversation_history = []
        self.current_context = {}
        if self.memory_file.exists():
            self.memory_file.unlink()
    
    def get_summary(self) -> str:
        """Get a summary of the conversation"""
        if not self.conversation_history:
            return "No conversation history"
        
        return f"Conversation has {len(self.conversation_history)} exchanges. Last topic: {self.current_context.get('last_query', 'N/A')}"
