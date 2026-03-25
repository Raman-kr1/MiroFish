"""
Zepconverted
convertedAgentconvertedZepconverted
"""

import os
import time
import threading
import json
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from queue import Queue, Empty

from zep_cloud.client import Zep

from ..config import Config
from ..utils.logger import get_logger

logger = get_logger('mirofish.zep_graph_memory_updater')


@dataclass
class AgentActivity:
    """Agentconverted"""
    platform: str           # twitter / reddit
    agent_id: int
    agent_name: str
    action_type: str        # CREATE_POST, LIKE_POST, etc.
    action_args: Dict[str, Any]
    round_num: int
    timestamp: str
    
    def to_episode_text(self) -> str:
        """
        convertedZepconverted
        
        details，convertedZepconverted
        details，details
        """
        # details
        action_descriptions = {
            "CREATE_POST": self._describe_create_post,
            "LIKE_POST": self._describe_like_post,
            "DISLIKE_POST": self._describe_dislike_post,
            "REPOST": self._describe_repost,
            "QUOTE_POST": self._describe_quote_post,
            "FOLLOW": self._describe_follow,
            "CREATE_COMMENT": self._describe_create_comment,
            "LIKE_COMMENT": self._describe_like_comment,
            "DISLIKE_COMMENT": self._describe_dislike_comment,
            "SEARCH_POSTS": self._describe_search,
            "SEARCH_USER": self._describe_search_user,
            "MUTE": self._describe_mute,
        }
        
        describe_func = action_descriptions.get(self.action_type, self._describe_generic)
        description = describe_func()
        
        # details "agentconverted: details" details，details
        return f"{self.agent_name}: {description}"
    
    def _describe_create_post(self) -> str:
        content = self.action_args.get("content", "")
        if content:
            return f"details：「{content}」"
        return "details"
    
    def _describe_like_post(self) -> str:
        """details - details"""
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if post_content and post_author:
            return f"details{post_author}details：「{post_content}」"
        elif post_content:
            return f"details：「{post_content}」"
        elif post_author:
            return f"details{post_author}details"
        return "details"
    
    def _describe_dislike_post(self) -> str:
        """details - details"""
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if post_content and post_author:
            return f"details{post_author}details：「{post_content}」"
        elif post_content:
            return f"details：「{post_content}」"
        elif post_author:
            return f"details{post_author}details"
        return "details"
    
    def _describe_repost(self) -> str:
        """details - details"""
        original_content = self.action_args.get("original_content", "")
        original_author = self.action_args.get("original_author_name", "")
        
        if original_content and original_author:
            return f"details{original_author}details：「{original_content}」"
        elif original_content:
            return f"details：「{original_content}」"
        elif original_author:
            return f"details{original_author}details"
        return "details"
    
    def _describe_quote_post(self) -> str:
        """details - details、details"""
        original_content = self.action_args.get("original_content", "")
        original_author = self.action_args.get("original_author_name", "")
        quote_content = self.action_args.get("quote_content", "") or self.action_args.get("content", "")
        
        base = ""
        if original_content and original_author:
            base = f"details{original_author}details「{original_content}」"
        elif original_content:
            base = f"details「{original_content}」"
        elif original_author:
            base = f"details{original_author}details"
        else:
            base = "details"
        
        if quote_content:
            base += f"，details：「{quote_content}」"
        return base
    
    def _describe_follow(self) -> str:
        """details - details"""
        target_user_name = self.action_args.get("target_user_name", "")
        
        if target_user_name:
            return f"details「{target_user_name}」"
        return "details"
    
    def _describe_create_comment(self) -> str:
        """details - details"""
        content = self.action_args.get("content", "")
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if content:
            if post_content and post_author:
                return f"details{post_author}details「{post_content}」details：「{content}」"
            elif post_content:
                return f"details「{post_content}」details：「{content}」"
            elif post_author:
                return f"details{post_author}details：「{content}」"
            return f"details：「{content}」"
        return "details"
    
    def _describe_like_comment(self) -> str:
        """details - details"""
        comment_content = self.action_args.get("comment_content", "")
        comment_author = self.action_args.get("comment_author_name", "")
        
        if comment_content and comment_author:
            return f"details{comment_author}details：「{comment_content}」"
        elif comment_content:
            return f"details：「{comment_content}」"
        elif comment_author:
            return f"details{comment_author}details"
        return "details"
    
    def _describe_dislike_comment(self) -> str:
        """details - details"""
        comment_content = self.action_args.get("comment_content", "")
        comment_author = self.action_args.get("comment_author_name", "")
        
        if comment_content and comment_author:
            return f"details{comment_author}details：「{comment_content}」"
        elif comment_content:
            return f"details：「{comment_content}」"
        elif comment_author:
            return f"details{comment_author}details"
        return "details"
    
    def _describe_search(self) -> str:
        """details - details"""
        query = self.action_args.get("query", "") or self.action_args.get("keyword", "")
        return f"details「{query}」" if query else "details"
    
    def _describe_search_user(self) -> str:
        """details - details"""
        query = self.action_args.get("query", "") or self.action_args.get("username", "")
        return f"details「{query}」" if query else "details"
    
    def _describe_mute(self) -> str:
        """details - details"""
        target_user_name = self.action_args.get("target_user_name", "")
        
        if target_user_name:
            return f"details「{target_user_name}」"
        return "details"
    
    def _describe_generic(self) -> str:
        # details，details
        return f"details{self.action_type}details"


