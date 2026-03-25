"""
Zepconverted
details、details、details，convertedReport Agentconverted

details（details）：
1. InsightForge（details）- details，details
2. PanoramaSearch（details）- details，details
3. QuickSearch（details）- details
"""

import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from zep_cloud.client import Zep

from ..config import Config
from ..utils.logger import get_logger
from ..utils.llm_client import LLMClient
from ..utils.zep_paging import fetch_all_nodes, fetch_all_edges

logger = get_logger('mirofish.zep_tools')


@dataclass
class SearchResult:
    """details"""
    facts: List[str]
    edges: List[Dict[str, Any]]
    nodes: List[Dict[str, Any]]
    query: str
    total_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "facts": self.facts,
            "edges": self.edges,
            "nodes": self.nodes,
            "query": self.query,
            "total_count": self.total_count
        }
    
    def to_text(self) -> str:
        """details，convertedLLMconverted"""
        text_parts = [f"details: {self.query}", f"details {self.total_count} details"]
        
        if self.facts:
            text_parts.append("\n### details:")
            for i, fact in enumerate(self.facts, 1):
                text_parts.append(f"{i}. {fact}")
        
        return "\n".join(text_parts)


@dataclass
class NodeInfo:
    """details"""
    uuid: str
    name: str
    labels: List[str]
    summary: str
    attributes: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "labels": self.labels,
            "summary": self.summary,
            "attributes": self.attributes
        }
    
    def to_text(self) -> str:
        """details"""
        entity_type = next((l for l in self.labels if l not in ["Entity", "Node"]), "details")
        return f"details: {self.name} (details: {entity_type})\nconverted: {self.summary}"


@dataclass
class EdgeInfo:
    """details"""
    uuid: str
    name: str
    fact: str
    source_node_uuid: str
    target_node_uuid: str
    source_node_name: Optional[str] = None
    target_node_name: Optional[str] = None
    # details
    created_at: Optional[str] = None
    valid_at: Optional[str] = None
    invalid_at: Optional[str] = None
    expired_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uuid": self.uuid,
            "name": self.name,
            "fact": self.fact,
            "source_node_uuid": self.source_node_uuid,
            "target_node_uuid": self.target_node_uuid,
            "source_node_name": self.source_node_name,
            "target_node_name": self.target_node_name,
            "created_at": self.created_at,
            "valid_at": self.valid_at,
            "invalid_at": self.invalid_at,
            "expired_at": self.expired_at
        }
    
    def to_text(self, include_temporal: bool = False) -> str:
        """details"""
        source = self.source_node_name or self.source_node_uuid[:8]
        target = self.target_node_name or self.target_node_uuid[:8]
        base_text = f"details: {source} --[{self.name}]--> {target}\nconverted: {self.fact}"
        
        if include_temporal:
            valid_at = self.valid_at or "details"
            invalid_at = self.invalid_at or "details"
            base_text += f"\nconverted: {valid_at} - {invalid_at}"
            if self.expired_at:
                base_text += f" (details: {self.expired_at})"
        
        return base_text
    
    @property
    def is_expired(self) -> bool:
        """details"""
        return self.expired_at is not None
    
    @property
    def is_invalid(self) -> bool:
        """details"""
        return self.invalid_at is not None


@dataclass
class InsightForgeResult:
    """
    details (InsightForge)
    details，details
    """
    query: str
    simulation_requirement: str
    sub_queries: List[str]
    
    # details
    semantic_facts: List[str] = field(default_factory=list)  # details
    entity_insights: List[Dict[str, Any]] = field(default_factory=list)  # details
    relationship_chains: List[str] = field(default_factory=list)  # details
    
    # details
    total_facts: int = 0
    total_entities: int = 0
    total_relationships: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "simulation_requirement": self.simulation_requirement,
            "sub_queries": self.sub_queries,
            "semantic_facts": self.semantic_facts,
            "entity_insights": self.entity_insights,
            "relationship_chains": self.relationship_chains,
            "total_facts": self.total_facts,
            "total_entities": self.total_entities,
            "total_relationships": self.total_relationships
        }
    
    def to_text(self) -> str:
        """details，convertedLLMconverted"""
        text_parts = [
            f"## details",
            f"details: {self.query}",
            f"details: {self.simulation_requirement}",
            f"\n### details",
            f"- details: {self.total_facts}details",
            f"- details: {self.total_entities}details",
            f"- details: {self.total_relationships}details"
        ]
        
        # details
        if self.sub_queries:
            text_parts.append(f"\n### details")
            for i, sq in enumerate(self.sub_queries, 1):
                text_parts.append(f"{i}. {sq}")
        
        # details
        if self.semantic_facts:
            text_parts.append(f"\n### 【details】(details)")
            for i, fact in enumerate(self.semantic_facts, 1):
                text_parts.append(f"{i}. \"{fact}\"")
        
        # details
        if self.entity_insights:
            text_parts.append(f"\n### 【details】")
            for entity in self.entity_insights:
                text_parts.append(f"- **{entity.get('name', 'details')}** ({entity.get('type', 'details')})")
                if entity.get('summary'):
                    text_parts.append(f"  details: \"{entity.get('summary')}\"")
                if entity.get('related_facts'):
                    text_parts.append(f"  details: {len(entity.get('related_facts', []))}details")
        
        # details
        if self.relationship_chains:
            text_parts.append(f"\n### 【details】")
            for chain in self.relationship_chains:
                text_parts.append(f"- {chain}")
        
        return "\n".join(text_parts)


