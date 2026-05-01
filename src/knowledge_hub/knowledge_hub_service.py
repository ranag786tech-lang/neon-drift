"""
Unified Knowledge Hub Service
Connects enterprise data, public information, and personal context into one intelligent workspace
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib
import json

class KnowledgeHubService:
    """
    Unified Knowledge Hub - Digital nerve center for seamless information navigation
    Connects multiple data sources with intelligent search and contextual recommendations
    """
    
    def __init__(self):
        self.documents = {}  # In-memory storage (will use DB in production)
        self.sources = {
            "enterprise": [],
            "public": [],
            "personal": []
        }
        self.user_context = {}  # User-specific context and preferences
        
    def add_document(self, 
                    title: str, 
                    content: str, 
                    source_type: str,
                    tags: List[str] = None,
                    metadata: Dict = None,
                    user_id: str = None) -> Dict:
        """
        Add a document to the knowledge hub
        
        Args:
            title: Document title
            content: Document content
            source_type: 'enterprise', 'public', or 'personal'
            tags: List of tags for categorization
            metadata: Additional metadata
            user_id: Owner user ID
            
        Returns:
            Document dict with ID
        """
        doc_id = hashlib.md5(f"{title}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12]
        
        document = {
            "id": doc_id,
            "title": title,
            "content": content,
            "source_type": source_type,
            "tags": tags or [],
            "metadata": metadata or {},
            "embedding": self._generate_embedding(content),  # Placeholder for vector embedding
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "user_id": user_id
        }
        
        self.documents[doc_id] = document
        self.sources[source_type].append(doc_id)
        
        return document
    
    def search(self, 
               query: str, 
               source_types: List[str] = None,
               tags: List[str] = None,
               user_id: str = None,
               limit: int = 10) -> List[Dict]:
        """
        Intelligent search across all knowledge sources
        
        Args:
            query: Search query
            source_types: Filter by source types
            tags: Filter by tags
            user_id: Filter by user
            limit: Maximum results
            
        Returns:
            List of matching documents ranked by relevance
        """
        results = []
        query_lower = query.lower()
        
        for doc_id, doc in self.documents.items():
            # Apply filters
            if source_types and doc["source_type"] not in source_types:
                continue
            if tags and not any(tag in doc["tags"] for tag in tags):
                continue
            if user_id and doc.get("user_id") != user_id:
                continue
            
            # Calculate relevance score
            score = self._calculate_relevance(query_lower, doc)
            
            if score > 0:
                results.append({
                    **doc,
                    "relevance_score": score,
                    "highlights": self._extract_highlights(query_lower, doc["content"])
                })
        
        # Sort by relevance and return top results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]
    
    def get_contextual_recommendations(self, 
                                       user_id: str, 
                                       current_task: str = None,
                                       limit: int = 5) -> List[Dict]:
        """
        Get personalized document recommendations based on user context and task
        
        Args:
            user_id: User ID
            current_task: Current task or project context
            limit: Maximum recommendations
            
        Returns:
            List of recommended documents
        """
        recommendations = []
        
        # Get user's context
        user_context = self.user_context.get(user_id, {})
        preferred_tags = user_context.get("preferred_tags", [])
        recent_docs = user_context.get("recent_documents", [])
        
        # Score documents based on context
        for doc_id, doc in self.documents.items():
            score = 0
            
            # Boost if matches preferred tags
            if any(tag in preferred_tags for tag in doc["tags"]):
                score += 3.0
            
            # Boost if from frequently accessed source
            if doc["source_type"] == user_context.get("preferred_source"):
                score += 2.0
            
            # Boost if related to current task
            if current_task and self._is_related_to_task(doc, current_task):
                score += 4.0
            
            # Avoid recently viewed documents
            if doc_id in recent_docs:
                score -= 2.0
            
            if score > 0:
                recommendations.append({
                    **doc,
                    "recommendation_score": score,
                    "reason": self._get_recommendation_reason(score, doc, user_context)
                })
        
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        return recommendations[:limit]
    
    def update_user_context(self, 
                           user_id: str, 
                           context_updates: Dict) -> Dict:
        """
        Update user's context and preferences for better recommendations
        
        Args:
            user_id: User ID
            context_updates: Dictionary of context updates
            
        Returns:
            Updated user context
        """
        if user_id not in self.user_context:
            self.user_context[user_id] = {
                "preferred_tags": [],
                "preferred_source": None,
                "recent_documents": [],
                "workflow_patterns": {},
                "last_active": datetime.utcnow()
            }
        
        self.user_context[user_id].update(context_updates)
        self.user_context[user_id]["last_active"] = datetime.utcnow()
        
        return self.user_context[user_id]
    
    def get_knowledge_graph(self, 
                           seed_doc_ids: List[str] = None,
                           depth: int = 2) -> Dict:
        """
        Build a knowledge graph showing relationships between documents
        
        Args:
            seed_doc_ids: Starting documents
            depth: How many hops to traverse
            
        Returns:
            Knowledge graph as nodes and edges
        """
        nodes = []
        edges = []
        
        if not seed_doc_ids:
            seed_doc_ids = list(self.documents.keys())[:10]
        
        visited = set()
        queue = [(doc_id, 0) for doc_id in seed_doc_ids]
        
        while queue:
            doc_id, current_depth = queue.pop(0)
            
            if doc_id in visited or current_depth > depth:
                continue
            
            visited.add(doc_id)
            doc = self.documents.get(doc_id)
            
            if doc:
                nodes.append({
                    "id": doc_id,
                    "title": doc["title"],
                    "source_type": doc["source_type"],
                    "tags": doc["tags"]
                })
                
                # Find related documents (by tags or content similarity)
                for other_id, other_doc in self.documents.items():
                    if other_id != doc_id and other_id not in visited:
                        relationship = self._find_relationship(doc, other_doc)
                        if relationship:
                            edges.append({
                                "source": doc_id,
                                "target": other_id,
                                "type": relationship,
                                "strength": 0.8
                            })
                            
                            if current_depth < depth:
                                queue.append((other_id, current_depth + 1))
        
        return {
            "nodes": nodes,
            "edges": edges,
            "total_documents": len(self.documents),
            "total_connections": len(edges)
        }
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Placeholder for generating vector embeddings"""
        # In production, use models like sentence-transformers
        return [hash(text[i:i+10]) % 1000 / 1000.0 for i in range(0, min(len(text), 100), 10)]
    
    def _calculate_relevance(self, query: str, doc: Dict) -> float:
        """Calculate relevance score between query and document"""
        score = 0.0
        
        # Title match (highest weight)
        if query in doc["title"].lower():
            score += 5.0
        
        # Content match
        if query in doc["content"].lower():
            score += 3.0
        
        # Tag match
        for tag in doc["tags"]:
            if query in tag.lower():
                score += 2.0
        
        # Partial word matches
        query_words = query.split()
        for word in query_words:
            if word in doc["title"].lower():
                score += 1.5
            if word in doc["content"].lower():
                score += 0.5
        
        return score
    
    def _extract_highlights(self, query: str, content: str, max_length: int = 200) -> List[str]:
        """Extract highlighted snippets from content"""
        highlights = []
        content_lower = content.lower()
        query_pos = content_lower.find(query)
        
        if query_pos != -1:
            start = max(0, query_pos - 50)
            end = min(len(content), query_pos + len(query) + 50)
            snippet = content[start:end].strip()
            if len(snippet) > max_length:
                snippet = snippet[:max_length] + "..."
            highlights.append(snippet)
        
        return highlights if highlights else [content[:max_length] + "..."]
    
    def _is_related_to_task(self, doc: Dict, task: str) -> bool:
        """Check if document is related to a task"""
        task_lower = task.lower()
        
        # Check title
        if task_lower in doc["title"].lower():
            return True
        
        # Check tags
        if any(task_lower in tag.lower() for tag in doc["tags"]):
            return True
        
        # Check content (first 500 chars for performance)
        if task_lower in doc["content"][:500].lower():
            return True
        
        return False
    
    def _get_recommendation_reason(self, score: float, doc: Dict, context: Dict) -> str:
        """Generate human-readable reason for recommendation"""
        reasons = []
        
        if score >= 4.0:
            reasons.append("Highly relevant to your current task")
        if any(tag in context.get("preferred_tags", []) for tag in doc["tags"]):
            reasons.append("Matches your interests")
        if doc["source_type"] == context.get("preferred_source"):
            reasons.append(f"From your preferred {doc['source_type']} source")
        
        return ". ".join(reasons) if reasons else "Potentially useful"
    
    def _find_relationship(self, doc1: Dict, doc2: Dict) -> Optional[str]:
        """Find relationship type between two documents"""
        # Check tag overlap
        common_tags = set(doc1["tags"]) & set(doc2["tags"])
        if len(common_tags) >= 2:
            return "related_by_tags"
        
        # Check same source
        if doc1["source_type"] == doc2["source_type"]:
            return "same_source"
        
        # Check author/metadata
        if doc1.get("metadata", {}).get("author") == doc2.get("metadata", {}).get("author"):
            return "same_author"
        
        return None
    
    def get_statistics(self) -> Dict:
        """Get knowledge hub statistics"""
        return {
            "total_documents": len(self.documents),
            "by_source": {
                source: len(doc_ids) 
                for source, doc_ids in self.sources.items()
            },
            "total_users": len(self.user_context),
            "average_tags_per_doc": sum(len(doc["tags"]) for doc in self.documents.values()) / max(len(self.documents), 1)
        }


# Initialize service instance
knowledge_hub = KnowledgeHubService()