class ZepGraphMemoryUpdater:
    """
    Zepconverted
    
    convertedactionsconverted，convertedagentconvertedZepconverted。
    details，convertedBATCH_SIZEconvertedZep。
    
    convertedZep，action_argsconverted：
    - details/details
    - details/details
    - details/details
    - details/details
    """
    
    # details（details）
    BATCH_SIZE = 5
    
    # details（details）
    PLATFORM_DISPLAY_NAMES = {
        'twitter': 'converted1',
        'reddit': 'converted2',
    }
    
    # details（details），details
    SEND_INTERVAL = 0.5
    
    # details
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # details
    
    def __init__(self, graph_id: str, api_key: Optional[str] = None):
        """
        details
        
        Args:
            graph_id: ZepconvertedID
            api_key: Zep API Key（details，details）
        """
        self.graph_id = graph_id
        self.api_key = api_key or Config.ZEP_API_KEY
        
        if not self.api_key:
            raise ValueError("ZEP_API_KEYconverted")
        
        self.client = Zep(api_key=self.api_key)
        
        # details
        self._activity_queue: Queue = Queue()
        
        # details（convertedBATCH_SIZEconverted）
        self._platform_buffers: Dict[str, List[AgentActivity]] = {
            'twitter': [],
            'reddit': [],
        }
        self._buffer_lock = threading.Lock()
        
        # details
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        
        # details
        self._total_activities = 0  # details
        self._total_sent = 0        # convertedZepconverted
        self._total_items_sent = 0  # convertedZepconverted
        self._failed_count = 0      # details
        self._skipped_count = 0     # details（DO_NOTHING）
        
        logger.info(f"ZepGraphMemoryUpdater details: graph_id={graph_id}, batch_size={self.BATCH_SIZE}")
    
    def _get_platform_display_name(self, platform: str) -> str:
        """details"""
        return self.PLATFORM_DISPLAY_NAMES.get(platform.lower(), platform)
    
    def start(self):
        """details"""
        if self._running:
            return
        
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name=f"ZepMemoryUpdater-{self.graph_id[:8]}"
        )
        self._worker_thread.start()
        logger.info(f"ZepGraphMemoryUpdater details: graph_id={self.graph_id}")
    
    def stop(self):
        """details"""
        self._running = False
        
        # details
        self._flush_remaining()
        
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=10)
        
        logger.info(f"ZepGraphMemoryUpdater details: graph_id={self.graph_id}, "
                   f"total_activities={self._total_activities}, "
                   f"batches_sent={self._total_sent}, "
                   f"items_sent={self._total_items_sent}, "
                   f"failed={self._failed_count}, "
                   f"skipped={self._skipped_count}")
    
    def add_activity(self, activity: AgentActivity):
        """
        convertedagentconverted
        
        details，details：
        - CREATE_POST（details）
        - CREATE_COMMENT（details）
        - QUOTE_POST（details）
        - SEARCH_POSTS（details）
        - SEARCH_USER（details）
        - LIKE_POST/DISLIKE_POST（details/details）
        - REPOST（details）
        - FOLLOW（details）
        - MUTE（details）
        - LIKE_COMMENT/DISLIKE_COMMENT（details/details）
        
        action_argsconverted（details、details）。
        
        Args:
            activity: Agentconverted
        """
        # convertedDO_NOTHINGconverted
        if activity.action_type == "DO_NOTHING":
            self._skipped_count += 1
            return
        
        self._activity_queue.put(activity)
        self._total_activities += 1
        logger.debug(f"convertedZepconverted: {activity.agent_name} - {activity.action_type}")
    
    def add_activity_from_dict(self, data: Dict[str, Any], platform: str):
        """
        details
        
        Args:
            data: convertedactions.jsonlconverted
            platform: details (twitter/reddit)
        """
        # details
        if "event_type" in data:
            return
        
        activity = AgentActivity(
            platform=platform,
            agent_id=data.get("agent_id", 0),
            agent_name=data.get("agent_name", ""),
            action_type=data.get("action_type", ""),
            action_args=data.get("action_args", {}),
            round_num=data.get("round", 0),
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )
        
        self.add_activity(activity)
    
    def _worker_loop(self):
        """details - convertedZep"""
        while self._running or not self._activity_queue.empty():
            try:
                # details（converted1converted）
                try:
                    activity = self._activity_queue.get(timeout=1)
                    
                    # details
                    platform = activity.platform.lower()
                    with self._buffer_lock:
                        if platform not in self._platform_buffers:
                            self._platform_buffers[platform] = []
                        self._platform_buffers[platform].append(activity)
                        
                        # details
                        if len(self._platform_buffers[platform]) >= self.BATCH_SIZE:
                            batch = self._platform_buffers[platform][:self.BATCH_SIZE]
                            self._platform_buffers[platform] = self._platform_buffers[platform][self.BATCH_SIZE:]
                            # details
                            self._send_batch_activities(batch, platform)
                            # details，details
                            time.sleep(self.SEND_INTERVAL)
                    
                except Empty:
                    pass
                    
            except Exception as e:
                logger.error(f"details: {e}")
                time.sleep(1)
    
    def _send_batch_activities(self, activities: List[AgentActivity], platform: str):
        """
        convertedZepconverted（details）
        
        Args:
            activities: Agentconverted
            platform: details
        """
        if not activities:
            return
        
        # details，details
        episode_texts = [activity.to_episode_text() for activity in activities]
        combined_text = "\n".join(episode_texts)
        
        # details
        for attempt in range(self.MAX_RETRIES):
            try:
                self.client.graph.add(
                    graph_id=self.graph_id,
                    type="text",
                    data=combined_text
                )
                
                self._total_sent += 1
                self._total_items_sent += len(activities)
                display_name = self._get_platform_display_name(platform)
                logger.info(f"details {len(activities)} details{display_name}details {self.graph_id}")
                logger.debug(f"details: {combined_text[:200]}...")
                return
                
            except Exception as e:
                if attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"convertedZepconverted (details {attempt + 1}/{self.MAX_RETRIES}): {e}")
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"convertedZepconverted，details{self.MAX_RETRIES}details: {e}")
                    self._failed_count += 1
    
    def _flush_remaining(self):
        """details"""
        # details，details
        while not self._activity_queue.empty():
            try:
                activity = self._activity_queue.get_nowait()
                platform = activity.platform.lower()
                with self._buffer_lock:
                    if platform not in self._platform_buffers:
                        self._platform_buffers[platform] = []
                    self._platform_buffers[platform].append(activity)
            except Empty:
                break
        
        # details（convertedBATCH_SIZEconverted）
        with self._buffer_lock:
            for platform, buffer in self._platform_buffers.items():
                if buffer:
                    display_name = self._get_platform_display_name(platform)
                    logger.info(f"details{display_name}details {len(buffer)} details")
                    self._send_batch_activities(buffer, platform)
            # details
            for platform in self._platform_buffers:
                self._platform_buffers[platform] = []
    
    def get_stats(self) -> Dict[str, Any]:
        """details"""
        with self._buffer_lock:
            buffer_sizes = {p: len(b) for p, b in self._platform_buffers.items()}
        
        return {
            "graph_id": self.graph_id,
            "batch_size": self.BATCH_SIZE,
            "total_activities": self._total_activities,  # details
            "batches_sent": self._total_sent,            # details
            "items_sent": self._total_items_sent,        # details
            "failed_count": self._failed_count,          # details
            "skipped_count": self._skipped_count,        # details（DO_NOTHING）
            "queue_size": self._activity_queue.qsize(),
            "buffer_sizes": buffer_sizes,                # details
            "running": self._running,
        }


