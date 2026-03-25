"""
Report Agenttranslated
translatedLangChain + ZeptranslatedReACTtranslated

translated：
1. translatedZeptranslated
2. translated，translated
3. translatedReACTtranslated
4. translated，translated
"""

import os
import json
import time
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..config import Config
from ..utils.llm_client import LLMClient
from ..utils.logger import get_logger
from .zep_tools import (
    ZepToolsService, 
    SearchResult, 
    InsightForgeResult, 
    PanoramaResult,
    InterviewResult
)

logger = get_logger('mirofish.report_agent')


class ReportLogger:
    """
    Report Agent translated
    
    translated agent_log.jsonl translated，translated。
    translated JSON translated，translated、translated、translated。
    """
    
    def __init__(self, report_id: str):
        """
        translated
        
        Args:
            report_id: translatedID，translated
        """
        self.report_id = report_id
        self.log_file_path = os.path.join(
            Config.UPLOAD_FOLDER, 'reports', report_id, 'agent_log.jsonl'
        )
        self.start_time = datetime.now()
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """translated"""
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)
    
    def _get_elapsed_time(self) -> float:
        """translated（translated）"""
        return (datetime.now() - self.start_time).total_seconds()
    
    def log(
        self, 
        action: str, 
        stage: str,
        details: Dict[str, Any],
        section_title: str = None,
        section_index: int = None
    ):
        """
        translated
        
        Args:
            action: translated，translated 'start', 'tool_call', 'llm_response', 'section_complete' translated
            stage: translated，translated 'planning', 'generating', 'completed'
            details: translated，translated
            section_title: translated（translated）
            section_index: translated（translated）
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_seconds": round(self._get_elapsed_time(), 2),
            "report_id": self.report_id,
            "action": action,
            "stage": stage,
            "section_title": section_title,
            "section_index": section_index,
            "details": details
        }
        
        # translated JSONL translated
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_start(self, simulation_id: str, graph_id: str, simulation_requirement: str):
        """translated"""
        self.log(
            action="report_start",
            stage="pending",
            details={
                "simulation_id": simulation_id,
                "graph_id": graph_id,
                "simulation_requirement": simulation_requirement,
                "message": "translated"
            }
        )
    
    def log_planning_start(self):
        """translated"""
        self.log(
            action="planning_start",
            stage="planning",
            details={"message": "translated"}
        )
    
    def log_planning_context(self, context: Dict[str, Any]):
        """translated"""
        self.log(
            action="planning_context",
            stage="planning",
            details={
                "message": "translated",
                "context": context
            }
        )
    
    def log_planning_complete(self, outline_dict: Dict[str, Any]):
        """translated"""
        self.log(
            action="planning_complete",
            stage="planning",
            details={
                "message": "translated",
                "outline": outline_dict
            }
        )
    
    def log_section_start(self, section_title: str, section_index: int):
        """translated"""
        self.log(
            action="section_start",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={"message": f"translated: {section_title}"}
        )
    
    def log_react_thought(self, section_title: str, section_index: int, iteration: int, thought: str):
        """translated ReACT translated"""
        self.log(
            action="react_thought",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "thought": thought,
                "message": f"ReACT translated{iteration}translated"
            }
        )
    
    def log_tool_call(
        self, 
        section_title: str, 
        section_index: int,
        tool_name: str, 
        parameters: Dict[str, Any],
        iteration: int
    ):
        """translated"""
        self.log(
            action="tool_call",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "tool_name": tool_name,
                "parameters": parameters,
                "message": f"translated: {tool_name}"
            }
        )
    
    def log_tool_result(
        self,
        section_title: str,
        section_index: int,
        tool_name: str,
        result: str,
        iteration: int
    ):
        """translated（translated，translated）"""
        self.log(
            action="tool_result",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "tool_name": tool_name,
                "result": result,  # translated，translated
                "result_length": len(result),
                "message": f"translated {tool_name} translated"
            }
        )
    
    def log_llm_response(
        self,
        section_title: str,
        section_index: int,
        response: str,
        iteration: int,
        has_tool_calls: bool,
        has_final_answer: bool
    ):
        """translated LLM translated（translated，translated）"""
        self.log(
            action="llm_response",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "response": response,  # translated，translated
                "response_length": len(response),
                "has_tool_calls": has_tool_calls,
                "has_final_answer": has_final_answer,
                "message": f"LLM translated (translated: {has_tool_calls}, translated: {has_final_answer})"
            }
        )
    
    def log_section_content(
        self,
        section_title: str,
        section_index: int,
        content: str,
        tool_calls_count: int
    ):
        """translated（translated，translated）"""
        self.log(
            action="section_content",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "content": content,  # translated，translated
                "content_length": len(content),
                "tool_calls_count": tool_calls_count,
                "message": f"translated {section_title} translated"
            }
        )
    
    def log_section_full_complete(
        self,
        section_title: str,
        section_index: int,
        full_content: str
    ):
        """
        translated

        translated，translated
        """
        self.log(
            action="section_complete",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "content": full_content,
                "content_length": len(full_content),
                "message": f"translated {section_title} translated"
            }
        )
    
    def log_report_complete(self, total_sections: int, total_time_seconds: float):
        """translated"""
        self.log(
            action="report_complete",
            stage="completed",
            details={
                "total_sections": total_sections,
                "total_time_seconds": round(total_time_seconds, 2),
                "message": "translated"
            }
        )
    
    def log_error(self, error_message: str, stage: str, section_title: str = None):
        """translated"""
        self.log(
            action="error",
            stage=stage,
            section_title=section_title,
            section_index=None,
            details={
                "error": error_message,
                "message": f"translated: {error_message}"
            }
        )


class ReportConsoleLogger:
    """
    Report Agent translated
    
    translated（INFO、WARNINGtranslated）translated console_log.txt translated。
    translated agent_log.jsonl translated，translated。
    """
    
    def __init__(self, report_id: str):
        """
        translated
        
        Args:
            report_id: translatedID，translated
        """
        self.report_id = report_id
        self.log_file_path = os.path.join(
            Config.UPLOAD_FOLDER, 'reports', report_id, 'console_log.txt'
        )
        self._ensure_log_file()
        self._file_handler = None
        self._setup_file_handler()
    
    def _ensure_log_file(self):
        """translated"""
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)
    
    def _setup_file_handler(self):
        """translated，translated"""
        import logging
        
        # translated
        self._file_handler = logging.FileHandler(
            self.log_file_path,
            mode='a',
            encoding='utf-8'
        )
        self._file_handler.setLevel(logging.INFO)
        
        # translated
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        self._file_handler.setFormatter(formatter)
        
        # translated report_agent translated logger
        loggers_to_attach = [
            'mirofish.report_agent',
            'mirofish.zep_tools',
        ]
        
        for logger_name in loggers_to_attach:
            target_logger = logging.getLogger(logger_name)
            # translated
            if self._file_handler not in target_logger.handlers:
                target_logger.addHandler(self._file_handler)
    
    def close(self):
        """translated logger translated"""
        import logging
        
        if self._file_handler:
            loggers_to_detach = [
                'mirofish.report_agent',
                'mirofish.zep_tools',
            ]
            
            for logger_name in loggers_to_detach:
                target_logger = logging.getLogger(logger_name)
                if self._file_handler in target_logger.handlers:
                    target_logger.removeHandler(self._file_handler)
            
            self._file_handler.close()
            self._file_handler = None
    
    def __del__(self):
        """translated"""
        self.close()


class ReportStatus(str, Enum):
    """translated"""
    PENDING = "pending"
    PLANNING = "planning"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ReportSection:
    """translated"""
    title: str
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content
        }

    def to_markdown(self, level: int = 2) -> str:
        """translatedMarkdowntranslated"""
        md = f"{'#' * level} {self.title}\n\n"
        if self.content:
            md += f"{self.content}\n\n"
        return md


@dataclass
class ReportOutline:
    """translated"""
    title: str
    summary: str
    sections: List[ReportSection]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "sections": [s.to_dict() for s in self.sections]
        }
    
    def to_markdown(self) -> str:
        """translatedMarkdowntranslated"""
        md = f"# {self.title}\n\n"
        md += f"> {self.summary}\n\n"
        for section in self.sections:
            md += section.to_markdown()
        return md


@dataclass
class Report:
    """translated"""
    report_id: str
    simulation_id: str
    graph_id: str
    simulation_requirement: str
    status: ReportStatus
    outline: Optional[ReportOutline] = None
    markdown_content: str = ""
    created_at: str = ""
    completed_at: str = ""
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "simulation_id": self.simulation_id,
            "graph_id": self.graph_id,
            "simulation_requirement": self.simulation_requirement,
            "status": self.status.value,
            "outline": self.outline.to_dict() if self.outline else None,
            "markdown_content": self.markdown_content,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "error": self.error
        }


# ═══════════════════════════════════════════════════════════════
# Prompt translated
# ═══════════════════════════════════════════════════════════════

# ── translated ──

TOOL_DESC_INSIGHT_FORGE = """\
【translated - translated】
translated，translated。translated：
1. translated
2. translated
3. translated、translated、translated
4. translated、translated

