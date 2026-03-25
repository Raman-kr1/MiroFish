"""
Report Agentconverted
convertedLangChain + ZepconvertedReACTconverted

details：
1. convertedZepconverted
2. details，details
3. convertedReACTconverted
4. details，details
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
    Report Agent details
    
    details agent_log.jsonl details，details。
    details JSON details，details、details、details。
    """
    
    def __init__(self, report_id: str):
        """
        details
        
        Args:
            report_id: convertedID，details
        """
        self.report_id = report_id
        self.log_file_path = os.path.join(
            Config.UPLOAD_FOLDER, 'reports', report_id, 'agent_log.jsonl'
        )
        self.start_time = datetime.now()
        self._ensure_log_file()
    
    def _ensure_log_file(self):
        """details"""
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)
    
    def _get_elapsed_time(self) -> float:
        """details（details）"""
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
        details
        
        Args:
            action: details，details 'start', 'tool_call', 'llm_response', 'section_complete' details
            stage: details，details 'planning', 'generating', 'completed'
            details: details，details
            section_title: details（details）
            section_index: details（details）
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
        
        # details JSONL details
        with open(self.log_file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def log_start(self, simulation_id: str, graph_id: str, simulation_requirement: str):
        """details"""
        self.log(
            action="report_start",
            stage="pending",
            details={
                "simulation_id": simulation_id,
                "graph_id": graph_id,
                "simulation_requirement": simulation_requirement,
                "message": "details"
            }
        )
    
    def log_planning_start(self):
        """details"""
        self.log(
            action="planning_start",
            stage="planning",
            details={"message": "details"}
        )
    
    def log_planning_context(self, context: Dict[str, Any]):
        """details"""
        self.log(
            action="planning_context",
            stage="planning",
            details={
                "message": "details",
                "context": context
            }
        )
    
    def log_planning_complete(self, outline_dict: Dict[str, Any]):
        """details"""
        self.log(
            action="planning_complete",
            stage="planning",
            details={
                "message": "details",
                "outline": outline_dict
            }
        )
    
    def log_section_start(self, section_title: str, section_index: int):
        """details"""
        self.log(
            action="section_start",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={"message": f"details: {section_title}"}
        )
    
    def log_react_thought(self, section_title: str, section_index: int, iteration: int, thought: str):
        """details ReACT details"""
        self.log(
            action="react_thought",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "thought": thought,
                "message": f"ReACT details{iteration}details"
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
        """details"""
        self.log(
            action="tool_call",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "tool_name": tool_name,
                "parameters": parameters,
                "message": f"details: {tool_name}"
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
        """details（details，details）"""
        self.log(
            action="tool_result",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "tool_name": tool_name,
                "result": result,  # details，details
                "result_length": len(result),
                "message": f"details {tool_name} details"
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
        """details LLM details（details，details）"""
        self.log(
            action="llm_response",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "iteration": iteration,
                "response": response,  # details，details
                "response_length": len(response),
                "has_tool_calls": has_tool_calls,
                "has_final_answer": has_final_answer,
                "message": f"LLM details (details: {has_tool_calls}, details: {has_final_answer})"
            }
        )
    
    def log_section_content(
        self,
        section_title: str,
        section_index: int,
        content: str,
        tool_calls_count: int
    ):
        """details（details，details）"""
        self.log(
            action="section_content",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "content": content,  # details，details
                "content_length": len(content),
                "tool_calls_count": tool_calls_count,
                "message": f"details {section_title} details"
            }
        )
    
    def log_section_full_complete(
        self,
        section_title: str,
        section_index: int,
        full_content: str
    ):
        """
        details

        details，details
        """
        self.log(
            action="section_complete",
            stage="generating",
            section_title=section_title,
            section_index=section_index,
            details={
                "content": full_content,
                "content_length": len(full_content),
                "message": f"details {section_title} details"
            }
        )
    
    def log_report_complete(self, total_sections: int, total_time_seconds: float):
        """details"""
        self.log(
            action="report_complete",
            stage="completed",
            details={
                "total_sections": total_sections,
                "total_time_seconds": round(total_time_seconds, 2),
                "message": "details"
            }
        )
    
    def log_error(self, error_message: str, stage: str, section_title: str = None):
        """details"""
        self.log(
            action="error",
            stage=stage,
            section_title=section_title,
            section_index=None,
            details={
                "error": error_message,
                "message": f"details: {error_message}"
            }
        )


class ReportConsoleLogger:
    """
    Report Agent details
    
    details（INFO、WARNINGconverted）details console_log.txt details。
    details agent_log.jsonl details，details。
    """
    
    def __init__(self, report_id: str):
        """
        details
        
        Args:
            report_id: convertedID，details
        """
        self.report_id = report_id
        self.log_file_path = os.path.join(
            Config.UPLOAD_FOLDER, 'reports', report_id, 'console_log.txt'
        )
        self._ensure_log_file()
        self._file_handler = None
        self._setup_file_handler()
    
    def _ensure_log_file(self):
        """details"""
        log_dir = os.path.dirname(self.log_file_path)
        os.makedirs(log_dir, exist_ok=True)
    
    def _setup_file_handler(self):
        """details，details"""
        import logging
        
        # details
        self._file_handler = logging.FileHandler(
            self.log_file_path,
            mode='a',
            encoding='utf-8'
        )
        self._file_handler.setLevel(logging.INFO)
        
        # details
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )
        self._file_handler.setFormatter(formatter)
        
        # details report_agent details logger
        loggers_to_attach = [
            'mirofish.report_agent',
            'mirofish.zep_tools',
        ]
        
        for logger_name in loggers_to_attach:
            target_logger = logging.getLogger(logger_name)
            # details
            if self._file_handler not in target_logger.handlers:
                target_logger.addHandler(self._file_handler)
    
    def close(self):
        """details logger details"""
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
        """details"""
        self.close()


class ReportStatus(str, Enum):
    """details"""
    PENDING = "pending"
    PLANNING = "planning"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ReportSection:
    """details"""
    title: str
    content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "content": self.content
        }

    def to_markdown(self, level: int = 2) -> str:
        """convertedMarkdownconverted"""
        md = f"{'#' * level} {self.title}\n\n"
        if self.content:
            md += f"{self.content}\n\n"
        return md


