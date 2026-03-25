"""
details
convertedLLMconverted、details、details
details，details

details，details：
1. details
2. details
3. convertedAgentconverted
4. details
"""

import json
import math
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime

from openai import OpenAI

from ..config import Config
from ..utils.logger import get_logger
from .zep_entity_reader import EntityNode, ZepEntityReader

logger = get_logger('mirofish.simulation_config')

# details（details）
CHINA_TIMEZONE_CONFIG = {
    # details（details）
    "dead_hours": [0, 1, 2, 3, 4, 5],
    # details（details）
    "morning_hours": [6, 7, 8],
    # details
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    # details（details）
    "peak_hours": [19, 20, 21, 22],
    # details（details）
    "night_hours": [23],
    # details
    "activity_multipliers": {
        "dead": 0.05,      # details
        "morning": 0.4,    # details
        "work": 0.7,       # details
        "peak": 1.5,       # details
        "night": 0.5       # details
    }
}


@dataclass
class AgentActivityConfig:
    """convertedAgentconverted"""
    agent_id: int
    entity_uuid: str
    entity_name: str
    entity_type: str
    
    # details (0.0-1.0)
    activity_level: float = 0.5  # details
    
    # details（details）
    posts_per_hour: float = 1.0
    comments_per_hour: float = 2.0
    
    # details（24converted，0-23）
    active_hours: List[int] = field(default_factory=lambda: list(range(8, 23)))
    
    # details（details，details：details）
    response_delay_min: int = 5
    response_delay_max: int = 60
    
    # details (-1.0converted1.0，details)
    sentiment_bias: float = 0.0
    
    # details（details）
    stance: str = "neutral"  # supportive, opposing, neutral, observer
    
    # details（convertedAgentconverted）
    influence_weight: float = 1.0