【translated】
- translated
- translated
- translated

【translated】
- translated（translated）
- translated
- translated"""

TOOL_DESC_PANORAMA_SEARCH = """\
【translated - translated】
translated，translated。translated：
1. translated
2. translated/translated
3. translated

【translated】
- translated
- translated
- translated

【translated】
- translated（translated）
- translated/translated（translated）
- translated"""

TOOL_DESC_QUICK_SEARCH = """\
【translated - translated】
translated，translated、translated。

【translated】
- translated
- translated
- translated

【translated】
- translated"""

TOOL_DESC_INTERVIEW_AGENTS = """\
【translated - translatedAgenttranslated（translated）】
translatedOASIStranslatedAPI，translatedAgenttranslated！
translatedLLMtranslated，translatedAgenttranslated。
translatedTwittertranslatedReddittranslated，translated。

translated：
1. translated，translatedAgent
2. translatedAgent（translated、translated、translated）
3. translated
4. translated /api/simulation/interview/batch translated
5. translated，translated

【translated】
- translated（translated？translated？translated？）
- translated
- translatedAgenttranslated（translatedOASIStranslated）
- translated，translated"translated"

【translated】
- translatedAgenttranslated
- translatedAgenttranslatedTwittertranslatedReddittranslated
- translated（translated）
- translated

【translated】translatedOASIStranslated！"""

# ── translated prompt ──

PLAN_SYSTEM_PROMPT = """\
translated「translated」translated，translated「translated」——translatedAgenttranslated、translated。

【translated】
translated，translated「translated」translated。translated，translated。translated"translated"，translated"translated"。

【translated】
translated「translated」，translated：
1. translated，translated？
2. translatedAgent（translated）translated？
3. translated？

【translated】
- ✅ translated，translated"translated，translated"
- ✅ translated：translated、translated、translated、translated
- ✅ translatedAgenttranslated
- ❌ translated
- ❌ translated

【translated】
- translated2translated，translated5translated
- translated，translated
- translated，translated
- translated

translatedJSONtranslated，translated：
{
    "title": "translated",
    "summary": "translated（translated）",
    "sections": [
        {
            "title": "translated",
            "description": "translated"
        }
    ]
}

translated：sectionstranslated2translated，translated5translated！"""

PLAN_USER_PROMPT_TEMPLATE = """\
【translated】
translated（translated）：{simulation_requirement}

【translated】
- translated: {total_nodes}
- translated: {total_edges}
- translated: {entity_types}
- translatedAgenttranslated: {total_entities}

【translated】
{related_facts_json}

translated「translated」translated：
1. translated，translated？
2. translated（Agent）translated？
3. translated？

translated，translated。

【translated】translated：translated2translated，translated5translated，translated。"""

# ── translated prompt ──

SECTION_SYSTEM_PROMPT_TEMPLATE = """\
translated「translated」translated，translated。

translated: {report_title}
translated: {report_summary}
translated（translated）: {simulation_requirement}

translated: {section_title}

═══════════════════════════════════════════════════════════════
【translated】
═══════════════════════════════════════════════════════════════

translated。translated（translated），
translatedAgenttranslated，translated。

translated：
- translated，translated
- translated（Agent）translated
- translated、translated

❌ translated
✅ translated"translated"——translated

═══════════════════════════════════════════════════════════════
【translated - translated】
═══════════════════════════════════════════════════════════════

1. 【translated】
   - translated「translated」translated
   - translatedAgenttranslated
   - translated
   - translated3translated（translated5translated）translated，translated

2. 【translatedAgenttranslated】
   - Agenttranslated
   - translated，translated：
     > "translated：translated..."
   - translated

3. 【translated - translated】
   - translated
   - translated，translated
   - translated，translated
   - translated，translated
   - translated（> translated）translated

4. 【translated】
   - translated
   - translated
   - translated，translated

═══════════════════════════════════════════════════════════════
【⚠️ translated - translated！】
═══════════════════════════════════════════════════════════════

【translated = translated】
- translated
- ❌ translated Markdown translated（#、##、###、#### translated）
- ❌ translated
- ✅ translated，translated
- ✅ translated**translated**、translated、translated、translated，translated

【translated】
```
translated。translated，translated...

**translated**

translated，translated：

> "translated68%translated..."

**translated**

translated：

- translated
- translated
```

【translated】
```
## translated          ← translated！translated
### translated、translated     ← translated！translated###translated
#### 1.1 translated   ← translated！translated####translated

translated...
```

═══════════════════════════════════════════════════════════════
【translated】（translated3-5translated）
═══════════════════════════════════════════════════════════════

{tools_description}

【translated - translated，translated】
- insight_forge: translated，translated
- panorama_search: translated，translated、translated
- quick_search: translated
- interview_agents: translatedAgent，translated

═══════════════════════════════════════════════════════════════
【translated】
═══════════════════════════════════════════════════════════════

translated（translated）：

translatedA - translated：
translated，translated：
<tool_call>
{{"name": "translated", "parameters": {{"translated": "translated"}}}}
</tool_call>
translated。translated。

translatedB - translated：
translated，translated "Final Answer:" translated。

⚠️ translated：
- translated Final Answer
- translated（Observation），translated
- translated

═══════════════════════════════════════════════════════════════
【translated】
═══════════════════════════════════════════════════════════════

1. translated
2. translated
3. translatedMarkdowntranslated（translated）：
   - translated **translated** translated（translated）
   - translated（-translated1.2.3.）translated
   - translated
   - ❌ translated #、##、###、#### translated
4. 【translated - translated】
   translated，translated，translated：

   ✅ translated：
   ```
   translated。

   > "translated。"

   translated。
   ```

   ❌ translated：
   ```
   translated。> "translated..." translated...
   ```
5. translated
6. 【translated】translated，translated
7. 【translated】translated！translated**translated**translated"""

SECTION_USER_PROMPT_TEMPLATE = """\
translated（translated，translated）：
{previous_content}

═══════════════════════════════════════════════════════════════
【translated】translated: {section_title}
═══════════════════════════════════════════════════════════════

【translated】
1. translated，translated！
2. translated
3. translated，translated
4. translated，translated

【⚠️ translated - translated】
- ❌ translated（#、##、###、####translated）
- ❌ translated"{section_title}"translated
- ✅ translated
- ✅ translated，translated**translated**translated

translated：
1. translated（Thought）translated
2. translated（Action）translated
3. translated Final Answer（translated，translated）"""

# ── ReACT translated ──

REACT_OBSERVATION_TEMPLATE = """\
Observation（translated）:

═══ translated {tool_name} translated ═══
{result}