@dataclass
class ReportOutline:
    """details"""
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
        """convertedMarkdownconverted"""
        md = f"# {self.title}\n\n"
        md += f"> {self.summary}\n\n"
        for section in self.sections:
            md += section.to_markdown()
        return md


@dataclass
class Report:
    """details"""
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
# Prompt details
# ═══════════════════════════════════════════════════════════════

# ── details ──

TOOL_DESC_INSIGHT_FORGE = """\
【details - details】
details，details。details：
1. details
2. details
3. details、details、details
4. details、details

【details】
- details
- details
- details

【details】
- details（details）
- details
- details"""

TOOL_DESC_PANORAMA_SEARCH = """\
【details - details】
details，details。details：
1. details
2. details/details
3. details

【details】
- details
- details
- details

【details】
- details（details）
- details/details（details）
- details"""

TOOL_DESC_QUICK_SEARCH = """\
【details - details】
details，details、details。

【details】
- details
- details
- details

【details】
- details"""

TOOL_DESC_INTERVIEW_AGENTS = """\
【details - convertedAgentconverted（details）】
convertedOASISconvertedAPI，convertedAgentconverted！
convertedLLMconverted，convertedAgentconverted。
convertedTwitterconvertedRedditconverted，details。

details：
1. details，convertedAgent
2. convertedAgent（details、details、details）
3. details
4. details /api/simulation/interview/batch details
5. details，details

【details】
- details（details？details？details？）
- details
- convertedAgentconverted（convertedOASISconverted）
- details，details"details"

【details】
- convertedAgentconverted
- convertedAgentconvertedTwitterconvertedRedditconverted
- details（details）
- details

【details】convertedOASISconverted！"""

# ── details prompt ──

PLAN_SYSTEM_PROMPT = """\
details「details」details，details「details」——convertedAgentconverted、details。

【details】
details，details「details」details。details，details。details"details"，details"details"。

【details】
details「details」，details：
1. details，details？
2. convertedAgent（details）details？
3. details？

【details】
- ✅ details，details"details，details"
- ✅ details：details、details、details、details
- ✅ convertedAgentconverted
- ❌ details
- ❌ details

【details】
- converted2converted，converted5converted
- details，details
- details，details
- details

convertedJSONconverted，details：
{
    "title": "details",
    "summary": "details（details）",
    "sections": [
        {
            "title": "details",
            "description": "details"
        }
    ]
}

details：sectionsconverted2converted，converted5converted！"""

PLAN_USER_PROMPT_TEMPLATE = """\
【details】
details（details）：{simulation_requirement}

【details】
- details: {total_nodes}
- details: {total_edges}
- details: {entity_types}
- convertedAgentconverted: {total_entities}

【details】
{related_facts_json}

details「details」details：
1. details，details？
2. details（Agent）details？
3. details？

details，details。

【details】details：converted2converted，converted5converted，details。"""

# ── details prompt ──

SECTION_SYSTEM_PROMPT_TEMPLATE = """\
details「details」details，details。

details: {report_title}
details: {report_summary}
details（details）: {simulation_requirement}

details: {section_title}

═══════════════════════════════════════════════════════════════
【details】
═══════════════════════════════════════════════════════════════

details。details（details），
convertedAgentconverted，details。

details：
- details，details
- details（Agent）details
- details、details

❌ details
✅ details"details"——details

═══════════════════════════════════════════════════════════════
【details - details】
═══════════════════════════════════════════════════════════════

1. 【details】
   - details「details」details
   - convertedAgentconverted
   - details
   - converted3converted（converted5converted）details，details

2. 【convertedAgentconverted】
   - Agentconverted
   - details，details：
     > "details：details..."
   - details

3. 【details - details】
   - details
   - details，details
   - details，details
   - details，details
   - details（> details）details

4. 【details】
   - details
   - details
   - details，details

═══════════════════════════════════════════════════════════════
【⚠️ details - details！】
═══════════════════════════════════════════════════════════════

【details = details】
- details
- ❌ details Markdown details（#、##、###、#### details）
- ❌ details
- ✅ details，details
- ✅ details**details**、details、details、details，details

【details】
```
details。details，details...

**details**

details，details：

> "converted68%details..."

**details**

details：

- details
- details
```

【details】
```
## details          ← details！details
### details、details     ← details！details###details
#### 1.1 details   ← details！details####details

details...
```

═══════════════════════════════════════════════════════════════
【details】（converted3-5converted）
═══════════════════════════════════════════════════════════════

{tools_description}

【details - details，details】
- insight_forge: details，details
- panorama_search: details，details、details
- quick_search: details
- interview_agents: convertedAgent，details

═══════════════════════════════════════════════════════════════
【details】
═══════════════════════════════════════════════════════════════

details（details）：

convertedA - details：
details，details：
<tool_call>
{{"name": "details", "parameters": {{"details": "details"}}}}
</tool_call>
details。details。

convertedB - details：
details，details "Final Answer:" details。

⚠️ details：
- details Final Answer
- details（Observation），details
- details

═══════════════════════════════════════════════════════════════
【details】
═══════════════════════════════════════════════════════════════

1. details
2. details
3. convertedMarkdownconverted（details）：
   - details **details** details（details）
   - details（-converted1.2.3.）details
   - details
   - ❌ details #、##、###、#### details
4. 【details - details】
   details，details，details：

   ✅ details：
   ```
   details。

   > "details。"

   details。
   ```

   ❌ details：
   ```
   details。> "details..." details...
   ```
5. details
6. 【details】details，details
7. 【details】details！details**details**details"""

