"""
translated
translatedLLMtranslated、translated、translated
translated，translated

translated，translated：
1. translated
2. translated
3. translatedAgenttranslated
4. translated
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

# translated（translated）
CHINA_TIMEZONE_CONFIG = {
    # translated（translated）
    "dead_hours": [0, 1, 2, 3, 4, 5],
    # translated（translated）
    "morning_hours": [6, 7, 8],
    # translated
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    # translated（translated）
    "peak_hours": [19, 20, 21, 22],
    # translated（translated）
    "night_hours": [23],
    # translated
    "activity_multipliers": {
        "dead": 0.05,      # translated
        "morning": 0.4,    # translated
        "work": 0.7,       # translated
        "peak": 1.5,       # translated
        "night": 0.5       # translated
    }
}


@dataclass
class AgentActivityConfig:
    """translatedAgenttranslated"""
    agent_id: int
    entity_uuid: str
    entity_name: str
    entity_type: str
    
    # translated (0.0-1.0)
    activity_level: float = 0.5  # translated
    
    # translated（translated）
    posts_per_hour: float = 1.0
    comments_per_hour: float = 2.0
    
    # translated（24translated，0-23）
    active_hours: List[int] = field(default_factory=lambda: list(range(8, 23)))
    
    # translated（translated，translated：translated）
    response_delay_min: int = 5
    response_delay_max: int = 60
    
    # translated (-1.0translated1.0，translated)
    sentiment_bias: float = 0.0
    
    # translated（translated）
    stance: str = "neutral"  # supportive, opposing, neutral, observer
    
    # translated（translatedAgenttranslated）
    influence_weight: float = 1.0


@dataclass  
class TimeSimulationConfig:
    """translated（translated）"""
    # translated（translated）
    total_simulation_hours: int = 72  # translated72translated（3translated）
    
    # translated（translated）- translated60translated（1translated），translated
    minutes_per_round: int = 60
    
    # translatedAgenttranslated
    agents_per_hour_min: int = 5
    agents_per_hour_max: int = 20
    
    # translated（translated19-22translated，translated）
    peak_hours: List[int] = field(default_factory=lambda: [19, 20, 21, 22])
    peak_activity_multiplier: float = 1.5
    
    # translated（translated0-5translated，translated）
    off_peak_hours: List[int] = field(default_factory=lambda: [0, 1, 2, 3, 4, 5])
    off_peak_activity_multiplier: float = 0.05  # translated
    
    # translated
    morning_hours: List[int] = field(default_factory=lambda: [6, 7, 8])
    morning_activity_multiplier: float = 0.4
    
    # translated
    work_hours: List[int] = field(default_factory=lambda: [9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    work_activity_multiplier: float = 0.7


@dataclass
class EventConfig:
    """translated"""
    # translated（translated）
    initial_posts: List[Dict[str, Any]] = field(default_factory=list)
    
    # translated（translated）
    scheduled_events: List[Dict[str, Any]] = field(default_factory=list)
    
    # translated
    hot_topics: List[str] = field(default_factory=list)
    
    # translated
    narrative_direction: str = ""


@dataclass
class PlatformConfig:
    """translated"""
    platform: str  # twitter or reddit
    
    # translated
    recency_weight: float = 0.4  # translated
    popularity_weight: float = 0.3  # translated
    relevance_weight: float = 0.3  # translated
    
    # translated（translated）
    viral_threshold: int = 10
    
    # translated（translated）
    echo_chamber_strength: float = 0.5


@dataclass
class SimulationParameters:
    """translated"""
    # translated
    simulation_id: str
    project_id: str
    graph_id: str
    simulation_requirement: str
    
    # translated
    time_config: TimeSimulationConfig = field(default_factory=TimeSimulationConfig)
    
    # Agenttranslated
    agent_configs: List[AgentActivityConfig] = field(default_factory=list)
    
    # translated
    event_config: EventConfig = field(default_factory=EventConfig)
    
    # translated
    twitter_config: Optional[PlatformConfig] = None
    reddit_config: Optional[PlatformConfig] = None
    
    # LLMtranslated
    llm_model: str = ""
    llm_base_url: str = ""
    
    # translated
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    generation_reasoning: str = ""  # LLMtranslated
    
    def to_dict(self) -> Dict[str, Any]:
        """translated"""
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
        """translatedJSONtranslated"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class SimulationConfigGenerator:
    """
    translated
    
    translatedLLMtranslated、translated、translated，
    translated
    
    translated：
    1. translated（translated）
    2. translatedAgenttranslated（translated10-20translated）
    3. translated
    """
    
    # translated
    MAX_CONTEXT_LENGTH = 50000
    # translatedAgenttranslated
    AGENTS_PER_BATCH = 15
    
    # translated（translated）
    TIME_CONFIG_CONTEXT_LENGTH = 10000   # translated
    EVENT_CONFIG_CONTEXT_LENGTH = 8000   # translated
    ENTITY_SUMMARY_LENGTH = 300          # translated
    AGENT_SUMMARY_LENGTH = 300           # Agenttranslated
    ENTITIES_PER_TYPE_DISPLAY = 20       # translated
    
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
            raise ValueError("LLM_API_KEY translated")
        
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
        translated（translated）
        
        Args:
            simulation_id: translatedID
            project_id: translatedID
            graph_id: translatedID
            simulation_requirement: translated
            document_text: translated
            entities: translated
            enable_twitter: translatedTwitter
            enable_reddit: translatedReddit
            progress_callback: translated(current_step, total_steps, message)
            
        Returns:
            SimulationParameters: translated
        """
        logger.info(f"translated: simulation_id={simulation_id}, translated={len(entities)}")
        
        # translated
        num_batches = math.ceil(len(entities) / self.AGENTS_PER_BATCH)
        total_steps = 3 + num_batches  # translated + translated + NtranslatedAgent + translated
        current_step = 0
        
        def report_progress(step: int, message: str):
            nonlocal current_step
            current_step = step
            if progress_callback:
                progress_callback(step, total_steps, message)
            logger.info(f"[{step}/{total_steps}] {message}")
        
        # 1. translated
        context = self._build_context(
            simulation_requirement=simulation_requirement,
            document_text=document_text,
            entities=entities
        )
        
        reasoning_parts = []
        
        # ========== translated1: translated ==========
        report_progress(1, "translated...")
        num_entities = len(entities)
        time_config_result = self._generate_time_config(context, num_entities)
        time_config = self._parse_time_config(time_config_result, num_entities)
        reasoning_parts.append(f"translated: {time_config_result.get('reasoning', 'translated')}")
        
        # ========== translated2: translated ==========
        report_progress(2, "translated...")
        event_config_result = self._generate_event_config(context, simulation_requirement, entities)
        event_config = self._parse_event_config(event_config_result)
        reasoning_parts.append(f"translated: {event_config_result.get('reasoning', 'translated')}")
        
        # ========== translated3-N: translatedAgenttranslated ==========
        all_agent_configs = []
        for batch_idx in range(num_batches):
            start_idx = batch_idx * self.AGENTS_PER_BATCH
            end_idx = min(start_idx + self.AGENTS_PER_BATCH, len(entities))
            batch_entities = entities[start_idx:end_idx]
            
            report_progress(
                3 + batch_idx,
                f"translatedAgenttranslated ({start_idx + 1}-{end_idx}/{len(entities)})..."
            )
            
            batch_configs = self._generate_agent_configs_batch(
                context=context,
                entities=batch_entities,
                start_idx=start_idx,
                simulation_requirement=simulation_requirement
            )
            all_agent_configs.extend(batch_configs)
        
        reasoning_parts.append(f"Agenttranslated: translated {len(all_agent_configs)} translated")
        
        # ========== translated Agent ==========
        logger.info("translated Agent...")
        event_config = self._assign_initial_post_agents(event_config, all_agent_configs)
        assigned_count = len([p for p in event_config.initial_posts if p.get("poster_agent_id") is not None])
        reasoning_parts.append(f"translated: {assigned_count} translated")
        
        # ========== translated: translated ==========
        report_progress(total_steps, "translated...")
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
        
        # translated
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
        
        logger.info(f"translated: {len(params.agent_configs)} translatedAgenttranslated")
        
        return params
    
    def _build_context(
        self,
        simulation_requirement: str,
        document_text: str,
        entities: List[EntityNode]
    ) -> str:
        """translatedLLMtranslated，translated"""
        
        # translated
        entity_summary = self._summarize_entities(entities)
        
        # translated
        context_parts = [
            f"## translated\n{simulation_requirement}",
            f"\n## translated ({len(entities)}translated)\n{entity_summary}",
        ]
        
        current_length = sum(len(p) for p in context_parts)
        remaining_length = self.MAX_CONTEXT_LENGTH - current_length - 500  # translated500translated
        
        if remaining_length > 0 and document_text:
            doc_text = document_text[:remaining_length]
            if len(document_text) > remaining_length:
                doc_text += "\n...(translated)"
            context_parts.append(f"\n## translated\n{doc_text}")
        
        return "\n".join(context_parts)
    
    def _summarize_entities(self, entities: List[EntityNode]) -> str:
        """translated"""
        lines = []
        
        # translated
        by_type: Dict[str, List[EntityNode]] = {}
        for e in entities:
            t = e.get_entity_type() or "Unknown"
            if t not in by_type:
                by_type[t] = []
            by_type[t].append(e)
        
        for entity_type, type_entities in by_type.items():
            lines.append(f"\n### {entity_type} ({len(type_entities)}translated)")
            # translated
            display_count = self.ENTITIES_PER_TYPE_DISPLAY
            summary_len = self.ENTITY_SUMMARY_LENGTH
            for e in type_entities[:display_count]:
                summary_preview = (e.summary[:summary_len] + "...") if len(e.summary) > summary_len else e.summary
                lines.append(f"- {e.name}: {summary_preview}")
            if len(type_entities) > display_count:
                lines.append(f"  ... translated {len(type_entities) - display_count} translated")
        
        return "\n".join(lines)
    
    def _call_llm_with_retry(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        """translatedLLMtranslated，translatedJSONtranslated"""
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
                    temperature=0.7 - (attempt * 0.1)  # translated
                    # translatedmax_tokens，translatedLLMtranslated
                )
                
                content = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason
                
                # translated
                if finish_reason == 'length':
                    logger.warning(f"LLMtranslated (attempt {attempt+1})")
                    content = self._fix_truncated_json(content)
                
                # translatedJSON
                try:
                    return json.loads(content)
                except json.JSONDecodeError as e:
                    logger.warning(f"JSONtranslated (attempt {attempt+1}): {str(e)[:80]}")
                    
                    # translatedJSON
                    fixed = self._try_fix_config_json(content)
                    if fixed:
                        return fixed
                    
                    last_error = e
                    
            except Exception as e:
                logger.warning(f"LLMtranslated (attempt {attempt+1}): {str(e)[:80]}")
                last_error = e
                import time
                time.sleep(2 * (attempt + 1))
        
        raise last_error or Exception("LLMtranslated")
    
    def _fix_truncated_json(self, content: str) -> str:
        """translatedJSON"""
        content = content.strip()
        
        # translated
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        # translated
        if content and content[-1] not in '",}]':
            content += '"'
        
        # translated
        content += ']' * open_brackets
        content += '}' * open_braces
        
        return content
    
    def _try_fix_config_json(self, content: str) -> Optional[Dict[str, Any]]:
        """translatedJSON"""
        import re
        
        # translated
        content = self._fix_truncated_json(content)
        
        # translatedJSONtranslated
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group()
            
            # translated
            def fix_string(match):
                s = match.group(0)
                s = s.replace('\n', ' ').replace('\r', ' ')
                s = re.sub(r'\s+', ' ', s)
                return s
            
            json_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', fix_string, json_str)
            
            try:
                return json.loads(json_str)
            except:
                # translated
                json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                json_str = re.sub(r'\s+', ' ', json_str)
                try:
                    return json.loads(json_str)
                except:
                    pass
        
        return None
    
    def _generate_time_config(self, context: str, num_entities: int) -> Dict[str, Any]:
        """translated"""
        # translated
        context_truncated = context[:self.TIME_CONFIG_CONTEXT_LENGTH]
        
        # translated（80%translatedagenttranslated）
        max_agents_allowed = max(1, int(num_entities * 0.9))
        
        prompt = f"""translated，translated。