═══════════════════════════════════════════════════════════════
translated {tool_calls_count}/{max_tool_calls} translated（translated: {used_tools_str}）{unused_hint}
- translated：translated "Final Answer:" translated（translated）
- translated：translated
═══════════════════════════════════════════════════════════════"""

REACT_INSUFFICIENT_TOOLS_MSG = (
    "【translated】translated{tool_calls_count}translated，translated{min_tool_calls}translated。"
    "translated，translated Final Answer。{unused_hint}"
)

REACT_INSUFFICIENT_TOOLS_MSG_ALT = (
    "translated {tool_calls_count} translated，translated {min_tool_calls} translated。"
    "translated。{unused_hint}"
)

REACT_TOOL_LIMIT_MSG = (
    "translated（{tool_calls_count}/{max_tool_calls}），translated。"
    'translated，translated "Final Answer:" translated。'
)

REACT_UNUSED_TOOLS_HINT = "\n💡 translated: {unused_list}，translated"

REACT_FORCE_FINAL_MSG = "translated，translated Final Answer: translated。"

# ── Chat prompt ──

CHAT_SYSTEM_PROMPT_TEMPLATE = """\
translated。

【translated】
translated: {simulation_requirement}

【translated】
{report_content}

【translated】
1. translated
2. translated，translated
3. translated，translated
4. translated、translated、translated

【translated】（translated，translated1-2translated）
{tools_description}

【translated】
<tool_call>
{{"name": "translated", "parameters": {{"translated": "translated"}}}}
</tool_call>