SECTION_USER_PROMPT_TEMPLATE = """\
details（details，details）：
{previous_content}

═══════════════════════════════════════════════════════════════
【details】details: {section_title}
═══════════════════════════════════════════════════════════════

【details】
1. details，details！
2. details
3. details，details
4. details，details

【⚠️ details - details】
- ❌ details（#、##、###、####details）
- ❌ details"{section_title}"details
- ✅ details
- ✅ details，details**details**details

details：
1. details（Thought）details
2. details（Action）details
3. details Final Answer（details，details）"""

# ── ReACT details ──

REACT_OBSERVATION_TEMPLATE = """\
Observation（details）:

═══ details {tool_name} details ═══
{result}

═══════════════════════════════════════════════════════════════
details {tool_calls_count}/{max_tool_calls} details（details: {used_tools_str}）{unused_hint}
- details：details "Final Answer:" details（details）
- details：details
═══════════════════════════════════════════════════════════════"""

REACT_INSUFFICIENT_TOOLS_MSG = (
    "【details】details{tool_calls_count}details，details{min_tool_calls}details。"
    "details，details Final Answer。{unused_hint}"
)

REACT_INSUFFICIENT_TOOLS_MSG_ALT = (
    "details {tool_calls_count} details，details {min_tool_calls} details。"
    "details。{unused_hint}"
)

REACT_TOOL_LIMIT_MSG = (
    "details（{tool_calls_count}/{max_tool_calls}），details。"
    'details，details "Final Answer:" details。'
)

REACT_UNUSED_TOOLS_HINT = "\n💡 details: {unused_list}，details"

REACT_FORCE_FINAL_MSG = "details，details Final Answer: details。"

# ── Chat prompt ──

CHAT_SYSTEM_PROMPT_TEMPLATE = """\
details。

【details】
details: {simulation_requirement}

【details】
{report_content}

【details】
1. details
2. details，details
3. details，details
4. details、details、details

【details】（details，converted1-2converted）
{tools_description}

【details】
<tool_call>
{{"name": "details", "parameters": {{"details": "details"}}}}
</tool_call>

【details】
- details，details
- details > details
- details，details"""

CHAT_OBSERVATION_SUFFIX = "\n\nconverted。"


# ═══════════════════════════════════════════════════════════════
# ReportAgent details
# ═══════════════════════════════════════════════════════════════