{context_truncated}

## translated
translatedJSON。

### translated（translated，translated）：
- translated，translated
- translated0-5translated（translated0.05）
- translated6-8translated（translated0.4）
- translated9-18translated（translated0.7）
- translated19-22translated（translated1.5）
- 23translated（translated0.5）
- translated：translated、translated、translated、translated
- **translated**：translated，translated、translated
  - translated：translated21-23translated；translated；translated
  - translated：translated，off_peak_hours translated

### translatedJSONtranslated（translatedmarkdown）

translated：
{{
    "total_simulation_hours": 72,
    "minutes_per_round": 60,
    "agents_per_hour_min": 5,
    "agents_per_hour_max": 50,
    "peak_hours": [19, 20, 21, 22],
    "off_peak_hours": [0, 1, 2, 3, 4, 5],
    "morning_hours": [6, 7, 8],
    "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "reasoning": "translated"
}}

translated：
- total_simulation_hours (int): translated，24-168translated，translated、translated
- minutes_per_round (int): translated，30-120translated，translated60translated
- agents_per_hour_min (int): translatedAgenttranslated（translated: 1-{max_agents_allowed}）
- agents_per_hour_max (int): translatedAgenttranslated（translated: 1-{max_agents_allowed}）
- peak_hours (inttranslated): translated，translated
- off_peak_hours (inttranslated): translated，translated
- morning_hours (inttranslated): translated
- work_hours (inttranslated): translated
- reasoning (string): translated"""

        system_prompt = "translated。translatedJSONtranslated，translated。"
        
        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"translatedLLMtranslated: {e}, translated")
            return self._get_default_time_config(num_entities)
    
    def _get_default_time_config(self, num_entities: int) -> Dict[str, Any]:
        """translated（translated）"""
        return {
            "total_simulation_hours": 72,
            "minutes_per_round": 60,  # translated1translated，translated
            "agents_per_hour_min": max(1, num_entities // 15),
            "agents_per_hour_max": max(5, num_entities // 5),
            "peak_hours": [19, 20, 21, 22],
            "off_peak_hours": [0, 1, 2, 3, 4, 5],
            "morning_hours": [6, 7, 8],
            "work_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "reasoning": "translated（translated1translated）"
        }
    
    def _parse_time_config(self, result: Dict[str, Any], num_entities: int) -> TimeSimulationConfig:
        """translated，translatedagents_per_hourtranslatedagenttranslated"""
        # translated
        agents_per_hour_min = result.get("agents_per_hour_min", max(1, num_entities // 15))
        agents_per_hour_max = result.get("agents_per_hour_max", max(5, num_entities // 5))
        
        # translated：translatedagenttranslated
        if agents_per_hour_min > num_entities:
            logger.warning(f"agents_per_hour_min ({agents_per_hour_min}) translatedAgenttranslated ({num_entities})，translated")
            agents_per_hour_min = max(1, num_entities // 10)
        
        if agents_per_hour_max > num_entities:
            logger.warning(f"agents_per_hour_max ({agents_per_hour_max}) translatedAgenttranslated ({num_entities})，translated")
            agents_per_hour_max = max(agents_per_hour_min + 1, num_entities // 2)
        
        # translated min < max
        if agents_per_hour_min >= agents_per_hour_max:
            agents_per_hour_min = max(1, agents_per_hour_max // 2)
            logger.warning(f"agents_per_hour_min >= max，translated {agents_per_hour_min}")
        
        return TimeSimulationConfig(
            total_simulation_hours=result.get("total_simulation_hours", 72),
            minutes_per_round=result.get("minutes_per_round", 60),  # translated1translated
            agents_per_hour_min=agents_per_hour_min,
            agents_per_hour_max=agents_per_hour_max,
            peak_hours=result.get("peak_hours", [19, 20, 21, 22]),
            off_peak_hours=result.get("off_peak_hours", [0, 1, 2, 3, 4, 5]),
            off_peak_activity_multiplier=0.05,  # translated
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
        """translated"""
        
        # translated，translated LLM translated
        entity_types_available = list(set(
            e.get_entity_type() or "Unknown" for e in entities
        ))
        
        # translated
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
        
        # translated
        context_truncated = context[:self.EVENT_CONFIG_CONTEXT_LENGTH]
        
        prompt = f"""translated，translated。