@dataclass
class PanoramaResult:
    """
    details (Panorama)
    details，details
    """
    query: str
    
    # details
    all_nodes: List[NodeInfo] = field(default_factory=list)
    # details（details）
    all_edges: List[EdgeInfo] = field(default_factory=list)
    # details
    active_facts: List[str] = field(default_factory=list)
    # details/details（details）
    historical_facts: List[str] = field(default_factory=list)
    
    # details
    total_nodes: int = 0
    total_edges: int = 0
    active_count: int = 0
    historical_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "all_nodes": [n.to_dict() for n in self.all_nodes],
            "all_edges": [e.to_dict() for e in self.all_edges],
            "active_facts": self.active_facts,
            "historical_facts": self.historical_facts,
            "total_nodes": self.total_nodes,
            "total_edges": self.total_edges,
            "active_count": self.active_count,
            "historical_count": self.historical_count
        }
    
    def to_text(self) -> str:
        """details（details，details）"""
        text_parts = [
            f"## details（details）",
            f"details: {self.query}",
            f"\n### details",
            f"- details: {self.total_nodes}",
            f"- details: {self.total_edges}",
            f"- details: {self.active_count}details",
            f"- details/details: {self.historical_count}details"
        ]
        
        # details（details，details）
        if self.active_facts:
            text_parts.append(f"\n### 【details】(details)")
            for i, fact in enumerate(self.active_facts, 1):
                text_parts.append(f"{i}. \"{fact}\"")
        
        # details/details（details，details）
        if self.historical_facts:
            text_parts.append(f"\n### 【details/details】(details)")
            for i, fact in enumerate(self.historical_facts, 1):
                text_parts.append(f"{i}. \"{fact}\"")
        
        # details（details，details）
        if self.all_nodes:
            text_parts.append(f"\n### 【details】")
            for node in self.all_nodes:
                entity_type = next((l for l in node.labels if l not in ["Entity", "Node"]), "details")
                text_parts.append(f"- **{node.name}** ({entity_type})")
        
        return "\n".join(text_parts)


@dataclass
class AgentInterview:
    """convertedAgentconverted"""
    agent_name: str
    agent_role: str  # details（details：details、details、details）
    agent_bio: str  # details
    question: str  # details
    response: str  # details
    key_quotes: List[str] = field(default_factory=list)  # details
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "agent_role": self.agent_role,
            "agent_bio": self.agent_bio,
            "question": self.question,
            "response": self.response,
            "key_quotes": self.key_quotes
        }
    
    def to_text(self) -> str:
        text = f"**{self.agent_name}** ({self.agent_role})\n"
        # convertedagent_bio，details
        text += f"_converted: {self.agent_bio}_\n\n"
        text += f"**Q:** {self.question}\n\n"
        text += f"**A:** {self.response}\n"
        if self.key_quotes:
            text += "\n**details:**\n"
            for quote in self.key_quotes:
                # details
                clean_quote = quote.replace('\u201c', '').replace('\u201d', '').replace('"', '')
                clean_quote = clean_quote.replace('\u300c', '').replace('\u300d', '')
                clean_quote = clean_quote.strip()
                # details
                while clean_quote and clean_quote[0] in '，,；;：:、。！？\n\r\t ':
                    clean_quote = clean_quote[1:]
                # details（converted1-9）
                skip = False
                for d in '123456789':
                    if f'\u95ee\u9898{d}' in clean_quote:
                        skip = True
                        break
                if skip:
                    continue
                # details（details，details）
                if len(clean_quote) > 150:
                    dot_pos = clean_quote.find('\u3002', 80)
                    if dot_pos > 0:
                        clean_quote = clean_quote[:dot_pos + 1]
                    else:
                        clean_quote = clean_quote[:147] + "..."
                if clean_quote and len(clean_quote) >= 10:
                    text += f'> "{clean_quote}"\n'
        return text


@dataclass
class InterviewResult:
    """
    details (Interview)
    convertedAgentconverted
    """
    interview_topic: str  # details
    interview_questions: List[str]  # details
    
    # convertedAgent
    selected_agents: List[Dict[str, Any]] = field(default_factory=list)
    # convertedAgentconverted
    interviews: List[AgentInterview] = field(default_factory=list)
    
    # convertedAgentconverted
    selection_reasoning: str = ""
    # details
    summary: str = ""
    
    # details
    total_agents: int = 0
    interviewed_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "interview_topic": self.interview_topic,
            "interview_questions": self.interview_questions,
            "selected_agents": self.selected_agents,
            "interviews": [i.to_dict() for i in self.interviews],
            "selection_reasoning": self.selection_reasoning,
            "summary": self.summary,
            "total_agents": self.total_agents,
            "interviewed_count": self.interviewed_count
        }
    
    def to_text(self) -> str:
        """details，convertedLLMconverted"""
        text_parts = [
            "## details",
            f"**details:** {self.interview_topic}",
            f"**details:** {self.interviewed_count} / {self.total_agents} convertedAgent",
            "\n### details",
            self.selection_reasoning or "（details）",
            "\n---",
            "\n### details",
        ]

        if self.interviews:
            for i, interview in enumerate(self.interviews, 1):
                text_parts.append(f"\n#### details #{i}: {interview.agent_name}")
                text_parts.append(interview.to_text())
                text_parts.append("\n---")
        else:
            text_parts.append("（details）\n\n---")

        text_parts.append("\n### details")
        text_parts.append(self.summary or "（details）")

        return "\n".join(text_parts)