@dataclass  
class TimeSimulationConfig:
    """details（details）"""
    # details（details）
    total_simulation_hours: int = 72  # converted72converted（3converted）
    
    # details（details）- converted60converted（1converted），details
    minutes_per_round: int = 60
    
    # convertedAgentconverted
    agents_per_hour_min: int = 5
    agents_per_hour_max: int = 20
    
    # details（converted19-22converted，details）
    peak_hours: List[int] = field(default_factory=lambda: [19, 20, 21, 22])
    peak_activity_multiplier: float = 1.5
    
    # details（converted0-5converted，details）
    off_peak_hours: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5])
    off_peak_activity_multiplier: float = 0.05  # details
    
    # details
    morning_hours: List[int] = field(default_factory=lambda: [6, 7, 8])
    morning_activity_multiplier: float = 0.4
    
    # details
    work_hours: List[int] = field(default_factory=lambda: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    work_activity_multiplier: float = 0.7


@dataclass
class EventConfig:
    """details"""
    # details（details）
    initial_posts: List[Dict[str, Any]] = field(default_factory=list)
    
    # details（details）
    scheduled_events: List[Dict[str, Any]] = field(default_factory=list)
    
    # details
    hot_topics: List[str] = field(default_factory=list)
    
    # details
    narrative_direction: str = ""


@dataclass
class PlatformConfig:
    """details"""
    platform: str  # twitter or reddit
    
    # details
    recency_weight: float = 0.4  # details
    popularity_weight: float = 0.3  # details
    relevance_weight: float = 0.3  # details
    
    # details（details）
    viral_threshold: int = 10
    
    # details（details）
    echo_chamber_strength: float = 0.5


@dataclass
class SimulationParameters:
    """details"""
    # details
    simulation_id: str
    project_id: str
    graph_id: str
    simulation_requirement: str
    
    # details
    time_config: TimeSimulationConfig = field(default_factory=TimeSimulationConfig)
    
    # Agentconverted
    agent_configs: List[AgentActivityConfig] = field(default_factory=list)
    
    # details
    event_config: EventConfig = field(default_factory=EventConfig)
    
    # details
    twitter_config: Optional[PlatformConfig] = None
    reddit_config: Optional[PlatformConfig] = None
    
    # LLMconverted
    llm_model: str = ""
    llm_base_url: str = ""
    
    # details
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    generation_reasoning: str = ""  # LLMconverted
    
    def to_dict(self) -> Dict[str, Any]:
        """details"""
        time_dict = asdict(self.time_config)
        return {
            "simulation_id": self.simulation_id,
            "project_id": self.project_id,
            "graph_id": self.graph_id,
            "simulation_requirement": self.simulation_requirement,
            "time_config": time_dict,
            "agent_configs": [asdict(a) for a in self.agent_configs],
            "event_config": asdict(self.event_config),
            "twitter_config": asdict(self.twitter_config) if self.twitter_config else None,
            "reddit_config": asdict(self.reddit_config) if self.reddit_config else None,
            "llm_model": self.llm_model,
            "llm_base_url": self.llm_base_url,
            "generated_at": self.generated_at,
            "generation_reasoning": self.generation_reasoning,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """convertedJSONconverted"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class SimulationConfigGenerator:
    """
    details
    
    convertedLLMconverted、details、details，
    details
    
    details：
    1. details（details）
    2. convertedAgentconverted（converted10-20converted）
    3. details
    """
    
    # details
    MAX_CONTEXT_LENGTH = 50000
    # convertedAgentconverted
    AGENTS_PER_BATCH = 15
    
    # details（details）
    TIME_CONFIG_CONTEXT_LENGTH = 10000   # details
    EVENT_CONFIG_CONTEXT_LENGTH = 8000   # details
    ENTITY_SUMMARY_LENGTH = 300          # details
    AGENT_SUMMARY_LENGTH = 300           # Agentconverted
    ENTITIES_PER_TYPE_DISPLAY = 20       # details
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model_name = model_name or Config.LLM_MODEL_NAME
        
        if not self.api_key:
            raise ValueError("LLM_API_KEY details")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def generate_config(
        self,
        simulation_id: str,
        project_id: str,
        graph_id: str,
        simulation_requirement: str,
        document_text: str,
        entities: List[EntityNode],
        enable_twitter: bool = True,
        enable_reddit: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> SimulationParameters:
        """
        details（details）
        
        Args:
            simulation_id: convertedID
            project_id: convertedID
            graph_id: convertedID
            simulation_requirement: details
            document_text: details
            entities: details
            enable_twitter: convertedTwitter
            enable_reddit: convertedReddit
            progress_callback: details(current_step, total_steps, message)
            
        Returns:
            SimulationParameters: details
        """
        logger.info(f"details: simulation_id={simulation_id}, details={len(entities)}")
        
        # details
        num_batches = math.ceil(len(entities) / self.AGENTS_PER_BATCH)
        total_steps = 3 + num_batches  # details + details + NconvertedAgent + details
        current_step = 0
        
        def report_progress(step: int, message: str):
            nonlocal current_step
            current_step = step
            if progress_callback:
                progress_callback(step, total_steps, message)
            logger.info(f"[{step}/{total_steps}] {message}")
        
        # 1. details
        context = self._build_context(
            simulation_requirement=simulation_requirement,
            document_text=document_text,
            entities=entities
        )
        
        reasoning_parts = []
        
        # ========== converted1: details ==========
        report_progress(1, "details...")
        num_entities = len(entities)
        time_config_result = self._generate_time_config(context, num_entities)
        time_config = self._parse_time_config(time_config_result, num_entities)
        reasoning_parts.append(f"details: {time_config_result.get('reasoning', 'details')}")
        
        # ========== converted2: details ==========
        report_progress(2, "details...")
        event_config_result = self._generate_event_config(context, simulation_requirement, entities)
        event_config = self._parse_event_config(event_config_result)
        reasoning_parts.append(f"details: {event_config_result.get('reasoning', 'details')}")
        
        # ========== converted3-N: convertedAgentconverted ==========
        all_agent_configs = []
        for batch_idx in range(num_batches):
            start_idx = batch_idx * self.AGENTS_PER_BATCH
            end_idx = min(start_idx + self.AGENTS_PER_BATCH, len(entities))
            batch_entities = entities[start_idx:end_idx]
            
            report_progress(
                3 + batch_idx,
                f"convertedAgentconverted ({start_idx + 1}-{end_idx}/{len(entities)})..."
            )
            
            batch_configs = self._generate_agent_configs_batch(
                context=context,
                entities=batch_entities,
                start_idx=start_idx,
                simulation_requirement=simulation_requirement
            )
            all_agent_configs.extend(batch_configs)
        
        reasoning_parts.append(f"Agentconverted: details {len(all_agent_configs)} details")
        
        # ========== details Agent ==========
        logger.info("details Agent...")
        event_config = self._assign_initial_post_agents(event_config, all_agent_configs)
        assigned_count = len([p for p in event_config.initial_posts if p.get("poster_agent_id") is not None])
        reasoning_parts.append(f"details: {assigned_count} details")
        
        # ========== details: details ==========
        report_progress(total_steps, "details...")
        twitter_config = None
        reddit_config = None
        
        if enable_twitter:
            twitter_config = PlatformConfig(
                platform="twitter",
                recency_weight=0.4,
                popularity_weight=0.3,
                relevance_weight=0.3,
                viral_threshold=10,
                echo_chamber_strength=0.5
            )
        
        if enable_reddit:
            reddit_config = PlatformConfig(
                platform="reddit",
                recency_weight=0.3,
                popularity_weight=0.4,
                relevance_weight=0.3,
                viral_threshold=15,
                echo_chamber_strength=0.6
            )
        
        # details
        params = SimulationParameters(
            simulation_id=simulation_id,
            project_id=project_id,
            graph_id=graph_id,
            simulation_requirement=simulation_requirement,
            time_config=time_config,
            agent_configs=all_agent_configs,
            event_config=event_config,
            twitter_config=twitter_config,
            reddit_config=reddit_config,
            llm_model=self.model_name,
            llm_base_url=self.base_url,
            generation_reasoning=" | ".join(reasoning_parts)
        )
        
        logger.info(f"details: {len(params.agent_configs)} convertedAgentconverted")
        
        return params
    
    def _build_context(
        self,
        simulation_requirement: str,
        document_text: str,
        entities: List[EntityNode]
    ) -> str:
        """convertedLLMconverted，details"""
        
        # details
        entity_summary = self._summarize_entities(entities)
        
        # details
        context_parts = [
            f"## details\n{simulation_requirement}",
            f"\n## details ({len(entities)}details)\n{entity_summary}",
        ]
        
        current_length = sum(len(p) for p in context_parts)
        remaining_length = self.MAX_CONTEXT_LENGTH - current_length - 500  # converted500converted
        
        if remaining_length > 0 and document_text:
            doc_text = document_text[:remaining_length]
            if len(document_text) > remaining_length:
                doc_text += "\n...(details)"
            context_parts.append(f"\n## details\n{doc_text}")
        
        return "\n".join(context_parts)
    
    def _summarize_entities(self, entities: List[EntityNode]) -> str:
        """details"""
        lines = []
        
        # details
        by_type: Dict[str, List[EntityNode]] = {}
        for e in entities:
            t = e.get_entity_type() or "Unknown"
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(e)
        
        for entity_type, type_entities in by_type.items():
            lines.append(f"\n### {entity_type} ({len(type_entities)}details)")
            # details
            display_count = self.ENTITIES_PER_TYPE_DISPLAY
            summary_len = self.ENTITY_SUMMARY_LENGTH
            for e in type_entities[:display_count]:
                summary_preview = (e.summary[:summary_len] + "...") if len(e.summary) > summary_len else e.summary
                lines.append(f"- {e.name}: {summary_preview}")
            if len(type_entities) > display_count:
                lines.append(f"  ... details {len(type_entities) - display_count} details")
        
        return "\n".join(lines)
    
    def _call_llm_with_retry(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        """convertedLLMconverted，convertedJSONconverted"""
        import re
        
        max_attempts = 3
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7 - (attempt * 0.1)  # details
                    # convertedmax_tokens，convertedLLMconverted
                )
                
                content = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason
                
                # details
                if finish_reason == 'length':
                    logger.warning(f"LLMconverted (attempt {attempt+1})")
                    content = self._fix_truncated_json(content)
                
                # convertedJSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logger.warning(f"JSONconverted (attempt {attempt+1}): {str(e)[:80]}")
                    
                    # convertedJSON
                    fixed = self._try_fix_config_json(content)
                    if fixed:
                        return fixed
                    
                    last_error = e
                    
            except Exception as e:
                logger.warning(f"LLMconverted (attempt {attempt+1}): {str(e)[:80]}")
                last_error = e
                import time
                time.sleep(2 * (attempt + 1))
        
        raise last_error or Exception("LLMconverted")
    
    def _fix_truncated_json(self, content: str) -> str:
        """convertedJSON"""
        content = content.strip()
        
        # details
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        # details
        if content and content[-1] not in '",}]':
            content += '"'
        
        # details
        content += ']' * open_brackets
        content += '}' * open_braces
        
        return content
    
    def _try_fix_config_json(self, content: str) -> Optional[Dict[str, Any]]:
        """convertedJSON"""
        import re
        
        # details
        content = self._fix_truncated_json(content)
        
        # convertedJSONconverted
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group()
            
            # details
            def fix_string(match):
                s = match.group(0)
                s = s.replace('\n', ' ').replace('\r', ' ')
                s = re.sub(r'\s+', ' ', s)
                return s
            
            json_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', fix_string, json_str)
            
            try:
                return json.loads(json_str)
            except:
                # details
                json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                json_str = re.sub(r'\s+', ' ', json_str)
                try:
                    return json.loads(json_str)
                except:
                    pass
        
        return None
    
    def _generate_time_config(self, context: str, num_entities: int) -> Dict[str, Any]:
        """details"""
        # details
        context_truncated = context[:self.TIME_CONFIG_CONTEXT_LENGTH]
        
        # details（80%convertedagentconverted）
        max_agents_allowed = max(1, int(num_entities * 0.9))
        
        prompt = f"""details，details。

{context_truncated}

## details
convertedJSON。

### details（details，details）：
- details，details
- converted0-5converted（converted0.05）
- converted6-8converted（converted0.4）
- converted9-18converted（converted0.7）
- converted19-22converted（converted1.5）
- 23converted（converted0.5）
- details：details、details、details、details
- **details**：details，details、details
  - details：converted21-23converted；details；details
  - details：details，off_peak_hours details

### convertedJSONconverted（convertedmarkdown）

details：
{{
    "total_simulation_hours": 72,
    "minutes_per_round": 60,
    "agents_per_hour_min": 5,
    "agents_per_hour_max": 50,
    "peak_hours": [19, 20, 21, 22],
    "off_peak_hours": [0, 1, 2, 3, 4, 5],
    "morning_hours": [6, 7, 8],
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "reasoning": "details"
}}

details：
- total_simulation_hours (int): details，24-168converted，details、details
- minutes_per_round (int): details，30-120converted，converted60converted
- agents_per_hour_min (int): convertedAgentconverted（details: 1-{max_agents_allowed}）
- agents_per_hour_max (int): convertedAgentconverted（details: 1-{max_agents_allowed}）
- peak_hours (intconverted): details，details
- off_peak_hours (intconverted): details，details
- morning_hours (intconverted): details
- work_hours (intconverted): details
- reasoning (string): details"""

        system_prompt = "details。convertedJSONconverted，details。"
        
        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"convertedLLMconverted: {e}, details")
            return self._get_default_time_config(num_entities)
    
    def _get_default_time_config(self, num_entities: int) -> Dict[str, Any]:
        """details（details）"""
        return {
            "total_simulation_hours": 72,
            "minutes_per_round": 60,  # converted1converted，details
            "agents_per_hour_min": max(1, num_entities // 15),
            "agents_per_hour_max": max(5, num_entities // 5),
            "peak_hours": [19, 20, 21, 22],
            "off_peak_hours": [0, 1, 2, 3, 4, 5],
            "morning_hours": [6, 7, 8],
            "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "reasoning": "details（converted1converted）"
        }
    
    def _parse_time_config(self, result: Dict[str, Any], num_entities: int) -> TimeSimulationConfig:
        """details，convertedagents_per_hourconvertedagentconverted"""
        # details
        agents_per_hour_min = result.get("agents_per_hour_min", max(1, num_entities // 15))
        agents_per_hour_max = result.get("agents_per_hour_max", max(5, num_entities // 5))
        
        # details：convertedagentconverted
        if agents_per_hour_min > num_entities:
            logger.warning(f"agents_per_hour_min ({agents_per_hour_min}) convertedAgentconverted ({num_entities})，details")
            agents_per_hour_min = max(1, num_entities // 10)
        
        if agents_per_hour_max > num_entities:
            logger.warning(f"agents_per_hour_max ({agents_per_hour_max}) convertedAgentconverted ({num_entities})，details")
            agents_per_hour_max = max(agents_per_hour_min + 1, num_entities // 2)
        
        # details min < max
        if agents_per_hour_min >= agents_per_hour_max:
            agents_per_hour_min = max(1, agents_per_hour_max // 2)
            logger.warning(f"agents_per_hour_min >= max，details {agents_per_hour_min}")
        
        return TimeSimulationConfig(
            total_simulation_hours=result.get("total_simulation_hours", 72),
            minutes_per_round=result.get("minutes_per_round", 60),  # converted1converted
            agents_per_hour_min=agents_per_hour_min,
            agents_per_hour_max=agents_per_hour_max,
            peak_hours=result.get("peak_hours", [19, 20, 21, 22]),
            off_peak_hours=result.get("off_peak_hours", [0, 1, 2, 3, 4, 5]),
            off_peak_activity_multiplier=0.05,  # details
            morning_hours=result.get("morning_hours", [6, 7, 8]),
            morning_activity_multiplier=0.4,
            work_hours=result.get("work_hours", list(range(9, 19))),
            work_activity_multiplier=0.7,
            peak_activity_multiplier=1.5
        )
    
    def _generate_event_config(
        self, 
        context: str, 
        simulation_requirement: str,
        entities: List[EntityNode]
    ) -> Dict[str, Any]:
        """details"""
        
        # details，details LLM details
        entity_types_available = list(set(
            e.get_entity_type() or "Unknown" for e in entities
        ))
        
        # details
        type_examples = {}
        for e in entities:
            etype = e.get_entity_type() or "Unknown"
            if etype not in type_examples:
                type_examples[etype] = []
            if len(type_examples[etype]) < 3:
                type_examples[etype].append(e.name)
        
        type_info = "\n".join([
            f"- {t}: {', '.join(examples)}" 
            for t, examples in type_examples.items()
        ])
        
        # details
        context_truncated = context[:self.EVENT_CONFIG_CONTEXT_LENGTH]
        
        prompt = f"""details，details。

details: {simulation_requirement}

{context_truncated}

## details
{type_info}

## details
convertedJSON：
- details
- details
- details，**details poster_type（details）**

**details**: poster_type details"details"details，details Agent details。
details：details Official/University details，details MediaOutlet details，details Student details。

convertedJSONconverted（convertedmarkdown）：
{{
    "hot_topics": ["converted1", "converted2", ...],
    "narrative_direction": "<details>",
    "initial_posts": [
        {{"content": "details", "poster_type": "details（details）"}},
        ...
    ],
    "reasoning": "<details>"
}}"""

        system_prompt = "details。convertedJSONconverted。details poster_type details。"
        
        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"convertedLLMconverted: {e}, details")
            return {
                "hot_topics": [],
                "narrative_direction": "",
                "initial_posts": [],
                "reasoning": "details"
            }
    
    def _parse_event_config(self, result: Dict[str, Any]) -> EventConfig:
        """details"""
        return EventConfig(
            initial_posts=result.get("initial_posts", []),
            scheduled_events=[],
            hot_topics=result.get("hot_topics", []),
            narrative_direction=result.get("narrative_direction", "")
        )
    
    def _assign_initial_post_agents(
        self,
        event_config: EventConfig,
        agent_configs: List[AgentActivityConfig]
    ) -> EventConfig:
        """
        details Agent
        
        details poster_type details agent_id
        """
        if not event_config.initial_posts:
            return event_config
        
        # details agent details
        agents_by_type: Dict[str, List[AgentActivityConfig]] = {}
        for agent in agent_configs:
            etype = agent.entity_type.lower()
            if etype not in agents_by_type:
                agents_by_type[etype] = []
            agents_by_type[etype].append(agent)
        
        # details（details LLM details）
        type_aliases = {
            "official": ["official", "university", "governmentagency", "government"],
            "university": ["university", "official"],
            "mediaoutlet": ["mediaoutlet", "media"],
            "student": ["student", "person"],
            "professor": ["professor", "expert", "teacher"],
            "alumni": ["alumni", "person"],
            "organization": ["organization", "ngo", "company", "group"],
            "person": ["person", "student", "alumni"],
        }
        
        # details agent details，details agent
        used_indices: Dict[str, int] = {}
        
        updated_posts = []
        for post in event_config.initial_posts:
            poster_type = post.get("poster_type", "").lower()
            content = post.get("content", "")
            
            # details agent
            matched_agent_id = None
            
            # 1. details
            if poster_type in agents_by_type:
                agents = agents_by_type[poster_type]
                idx = used_indices.get(poster_type, 0) % len(agents)
                matched_agent_id = agents[idx].agent_id
                used_indices[poster_type] = idx + 1
            else:
                # 2. details
                for alias_key, aliases in type_aliases.items():
                    if poster_type in aliases or alias_key == poster_type:
                        for alias in aliases:
                            if alias in agents_by_type:
                                agents = agents_by_type[alias]
                                idx = used_indices.get(alias, 0) % len(agents)
                                matched_agent_id = agents[idx].agent_id
                                used_indices[alias] = idx + 1
                                break
                    if matched_agent_id is not None:
                        break
            
            # 3. details，details agent
            if matched_agent_id is None:
                logger.warning(f"details '{poster_type}' details Agent，details Agent")
                if agent_configs:
                    # details，details
                    sorted_agents = sorted(agent_configs, key=lambda a: a.influence_weight, reverse=True)
                    matched_agent_id = sorted_agents[0].agent_id
                else:
                    matched_agent_id = 0
            
            updated_posts.append({
                "content": content,
                "poster_type": post.get("poster_type", "Unknown"),
                "poster_agent_id": matched_agent_id
            })
            
            logger.info(f"details: poster_type='{poster_type}' -> agent_id={matched_agent_id}")
        
        event_config.initial_posts = updated_posts
        return event_config
    
    def _generate_agent_configs_batch(
        self,
        context: str,
        entities: List[EntityNode],
        start_idx: int,
        simulation_requirement: str
    ) -> List[AgentActivityConfig]:
        """convertedAgentconverted"""
        
        # details（details）
        entity_list = []
        summary_len = self.AGENT_SUMMARY_LENGTH
        for i, e in enumerate(entities):
            entity_list.append({
                "agent_id": start_idx + i,
                "entity_name": e.name,
                "entity_type": e.get_entity_type() or "Unknown",
                "summary": e.summary[:summary_len] if e.summary else ""
            })
        
        prompt = f"""details，details。

details: {simulation_requirement}

## details
```json
{json.dumps(entity_list, ensure_ascii=False, indent=2)}
```

## details
details，details：
- **details**：converted0-5converted，converted19-22converted
- **details**（University/GovernmentAgency）：details(0.1-0.3)，details(9-17)details，details(60-240converted)，details(2.5-3.0)
- **details**（MediaOutlet）：details(0.4-0.6)，details(8-23)，details(5-30converted)，details(2.0-2.5)
- **details**（Student/Person/Alumni）：details(0.6-0.9)，details(18-23)，details(1-15converted)，details(0.8-1.2)
- **details/details**：details(0.4-0.6)，details(1.5-2.0)

convertedJSONconverted（convertedmarkdown）：
{{
    "agent_configs": [
        {{
            "agent_id": <details>,
            "activity_level": <0.0-1.0>,
            "posts_per_hour": <details>,
            "comments_per_hour": <details>,
            "active_hours": [<details，details>],
            "response_delay_min": <details>,
            "response_delay_max": <details>,
            "sentiment_bias": <-1.0converted1.0>,
            "stance": "<supportive/opposing/neutral/observer>",
            "influence_weight": <details>
        }},
        ...
    ]
}}"""

        system_prompt = "details。convertedJSON，details。"
        
        try:
            result = self._call_llm_with_retry(prompt, system_prompt)
            llm_configs = {cfg["agent_id"]: cfg for cfg in result.get("agent_configs", [])}
        except Exception as e:
            logger.warning(f"AgentconvertedLLMconverted: {e}, details")
            llm_configs = {}
        
        # convertedAgentActivityConfigconverted
        configs = []
        for i, entity in enumerate(entities):
            agent_id = start_idx + i
            cfg = llm_configs.get(agent_id, {})
            
            # convertedLLMconverted，details
            if not cfg:
                cfg = self._generate_agent_config_by_rule(entity)
            
            config = AgentActivityConfig(
                agent_id=agent_id,
                entity_uuid=entity.uuid,
                entity_name=entity.name,
                entity_type=entity.get_entity_type() or "Unknown",
                activity_level=cfg.get("activity_level", 0.5),
                posts_per_hour=cfg.get("posts_per_hour", 0.5),
                comments_per_hour=cfg.get("comments_per_hour", 1.0),
                active_hours=cfg.get("active_hours", list(range(9, 23))),
                response_delay_min=cfg.get("response_delay_min", 5),
                response_delay_max=cfg.get("response_delay_max", 60),
                sentiment_bias=cfg.get("sentiment_bias", 0.0),
                stance=cfg.get("stance", "neutral"),
                influence_weight=cfg.get("influence_weight", 1.0)
            )
            configs.append(config)
        
        return configs
    
    def _generate_agent_config_by_rule(self, entity: EntityNode) -> Dict[str, Any]:
        """convertedAgentconverted（details）"""
        entity_type = (entity.get_entity_type() or "Unknown").lower()
        
        if entity_type in ["university", "governmentagency", "ngo"]:
            # details：details，details，details
            return {
                "activity_level": 0.2,
                "posts_per_hour": 0.1,
                "comments_per_hour": 0.05,
                "active_hours": list(range(9, 18)),  # 9:00-17:59
                "response_delay_min": 60,
                "response_delay_max": 240,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 3.0
            }
        elif entity_type in ["mediaoutlet"]:
            # details：details，details，details
            return {
                "activity_level": 0.5,
                "posts_per_hour": 0.8,
                "comments_per_hour": 0.3,
                "active_hours": list(range(7, 24)),  # 7:00-23:59
                "response_delay_min": 5,
                "response_delay_max": 30,
                "sentiment_bias": 0.0,
                "stance": "observer",
                "influence_weight": 2.5
            }
        elif entity_type in ["professor", "expert", "official"]:
            # details/details：details+details，details
            return {
                "activity_level": 0.4,
                "posts_per_hour": 0.3,
                "comments_per_hour": 0.5,
                "active_hours": list(range(8, 22)),  # 8:00-21:59
                "response_delay_min": 15,
                "response_delay_max": 90,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 2.0
            }
        elif entity_type in ["student"]:
            # details：details，details
            return {
                "activity_level": 0.8,
                "posts_per_hour": 0.6,
                "comments_per_hour": 1.5,
                "active_hours": [8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],  # details+details
                "response_delay_min": 1,
                "response_delay_max": 15,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 0.8
            }
        elif entity_type in ["alumni"]:
            # details：details
            return {
                "activity_level": 0.6,
                "posts_per_hour": 0.4,
                "comments_per_hour": 0.8,
                "active_hours": [12, 13, 19, 20, 21, 22, 23],  # details+details
                "response_delay_min": 5,
                "response_delay_max": 30,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
        else:
            # details：details
            return {
                "activity_level": 0.7,
                "posts_per_hour": 0.5,
                "comments_per_hour": 1.2,
                "active_hours": [9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],  # details+details
                "response_delay_min": 2,
                "response_delay_max": 20,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
    