translated: {simulation_requirement}

{context_truncated}

## translated
{type_info}

## translated
translatedJSON：
- translated
- translated
- translated，**translated poster_type（translated）**

**translated**: poster_type translated"translated"translated，translated Agent translated。
translated：translated Official/University translated，translated MediaOutlet translated，translated Student translated。

translatedJSONtranslated（translatedmarkdown）：
{{
    "hot_topics": ["translated1", "translated2", ...],
    "narrative_direction": "<translated>",
    "initial_posts": [
        {{"content": "translated", "poster_type": "translated（translated）"}},
        ...
    ],
    "reasoning": "<translated>"
}}"""

        system_prompt = "translated。translatedJSONtranslated。translated poster_type translated。"
        
        try:
            return self._call_llm_with_retry(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"translatedLLMtranslated: {e}, translated")
            return {
                "hot_topics": [],
                "narrative_direction": "",
                "initial_posts": [],
                "reasoning": "translated"
            }
    
    def _parse_event_config(self, result: Dict[str, Any]) -> EventConfig:
        """translated"""
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
        translated Agent
        
        translated poster_type translated agent_id
        """
        if not event_config.initial_posts:
            return event_config
        
        # translated agent translated
        agents_by_type: Dict[str, List[AgentActivityConfig]] = {}
        for agent in agent_configs:
            etype = agent.entity_type.lower()
            if etype not in agents_by_type:
                agents_by_type[etype] = []
            agents_by_type[etype].append(agent)
        
        # translated（translated LLM translated）
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
        
        # translated agent translated，translated agent
        used_indices: Dict[str, int] = {}
        
        updated_posts = []
        for post in event_config.initial_posts:
            poster_type = post.get("poster_type", "").lower()
            content = post.get("content", "")
            
            # translated agent
            matched_agent_id = None
            
            # 1. translated
            if poster_type in agents_by_type:
                agents = agents_by_type[poster_type]
                idx = used_indices.get(poster_type, 0) % len(agents)
                matched_agent_id = agents[idx].agent_id
                used_indices[poster_type] = idx + 1
            else:
                # 2. translated
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
            
            # 3. translated，translated agent
            if matched_agent_id is None:
                logger.warning(f"translated '{poster_type}' translated Agent，translated Agent")
                if agent_configs:
                    # translated，translated
                    sorted_agents = sorted(agent_configs, key=lambda a: a.influence_weight, reverse=True)
                    matched_agent_id = sorted_agents[0].agent_id
                else:
                    matched_agent_id = 0
            
            updated_posts.append({
                "content": content,
                "poster_type": post.get("poster_type", "Unknown"),
                "poster_agent_id": matched_agent_id
            })
            
            logger.info(f"translated: poster_type='{poster_type}' -> agent_id={matched_agent_id}")
        
        event_config.initial_posts = updated_posts
        return event_config
    
    def _generate_agent_configs_batch(
        self,
        context: str,
        entities: List[EntityNode],
        start_idx: int,
        simulation_requirement: str
    ) -> List[AgentActivityConfig]:
        """translatedAgenttranslated"""
        
        # translated（translated）
        entity_list = []
        summary_len = self.AGENT_SUMMARY_LENGTH
        for i, e in enumerate(entities):
            entity_list.append({
                "agent_id": start_idx + i,
                "entity_name": e.name,
                "entity_type": e.get_entity_type() or "Unknown",
                "summary": e.summary[:summary_len] if e.summary else ""
            })
        
        prompt = f"""translated，translated。

translated: {simulation_requirement}

## translated
```json
{json.dumps(entity_list, ensure_ascii=False, indent=2)}
```

## translated
translated，translated：
- **translated**：translated0-5translated，translated19-22translated
- **translated**（University/GovernmentAgency）：translated(0.1-0.3)，translated(9-17)translated，translated(60-240translated)，translated(2.5-3.0)
- **translated**（MediaOutlet）：translated(0.4-0.6)，translated(8-23)，translated(5-30translated)，translated(2.0-2.5)
- **translated**（Student/Person/Alumni）：translated(0.6-0.9)，translated(18-23)，translated(1-15translated)，translated(0.8-1.2)
- **translated/translated**：translated(0.4-0.6)，translated(1.5-2.0)

translatedJSONtranslated（translatedmarkdown）：
{{
    "agent_configs": [
        {{
            "agent_id": <translated>,
            "activity_level": <0.0-1.0>,
            "posts_per_hour": <translated>,
            "comments_per_hour": <translated>,
            "active_hours": [<translated，translated>],
            "response_delay_min": <translated>,
            "response_delay_max": <translated>,
            "sentiment_bias": <-1.0translated1.0>,
            "stance": "<supportive/opposing/neutral/observer>",
            "influence_weight": <translated>
        }},
        ...
    ]
}}"""

        system_prompt = "translated。translatedJSON，translated。"
        
        try:
            result = self._call_llm_with_retry(prompt, system_prompt)
            llm_configs = {cfg["agent_id"]: cfg for cfg in result.get("agent_configs", [])}
        except Exception as e:
            logger.warning(f"AgenttranslatedLLMtranslated: {e}, translated")
            llm_configs = {}
        
        # translatedAgentActivityConfigtranslated
        configs = []
        for i, entity in enumerate(entities):
            agent_id = start_idx + i
            cfg = llm_configs.get(agent_id, {})
            
            # translatedLLMtranslated，translated
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
        """translatedAgenttranslated（translated）"""
        entity_type = (entity.get_entity_type() or "Unknown").lower()
        
        if entity_type in ["university", "governmentagency", "ngo"]:
            # translated：translated，translated，translated
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
            # translated：translated，translated，translated
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
            # translated/translated：translated+translated，translated
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
            # translated：translated，translated
            return {
                "activity_level": 0.8,
                "posts_per_hour": 0.6,
                "comments_per_hour": 1.5,
                "active_hours": [8, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],  # translated+translated
                "response_delay_min": 1,
                "response_delay_max": 15,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 0.8
            }
        elif entity_type in ["alumni"]:
            # translated：translated
            return {
                "activity_level": 0.6,
                "posts_per_hour": 0.4,
                "comments_per_hour": 0.8,
                "active_hours": [12, 13, 19, 20, 21, 22, 23],  # translated+translated
                "response_delay_min": 5,
                "response_delay_max": 30,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
        else:
            # translated：translated
            return {
                "activity_level": 0.7,
                "posts_per_hour": 0.5,
                "comments_per_hour": 1.2,
                "active_hours": [9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 23],  # translated+translated
                "response_delay_min": 2,
                "response_delay_max": 20,
                "sentiment_bias": 0.0,
                "stance": "neutral",
                "influence_weight": 1.0
            }
    