class ZepToolsService:
    """
    Zepconverted
    
    【details - details】
    1. insight_forge - details（details，details，details）
    2. panorama_search - details（details，details）
    3. quick_search - details（details）
    4. interview_agents - details（convertedAgent，details）
    
    【details】
    - search_graph - details
    - get_all_nodes - details
    - get_all_edges - details（details）
    - get_node_detail - details
    - get_node_edges - details
    - get_entities_by_type - details
    - get_entity_summary - details
    """
    
    # details
    MAX_RETRIES = 3
    RETRY_DELAY = 2.0
    
    def __init__(self, api_key: Optional[str] = None, llm_client: Optional[LLMClient] = None):
        self.api_key = api_key or Config.ZEP_API_KEY
        if not self.api_key:
            raise ValueError("ZEP_API_KEY details")
        
        self.client = Zep(api_key=self.api_key)
        # LLMconvertedInsightForgeconverted
        self._llm_client = llm_client
        logger.info("ZepToolsService details")
    
    @property
    def llm(self) -> LLMClient:
        """convertedLLMconverted"""
        if self._llm_client is None:
            self._llm_client = LLMClient()
        return self._llm_client
    
    def _call_with_retry(self, func, operation_name: str, max_retries: int = None):
        """convertedAPIconverted"""
        max_retries = max_retries or self.MAX_RETRIES
        last_exception = None
        delay = self.RETRY_DELAY
        
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.warning(
                        f"Zep {operation_name} details {attempt + 1} details: {str(e)[:100]}, "
                        f"{delay:.1f}details..."
                    )
                    time.sleep(delay)
                    delay *= 2
                else:
                    logger.error(f"Zep {operation_name} details {max_retries} details: {str(e)}")
        
        raise last_exception
    
    def search_graph(
        self, 
        graph_id: str, 
        query: str, 
        limit: int = 10,
        scope: str = "edges"
    ) -> SearchResult:
        """
        details
        
        details（details+BM25）details。
        convertedZep Cloudconvertedsearch APIconverted，details。
        
        Args:
            graph_id: convertedID (Standalone Graph)
            query: details
            limit: details
            scope: details，"edges" details "nodes"
            
        Returns:
            SearchResult: details
        """
        logger.info(f"details: graph_id={graph_id}, query={query[:50]}...")
        
        # convertedZep Cloud Search API
        try:
            search_results = self._call_with_retry(
                func=lambda: self.client.graph.search(
                    graph_id=graph_id,
                    query=query,
                    limit=limit,
                    scope=scope,
                    reranker="cross_encoder"
                ),
                operation_name=f"details(graph={graph_id})"
            )
            
            facts = []
            edges = []
            nodes = []
            
            # details
            if hasattr(search_results, 'edges') and search_results.edges:
                for edge in search_results.edges:
                    if hasattr(edge, 'fact') and edge.fact:
                        facts.append(edge.fact)
                    edges.append({
                        "uuid": getattr(edge, 'uuid_', None) or getattr(edge, 'uuid', ''),
                        "name": getattr(edge, 'name', ''),
                        "fact": getattr(edge, 'fact', ''),
                        "source_node_uuid": getattr(edge, 'source_node_uuid', ''),
                        "target_node_uuid": getattr(edge, 'target_node_uuid', ''),
                    })
            
            # details
            if hasattr(search_results, 'nodes') and search_results.nodes:
                for node in search_results.nodes:
                    nodes.append({
                        "uuid": getattr(node, 'uuid_', None) or getattr(node, 'uuid', ''),
                        "name": getattr(node, 'name', ''),
                        "labels": getattr(node, 'labels', []),
                        "summary": getattr(node, 'summary', ''),
                    })
                    # details
                    if hasattr(node, 'summary') and node.summary:
                        facts.append(f"[{node.name}]: {node.summary}")
            
            logger.info(f"details: details {len(facts)} details")
            
            return SearchResult(
                facts=facts,
                edges=edges,
                nodes=nodes,
                query=query,
                total_count=len(facts)
            )
            
        except Exception as e:
            logger.warning(f"Zep Search APIconverted，details: {str(e)}")
            # details：details
            return self._local_search(graph_id, query, limit, scope)
    
    def _local_search(
        self, 
        graph_id: str, 
        query: str, 
        limit: int = 10,
        scope: str = "edges"
    ) -> SearchResult:
        """
        details（convertedZep Search APIconverted）
        
        details/details，details
        
        Args:
            graph_id: convertedID
            query: details
            limit: details
            scope: details
            
        Returns:
            SearchResult: details
        """
        logger.info(f"details: query={query[:30]}...")
        
        facts = []
        edges_result = []
        nodes_result = []
        
        # details（details）
        query_lower = query.lower()
        keywords = [w.strip() for w in query_lower.replace(',', ' ').replace('，', ' ').split() if len(w.strip()) > 1]
        
        def match_score(text: str) -> int:
            """details"""
            if not text:
                return 0
            text_lower = text.lower()
            # details
            if query_lower in text_lower:
                return 100
            # details
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 10
            return score
        
        try:
            if scope in ["edges", "both"]:
                # details
                all_edges = self.get_all_edges(graph_id)
                scored_edges = []
                for edge in all_edges:
                    score = match_score(edge.fact) + match_score(edge.name)
                    if score > 0:
                        scored_edges.append((score, edge))
                
                # details
                scored_edges.sort(key=lambda x: x[0], reverse=True)
                
                for score, edge in scored_edges[:limit]:
                    if edge.fact:
                        facts.append(edge.fact)
                    edges_result.append({
                        "uuid": edge.uuid,
                        "name": edge.name,
                        "fact": edge.fact,
                        "source_node_uuid": edge.source_node_uuid,
                        "target_node_uuid": edge.target_node_uuid,
                    })
            
            if scope in ["nodes", "both"]:
                # details
                all_nodes = self.get_all_nodes(graph_id)
                scored_nodes = []
                for node in all_nodes:
                    score = match_score(node.name) + match_score(node.summary)
                    if score > 0:
                        scored_nodes.append((score, node))
                
                scored_nodes.sort(key=lambda x: x[0], reverse=True)
                
                for score, node in scored_nodes[:limit]:
                    nodes_result.append({
                        "uuid": node.uuid,
                        "name": node.name,
                        "labels": node.labels,
                        "summary": node.summary,
                    })
                    if node.summary:
                        facts.append(f"[{node.name}]: {node.summary}")
            
            logger.info(f"details: details {len(facts)} details")
            
        except Exception as e:
            logger.error(f"details: {str(e)}")
        
        return SearchResult(
            facts=facts,
            edges=edges_result,
            nodes=nodes_result,
            query=query,
            total_count=len(facts)
        )
    
    def get_all_nodes(self, graph_id: str) -> List[NodeInfo]:
        """
        details（details）

        Args:
            graph_id: convertedID

        Returns:
            details
        """
        logger.info(f"details {graph_id} details...")

        nodes = fetch_all_nodes(self.client, graph_id)

        result = []
        for node in nodes:
            node_uuid = getattr(node, 'uuid_', None) or getattr(node, 'uuid', None) or ""
            result.append(NodeInfo(
                uuid=str(node_uuid) if node_uuid else "",
                name=node.name or "",
                labels=node.labels or [],
                summary=node.summary or "",
                attributes=node.attributes or {}
            ))

        logger.info(f"details {len(result)} details")
        return result

    def get_all_edges(self, graph_id: str, include_temporal: bool = True) -> List[EdgeInfo]:
        """
        details（details，details）

        Args:
            graph_id: convertedID
            include_temporal: details（convertedTrue）

        Returns:
            details（convertedcreated_at, valid_at, invalid_at, expired_at）
        """
        logger.info(f"details {graph_id} details...")

        edges = fetch_all_edges(self.client, graph_id)

        result = []
        for edge in edges:
            edge_uuid = getattr(edge, 'uuid_', None) or getattr(edge, 'uuid', None) or ""
            edge_info = EdgeInfo(
                uuid=str(edge_uuid) if edge_uuid else "",
                name=edge.name or "",
                fact=edge.fact or "",
                source_node_uuid=edge.source_node_uuid or "",
                target_node_uuid=edge.target_node_uuid or ""
            )

            # details
            if include_temporal:
                edge_info.created_at = getattr(edge, 'created_at', None)
                edge_info.valid_at = getattr(edge, 'valid_at', None)
                edge_info.invalid_at = getattr(edge, 'invalid_at', None)
                edge_info.expired_at = getattr(edge, 'expired_at', None)

            result.append(edge_info)

        logger.info(f"details {len(result)} details")
        return result
    
    def get_node_detail(self, node_uuid: str) -> Optional[NodeInfo]:
        """
        details
        
        Args:
            node_uuid: convertedUUID
            
        Returns:
            convertedNone
        """
        logger.info(f"details: {node_uuid[:8]}...")
        
        try:
            node = self._call_with_retry(
                func=lambda: self.client.graph.node.get(uuid_=node_uuid),
                operation_name=f"details(uuid={node_uuid[:8]}...)"
            )
            
            if not node:
                return None
            
            return NodeInfo(
                uuid=getattr(node, 'uuid_', None) or getattr(node, 'uuid', ''),
                name=node.name or "",
                labels=node.labels or [],
                summary=node.summary or "",
                attributes=node.attributes or {}
            )
        except Exception as e:
            logger.error(f"details: {str(e)}")
            return None
    
    def get_node_edges(self, graph_id: str, node_uuid: str) -> List[EdgeInfo]:
        """
        details
        
        details，details
        
        Args:
            graph_id: convertedID
            node_uuid: convertedUUID
            
        Returns:
            details
        """
        logger.info(f"details {node_uuid[:8]}... details")
        
        try:
            # details，details
            all_edges = self.get_all_edges(graph_id)
            
            result = []
            for edge in all_edges:
                # details（details）
                if edge.source_node_uuid == node_uuid or edge.target_node_uuid == node_uuid:
                    result.append(edge)
            
            logger.info(f"details {len(result)} details")
            return result
            
        except Exception as e:
            logger.warning(f"details: {str(e)}")
            return []
    
    def get_entities_by_type(
        self, 
        graph_id: str, 
        entity_type: str
    ) -> List[NodeInfo]:
        """
        details
        
        Args:
            graph_id: convertedID
            entity_type: details（details Student, PublicFigure details）
            
        Returns:
            details
        """
        logger.info(f"details {entity_type} details...")
        
        all_nodes = self.get_all_nodes(graph_id)
        
        filtered = []
        for node in all_nodes:
            # convertedlabelsconverted
            if entity_type in node.labels:
                filtered.append(node)
        
        logger.info(f"details {len(filtered)} details {entity_type} details")
        return filtered
    
    def get_entity_summary(
        self, 
        graph_id: str, 
        entity_name: str
    ) -> Dict[str, Any]:
        """
        details
        
        details，details
        
        Args:
            graph_id: convertedID
            entity_name: details
            
        Returns:
            details
        """
        logger.info(f"details {entity_name} details...")
        
        # details
        search_result = self.search_graph(
            graph_id=graph_id,
            query=entity_name,
            limit=20
        )
        
        # details
        all_nodes = self.get_all_nodes(graph_id)
        entity_node = None
        for node in all_nodes:
            if node.name.lower() == entity_name.lower():
                entity_node = node
                break
        
        related_edges = []
        if entity_node:
            # convertedgraph_idconverted
            related_edges = self.get_node_edges(graph_id, entity_node.uuid)
        
        return {
            "entity_name": entity_name,
            "entity_info": entity_node.to_dict() if entity_node else None,
            "related_facts": search_result.facts,
            "related_edges": [e.to_dict() for e in related_edges],
            "total_relations": len(related_edges)
        }
    
    def get_graph_statistics(self, graph_id: str) -> Dict[str, Any]:
        """
        details
        
        Args:
            graph_id: convertedID
            
        Returns:
            details
        """
        logger.info(f"details {graph_id} details...")
        
        nodes = self.get_all_nodes(graph_id)
        edges = self.get_all_edges(graph_id)
        
        # details
        entity_types = {}
        for node in nodes:
            for label in node.labels:
                if label not in ["Entity", "Node"]:
                    entity_types[label] = entity_types.get(label, 0) + 1
        
        # details
        relation_types = {}
        for edge in edges:
            relation_types[edge.name] = relation_types.get(edge.name, 0) + 1
        
        return {
            "graph_id": graph_id,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "entity_types": entity_types,
            "relation_types": relation_types
        }
    
    def get_simulation_context(
        self, 
        graph_id: str,
        simulation_requirement: str,
        limit: int = 30
    ) -> Dict[str, Any]:
        """
        details
        
        details
        
        Args:
            graph_id: convertedID
            simulation_requirement: details
            limit: details
            
        Returns:
            details
        """
        logger.info(f"details: {simulation_requirement[:50]}...")
        
        # details
        search_result = self.search_graph(
            graph_id=graph_id,
            query=simulation_requirement,
            limit=limit
        )
        
        # details
        stats = self.get_graph_statistics(graph_id)
        
        # details
        all_nodes = self.get_all_nodes(graph_id)
        
        # details（convertedEntityconverted）
        entities = []
        for node in all_nodes:
            custom_labels = [l for l in node.labels if l not in ["Entity", "Node"]]
            if custom_labels:
                entities.append({
                    "name": node.name,
                    "type": custom_labels[0],
                    "summary": node.summary
                })
        
        return {
            "simulation_requirement": simulation_requirement,
            "related_facts": search_result.facts,
            "graph_statistics": stats,
            "entities": entities[:limit],  # details
            "total_entities": len(entities)
        }
    
    # ========== details（details） ==========
    
    def insight_forge(
        self,
        graph_id: str,
        query: str,
        simulation_requirement: str,
        report_context: str = "",
        max_sub_queries: int = 5
    ) -> InsightForgeResult:
        """
        【InsightForge - details】
        
        details，details：
        1. convertedLLMconverted
        2. details
        3. details
        4. details
        5. details，details
        
        Args:
            graph_id: convertedID
            query: details
            simulation_requirement: details
            report_context: details（details，details）
            max_sub_queries: details
            
        Returns:
            InsightForgeResult: details
        """
        logger.info(f"InsightForge details: {query[:50]}...")
        
        result = InsightForgeResult(
            query=query,
            simulation_requirement=simulation_requirement,
            sub_queries=[]
        )
        
        # Step 1: convertedLLMconverted
        sub_queries = self._generate_sub_queries(
            query=query,
            simulation_requirement=simulation_requirement,
            report_context=report_context,
            max_queries=max_sub_queries
        )
        result.sub_queries = sub_queries
        logger.info(f"details {len(sub_queries)} details")
        
        # Step 2: details
        all_facts = []
        all_edges = []
        seen_facts = set()
        
        for sub_query in sub_queries:
            search_result = self.search_graph(
                graph_id=graph_id,
                query=sub_query,
                limit=15,
                scope="edges"
            )
            
            for fact in search_result.facts:
                if fact not in seen_facts:
                    all_facts.append(fact)
                    seen_facts.add(fact)
            
            all_edges.extend(search_result.edges)
        
        # details
        main_search = self.search_graph(
            graph_id=graph_id,
            query=query,
            limit=20,
            scope="edges"
        )
        for fact in main_search.facts:
            if fact not in seen_facts:
                all_facts.append(fact)
                seen_facts.add(fact)
        
        result.semantic_facts = all_facts
        result.total_facts = len(all_facts)
        
        # Step 3: convertedUUID，details（details）
        entity_uuids = set()
        for edge_data in all_edges:
            if isinstance(edge_data, dict):
                source_uuid = edge_data.get('source_node_uuid', '')
                target_uuid = edge_data.get('target_node_uuid', '')
                if source_uuid:
                    entity_uuids.add(source_uuid)
                if target_uuid:
                    entity_uuids.add(target_uuid)
        
        # details（details，details）
        entity_insights = []
        node_map = {}  # details
        
        for uuid in list(entity_uuids):  # details，details
            if not uuid:
                continue
            try:
                # details
                node = self.get_node_detail(uuid)
                if node:
                    node_map[uuid] = node
                    entity_type = next((l for l in node.labels if l not in ["Entity", "Node"]), "details")
                    
                    # details（details）
                    related_facts = [
                        f for f in all_facts 
                        if node.name.lower() in f.lower()
                    ]
                    
                    entity_insights.append({
                        "uuid": node.uuid,
                        "name": node.name,
                        "type": entity_type,
                        "summary": node.summary,
                        "related_facts": related_facts  # details，details
                    })
            except Exception as e:
                logger.debug(f"details {uuid} details: {e}")
                continue
        
        result.entity_insights = entity_insights
        result.total_entities = len(entity_insights)
        
        # Step 4: details（details）
        relationship_chains = []
        for edge_data in all_edges:  # details，details
            if isinstance(edge_data, dict):
                source_uuid = edge_data.get('source_node_uuid', '')
                target_uuid = edge_data.get('target_node_uuid', '')
                relation_name = edge_data.get('name', '')
                
                source_name = node_map.get(source_uuid, NodeInfo('', '', [], '', {})).name or source_uuid[:8]
                target_name = node_map.get(target_uuid, NodeInfo('', '', [], '', {})).name or target_uuid[:8]
                
                chain = f"{source_name} --[{relation_name}]--> {target_name}"
                if chain not in relationship_chains:
                    relationship_chains.append(chain)
        
        result.relationship_chains = relationship_chains
        result.total_relationships = len(relationship_chains)
        
        logger.info(f"InsightForgeconverted: {result.total_facts}details, {result.total_entities}details, {result.total_relationships}details")
        return result
    
    def _generate_sub_queries(
        self,
        query: str,
        simulation_requirement: str,
        report_context: str = "",
        max_queries: int = 5
    ) -> List[str]:
        """
        convertedLLMconverted
        
        details
        """
        system_prompt = """details。details。

details：
1. details，convertedAgentconverted
2. details（details：details、details、details、details、details、details）
3. details
4. convertedJSONconverted：{"sub_queries": ["converted1", "converted2", ...]}"""

        user_prompt = f"""details：
{simulation_requirement}

{f"details：{report_context[:500]}" if report_context else ""}

details{max_queries}details：
{query}

convertedJSONconverted。"""

        try:
            response = self.llm.chat_json(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            sub_queries = response.get("sub_queries", [])
            # details
            return [str(sq) for sq in sub_queries[:max_queries]]
            
        except Exception as e:
            logger.warning(f"details: {str(e)}，details")
            # details：details
            return [
                query,
                f"{query} details",
                f"{query} details",
                f"{query} details"
            ][:max_queries]
    
    def panorama_search(
        self,
        graph_id: str,
        query: str,
        include_expired: bool = True,
        limit: int = 50
    ) -> PanoramaResult:
        """
        【PanoramaSearch - details】
        
        details，details/details：
        1. details
        2. details（details/details）
        3. details
        
        details、details。
        
        Args:
            graph_id: convertedID
            query: details（details）
            include_expired: details（convertedTrue）
            limit: details
            
        Returns:
            PanoramaResult: details
        """
        logger.info(f"PanoramaSearch details: {query[:50]}...")
        
        result = PanoramaResult(query=query)
        
        # details
        all_nodes = self.get_all_nodes(graph_id)
        node_map = {n.uuid: n for n in all_nodes}
        result.all_nodes = all_nodes
        result.total_nodes = len(all_nodes)
        
        # details（details）
        all_edges = self.get_all_edges(graph_id, include_temporal=True)
        result.all_edges = all_edges
        result.total_edges = len(all_edges)
        
        # details
        active_facts = []
        historical_facts = []
        
        for edge in all_edges:
            if not edge.fact:
                continue
            
            # details
            source_name = node_map.get(edge.source_node_uuid, NodeInfo('', '', [], '', {})).name or edge.source_node_uuid[:8]
            target_name = node_map.get(edge.target_node_uuid, NodeInfo('', '', [], '', {})).name or edge.target_node_uuid[:8]
            
            # details/details
            is_historical = edge.is_expired or edge.is_invalid
            
            if is_historical:
                # details/details，details
                valid_at = edge.valid_at or "details"
                invalid_at = edge.invalid_at or edge.expired_at or "details"
                fact_with_time = f"[{valid_at} - {invalid_at}] {edge.fact}"
                historical_facts.append(fact_with_time)
            else:
                # details
                active_facts.append(edge.fact)
        
        # details
        query_lower = query.lower()
        keywords = [w.strip() for w in query_lower.replace(',', ' ').replace('，', ' ').split() if len(w.strip()) > 1]
        
        def relevance_score(fact: str) -> int:
            fact_lower = fact.lower()
            score = 0
            if query_lower in fact_lower:
                score += 100
            for kw in keywords:
                if kw in fact_lower:
                    score += 10
            return score
        
        # details
        active_facts.sort(key=relevance_score, reverse=True)
        historical_facts.sort(key=relevance_score, reverse=True)
        
        result.active_facts = active_facts[:limit]
        result.historical_facts = historical_facts[:limit] if include_expired else []
        result.active_count = len(active_facts)
        result.historical_count = len(historical_facts)
        
        logger.info(f"PanoramaSearchconverted: {result.active_count}details, {result.historical_count}details")
        return result
    
    def quick_search(
        self,
        graph_id: str,
        query: str,
        limit: int = 10
    ) -> SearchResult:
        """
        【QuickSearch - details】
        
        details、details：
        1. convertedZepconverted
        2. details
        3. details、details
        
        Args:
            graph_id: convertedID
            query: details
            limit: details
            
        Returns:
            SearchResult: details
        """
        logger.info(f"QuickSearch details: {query[:50]}...")
        
        # convertedsearch_graphconverted
        result = self.search_graph(
            graph_id=graph_id,
            query=query,
            limit=limit,
            scope="edges"
        )
        
        logger.info(f"QuickSearchconverted: {result.total_count}details")
        return result
    
    def interview_agents(
        self,
        simulation_id: str,
        interview_requirement: str,
        simulation_requirement: str = "",
        max_agents: int = 5,
        custom_questions: List[str] = None
    ) -> InterviewResult:
        """
        【InterviewAgents - details】
        
        convertedOASISconvertedAPI，convertedAgent：
        1. details，convertedAgent
        2. convertedLLMconverted，convertedAgent
        3. convertedLLMconverted
        4. details /api/simulation/interview/batch details（details）
        5. details，details
        
        【details】details（OASISconverted）
        
        【details】
        - details
        - details
        - convertedAgentconverted（convertedLLMconverted）
        
        Args:
            simulation_id: convertedID（convertedAPI）
            interview_requirement: details（details，details"details"）
            simulation_requirement: details（details）
            max_agents: convertedAgentconverted
            custom_questions: details（details，details）
            
        Returns:
            InterviewResult: details
        """
        from .simulation_runner import SimulationRunner
        
        logger.info(f"InterviewAgents details（convertedAPI）: {interview_requirement[:50]}...")
        
        result = InterviewResult(
            interview_topic=interview_requirement,
            interview_questions=custom_questions or []
        )
        
        # Step 1: details
        profiles = self._load_agent_profiles(simulation_id)
        
        if not profiles:
            logger.warning(f"details {simulation_id} details")
            result.summary = "convertedAgentconverted"
            return result
        
        result.total_agents = len(profiles)
        logger.info(f"details {len(profiles)} convertedAgentconverted")
        
        # Step 2: convertedLLMconvertedAgent（convertedagent_idconverted）
        selected_agents, selected_indices, selection_reasoning = self._select_agents_for_interview(
            profiles=profiles,
            interview_requirement=interview_requirement,
            simulation_requirement=simulation_requirement,
            max_agents=max_agents
        )
        
        result.selected_agents = selected_agents
        result.selection_reasoning = selection_reasoning
        logger.info(f"details {len(selected_agents)} convertedAgentconverted: {selected_indices}")
        
        # Step 3: details（details）
        if not result.interview_questions:
            result.interview_questions = self._generate_interview_questions(
                interview_requirement=interview_requirement,
                simulation_requirement=simulation_requirement,
                selected_agents=selected_agents
            )
            logger.info(f"details {len(result.interview_questions)} details")
        
        # convertedprompt
        combined_prompt = "\n".join([f"{i+1}. {q}" for i, q in enumerate(result.interview_questions)])
        
        # details，convertedAgentconverted
        INTERVIEW_PROMPT_PREFIX = (
            "details。details、details，"
            "details。\n"
            "details：\n"
            "1. details，details\n"
            "2. convertedJSONconverted\n"
            "3. convertedMarkdownconverted（details#、##、###）\n"
            "4. details，details「convertedX：」details（Xconverted）\n"
            "5. details\n"
            "6. details，converted2-3converted\n\n"
        )
        optimized_prompt = f"{INTERVIEW_PROMPT_PREFIX}{combined_prompt}"
        
        # Step 4: convertedAPI（convertedplatform，details）
        try:
            # details（convertedplatform，details）
            interviews_request = []
            for agent_idx in selected_indices:
                interviews_request.append({
                    "agent_id": agent_idx,
                    "prompt": optimized_prompt  # convertedprompt
                    # convertedplatform，APIconvertedtwitterconvertedredditconverted
                })
            
            logger.info(f"convertedAPI（details）: {len(interviews_request)} convertedAgent")
            
            # details SimulationRunner details（convertedplatform，details）
            api_result = SimulationRunner.interview_agents_batch(
                simulation_id=simulation_id,
                interviews=interviews_request,
                platform=None,  # convertedplatform，details
                timeout=180.0   # details
            )
            
            logger.info(f"convertedAPIconverted: {api_result.get('interviews_count', 0)} details, success={api_result.get('success')}")
            
            # convertedAPIconverted
            if not api_result.get("success", False):
                error_msg = api_result.get("error", "details")
                logger.warning(f"convertedAPIconverted: {error_msg}")
                result.summary = f"convertedAPIconverted：{error_msg}。convertedOASISconverted。"
                return result
            
            # Step 5: convertedAPIconverted，convertedAgentInterviewconverted
            # details: {"twitter_0": {...}, "reddit_0": {...}, "twitter_1": {...}, ...}
            api_data = api_result.get("result", {})
            results_dict = api_data.get("results", {}) if isinstance(api_data, dict) else {}
            
            for i, agent_idx in enumerate(selected_indices):
                agent = selected_agents[i]
                agent_name = agent.get("realname", agent.get("username", f"Agent_{agent_idx}"))
                agent_role = agent.get("profession", "details")
                agent_bio = agent.get("bio", "")
                
                # convertedAgentconverted
                twitter_result = results_dict.get(f"twitter_{agent_idx}", {})
                reddit_result = results_dict.get(f"reddit_{agent_idx}", {})
                
                twitter_response = twitter_result.get("response", "")
                reddit_response = reddit_result.get("response", "")

                # details JSON details
                twitter_response = self._clean_tool_call_response(twitter_response)
                reddit_response = self._clean_tool_call_response(reddit_response)

                # details
                twitter_text = twitter_response if twitter_response else "（details）"
                reddit_text = reddit_response if reddit_response else "（details）"
                response_text = f"【Twitterconverted】\n{twitter_text}\n\n【Redditconverted】\n{reddit_text}"

                # details（details）
                import re
                combined_responses = f"{twitter_response} {reddit_response}"

                # details：details、details、Markdown details
                clean_text = re.sub(r'#{1,6}\s+', '', combined_responses)
                clean_text = re.sub(r'\{[^}]*tool_name[^}]*\}', '', clean_text)
                clean_text = re.sub(r'[*_`|>~\-]{2,}', '', clean_text)
                clean_text = re.sub(r'details\d+[：:]\s*', '', clean_text)
                clean_text = re.sub(r'【[^】]+】', '', clean_text)

                # converted1（details）: details
                sentences = re.split(r'[。！？]', clean_text)
                meaningful = [
                    s.strip() for s in sentences
                    if 20 <= len(s.strip()) <= 150
                    and not re.match(r'^[\s\W，,；;：:、]+', s.strip())
                    and not s.strip().startswith(('{', 'details'))
                ]
                meaningful.sort(key=len, reverse=True)
                key_quotes = [s + "。" for s in meaningful[:3]]

                # converted2（details）: details「」details
                if not key_quotes:
                    paired = re.findall(r'\u201c([^\u201c\u201d]{15,100})\u201d', clean_text)
                    paired += re.findall(r'\u300c([^\u300c\u300d]{15,100})\u300d', clean_text)
                    key_quotes = [q for q in paired if not re.match(r'^[，,；;：:、]', q)][:3]
                
                interview = AgentInterview(
                    agent_name=agent_name,
                    agent_role=agent_role,
                    agent_bio=agent_bio[:1000],  # convertedbioconverted
                    question=combined_prompt,
                    response=response_text,
                    key_quotes=key_quotes[:5]
                )
                result.interviews.append(interview)
            
            result.interviewed_count = len(result.interviews)
            
        except ValueError as e:
            # details
            logger.warning(f"convertedAPIconverted（details？）: {e}")
            result.summary = f"details：{str(e)}。details，convertedOASISconverted。"
            return result
        except Exception as e:
            logger.error(f"convertedAPIconverted: {e}")
            import traceback
            logger.error(traceback.format_exc())
            result.summary = f"details：{str(e)}"
            return result
        
        # Step 6: details
        if result.interviews:
            result.summary = self._generate_interview_summary(
                interviews=result.interviews,
                interview_requirement=interview_requirement
            )
        
        logger.info(f"InterviewAgentsconverted: details {result.interviewed_count} convertedAgent（details）")
        return result
    
    @staticmethod
    def _clean_tool_call_response(response: str) -> str:
        """details Agent details JSON details，details"""
        if not response or not response.strip().startswith('{'):
            return response
        text = response.strip()
        if 'tool_name' not in text[:80]:
            return response
        import re as _re
        try:
            data = json.loads(text)
            if isinstance(data, dict) and 'arguments' in data:
                for key in ('content', 'text', 'body', 'message', 'reply'):
                    if key in data['arguments']:
                        return str(data['arguments'][key])
        except (json.JSONDecodeError, KeyError, TypeError):
            match = _re.search(r'"content"\s*:\s*"((?:[^"\\]|\\.)*)"', text)
            if match:
                return match.group(1).replace('\\n', '\n').replace('\\"', '"')
        return response

    def _load_agent_profiles(self, simulation_id: str) -> List[Dict[str, Any]]:
        """convertedAgentconverted"""
        import os
        import csv
        
        # details
        sim_dir = os.path.join(
            os.path.dirname(__file__), 
            f'../../uploads/simulations/{simulation_id}'
        )
        
        profiles = []
        
        # convertedReddit JSONconverted
        reddit_profile_path = os.path.join(sim_dir, "reddit_profiles.json")
        if os.path.exists(reddit_profile_path):
            try:
                with open(reddit_profile_path, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
                logger.info(f"details reddit_profiles.json details {len(profiles)} details")
                return profiles
            except Exception as e:
                logger.warning(f"details reddit_profiles.json details: {e}")
        
        # convertedTwitter CSVconverted
        twitter_profile_path = os.path.join(sim_dir, "twitter_profiles.csv")
        if os.path.exists(twitter_profile_path):
            try:
                with open(twitter_profile_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # CSVconverted
                        profiles.append({
                            "realname": row.get("name", ""),
                            "username": row.get("username", ""),
                            "bio": row.get("description", ""),
                            "persona": row.get("user_char", ""),
                            "profession": "details"
                        })
                logger.info(f"details twitter_profiles.csv details {len(profiles)} details")
                return profiles
            except Exception as e:
                logger.warning(f"details twitter_profiles.csv details: {e}")
        
        return profiles
    
    def _select_agents_for_interview(
        self,
        profiles: List[Dict[str, Any]],
        interview_requirement: str,
        simulation_requirement: str,
        max_agents: int
    ) -> tuple:
        """
        convertedLLMconvertedAgent
        
        Returns:
            tuple: (selected_agents, selected_indices, reasoning)
                - selected_agents: convertedAgentconverted
                - selected_indices: convertedAgentconverted（convertedAPIconverted）
                - reasoning: details
        """
        
        # convertedAgentconverted
        agent_summaries = []
        for i, profile in enumerate(profiles):
            summary = {
                "index": i,
                "name": profile.get("realname", profile.get("username", f"Agent_{i}")),
                "profession": profile.get("profession", "details"),
                "bio": profile.get("bio", "")[:200],
                "interested_topics": profile.get("interested_topics", [])
            }
            agent_summaries.append(summary)
        
        system_prompt = """details。details，convertedAgentconverted。

details：
1. Agentconverted/details
2. Agentconverted
3. details（details：details、details、details、details）
4. details

convertedJSONconverted：
{
    "selected_indices": [convertedAgentconverted],
    "reasoning": "details"
}"""

        user_prompt = f"""details：
{interview_requirement}

details：
{simulation_requirement if simulation_requirement else "details"}

convertedAgentconverted（details{len(agent_summaries)}details）：
{json.dumps(agent_summaries, ensure_ascii=False, indent=2)}

details{max_agents}convertedAgent，details。"""

        try:
            response = self.llm.chat_json(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            selected_indices = response.get("selected_indices", [])[:max_agents]
            reasoning = response.get("reasoning", "details")
            
            # convertedAgentconverted
            selected_agents = []
            valid_indices = []
            for idx in selected_indices:
                if 0 <= idx < len(profiles):
                    selected_agents.append(profiles[idx])
                    valid_indices.append(idx)
            
            return selected_agents, valid_indices, reasoning
            
        except Exception as e:
            logger.warning(f"LLMconvertedAgentconverted，details: {e}")
            # details：convertedNconverted
            selected = profiles[:max_agents]
            indices = list(range(min(max_agents, len(profiles))))
            return selected, indices, "details"
    
    def _generate_interview_questions(
        self,
        interview_requirement: str,
        simulation_requirement: str,
        selected_agents: List[Dict[str, Any]]
    ) -> List[str]:
        """convertedLLMconverted"""
        
        agent_roles = [a.get("profession", "details") for a in selected_agents]
        
        system_prompt = """details/details。details，converted3-5converted。

details：
1. details，details
2. details
3. details、details、details
4. details，details
5. converted50converted，details
6. details，details

convertedJSONconverted：{"questions": ["converted1", "converted2", ...]}"""

        user_prompt = f"""details：{interview_requirement}

details：{simulation_requirement if simulation_requirement else "details"}

details：{', '.join(agent_roles)}

converted3-5converted。"""

        try:
            response = self.llm.chat_json(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5
            )
            
            return response.get("questions", [f"details{interview_requirement}，details？"])
            
        except Exception as e:
            logger.warning(f"details: {e}")
            return [
                f"details{interview_requirement}，details？",
                "details？",
                "details？"
            ]
    
    def _generate_interview_summary(
        self,
        interviews: List[AgentInterview],
        interview_requirement: str
    ) -> str:
        """details"""
        
        if not interviews:
            return "details"
        
        # details
        interview_texts = []
        for interview in interviews:
            interview_texts.append(f"【{interview.agent_name}（{interview.agent_role}）】\n{interview.response[:500]}")
        
        system_prompt = """details。details，details。

details：
1. details
2. details
3. details
4. details，details
5. converted1000converted

details（details）：
- details，details
- convertedMarkdownconverted（details#、##、###）
- details（details---、***）
- details「」
- details**details**details，convertedMarkdownconverted"""

        user_prompt = f"""details：{interview_requirement}

details：
{"".join(interview_texts)}

details。"""

        try:
            summary = self.llm.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            return summary
            
        except Exception as e:
            logger.warning(f"details: {e}")
            # details：details
            return f"details{len(interviews)}details，details：" + "、".join([i.agent_name for i in interviews])