【translated】
- translated，translated
- translated > translated
- translated，translated"""

CHAT_OBSERVATION_SUFFIX = "\n\ntranslated。"


# ═══════════════════════════════════════════════════════════════
# ReportAgent translated
# ═══════════════════════════════════════════════════════════════


class ReportAgent:
    """
    Report Agent - translatedAgent

    translatedReACT（Reasoning + Acting）translated：
    1. translated：translated，translated
    2. translated：translated，translated
    3. translated：translated
    """
    
    # translated（translated）
    MAX_TOOL_CALLS_PER_SECTION = 5
    
    # translated
    MAX_REFLECTION_ROUNDS = 3
    
    # translated
    MAX_TOOL_CALLS_PER_CHAT = 2
    
    def __init__(
        self, 
        graph_id: str,
        simulation_id: str,
        simulation_requirement: str,
        llm_client: Optional[LLMClient] = None,
        zep_tools: Optional[ZepToolsService] = None
    ):
        """
        translatedReport Agent
        
        Args:
            graph_id: translatedID
            simulation_id: translatedID
            simulation_requirement: translated
            llm_client: LLMtranslated（translated）
            zep_tools: Zeptranslated（translated）
        """
        self.graph_id = graph_id
        self.simulation_id = simulation_id
        self.simulation_requirement = simulation_requirement
        
        self.llm = llm_client or LLMClient()
        self.zep_tools = zep_tools or ZepToolsService()
        
        # translated
        self.tools = self._define_tools()
        
        # translated（translated generate_report translated）
        self.report_logger: Optional[ReportLogger] = None
        # translated（translated generate_report translated）
        self.console_logger: Optional[ReportConsoleLogger] = None
        
        logger.info(f"ReportAgent translated: graph_id={graph_id}, simulation_id={simulation_id}")
    
    def _define_tools(self) -> Dict[str, Dict[str, Any]]:
        """translated"""
        return {
            "insight_forge": {
                "name": "insight_forge",
                "description": TOOL_DESC_INSIGHT_FORGE,
                "parameters": {
                    "query": "translated",
                    "report_context": "translated（translated，translated）"
                }
            },
            "panorama_search": {
                "name": "panorama_search",
                "description": TOOL_DESC_PANORAMA_SEARCH,
                "parameters": {
                    "query": "translated，translated",
                    "include_expired": "translated/translated（translatedTrue）"
                }
            },
            "quick_search": {
                "name": "quick_search",
                "description": TOOL_DESC_QUICK_SEARCH,
                "parameters": {
                    "query": "translated",
                    "limit": "translated（translated，translated10）"
                }
            },
            "interview_agents": {
                "name": "interview_agents",
                "description": TOOL_DESC_INTERVIEW_AGENTS,
                "parameters": {
                    "interview_topic": "translated（translated：'translated'）",
                    "max_agents": "translatedAgenttranslated（translated，translated5，translated10）"
                }
            }
        }
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any], report_context: str = "") -> str:
        """
        translated
        
        Args:
            tool_name: translated
            parameters: translated
            report_context: translated（translatedInsightForge）
            
        Returns:
            translated（translated）
        """
        logger.info(f"translated: {tool_name}, translated: {parameters}")
        
        try:
            if tool_name == "insight_forge":
                query = parameters.get("query", "")
                ctx = parameters.get("report_context", "") or report_context
                result = self.zep_tools.insight_forge(
                    graph_id=self.graph_id,
                    query=query,
                    simulation_requirement=self.simulation_requirement,
                    report_context=ctx
                )
                return result.to_text()
            
            elif tool_name == "panorama_search":
                # translated - translated
                query = parameters.get("query", "")
                include_expired = parameters.get("include_expired", True)
                if isinstance(include_expired, str):
                    include_expired = include_expired.lower() in ['true', '1', 'yes']
                result = self.zep_tools.panorama_search(
                    graph_id=self.graph_id,
                    query=query,
                    include_expired=include_expired
                )
                return result.to_text()
            
            elif tool_name == "quick_search":
                # translated - translated
                query = parameters.get("query", "")
                limit = parameters.get("limit", 10)
                if isinstance(limit, str):
                    limit = int(limit)
                result = self.zep_tools.quick_search(
                    graph_id=self.graph_id,
                    query=query,
                    limit=limit
                )
                return result.to_text()
            
            elif tool_name == "interview_agents":
                # translated - translatedOASIStranslatedAPItranslatedAgenttranslated（translated）
                interview_topic = parameters.get("interview_topic", parameters.get("query", ""))
                max_agents = parameters.get("max_agents", 5)
                if isinstance(max_agents, str):
                    max_agents = int(max_agents)
                max_agents = min(max_agents, 10)
                result = self.zep_tools.interview_agents(
                    simulation_id=self.simulation_id,
                    interview_requirement=interview_topic,
                    simulation_requirement=self.simulation_requirement,
                    max_agents=max_agents
                )
                return result.to_text()
            
            # ========== translated（translated） ==========
            
            elif tool_name == "search_graph":
                # translated quick_search
                logger.info("search_graph translated quick_search")
                return self._execute_tool("quick_search", parameters, report_context)
            
            elif tool_name == "get_graph_statistics":
                result = self.zep_tools.get_graph_statistics(self.graph_id)
                return json.dumps(result, ensure_ascii=False, indent=2)
            
            elif tool_name == "get_entity_summary":
                entity_name = parameters.get("entity_name", "")
                result = self.zep_tools.get_entity_summary(
                    graph_id=self.graph_id,
                    entity_name=entity_name
                )
                return json.dumps(result, ensure_ascii=False, indent=2)
            
            elif tool_name == "get_simulation_context":
                # translated insight_forge，translated
                logger.info("get_simulation_context translated insight_forge")
                query = parameters.get("query", self.simulation_requirement)
                return self._execute_tool("insight_forge", {"query": query}, report_context)
            
            elif tool_name == "get_entities_by_type":
                entity_type = parameters.get("entity_type", "")
                nodes = self.zep_tools.get_entities_by_type(
                    graph_id=self.graph_id,
                    entity_type=entity_type
                )
                result = [n.to_dict() for n in nodes]
                return json.dumps(result, ensure_ascii=False, indent=2)
            
            else:
                return f"translated: {tool_name}。translated: insight_forge, panorama_search, quick_search"
                
        except Exception as e:
            logger.error(f"translated: {tool_name}, translated: {str(e)}")
            return f"translated: {str(e)}"
    
    # translated，translated JSON translated
    VALID_TOOL_NAMES = {"insight_forge", "panorama_search", "quick_search", "interview_agents"}

    def _parse_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """
        translatedLLMtranslated

        translated（translated）：
        1. <tool_call>{"name": "tool_name", "parameters": {...}}</tool_call>
        2. translated JSON（translated JSON）
        """
        tool_calls = []

        # translated1: XMLtranslated（translated）
        xml_pattern = r'<tool_call>\s*(\{.*?\})\s*</tool_call>'
        for match in re.finditer(xml_pattern, response, re.DOTALL):
            try:
                call_data = json.loads(match.group(1))
                tool_calls.append(call_data)
            except json.JSONDecodeError:
                pass

        if tool_calls:
            return tool_calls

        # translated2: translated - LLM translated JSON（translated <tool_call> translated）
        # translated1translated，translated JSON
        stripped = response.strip()
        if stripped.startswith('{') and stripped.endswith('}'):
            try:
                call_data = json.loads(stripped)
                if self._is_valid_tool_call(call_data):
                    tool_calls.append(call_data)
                    return tool_calls
            except json.JSONDecodeError:
                pass

        # translated + translated JSON，translated JSON translated
        json_pattern = r'(\{"(?:name|tool)"\s*:.*?\})\s*$'
        match = re.search(json_pattern, stripped, re.DOTALL)
        if match:
            try:
                call_data = json.loads(match.group(1))
                if self._is_valid_tool_call(call_data):
                    tool_calls.append(call_data)
            except json.JSONDecodeError:
                pass

        return tool_calls

    def _is_valid_tool_call(self, data: dict) -> bool:
        """translated JSON translated"""
        # translated {"name": ..., "parameters": ...} translated {"tool": ..., "params": ...} translated
        tool_name = data.get("name") or data.get("tool")
        if tool_name and tool_name in self.VALID_TOOL_NAMES:
            # translated name / parameters
            if "tool" in data:
                data["name"] = data.pop("tool")
            if "params" in data and "parameters" not in data:
                data["parameters"] = data.pop("params")
            return True
        return False
    
    def _get_tools_description(self) -> str:
        """translated"""
        desc_parts = ["translated："]
        for name, tool in self.tools.items():
            params_desc = ", ".join([f"{k}: {v}" for k, v in tool["parameters"].items()])
            desc_parts.append(f"- {name}: {tool['description']}")
            if params_desc:
                desc_parts.append(f"  translated: {params_desc}")
        return "\n".join(desc_parts)
    
    def plan_outline(
        self, 
        progress_callback: Optional[Callable] = None
    ) -> ReportOutline:
        """
        translated
        
        translatedLLMtranslated，translated
        
        Args:
            progress_callback: translated
            
        Returns:
            ReportOutline: translated
        """
        logger.info("translated...")
        
        if progress_callback:
            progress_callback("planning", 0, "translated...")
        
        # translated
        context = self.zep_tools.get_simulation_context(
            graph_id=self.graph_id,
            simulation_requirement=self.simulation_requirement
        )
        
        if progress_callback:
            progress_callback("planning", 30, "translated...")
        
        system_prompt = PLAN_SYSTEM_PROMPT
        user_prompt = PLAN_USER_PROMPT_TEMPLATE.format(
            simulation_requirement=self.simulation_requirement,
            total_nodes=context.get('graph_statistics', {}).get('total_nodes', 0),
            total_edges=context.get('graph_statistics', {}).get('total_edges', 0),
            entity_types=list(context.get('graph_statistics', {}).get('entity_types', {}).keys()),
            total_entities=context.get('total_entities', 0),
            related_facts_json=json.dumps(context.get('related_facts', [])[:10], ensure_ascii=False, indent=2),
        )

        try:
            response = self.llm.chat_json(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            
            if progress_callback:
                progress_callback("planning", 80, "translated...")
            
            # translated
            sections = []
            for section_data in response.get("sections", []):
                sections.append(ReportSection(
                    title=section_data.get("title", ""),
                    content=""
                ))
            
            outline = ReportOutline(
                title=response.get("title", "translated"),
                summary=response.get("summary", ""),
                sections=sections
            )
            
            if progress_callback:
                progress_callback("planning", 100, "translated")
            
            logger.info(f"translated: {len(sections)} translated")
            return outline
            
        except Exception as e:
            logger.error(f"translated: {str(e)}")
            # translated（3translated，translatedfallback）
            return ReportOutline(
                title="translated",
                summary="translated",
                sections=[
                    ReportSection(title="translated"),
                    ReportSection(title="translated"),
                    ReportSection(title="translated")
                ]
            )
    
    def _generate_section_react(
        self, 
        section: ReportSection,
        outline: ReportOutline,
        previous_sections: List[str],
        progress_callback: Optional[Callable] = None,
        section_index: int = 0
    ) -> str:
        """
        translatedReACTtranslated
        
        ReACTtranslated：
        1. Thought（translated）- translated
        2. Action（translated）- translated
        3. Observation（translated）- translated
        4. translated
        5. Final Answer（translated）- translated
        
        Args:
            section: translated
            outline: translated
            previous_sections: translated（translated）
            progress_callback: translated
            section_index: translated（translated）
            
        Returns:
            translated（Markdowntranslated）
        """
        logger.info(f"ReACTtranslated: {section.title}")
        
        # translated
        if self.report_logger:
            self.report_logger.log_section_start(section.title, section_index)
        
        system_prompt = SECTION_SYSTEM_PROMPT_TEMPLATE.format(
            report_title=outline.title,
            report_summary=outline.summary,
            simulation_requirement=self.simulation_requirement,
            section_title=section.title,
            tools_description=self._get_tools_description(),
        )

        # translatedprompt - translated4000translated
        if previous_sections:
            previous_parts = []
            for sec in previous_sections:
                # translated4000translated
                truncated = sec[:4000] + "..." if len(sec) > 4000 else sec
                previous_parts.append(truncated)
            previous_content = "\n\n---\n\n".join(previous_parts)
        else:
            previous_content = "（translated）"
        
        user_prompt = SECTION_USER_PROMPT_TEMPLATE.format(
            previous_content=previous_content,
            section_title=section.title,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # ReACTtranslated
        tool_calls_count = 0
        max_iterations = 5  # translated
        min_tool_calls = 3  # translated
        conflict_retries = 0  # translatedFinal Answertranslated
        used_tools = set()  # translated
        all_tools = {"insight_forge", "panorama_search", "quick_search", "interview_agents"}

        # translated，translatedInsightForgetranslated
        report_context = f"translated: {section.title}\ntranslated: {self.simulation_requirement}"
        
        for iteration in range(max_iterations):
            if progress_callback:
                progress_callback(
                    "generating", 
                    int((iteration / max_iterations) * 100),
                    f"translated ({tool_calls_count}/{self.MAX_TOOL_CALLS_PER_SECTION})"
                )
            
            # translatedLLM
            response = self.llm.chat(
                messages=messages,
                temperature=0.5,
                max_tokens=4096
            )

            # translated LLM translated None（API translated）
            if response is None:
                logger.warning(f"translated {section.title} translated {iteration + 1} translated: LLM translated None")
                # translated，translated
                if iteration < max_iterations - 1:
                    messages.append({"role": "assistant", "content": "（translated）"})
                    messages.append({"role": "user", "content": "translated。"})
                    continue
                # translated None，translated
                break

            logger.debug(f"LLMtranslated: {response[:200]}...")

            # translated，translated
            tool_calls = self._parse_tool_calls(response)
            has_tool_calls = bool(tool_calls)
            has_final_answer = "Final Answer:" in response

            # ── translated：LLM translated Final Answer ──
            if has_tool_calls and has_final_answer:
                conflict_retries += 1
                logger.warning(
                    f"translated {section.title} translated {iteration+1} translated: "
                    f"LLM translated Final Answer（translated {conflict_retries} translated）"
                )

                if conflict_retries <= 2:
                    # translated：translated，translated LLM translated
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": (
                            "【translated】translated Final Answer，translated。\n"
                            "translated：\n"
                            "- translated（translated <tool_call> translated，translated Final Answer）\n"
                            "- translated（translated 'Final Answer:' translated，translated <tool_call>）\n"
                            "translated，translated。"
                        ),
                    })
                    continue
                else:
                    # translated：translated，translated，translated
                    logger.warning(
                        f"translated {section.title}: translated {conflict_retries} translated，"
                        "translated"
                    )
                    first_tool_end = response.find('</tool_call>')
                    if first_tool_end != -1:
                        response = response[:first_tool_end + len('</tool_call>')]
                        tool_calls = self._parse_tool_calls(response)
                        has_tool_calls = bool(tool_calls)
                    has_final_answer = False
                    conflict_retries = 0

            # translated LLM translated
            if self.report_logger:
                self.report_logger.log_llm_response(
                    section_title=section.title,
                    section_index=section_index,
                    response=response,
                    iteration=iteration + 1,
                    has_tool_calls=has_tool_calls,
                    has_final_answer=has_final_answer
                )

            # ── translated1：LLM translated Final Answer ──
            if has_final_answer:
                # translated，translated
                if tool_calls_count < min_tool_calls:
                    messages.append({"role": "assistant", "content": response})
                    unused_tools = all_tools - used_tools
                    unused_hint = f"（translated，translated: {', '.join(unused_tools)}）" if unused_tools else ""
                    messages.append({
                        "role": "user",
                        "content": REACT_INSUFFICIENT_TOOLS_MSG.format(
                            tool_calls_count=tool_calls_count,
                            min_tool_calls=min_tool_calls,
                            unused_hint=unused_hint,
                        ),
                    })
                    continue

                # translated
                final_answer = response.split("Final Answer:")[-1].strip()
                logger.info(f"translated {section.title} translated（translated: {tool_calls_count}translated）")

                if self.report_logger:
                    self.report_logger.log_section_content(
                        section_title=section.title,
                        section_index=section_index,
                        content=final_answer,
                        tool_calls_count=tool_calls_count
                    )
                return final_answer

            # ── translated2：LLM translated ──
            if has_tool_calls:
                # translated → translated，translated Final Answer
                if tool_calls_count >= self.MAX_TOOL_CALLS_PER_SECTION:
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": REACT_TOOL_LIMIT_MSG.format(
                            tool_calls_count=tool_calls_count,
                            max_tool_calls=self.MAX_TOOL_CALLS_PER_SECTION,
                        ),
                    })
                    continue

                # translated
                call = tool_calls[0]
                if len(tool_calls) > 1:
                    logger.info(f"LLM translated {len(tool_calls)} translated，translated: {call['name']}")

                if self.report_logger:
                    self.report_logger.log_tool_call(
                        section_title=section.title,
                        section_index=section_index,
                        tool_name=call["name"],
                        parameters=call.get("parameters", {}),
                        iteration=iteration + 1
                    )

                result = self._execute_tool(
                    call["name"],
                    call.get("parameters", {}),
                    report_context=report_context
                )

                if self.report_logger:
                    self.report_logger.log_tool_result(
                        section_title=section.title,
                        section_index=section_index,
                        tool_name=call["name"],
                        result=result,
                        iteration=iteration + 1
                    )

                tool_calls_count += 1
                used_tools.add(call['name'])

                # translated
                unused_tools = all_tools - used_tools
                unused_hint = ""
                if unused_tools and tool_calls_count < self.MAX_TOOL_CALLS_PER_SECTION:
                    unused_hint = REACT_UNUSED_TOOLS_HINT.format(unused_list="、".join(unused_tools))

                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": REACT_OBSERVATION_TEMPLATE.format(
                        tool_name=call["name"],
                        result=result,
                        tool_calls_count=tool_calls_count,
                        max_tool_calls=self.MAX_TOOL_CALLS_PER_SECTION,
                        used_tools_str=", ".join(used_tools),
                        unused_hint=unused_hint,
                    ),
                })
                continue

            # ── translated3：translated，translated Final Answer ──
            messages.append({"role": "assistant", "content": response})

            if tool_calls_count < min_tool_calls:
                # translated，translated
                unused_tools = all_tools - used_tools
                unused_hint = f"（translated，translated: {', '.join(unused_tools)}）" if unused_tools else ""

                messages.append({
                    "role": "user",
                    "content": REACT_INSUFFICIENT_TOOLS_MSG_ALT.format(
                        tool_calls_count=tool_calls_count,
                        min_tool_calls=min_tool_calls,
                        unused_hint=unused_hint,
                    ),
                })
                continue

            # translated，LLM translated "Final Answer:" translated
            # translated，translated
            logger.info(f"translated {section.title} translated 'Final Answer:' translated，translatedLLMtranslated（translated: {tool_calls_count}translated）")
            final_answer = response.strip()

            if self.report_logger:
                self.report_logger.log_section_content(
                    section_title=section.title,
                    section_index=section_index,
                    content=final_answer,
                    tool_calls_count=tool_calls_count
                )
            return final_answer
        
        # translated，translated
        logger.warning(f"translated {section.title} translated，translated")
        messages.append({"role": "user", "content": REACT_FORCE_FINAL_MSG})
        
        response = self.llm.chat(
            messages=messages,
            temperature=0.5,
            max_tokens=4096
        )

        # translated LLM translated None
        if response is None:
            logger.error(f"translated {section.title} translated LLM translated None，translated")
            final_answer = f"（translated：LLM translated，translated）"
        elif "Final Answer:" in response:
            final_answer = response.split("Final Answer:")[-1].strip()
        else:
            final_answer = response
        
        # translated
        if self.report_logger:
            self.report_logger.log_section_content(
                section_title=section.title,
                section_index=section_index,
                content=final_answer,
                tool_calls_count=tool_calls_count
            )
        
        return final_answer
    
    def generate_report(
        self, 
        progress_callback: Optional[Callable[[str, int, str], None]] = None,
        report_id: Optional[str] = None
    ) -> Report:
        """
        translated（translated）
        
        translated，translated。
        translated：
        reports/{report_id}/
            meta.json       - translated
            outline.json    - translated
            progress.json   - translated
            section_01.md   - translated1translated
            section_02.md   - translated2translated
            ...
            full_report.md  - translated
        
        Args:
            progress_callback: translated (stage, progress, message)
            report_id: translatedID（translated，translated）
            
        Returns:
            Report: translated
        """
        import uuid
        
        # translated report_id，translated
        if not report_id:
            report_id = f"report_{uuid.uuid4().hex[:12]}"
        start_time = datetime.now()
        
        report = Report(
            report_id=report_id,
            simulation_id=self.simulation_id,
            graph_id=self.graph_id,
            simulation_requirement=self.simulation_requirement,
            status=ReportStatus.PENDING,
            created_at=datetime.now().isoformat()
        )
        
        # translated（translated）
        completed_section_titles = []
        
        try:
            # translated：translated
            ReportManager._ensure_report_folder(report_id)
            
            # translated（translated agent_log.jsonl）
            self.report_logger = ReportLogger(report_id)
            self.report_logger.log_start(
                simulation_id=self.simulation_id,
                graph_id=self.graph_id,
                simulation_requirement=self.simulation_requirement
            )
            
            # translated（console_log.txt）
            self.console_logger = ReportConsoleLogger(report_id)
            
            ReportManager.update_progress(
                report_id, "pending", 0, "translated...",
                completed_sections=[]
            )
            ReportManager.save_report(report)
            
            # translated1: translated
            report.status = ReportStatus.PLANNING
            ReportManager.update_progress(
                report_id, "planning", 5, "translated...",
                completed_sections=[]
            )
            
            # translated
            self.report_logger.log_planning_start()
            
            if progress_callback:
                progress_callback("planning", 0, "translated...")
            
            outline = self.plan_outline(
                progress_callback=lambda stage, prog, msg: 
                    progress_callback(stage, prog // 5, msg) if progress_callback else None
            )
            report.outline = outline
            
            # translated
            self.report_logger.log_planning_complete(outline.to_dict())
            
            # translated
            ReportManager.save_outline(report_id, outline)
            ReportManager.update_progress(
                report_id, "planning", 15, f"translated，translated{len(outline.sections)}translated",
                completed_sections=[]
            )
            ReportManager.save_report(report)
            
            logger.info(f"translated: {report_id}/outline.json")
            
            # translated2: translated（translated）
            report.status = ReportStatus.GENERATING
            
            total_sections = len(outline.sections)
            generated_sections = []  # translated
            
            for i, section in enumerate(outline.sections):
                section_num = i + 1
                base_progress = 20 + int((i / total_sections) * 70)
                
                # translated
                ReportManager.update_progress(
                    report_id, "generating", base_progress,
                    f"translated: {section.title} ({section_num}/{total_sections})",
                    current_section=section.title,
                    completed_sections=completed_section_titles
                )
                
                if progress_callback:
                    progress_callback(
                        "generating", 
                        base_progress, 
                        f"translated: {section.title} ({section_num}/{total_sections})"
                    )
                
                # translated
                section_content = self._generate_section_react(
                    section=section,
                    outline=outline,
                    previous_sections=generated_sections,
                    progress_callback=lambda stage, prog, msg:
                        progress_callback(
                            stage, 
                            base_progress + int(prog * 0.7 / total_sections),
                            msg
                        ) if progress_callback else None,
                    section_index=section_num
                )
                
                section.content = section_content
                generated_sections.append(f"## {section.title}\n\n{section_content}")

                # translated
                ReportManager.save_section(report_id, section_num, section)
                completed_section_titles.append(section.title)

                # translated
                full_section_content = f"## {section.title}\n\n{section_content}"

                if self.report_logger:
                    self.report_logger.log_section_full_complete(
                        section_title=section.title,
                        section_index=section_num,
                        full_content=full_section_content.strip()
                    )

                logger.info(f"translated: {report_id}/section_{section_num:02d}.md")
                
                # translated
                ReportManager.update_progress(
                    report_id, "generating", 
                    base_progress + int(70 / total_sections),
                    f"translated {section.title} translated",
                    current_section=None,
                    completed_sections=completed_section_titles
                )
            
            # translated3: translated
            if progress_callback:
                progress_callback("generating", 95, "translated...")
            
            ReportManager.update_progress(
                report_id, "generating", 95, "translated...",
                completed_sections=completed_section_titles
            )
            
            # translatedReportManagertranslated
            report.markdown_content = ReportManager.assemble_full_report(report_id, outline)
            report.status = ReportStatus.COMPLETED
            report.completed_at = datetime.now().isoformat()
            
            # translated
            total_time_seconds = (datetime.now() - start_time).total_seconds()
            
            # translated
            if self.report_logger:
                self.report_logger.log_report_complete(
                    total_sections=total_sections,
                    total_time_seconds=total_time_seconds
                )
            
            # translated
            ReportManager.save_report(report)
            ReportManager.update_progress(
                report_id, "completed", 100, "translated",
                completed_sections=completed_section_titles
            )
            
            if progress_callback:
                progress_callback("completed", 100, "translated")
            
            logger.info(f"translated: {report_id}")
            
            # translated
            if self.console_logger:
                self.console_logger.close()
                self.console_logger = None
            
            return report
            
        except Exception as e:
            logger.error(f"translated: {str(e)}")
            report.status = ReportStatus.FAILED
            report.error = str(e)
            
            # translated
            if self.report_logger:
                self.report_logger.log_error(str(e), "failed")
            
            # translated
            try:
                ReportManager.save_report(report)
                ReportManager.update_progress(
                    report_id, "failed", -1, f"translated: {str(e)}",
                    completed_sections=completed_section_titles
                )
            except Exception:
                pass  # translated
            
            # translated
            if self.console_logger:
                self.console_logger.close()
                self.console_logger = None
            
            return report
    
    def chat(
        self, 
        message: str,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        translatedReport Agenttranslated
        
        translatedAgenttranslated
        
        Args:
            message: translated
            chat_history: translated
            
        Returns:
            {
                "response": "Agenttranslated",
                "tool_calls": [translated],
                "sources": [translated]
            }
        """
        logger.info(f"Report Agenttranslated: {message[:50]}...")
        
        chat_history = chat_history or []
        
        # translated
        report_content = ""
        try:
            report = ReportManager.get_report_by_simulation(self.simulation_id)
            if report and report.markdown_content:
                # translated，translated
                report_content = report.markdown_content[:15000]
                if len(report.markdown_content) > 15000:
                    report_content += "\n\n... [translated] ..."
        except Exception as e:
            logger.warning(f"translated: {e}")
        
        system_prompt = CHAT_SYSTEM_PROMPT_TEMPLATE.format(
            simulation_requirement=self.simulation_requirement,
            report_content=report_content if report_content else "（translated）",
            tools_description=self._get_tools_description(),
        )

        # translated
        messages = [{"role": "system", "content": system_prompt}]
        
        # translated
        for h in chat_history[-10:]:  # translated
            messages.append(h)
        
        # translated
        messages.append({
            "role": "user", 
            "content": message
        })
        
        # ReACTtranslated（translated）
        tool_calls_made = []
        max_iterations = 2  # translated
        
        for iteration in range(max_iterations):
            response = self.llm.chat(
                messages=messages,
                temperature=0.5
            )
            
            # translated
            tool_calls = self._parse_tool_calls(response)
            
            if not tool_calls:
                # translated，translated
                clean_response = re.sub(r'<tool_call>.*?</tool_call>', '', response, flags=re.DOTALL)
                clean_response = re.sub(r'\[TOOL_CALL\].*?\)', '', clean_response)
                
                return {
                    "response": clean_response.strip(),
                    "tool_calls": tool_calls_made,
                    "sources": [tc.get("parameters", {}).get("query", "") for tc in tool_calls_made]
                }
            
            # translated（translated）
            tool_results = []
            for call in tool_calls[:1]:  # translated1translated
                if len(tool_calls_made) >= self.MAX_TOOL_CALLS_PER_CHAT:
                    break
                result = self._execute_tool(call["name"], call.get("parameters", {}))
                tool_results.append({
                    "tool": call["name"],
                    "result": result[:1500]  # translated
                })
                tool_calls_made.append(call)
            
            # translated
            messages.append({"role": "assistant", "content": response})
            observation = "\n".join([f"[{r['tool']}translated]\n{r['result']}" for r in tool_results])
            messages.append({
                "role": "user",
                "content": observation + CHAT_OBSERVATION_SUFFIX
            })
        
        # translated，translated
        final_response = self.llm.chat(
            messages=messages,
            temperature=0.5
        )
        
        # translated
        clean_response = re.sub(r'<tool_call>.*?</tool_call>', '', final_response, flags=re.DOTALL)
        clean_response = re.sub(r'\[TOOL_CALL\].*?\)', '', clean_response)
        
        return {
            "response": clean_response.strip(),
            "tool_calls": tool_calls_made,
            "sources": [tc.get("parameters", {}).get("query", "") for tc in tool_calls_made]
        }