class ZepGraphMemoryManager:
    """
    convertedZepconverted
    
    details
    """
    
    _updaters: Dict[str, ZepGraphMemoryUpdater] = {}
    _lock = threading.Lock()
    
    @classmethod
    def create_updater(cls, simulation_id: str, graph_id: str) -> ZepGraphMemoryUpdater:
        """
        details
        
        Args:
            simulation_id: convertedID
            graph_id: ZepconvertedID
            
        Returns:
            ZepGraphMemoryUpdaterconverted
        """
        with cls._lock:
            # details，details
            if simulation_id in cls._updaters:
                cls._updaters[simulation_id].stop()
            
            updater = ZepGraphMemoryUpdater(graph_id)
            updater.start()
            cls._updaters[simulation_id] = updater
            
            logger.info(f"details: simulation_id={simulation_id}, graph_id={graph_id}")
            return updater
    
    @classmethod
    def get_updater(cls, simulation_id: str) -> Optional[ZepGraphMemoryUpdater]:
        """details"""
        return cls._updaters.get(simulation_id)
    
    @classmethod
    def stop_updater(cls, simulation_id: str):
        """details"""
        with cls._lock:
            if simulation_id in cls._updaters:
                cls._updaters[simulation_id].stop()
                del cls._updaters[simulation_id]
                logger.info(f"details: simulation_id={simulation_id}")
    
    # details stop_all details
    _stop_all_done = False
    
    @classmethod
    def stop_all(cls):
        """details"""
        # details
        if cls._stop_all_done:
            return
        cls._stop_all_done = True
        
        with cls._lock:
            if cls._updaters:
                for simulation_id, updater in list(cls._updaters.items()):
                    try:
                        updater.stop()
                    except Exception as e:
                        logger.error(f"details: simulation_id={simulation_id}, error={e}")
                cls._updaters.clear()
            logger.info("details")
    
    @classmethod
    def get_all_stats(cls) -> Dict[str, Dict[str, Any]]:
        """details"""
        return {
            sim_id: updater.get_stats() 
            for sim_id, updater in cls._updaters.items()
        }