class ReportAgent:
    """
    Report Agent - convertedAgent

    convertedReACT（Reasoning + Acting）details：
    1. details：details，details
    2. details：details，details
    3. details：details
    """
    
    # details（details）
    MAX_TOOL_CALLS_PER_SECTION = 5
    
    # details
    MAX_REFLECTION_ROUNDS = 3
    
    # details
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
        convertedReport Agent
        
        Args:
            graph_id: convertedID
            simulation_id: convertedID
            simulation_requirement: details
            llm_client: LLMconverted（details）
            zep_tools: Zepconverted（details）
        """
        self.graph_id = graph_id
        self.simulation_id = simulation_id
        self.simulation_requirement = simulation_requirement
        
        self.llm = llm_client or LLMClient()
        self.zep_tools = zep_tools or ZepToolsService()
        
        # details
        self.tools = self._define_tools()
        
        # details（details generate_report details）
        self.report_logger: Optional[ReportLogger] = None
        # details（details generate_report details）
        self.console_logger: Optional[ReportConsoleLogger] = None
        
        logger.info(f"ReportAgent details: graph_id={graph_id}, simulation_id={simulation_id}")
    
    def _define_tools(self) -> Dict[str, Dict[str, Any]]:
        """details"""
        return {
            "insight_forge": {
                "name": "insight_forge",
                "description": TOOL_DESC_INSIGHT_FORGE,
                "parameters": {
                    "query": "details",
                    "report_context": "details（details，details）"
                }
            },
            "panorama_search": {
                "name": "panorama_search",
                "description": TOOL_DESC_PANORAMA_SEARCH,
                "parameters": {
                    "query": "details，details",
                    "include_expired": "details/details（convertedTrue）"
                }
            },
            "quick_search": {
                "name": "quick_search",
                "description": TOOL_DESC_QUICK_SEARCH,
                "parameters": {
                    "query": "details",
                    "limit": "details（details，converted10）"
                }
            },
            "interview_agents": {
                "name": "interview_agents",
                "description": TOOL_DESC_INTERVIEW_AGENTS,
                "parameters": {
                    "interview_topic": "details（details：'details'）",
                    "max_agents": "convertedAgentconverted（details，converted5，converted10）"
                }
            }
        }
    
    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any], report_context: str = "") -> str:
        """
        details
        
        Args:
            tool_name: details
            parameters: details
            report_context: details（convertedInsightForge）
            
        Returns:
            details（details）
        """
        logger.info(f"details: {tool_name}, details: {parameters}")
        
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
                # details - details
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
                # details - details
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
                # details - convertedOASISconvertedAPIconvertedAgentconverted（details）
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
            
            # ========== details（details） ==========
            
            elif tool_name == "search_graph":
                # details quick_search
                logger.info("search_graph details quick_search")
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
                # details insight_forge，details
                logger.info("get_simulation_context details insight_forge")
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
                return f"details: {tool_name}。details: insight_forge, panorama_search, quick_search"
                
        except Exception as e:
            logger.error(f"details: {tool_name}, details: {str(e)}")
            return f"details: {str(e)}"
    
    # details，details JSON details
    VALID_TOOL_NAMES = {"insight_forge", "panorama_search", "quick_search", "interview_agents"}

    def _parse_tool_calls(self, response: str) -> List[Dict[str, Any]]:
        """
        convertedLLMconverted

        details（details）：
        1. <tool_call>{"name": "tool_name", "parameters": {...}}</tool_call>
        2. details JSON（details JSON）
        """
        tool_calls = []

        # converted1: XMLconverted（details）
        xml_pattern = r'<tool_call>\s*(\{.*?\})\s*</tool_call>'
        for match in re.finditer(xml_pattern, response, re.DOTALL):
            try:
                call_data = json.loads(match.group(1))
                tool_calls.append(call_data)
            except json.JSONDecodeError:
                pass

        if tool_calls:
            return tool_calls

        # converted2: details - LLM details JSON（details <tool_call> details）
        # converted1converted，details JSON
        stripped = response.strip()
        if stripped.startswith('{') and stripped.endswith('}'):
            try:
                call_data = json.loads(stripped)
                if self._is_valid_tool_call(call_data):
                    tool_calls.append(call_data)
                    return tool_calls
            except json.JSONDecodeError:
                pass

        # details + details JSON，details JSON details
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
        """details JSON details"""
        # details {"name": ..., "parameters": ...} details {"tool": ..., "params": ...} details
        tool_name = data.get("name") or data.get("tool")
        if tool_name and tool_name in self.VALID_TOOL_NAMES:
            # details name / parameters
            if "tool" in data:
                data["name"] = data.pop("tool")
            if "params" in data and "parameters" not in data:
                data["parameters"] = data.pop("params")
            return True
        return False
    
    def _get_tools_description(self) -> str:
        """details"""
        desc_parts = ["details："]
        for name, tool in self.tools.items():
            params_desc = ", ".join([f"{k}: {v}" for k, v in tool["parameters"].items()])
            desc_parts.append(f"- {name}: {tool['description']}")
            if params_desc:
                desc_parts.append(f"  details: {params_desc}")
        return "\n".join(desc_parts)
    
    def plan_outline(
        self, 
        progress_callback: Optional[Callable] = None
    ) -> ReportOutline:
        """
        details
        
        convertedLLMconverted，details
        
        Args:
            progress_callback: details
            
        Returns:
            ReportOutline: details
        """
        logger.info("details...")
        
        if progress_callback:
            progress_callback("planning", 0, "details...")
        
        # details
        context = self.zep_tools.get_simulation_context(
            graph_id=self.graph_id,
            simulation_requirement=self.simulation_requirement
        )
        
        if progress_callback:
            progress_callback("planning", 30, "details...")
        
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
                progress_callback("planning", 80, "details...")
            
            # details
            sections = []
            for section_data in response.get("sections", []):
                sections.append(ReportSection(
                    title=section_data.get("title", ""),
                    content=""
                ))
            
            outline = ReportOutline(
                title=response.get("title", "details"),
                summary=response.get("summary", ""),
                sections=sections
            )
            
            if progress_callback:
                progress_callback("planning", 100, "details")
            
            logger.info(f"details: {len(sections)} details")
            return outline
            
        except Exception as e:
            logger.error(f"details: {str(e)}")
            # details（3converted，convertedfallback）
            return ReportOutline(
                title="details",
                summary="details",
                sections=[
                    ReportSection(title="details"),
                    ReportSection(title="details"),
                    ReportSection(title="details")
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
        convertedReACTconverted
        
        ReACTconverted：
        1. Thought（details）- details
        2. Action（details）- details
        3. Observation（details）- details
        4. details
        5. Final Answer（details）- details
        
        Args:
            section: details
            outline: details
            previous_sections: details（details）
            progress_callback: details
            section_index: details（details）
            
        Returns:
            details（Markdownconverted）
        """
        logger.info(f"ReACTconverted: {section.title}")
        
        # details
        if self.report_logger:
            self.report_logger.log_section_start(section.title, section_index)
        
        system_prompt = SECTION_SYSTEM_PROMPT_TEMPLATE.format(
            report_title=outline.title,
            report_summary=outline.summary,
            simulation_requirement=self.simulation_requirement,
            section_title=section.title,
            tools_description=self._get_tools_description(),
        )

        # convertedprompt - converted4000converted
        if previous_sections:
            previous_parts = []
            for sec in previous_sections:
                # converted4000converted
                truncated = sec[:4000] + "..." if len(sec) > 4000 else sec
                previous_parts.append(truncated)
            previous_content = "\n\n---\n\n".join(previous_parts)
        else:
            previous_content = "（details）"
        
        user_prompt = SECTION_USER_PROMPT_TEMPLATE.format(
            previous_content=previous_content,
            section_title=section.title,
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # ReACTconverted
        tool_calls_count = 0
        max_iterations = 5  # details
        min_tool_calls = 3  # details
        conflict_retries = 0  # convertedFinal Answerconverted
        used_tools = set()  # details
        all_tools = {"insight_forge", "panorama_search", "quick_search", "interview_agents"}

        # details，convertedInsightForgeconverted
        report_context = f"details: {section.title}\nconverted: {self.simulation_requirement}"
        
        for iteration in range(max_iterations):
            if progress_callback:
                progress_callback(
                    "generating", 
                    int((iteration / max_iterations) * 100),
                    f"details ({tool_calls_count}/{self.MAX_TOOL_CALLS_PER_SECTION})"
                )
            
            # convertedLLM
            response = self.llm.chat(
                messages=messages,
                temperature=0.5,
                max_tokens=4096
            )

            # details LLM details None（API details）
            if response is None:
                logger.warning(f"details {section.title} details {iteration + 1} details: LLM details None")
                # details，details
                if iteration < max_iterations - 1:
                    messages.append({"role": "assistant", "content": "（details）"})
                    messages.append({"role": "user", "content": "details。"})
                    continue
                # details None，details
                break

            logger.debug(f"LLMconverted: {response[:200]}...")

            # details，details
            tool_calls = self._parse_tool_calls(response)
            has_tool_calls = bool(tool_calls)
            has_final_answer = "Final Answer:" in response

            # ── details：LLM details Final Answer ──
            if has_tool_calls and has_final_answer:
                conflict_retries += 1
                logger.warning(
                    f"details {section.title} details {iteration+1} details: "
                    f"LLM details Final Answer（details {conflict_retries} details）"
                )

                if conflict_retries <= 2:
                    # details：details，details LLM details
                    messages.append({"role": "assistant", "content": response})
                    messages.append({
                        "role": "user",
                        "content": (
                            "【details】details Final Answer，details。\n"
                            "details：\n"
                            "- details（details <tool_call> details，details Final Answer）\n"
                            "- details（details 'Final Answer:' details，details <tool_call>）\n"
                            "details，details。"
                        ),
                    })
                    continue
                else:
                    # details：details，details，details
                    logger.warning(
                        f"details {section.title}: details {conflict_retries} details，"
                        "details"
                    )
                    first_tool_end = response.find('</tool_call>')
                    if first_tool_end != -1:
                        response = response[:first_tool_end + len('</tool_call>')]
                        tool_calls = self._parse_tool_calls(response)
                        has_tool_calls = bool(tool_calls)
                    has_final_answer = False
                    conflict_retries = 0

            # details LLM details
            if self.report_logger:
                self.report_logger.log_llm_response(
                    section_title=section.title,
                    section_index=section_index,
                    response=response,
                    iteration=iteration + 1,
                    has_tool_calls=has_tool_calls,
                    has_final_answer=has_final_answer
                )

            # ── converted1：LLM details Final Answer ──
            if has_final_answer:
                # details，details
                if tool_calls_count < min_tool_calls:
                    messages.append({"role": "assistant", "content": response})
                    unused_tools = all_tools - used_tools
                    unused_hint = f"（details，details: {', '.join(unused_tools)}）" if unused_tools else ""
                    messages.append({
                        "role": "user",
                        "content": REACT_INSUFFICIENT_TOOLS_MSG.format(
                            tool_calls_count=tool_calls_count,
                            min_tool_calls=min_tool_calls,
                            unused_hint=unused_hint,
                        ),
                    })
                    continue

                # details
                final_answer = response.split("Final Answer:")[-1].strip()
                logger.info(f"details {section.title} details（details: {tool_calls_count}details）")

                if self.report_logger:
                    self.report_logger.log_section_content(
                        section_title=section.title,
                        section_index=section_index,
                        content=final_answer,
                        tool_calls_count=tool_calls_count
                    )
                return final_answer

            # ── converted2：LLM details ──
            if has_tool_calls:
                # details → details，details Final Answer
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

                # details
                call = tool_calls[0]
                if len(tool_calls) > 1:
                    logger.info(f"LLM details {len(tool_calls)} details，details: {call['name']}")

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

                # details
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

            # ── converted3：details，details Final Answer ──
            messages.append({"role": "assistant", "content": response})

            if tool_calls_count < min_tool_calls:
                # details，details
                unused_tools = all_tools - used_tools
                unused_hint = f"（details，details: {', '.join(unused_tools)}）" if unused_tools else ""

                messages.append({
                    "role": "user",
                    "content": REACT_INSUFFICIENT_TOOLS_MSG_ALT.format(
                        tool_calls_count=tool_calls_count,
                        min_tool_calls=min_tool_calls,
                        unused_hint=unused_hint,
                    ),
                })
                continue

            # details，LLM details "Final Answer:" details
            # details，details
            logger.info(f"details {section.title} details 'Final Answer:' details，convertedLLMconverted（details: {tool_calls_count}details）")
            final_answer = response.strip()

            if self.report_logger:
                self.report_logger.log_section_content(
                    section_title=section.title,
                    section_index=section_index,
                    content=final_answer,
                    tool_calls_count=tool_calls_count
                )
            return final_answer
        
        # details，details
        logger.warning(f"details {section.title} details，details")
        messages.append({"role": "user", "content": REACT_FORCE_FINAL_MSG})
        
        response = self.llm.chat(
            messages=messages,
            temperature=0.5,
            max_tokens=4096
        )

        # details LLM details None
        if response is None:
            logger.error(f"details {section.title} details LLM details None，details")
            final_answer = f"（details：LLM details，details）"
        elif "Final Answer:" in response:
            final_answer = response.split("Final Answer:")[-1].strip()
        else:
            final_answer = response
        
        # details
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
        details（details）
        
        details，details。
        details：
        reports/{report_id}/
            meta.json       - details
            outline.json    - details
            progress.json   - details
            section_01.md   - converted1converted
            section_02.md   - converted2converted
            ...
            full_report.md  - details
        
        Args:
            progress_callback: details (stage, progress, message)
            report_id: convertedID（details，details）
            
        Returns:
            Report: details
        """
        import uuid
        
        # details report_id，details
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
        
        # details（details）
        completed_section_titles = []
        
        try:
            # details：details
            ReportManager._ensure_report_folder(report_id)
            
            # details（details agent_log.jsonl）
            self.report_logger = ReportLogger(report_id)
            self.report_logger.log_start(
                simulation_id=self.simulation_id,
                graph_id=self.graph_id,
                simulation_requirement=self.simulation_requirement
            )
            
            # details（console_log.txt）
            self.console_logger = ReportConsoleLogger(report_id)
            
            ReportManager.update_progress(
                report_id, "pending", 0, "details...",
                completed_sections=[]
            )
            ReportManager.save_report(report)
            
            # converted1: details
            report.status = ReportStatus.PLANNING
            ReportManager.update_progress(
                report_id, "planning", 5, "details...",
                completed_sections=[]
            )
            
            # details
            self.report_logger.log_planning_start()
            
            if progress_callback:
                progress_callback("planning", 0, "details...")
            
            outline = self.plan_outline(
                progress_callback=lambda stage, prog, msg: 
                    progress_callback(stage, prog // 5, msg) if progress_callback else None
            )
            report.outline = outline
            
            # details
            self.report_logger.log_planning_complete(outline.to_dict())
            
            # details
            ReportManager.save_outline(report_id, outline)
            ReportManager.update_progress(
                report_id, "planning", 15, f"details，details{len(outline.sections)}details",
                completed_sections=[]
            )
            ReportManager.save_report(report)
            
            logger.info(f"details: {report_id}/outline.json")
            
            # converted2: details（details）
            report.status = ReportStatus.GENERATING
            
            total_sections = len(outline.sections)
            generated_sections = []  # details
            
            for i, section in enumerate(outline.sections):
                section_num = i + 1
                base_progress = 20 + int((i / total_sections) * 70)
                
                # details
                ReportManager.update_progress(
                    report_id, "generating", base_progress,
                    f"details: {section.title} ({section_num}/{total_sections})",
                    current_section=section.title,
                    completed_sections=completed_section_titles
                )
                
                if progress_callback:
                    progress_callback(
                        "generating", 
                        base_progress, 
                        f"details: {section.title} ({section_num}/{total_sections})"
                    )
                
                # details
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

                # details
                ReportManager.save_section(report_id, section_num, section)
                completed_section_titles.append(section.title)

                # details
                full_section_content = f"## {section.title}\n\n{section_content}"

                if self.report_logger:
                    self.report_logger.log_section_full_complete(
                        section_title=section.title,
                        section_index=section_num,
                        full_content=full_section_content.strip()
                    )

                logger.info(f"details: {report_id}/section_{section_num:02d}.md")
                
                # details
                ReportManager.update_progress(
                    report_id, "generating", 
                    base_progress + int(70 / total_sections),
                    f"details {section.title} details",
                    current_section=None,
                    completed_sections=completed_section_titles
                )
            
            # converted3: details
            if progress_callback:
                progress_callback("generating", 95, "details...")
            
            ReportManager.update_progress(
                report_id, "generating", 95, "details...",
                completed_sections=completed_section_titles
            )
            
            # convertedReportManagerconverted
            report.markdown_content = ReportManager.assemble_full_report(report_id, outline)
            report.status = ReportStatus.COMPLETED
            report.completed_at = datetime.now().isoformat()
            
            # details
            total_time_seconds = (datetime.now() - start_time).total_seconds()
            
            # details
            if self.report_logger:
                self.report_logger.log_report_complete(
                    total_sections=total_sections,
                    total_time_seconds=total_time_seconds
                )
            
            # details
            ReportManager.save_report(report)
            ReportManager.update_progress(
                report_id, "completed", 100, "details",
                completed_sections=completed_section_titles
            )
            
            if progress_callback:
                progress_callback("completed", 100, "details")
            
            logger.info(f"details: {report_id}")
            
            # details
            if self.console_logger:
                self.console_logger.close()
                self.console_logger = None
            
            return report
            
        except Exception as e:
            logger.error(f"details: {str(e)}")
            report.status = ReportStatus.FAILED
            report.error = str(e)
            
            # details
            if self.report_logger:
                self.report_logger.log_error(str(e), "failed")
            
            # details
            try:
                ReportManager.save_report(report)
                ReportManager.update_progress(
                    report_id, "failed", -1, f"details: {str(e)}",
                    completed_sections=completed_section_titles
                )
            except Exception:
                pass  # details
            
            # details
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
        convertedReport Agentconverted
        
        convertedAgentconverted
        
        Args:
            message: details
            chat_history: details
            
        Returns:
            {
                "response": "Agentconverted",
                "tool_calls": [details],
                "sources": [details]
            }
        """
        logger.info(f"Report Agentconverted: {message[:50]}...")
        
        chat_history = chat_history or []
        
        # details
        report_content = ""
        try:
            report = ReportManager.get_report_by_simulation(self.simulation_id)
            if report and report.markdown_content:
                # details，details
                report_content = report.markdown_content[:15000]
                if len(report.markdown_content) > 15000:
                    report_content += "\n\n... [details] ..."
        except Exception as e:
            logger.warning(f"details: {e}")
        
        system_prompt = CHAT_SYSTEM_PROMPT_TEMPLATE.format(
            simulation_requirement=self.simulation_requirement,
            report_content=report_content if report_content else "（details）",
            tools_description=self._get_tools_description(),
        )

        # details
        messages = [{"role": "system", "content": system_prompt}]
        
        # details
        for h in chat_history[-10:]:  # details
            messages.append(h)
        
        # details
        messages.append({
            "role": "user", 
            "content": message
        })
        
        # ReACTconverted（details）
        tool_calls_made = []
        max_iterations = 2  # details
        
        for iteration in range(max_iterations):
            response = self.llm.chat(
                messages=messages,
                temperature=0.5
            )
            
            # details
            tool_calls = self._parse_tool_calls(response)
            
            if not tool_calls:
                # details，details
                clean_response = re.sub(r'<tool_call>.*?</tool_call>', '', response, flags=re.DOTALL)
                clean_response = re.sub(r'\[TOOL_CALL\].*?\)', '', clean_response)
                
                return {
                    "response": clean_response.strip(),
                    "tool_calls": tool_calls_made,
                    "sources": [tc.get("parameters", {}).get("query", "") for tc in tool_calls_made]
                }
            
            # details（details）
            tool_results = []
            for call in tool_calls[:1]:  # converted1converted
                if len(tool_calls_made) >= self.MAX_TOOL_CALLS_PER_CHAT:
                    break
                result = self._execute_tool(call["name"], call.get("parameters", {}))
                tool_results.append({
                    "tool": call["name"],
                    "result": result[:1500]  # details
                })
                tool_calls_made.append(call)
            
            # details
            messages.append({"role": "assistant", "content": response})
            observation = "\n".join([f"[{r['tool']}details]\n{r['result']}" for r in tool_results])
            messages.append({
                "role": "user",
                "content": observation + CHAT_OBSERVATION_SUFFIX
            })
        
        # details，details
        final_response = self.llm.chat(
            messages=messages,
            temperature=0.5
        )
        
        # details
        clean_response = re.sub(r'<tool_call>.*?</tool_call>', '', final_response, flags=re.DOTALL)
        clean_response = re.sub(r'\[TOOL_CALL\].*?\)', '', clean_response)
        
        return {
            "response": clean_response.strip(),
            "tool_calls": tool_calls_made,
            "sources": [tc.get("parameters", {}).get("query", "") for tc in tool_calls_made]
        }


class ReportManager:
    """
    details
    
    details
    
    details（details）：
    reports/
      {report_id}/
        meta.json          - details
        outline.json       - details
        progress.json      - details
        section_01.md      - converted1converted
        section_02.md      - converted2converted
        ...
        full_report.md     - details
    """
    
    # details
    REPORTS_DIR = os.path.join(Config.UPLOAD_FOLDER, 'reports')
    
    @classmethod
    def _ensure_reports_dir(cls):
        """details"""
        os.makedirs(cls.REPORTS_DIR, exist_ok=True)
    
    @classmethod
    def _get_report_folder(cls, report_id: str) -> str:
        """details"""
        return os.path.join(cls.REPORTS_DIR, report_id)
    
    @classmethod
    def _ensure_report_folder(cls, report_id: str) -> str:
        """details"""
        folder = cls._get_report_folder(report_id)
        os.makedirs(folder, exist_ok=True)
        return folder
    
    @classmethod
    def _get_report_path(cls, report_id: str) -> str:
        """details"""
        return os.path.join(cls._get_report_folder(report_id), "meta.json")
    
    @classmethod
    def _get_report_markdown_path(cls, report_id: str) -> str:
        """convertedMarkdownconverted"""
        return os.path.join(cls._get_report_folder(report_id), "full_report.md")
    
    @classmethod
    def _get_outline_path(cls, report_id: str) -> str:
        """details"""
        return os.path.join(cls._get_report_folder(report_id), "outline.json")
    
    @classmethod
    def _get_progress_path(cls, report_id: str) -> str:
        """details"""
        return os.path.join(cls._get_report_folder(report_id), "progress.json")
    
    @classmethod
    def _get_section_path(cls, report_id: str, section_index: int) -> str:
        """convertedMarkdownconverted"""
        return os.path.join(cls._get_report_folder(report_id), f"section_{section_index:02d}.md")
    
    @classmethod
    def _get_agent_log_path(cls, report_id: str) -> str:
        """details Agent details"""
        return os.path.join(cls._get_report_folder(report_id), "agent_log.jsonl")
    
    @classmethod
    def _get_console_log_path(cls, report_id: str) -> str:
        """details"""
        return os.path.join(cls._get_report_folder(report_id), "console_log.txt")
    
    @classmethod
    def get_console_log(cls, report_id: str, from_line: int = 0) -> Dict[str, Any]:
        """
        details
        
        details（INFO、WARNINGconverted），
        details agent_log.jsonl details。
        
        Args:
            report_id: convertedID
            from_line: details（details，0 details）
            
        Returns:
            {
                "logs": [details],
                "total_lines": details,
                "from_line": details,
                "has_more": details
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
                    # details，details
                    logs.append(line.rstrip('\n\r'))
        
        return {
            "logs": logs,
            "total_lines": total_lines,
            "from_line": from_line,
            "has_more": False  # details
        }
    
    @classmethod
    def get_console_log_stream(cls, report_id: str) -> List[str]:
        """
        details（details）
        
        Args:
            report_id: convertedID
            
        Returns:
            details
        """
        result = cls.get_console_log(report_id, from_line=0)
        return result["logs"]
    
    @classmethod
    def get_agent_log(cls, report_id: str, from_line: int = 0) -> Dict[str, Any]:
        """
        details Agent details
        
        Args:
            report_id: convertedID
            from_line: details（details，0 details）
            
        Returns:
            {
                "logs": [details],
                "total_lines": details,
                "from_line": details,
                "has_more": details
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
                        # details
                        continue
        
        return {
            "logs": logs,
            "total_lines": total_lines,
            "from_line": from_line,
            "has_more": False  # details
        }
    
    @classmethod
    def get_agent_log_stream(cls, report_id: str) -> List[Dict[str, Any]]:
        """
        details Agent details（details）
        
        Args:
            report_id: convertedID
            
        Returns:
            details
        """
        result = cls.get_agent_log(report_id, from_line=0)
        return result["logs"]
    
    @classmethod
    def save_outline(cls, report_id: str, outline: ReportOutline) -> None:
        """
        details
        
        details
        """
        cls._ensure_report_folder(report_id)
        
        with open(cls._get_outline_path(report_id), 'w', encoding='utf-8') as f:
            json.dump(outline.to_dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"details: {report_id}")
    
    @classmethod
    def save_section(
        cls,
        report_id: str,
        section_index: int,
        section: ReportSection
    ) -> str:
        """
        details

        details，details

        Args:
            report_id: convertedID
            section_index: details（converted1converted）
            section: details

        Returns:
            details
        """
        cls._ensure_report_folder(report_id)

        # convertedMarkdownconverted - details
        cleaned_content = cls._clean_section_content(section.content, section.title)
        md_content = f"## {section.title}\n\n"
        if cleaned_content:
            md_content += f"{cleaned_content}\n\n"

        # details
        file_suffix = f"section_{section_index:02d}.md"
        file_path = os.path.join(cls._get_report_folder(report_id), file_suffix)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        logger.info(f"details: {report_id}/{file_suffix}")
        return file_path
    
    @classmethod
    def _clean_section_content(cls, content: str, section_title: str) -> str:
        """
        details
        
        1. convertedMarkdownconverted
        2. details ### details
        
        Args:
            content: details
            section_title: details
            
        Returns:
            details
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
            
            # convertedMarkdownconverted
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            
            if heading_match:
                level = len(heading_match.group(1))
                title_text = heading_match.group(2).strip()
                
                # details（converted5converted）
                if i < 5:
                    if title_text == section_title or title_text.replace(' ', '') == section_title.replace(' ', ''):
                        skip_next_empty = True
                        continue
                
                # details（#, ##, ###, ####details）details
                # details，details
                cleaned_lines.append(f"**{title_text}**")
                cleaned_lines.append("")  # details
                continue
            
            # details，details，details
            if skip_next_empty and stripped == '':
                skip_next_empty = False
                continue
            
            skip_next_empty = False
            cleaned_lines.append(line)
        
        # details
        while cleaned_lines and cleaned_lines[0].strip() == '':
            cleaned_lines.pop(0)
        
        # details
        while cleaned_lines and cleaned_lines[0].strip() in ['---', '***', '___']:
            cleaned_lines.pop(0)
            # details
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
        details
        
        convertedprogress.jsonconverted
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
        """details"""
        path = cls._get_progress_path(report_id)
        
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @classmethod
    def get_generated_sections(cls, report_id: str) -> List[Dict[str, Any]]:
        """
        details
        
        details
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

                # details
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
        details
        
        details，details
        """
        folder = cls._get_report_folder(report_id)
        
        # details
        md_content = f"# {outline.title}\n\n"
        md_content += f"> {outline.summary}\n\n"
        md_content += f"---\n\n"
        
        # details
        sections = cls.get_generated_sections(report_id)
        for section_info in sections:
            md_content += section_info["content"]
        
        # details：details
        md_content = cls._post_process_report(md_content, outline)
        
        # details
        full_path = cls._get_report_markdown_path(report_id)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"details: {report_id}")
        return md_content
    
    @classmethod
    def _post_process_report(cls, content: str, outline: ReportOutline) -> str:
        """
        details
        
        1. details
        2. details(#)details(##)，details(###, ####details)
        3. details
        
        Args:
            content: details
            outline: details
            
        Returns:
            details
        """
        import re
        
        lines = content.split('\n')
        processed_lines = []
        prev_was_heading = False
        
        # details
        section_titles = set()
        for section in outline.sections:
            section_titles.add(section.title)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # details
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                
                # details（converted5converted）
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
                    # details
                    i += 1
                    while i < len(lines) and lines[i].strip() == '':
                        i += 1
                    continue
                
                # details：
                # - # (level=1) details
                # - ## (level=2) details
                # - ### details (level>=3) details
                
                if level == 1:
                    if title == outline.title:
                        # details
                        processed_lines.append(line)
                        prev_was_heading = True
                    elif title in section_titles:
                        # details#，details##
                        processed_lines.append(f"## {title}")
                        prev_was_heading = True
                    else:
                        # details
                        processed_lines.append(f"**{title}**")
                        processed_lines.append("")
                        prev_was_heading = False
                elif level == 2:
                    if title in section_titles or title == outline.title:
                        # details
                        processed_lines.append(line)
                        prev_was_heading = True
                    else:
                        # details
                        processed_lines.append(f"**{title}**")
                        processed_lines.append("")
                        prev_was_heading = False
                else:
                    # ### details
                    processed_lines.append(f"**{title}**")
                    processed_lines.append("")
                    prev_was_heading = False
                
                i += 1
                continue
            
            elif stripped == '---' and prev_was_heading:
                # details
                i += 1
                continue
            
            elif stripped == '' and prev_was_heading:
                # details
                if processed_lines and processed_lines[-1].strip() != '':
                    processed_lines.append(line)
                prev_was_heading = False
            
            else:
                processed_lines.append(line)
                prev_was_heading = False
            
            i += 1
        
        # details（converted2converted）
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
        """details"""
        cls._ensure_report_folder(report.report_id)
        
        # convertedJSON
        with open(cls._get_report_path(report.report_id), 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)
        
        # details
        if report.outline:
            cls.save_outline(report.report_id, report.outline)
        
        # convertedMarkdownconverted
        if report.markdown_content:
            with open(cls._get_report_markdown_path(report.report_id), 'w', encoding='utf-8') as f:
                f.write(report.markdown_content)
        
        logger.info(f"details: {report.report_id}")
    
    @classmethod
    def get_report(cls, report_id: str) -> Optional[Report]:
        """details"""
        path = cls._get_report_path(report_id)
        
        if not os.path.exists(path):
            # details：convertedreportsconverted
            old_path = os.path.join(cls.REPORTS_DIR, f"{report_id}.json")
            if os.path.exists(old_path):
                path = old_path
            else:
                return None
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # convertedReportconverted
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
        
        # convertedmarkdown_contentconverted，convertedfull_report.mdconverted
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
        """convertedIDconverted"""
        cls._ensure_reports_dir()
        
        for item in os.listdir(cls.REPORTS_DIR):
            item_path = os.path.join(cls.REPORTS_DIR, item)
            # details：details
            if os.path.isdir(item_path):
                report = cls.get_report(item)
                if report and report.simulation_id == simulation_id:
                    return report
            # details：JSONconverted
            elif item.endswith('.json'):
                report_id = item[:-5]
                report = cls.get_report(report_id)
                if report and report.simulation_id == simulation_id:
                    return report
        
        return None
    
    @classmethod
    def list_reports(cls, simulation_id: Optional[str] = None, limit: int = 50) -> List[Report]:
        """details"""
        cls._ensure_reports_dir()
        
        reports = []
        for item in os.listdir(cls.REPORTS_DIR):
            item_path = os.path.join(cls.REPORTS_DIR, item)
            # details：details
            if os.path.isdir(item_path):
                report = cls.get_report(item)
                if report:
                    if simulation_id is None or report.simulation_id == simulation_id:
                        reports.append(report)
            # details：JSONconverted
            elif item.endswith('.json'):
                report_id = item[:-5]
                report = cls.get_report(report_id)
                if report:
                    if simulation_id is None or report.simulation_id == simulation_id:
                        reports.append(report)
        
        # details
        reports.sort(key=lambda r: r.created_at, reverse=True)
        
        return reports[:limit]
    
    @classmethod
    def delete_report(cls, report_id: str) -> bool:
        """details（details）"""
        import shutil
        
        folder_path = cls._get_report_folder(report_id)
        
        # details：details
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
            logger.info(f"details: {report_id}")
            return True
        
        # details：details
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