class ReportManager:
    """
    translated
    
    translated
    
    translated（translated）：
    reports/
      {report_id}/
        meta.json          - translated
        outline.json       - translated
        progress.json      - translated
        section_01.md      - translated1translated
        section_02.md      - translated2translated
        ...
        full_report.md     - translated
    """
    
    # translated
    REPORTS_DIR = os.path.join(Config.UPLOAD_FOLDER, 'reports')
    
    @classmethod
    def _ensure_reports_dir(cls):
        """translated"""
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
    
    @classmethod
    def _get_report_folder(cls, report_id: str) -> str:
        """translated"""
        return os.path.join(cls.REPORTS_DIR, report_id)
    
    @classmethod
    def _ensure_report_folder(cls, report_id: str) -> str:
        """translated"""
        folder = cls._get_report_folder(report_id)
        os.makedirs(folder, exist_ok=True)
        return folder
    
    @classmethod
    def _get_report_path(cls, report_id: str) -> str:
        """translated"""
        return os.path.join(cls._get_report_folder(report_id), "meta.json")
    
    @classmethod
    def _get_report_markdown_path(cls, report_id: str) -> str:
        """translatedMarkdowntranslated"""
        return os.path.join(cls._get_report_folder(report_id), "full_report.md")
    
    @classmethod
    def _get_outline_path(cls, report_id: str) -> str:
        """translated"""
        return os.path.join(cls._get_report_folder(report_id), "outline.json")
    
    @classmethod
    def _get_progress_path(cls, report_id: str) -> str:
        """translated"""
        return os.path.join(cls._get_report_folder(report_id), "progress.json")
    
    @classmethod
    def _get_section_path(cls, report_id: str, section_index: int) -> str:
        """translatedMarkdowntranslated"""
        return os.path.join(cls._get_report_folder(report_id), f"section_{section_index:02d}.md")
    
    @classmethod
    def _get_agent_log_path(cls, report_id: str) -> str:
        """translated Agent translated"""
        return os.path.join(cls._get_report_folder(report_id), "agent_log.jsonl")
    
    @classmethod
    def _get_console_log_path(cls, report_id: str) -> str:
        """translated"""
        return os.path.join(cls._get_report_folder(report_id), "console_log.txt")
    
    @classmethod
    def get_console_log(cls, report_id: str, from_line: int = 0) -> Dict[str, Any]:
        """
        translated
        
        translated（INFO、WARNINGtranslated），
        translated agent_log.jsonl translated。
        
        Args:
            report_id: translatedID
            from_line: translated（translated，0 translated）
            
        Returns:
            {
                "logs": [translated],
                "total_lines": translated,
                "from_line": translated,
                "has_more": translated
            }
        """
        log_path = cls._get_console_log_path(report_id)
        
        if not os.path.exists(log_path):
            return {
                "logs": [],
                "total_lines": 0,
                "from_line": 0,
                "has_more": False
            }
        
        logs = []
        total_lines = 0
        
        with open(log_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                total_lines = i + 1
                if i >= from_line:
                    # translated，translated
                    logs.append(line.rstrip('\n\r'))
        
        return {
            "logs": logs,
            "total_lines": total_lines,
            "from_line": from_line,
            "has_more": False  # translated
        }
    
    @classmethod
    def get_console_log_stream(cls, report_id: str) -> List[str]:
        """
        translated（translated）
        
        Args:
            report_id: translatedID
            
        Returns:
            translated
        """
        result = cls.get_console_log(report_id, from_line=0)
        return result["logs"]
    
    @classmethod
    def get_agent_log(cls, report_id: str, from_line: int = 0) -> Dict[str, Any]:
        """
        translated Agent translated
        
        Args:
            report_id: translatedID
            from_line: translated（translated，0 translated）
            
        Returns:
            {
                "logs": [translated],
                "total_lines": translated,
                "from_line": translated,
                "has_more": translated
            }
        """
        log_path = cls._get_agent_log_path(report_id)
        
        if not os.path.exists(log_path):
            return {
                "logs": [],
                "total_lines": 0,
                "from_line": 0,
                "has_more": False
            }
        
        logs = []
        total_lines = 0
        
        with open(log_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                total_lines = i + 1
                if i >= from_line:
                    try:
                        log_entry = json.loads(line.strip())
                        logs.append(log_entry)
                    except json.JSONDecodeError:
                        # translated
                        continue
        
        return {
            "logs": logs,
            "total_lines": total_lines,
            "from_line": from_line,
            "has_more": False  # translated
        }
    
    @classmethod
    def get_agent_log_stream(cls, report_id: str) -> List[Dict[str, Any]]:
        """
        translated Agent translated（translated）
        
        Args:
            report_id: translatedID
            
        Returns:
            translated
        """
        result = cls.get_agent_log(report_id, from_line=0)
        return result["logs"]
    
    @classmethod
    def save_outline(cls, report_id: str, outline: ReportOutline) -> None:
        """
        translated
        
        translated
        """
        cls._ensure_report_folder(report_id)
        
        with open(cls._get_outline_path(report_id), 'w', encoding='utf-8') as f:
            json.dump(outline.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"translated: {report_id}")
    
    @classmethod
    def save_section(
        cls,
        report_id: str,
        section_index: int,
        section: ReportSection
    ) -> str:
        """
        translated

        translated，translated

        Args:
            report_id: translatedID
            section_index: translated（translated1translated）
            section: translated

        Returns:
            translated
        """
        cls._ensure_report_folder(report_id)

        # translatedMarkdowntranslated - translated
        cleaned_content = cls._clean_section_content(section.content, section.title)
        md_content = f"## {section.title}\n\n"
        if cleaned_content:
            md_content += f"{cleaned_content}\n\n"

        # translated
        file_suffix = f"section_{section_index:02d}.md"
        file_path = os.path.join(cls._get_report_folder(report_id), file_suffix)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        logger.info(f"translated: {report_id}/{file_suffix}")
        return file_path
    
    @classmethod
    def _clean_section_content(cls, content: str, section_title: str) -> str:
        """
        translated
        
        1. translatedMarkdowntranslated
        2. translated ### translated
        
        Args:
            content: translated
            section_title: translated
            
        Returns:
            translated
        """
        import re
        
        if not content:
            return content
        
        content = content.strip()
        lines = content.split('\n')
        cleaned_lines = []
        skip_next_empty = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # translatedMarkdowntranslated
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            
            if heading_match:
                level = len(heading_match.group(1))
                title_text = heading_match.group(2).strip()
                
                # translated（translated5translated）
                if i < 5:
                    if title_text == section_title or title_text.replace(' ', '') == section_title.replace(' ', ''):
                        skip_next_empty = True
                        continue
                
                # translated（#, ##, ###, ####translated）translated
                # translated，translated
                cleaned_lines.append(f"**{title_text}**")
                cleaned_lines.append("")  # translated
                continue
            
            # translated，translated，translated
            if skip_next_empty and stripped == '':
                skip_next_empty = False
                continue
            
            skip_next_empty = False
            cleaned_lines.append(line)
        
        # translated
        while cleaned_lines and cleaned_lines[0].strip() == '':
            cleaned_lines.pop(0)
        
        # translated
        while cleaned_lines and cleaned_lines[0].strip() in ['---', '***', '___']:
            cleaned_lines.pop(0)
            # translated
            while cleaned_lines and cleaned_lines[0].strip() == '':
                cleaned_lines.pop(0)
        
        return '\n'.join(cleaned_lines)
    
    @classmethod
    def update_progress(
        cls, 
        report_id: str, 
        status: str, 
        progress: int, 
        message: str,
        current_section: str = None,
        completed_sections: List[str] = None
    ) -> None:
        """
        translated
        
        translatedprogress.jsontranslated
        """
        cls._ensure_report_folder(report_id)
        
        progress_data = {
            "status": status,
            "progress": progress,
            "message": message,
            "current_section": current_section,
            "completed_sections": completed_sections or [],
            "updated_at": datetime.now().isoformat()
        }
        
        with open(cls._get_progress_path(report_id), 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def get_progress(cls, report_id: str) -> Optional[Dict[str, Any]]:
        """translated"""
        path = cls._get_progress_path(report_id)
        
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @classmethod
    def get_generated_sections(cls, report_id: str) -> List[Dict[str, Any]]:
        """
        translated
        
        translated
        """
        folder = cls._get_report_folder(report_id)
        
        if not os.path.exists(folder):
            return []
        
        sections = []
        for filename in sorted(os.listdir(folder)):
            if filename.startswith('section_') and filename.endswith('.md'):
                file_path = os.path.join(folder, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # translated
                parts = filename.replace('.md', '').split('_')
                section_index = int(parts[1])

                sections.append({
                    "filename": filename,
                    "section_index": section_index,
                    "content": content
                })

        return sections
    
    @classmethod
    def assemble_full_report(cls, report_id: str, outline: ReportOutline) -> str:
        """
        translated
        
        translated，translated
        """
        folder = cls._get_report_folder(report_id)
        
        # translated
        md_content = f"# {outline.title}\n\n"
        md_content += f"> {outline.summary}\n\n"
        md_content += f"---\n\n"
        
        # translated
        sections = cls.get_generated_sections(report_id)
        for section_info in sections:
            md_content += section_info["content"]
        
        # translated：translated
        md_content = cls._post_process_report(md_content, outline)
        
        # translated
        full_path = cls._get_report_markdown_path(report_id)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"translated: {report_id}")
        return md_content
    
    @classmethod
    def _post_process_report(cls, content: str, outline: ReportOutline) -> str:
        """
        translated
        
        1. translated
        2. translated(#)translated(##)，translated(###, ####translated)
        3. translated
        
        Args:
            content: translated
            outline: translated
            
        Returns:
            translated
        """
        import re
        
        lines = content.split('\n')
        processed_lines = []
        prev_was_heading = False
        
        # translated
        section_titles = set()
        for section in outline.sections:
            section_titles.add(section.title)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # translated
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                # translated（translated5translated）
                is_duplicate = False
                for j in range(max(0, len(processed_lines) - 5), len(processed_lines)):
                    prev_line = processed_lines[j].strip()
                    prev_match = re.match(r'^(#{1,6})\s+(.+)$', prev_line)
                    if prev_match:
                        prev_title = prev_match.group(2).strip()
                        if prev_title == title:
                            is_duplicate = True
                            break
                
                if is_duplicate:
                    # translated
                    i += 1
                    while i < len(lines) and lines[i].strip() == '':
                        i += 1
                    continue
                
                # translated：
                # - # (level=1) translated
                # - ## (level=2) translated
                # - ### translated (level>=3) translated
                
                if level == 1:
                    if title == outline.title:
                        # translated
                        processed_lines.append(line)
                        prev_was_heading = True
                    elif title in section_titles:
                        # translated#，translated##
                        processed_lines.append(f"## {title}")
                        prev_was_heading = True
                    else:
                        # translated
                        processed_lines.append(f"**{title}**")
                        processed_lines.append("")
                        prev_was_heading = False
                elif level == 2:
                    if title in section_titles or title == outline.title:
                        # translated
                        processed_lines.append(line)
                        prev_was_heading = True
                    else:
                        # translated
                        processed_lines.append(f"**{title}**")
                        processed_lines.append("")
                        prev_was_heading = False
                else:
                    # ### translated
                    processed_lines.append(f"**{title}**")
                    processed_lines.append("")
                    prev_was_heading = False
                
                i += 1
                continue
            
            elif stripped == '---' and prev_was_heading:
                # translated
                i += 1
                continue
            
            elif stripped == '' and prev_was_heading:
                # translated
                if processed_lines and processed_lines[-1].strip() != '':
                    processed_lines.append(line)
                prev_was_heading = False
            
            else:
                processed_lines.append(line)
                prev_was_heading = False
            
            i += 1
        
        # translated（translated2translated）
        result_lines = []
        empty_count = 0
        for line in processed_lines:
            if line.strip() == '':
                empty_count += 1
                if empty_count <= 2:
                    result_lines.append(line)
            else:
                empty_count = 0
                result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    @classmethod
    def save_report(cls, report: Report) -> None:
        """translated"""
        cls._ensure_report_folder(report.report_id)
        
        # translatedJSON
        with open(cls._get_report_path(report.report_id), 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        
        # translated
        if report.outline:
            cls.save_outline(report.report_id, report.outline)
        
        # translatedMarkdowntranslated
        if report.markdown_content:
            with open(cls._get_report_markdown_path(report.report_id), 'w', encoding='utf-8') as f:
                f.write(report.markdown_content)
        
        logger.info(f"translated: {report.report_id}")
    
    @classmethod
    def get_report(cls, report_id: str) -> Optional[Report]:
        """translated"""
        path = cls._get_report_path(report_id)
        
        if not os.path.exists(path):
            # translated：translatedreportstranslated
            old_path = os.path.join(cls.REPORTS_DIR, f"{report_id}.json")
            if os.path.exists(old_path):
                path = old_path
            else:
                return None
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # translatedReporttranslated
        outline = None
        if data.get('outline'):
            outline_data = data['outline']
            sections = []
            for s in outline_data.get('sections', []):
                sections.append(ReportSection(
                    title=s['title'],
                    content=s.get('content', '')
                ))
            outline = ReportOutline(
                title=outline_data['title'],
                summary=outline_data['summary'],
                sections=sections
            )
        
        # translatedmarkdown_contenttranslated，translatedfull_report.mdtranslated
        markdown_content = data.get('markdown_content', '')
        if not markdown_content:
            full_report_path = cls._get_report_markdown_path(report_id)
            if os.path.exists(full_report_path):
                with open(full_report_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
        
        return Report(
            report_id=data['report_id'],
            simulation_id=data['simulation_id'],
            graph_id=data['graph_id'],
            simulation_requirement=data['simulation_requirement'],
            status=ReportStatus(data['status']),
            outline=outline,
            markdown_content=markdown_content,
            created_at=data.get('created_at', ''),
            completed_at=data.get('completed_at', ''),
            error=data.get('error')
        )
    
    @classmethod
    def get_report_by_simulation(cls, simulation_id: str) -> Optional[Report]:
        """translatedIDtranslated"""
        cls._ensure_reports_dir()
        
        for item in os.listdir(cls.REPORTS_DIR):
            item_path = os.path.join(cls.REPORTS_DIR, item)
            # translated：translated
            if os.path.isdir(item_path):
                report = cls.get_report(item)
                if report and report.simulation_id == simulation_id:
                    return report
            # translated：JSONtranslated
            elif item.endswith('.json'):
                report_id = item[:-5]
                report = cls.get_report(report_id)
                if report and report.simulation_id == simulation_id:
                    return report
        
        return None
    
    @classmethod
    def list_reports(cls, simulation_id: Optional[str] = None, limit: int = 50) -> List[Report]:
        """translated"""
        cls._ensure_reports_dir()
        
        reports = []
        for item in os.listdir(cls.REPORTS_DIR):
            item_path = os.path.join(cls.REPORTS_DIR, item)
            # translated：translated
            if os.path.isdir(item_path):
                report = cls.get_report(item)
                if report:
                    if simulation_id is None or report.simulation_id == simulation_id:
                        reports.append(report)
            # translated：JSONtranslated
            elif item.endswith('.json'):
                report_id = item[:-5]
                report = cls.get_report(report_id)
                if report:
                    if simulation_id is None or report.simulation_id == simulation_id:
                        reports.append(report)
        
        # translated
        reports.sort(key=lambda r: r.created_at, reverse=True)
        
        return reports[:limit]
    
    @classmethod
    def delete_report(cls, report_id: str) -> bool:
        """translated（translated）"""
        import shutil
        
        folder_path = cls._get_report_folder(report_id)
        
        # translated：translated
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logger.info(f"translated: {report_id}")
            return True
        
        # translated：translated
        deleted = False
        old_json_path = os.path.join(cls.REPORTS_DIR, f"{report_id}.json")
        old_md_path = os.path.join(cls.REPORTS_DIR, f"{report_id}.md")
        
        if os.path.exists(old_json_path):
            os.remove(old_json_path)
            deleted = True
        if os.path.exists(old_md_path):
            os.remove(old_md_path)
            deleted = True
        
        return deleted
