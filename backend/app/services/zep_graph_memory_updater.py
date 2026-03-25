"""
Zeptranslated
translatedAgenttranslatedZeptranslated
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
    """Agenttranslated"""
    platform: str           # twitter / reddit
    agent_id: int
    agent_name: str
    action_type: str        # CREATE_POST, LIKE_POST, etc.
    action_args: Dict[str, Any]
    round_num: int
    timestamp: str
    
    def to_episode_text(self) -> str:
        """
        translatedZeptranslated
        
        translated，translatedZeptranslated
        translated，translated
        """
        # translated
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
        
        # translated "agenttranslated: translated" translated，translated
        return f"{self.agent_name}: {description}"
    
    def _describe_create_post(self) -> str:
        content = self.action_args.get("content", "")
        if content:
            return f"translated：「{content}」"
        return "translated"
    
    def _describe_like_post(self) -> str:
        """translated - translated"""
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if post_content and post_author:
            return f"translated{post_author}translated：「{post_content}」"
        elif post_content:
            return f"translated：「{post_content}」"
        elif post_author:
            return f"translated{post_author}translated"
        return "translated"
    
    def _describe_dislike_post(self) -> str:
        """translated - translated"""
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if post_content and post_author:
            return f"translated{post_author}translated：「{post_content}」"
        elif post_content:
            return f"translated：「{post_content}」"
        elif post_author:
            return f"translated{post_author}translated"
        return "translated"
    
    def _describe_repost(self) -> str:
        """translated - translated"""
        original_content = self.action_args.get("original_content", "")
        original_author = self.action_args.get("original_author_name", "")
        
        if original_content and original_author:
            return f"translated{original_author}translated：「{original_content}」"
        elif original_content:
            return f"translated：「{original_content}」"
        elif original_author:
            return f"translated{original_author}translated"
        return "translated"
    
    def _describe_quote_post(self) -> str:
        """translated - translated、translated"""
        original_content = self.action_args.get("original_content", "")
        original_author = self.action_args.get("original_author_name", "")
        quote_content = self.action_args.get("quote_content", "") or self.action_args.get("content", "")
        
        base = ""
        if original_content and original_author:
            base = f"translated{original_author}translated「{original_content}」"
        elif original_content:
            base = f"translated「{original_content}」"
        elif original_author:
            base = f"translated{original_author}translated"
        else:
            base = "translated"
        
        if quote_content:
            base += f"，translated：「{quote_content}」"
        return base
    
    def _describe_follow(self) -> str:
        """translated - translated"""
        target_user_name = self.action_args.get("target_user_name", "")
        
        if target_user_name:
            return f"translated「{target_user_name}」"
        return "translated"
    
    def _describe_create_comment(self) -> str:
        """translated - translated"""
        content = self.action_args.get("content", "")
        post_content = self.action_args.get("post_content", "")
        post_author = self.action_args.get("post_author_name", "")
        
        if content:
            if post_content and post_author:
                return f"translated{post_author}translated「{post_content}」translated：「{content}」"
            elif post_content:
                return f"translated「{post_content}」translated：「{content}」"
            elif post_author:
                return f"translated{post_author}translated：「{content}」"
            return f"translated：「{content}」"
        return "translated"
    
    def _describe_like_comment(self) -> str:
        """translated - translated"""
        comment_content = self.action_args.get("comment_content", "")
        comment_author = self.action_args.get("comment_author_name", "")
        
        if comment_content and comment_author:
            return f"translated{comment_author}translated：「{comment_content}」"
        elif comment_content:
            return f"translated：「{comment_content}」"
        elif comment_author:
            return f"translated{comment_author}translated"
        return "translated"
    
    def _describe_dislike_comment(self) -> str:
        """translated - translated"""
        comment_content = self.action_args.get("comment_content", "")
        comment_author = self.action_args.get("comment_author_name", "")
        
        if comment_content and comment_author:
            return f"translated{comment_author}translated：「{comment_content}」"
        elif comment_content:
            return f"translated：「{comment_content}」"
        elif comment_author:
            return f"translated{comment_author}translated"
        return "translated"
    
    def _describe_search(self) -> str:
        """translated - translated"""
        query = self.action_args.get("query", "") or self.action_args.get("keyword", "")
        return f"translated「{query}」" if query else "translated"
    
    def _describe_search_user(self) -> str:
        """translated - translated"""
        query = self.action_args.get("query", "") or self.action_args.get("username", "")
        return f"translated「{query}」" if query else "translated"
    
    def _describe_mute(self) -> str:
        """translated - translated"""
        target_user_name = self.action_args.get("target_user_name", "")
        
        if target_user_name:
            return f"translated「{target_user_name}」"
        return "translated"
    
    def _describe_generic(self) -> str:
        # translated，translated
        return f"translated{self.action_type}translated"


class ZepGraphMemoryUpdater:
    """
    Zeptranslated
    
    translatedactionstranslated，translatedagenttranslatedZeptranslated。
    translated，translatedBATCH_SIZEtranslatedZep。
    
    translatedZep，action_argstranslated：
    - translated/translated
    - translated/translated
    - translated/translated
    - translated/translated
    """
    
    # translated（translated）
    BATCH_SIZE = 5
    
    # translated（translated）
    PLATFORM_DISPLAY_NAMES = {
        'twitter': 'translated1',
        'reddit': 'translated2',
    }
    
    # translated（translated），translated
    SEND_INTERVAL = 0.5
    
    # translated
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # translated
    
    def __init__(self, graph_id: str, api_key: Optional[str] = None):
        """
        translated
        
        Args:
            graph_id: ZeptranslatedID
            api_key: Zep API Key（translated，translated）
        """
        self.graph_id = graph_id
        self.api_key = api_key or Config.ZEP_API_KEY
        
        if not self.api_key:
            raise ValueError("ZEP_API_KEYtranslated")
        
        self.client = Zep(api_key=self.api_key)
        
        # translated
        self._activity_queue: Queue = Queue()
        
        # translated（translatedBATCH_SIZEtranslated）
        self._platform_buffers: Dict[str, List[AgentActivity]] = {
            'twitter': [],
            'reddit': [],
        }
        self._buffer_lock = threading.Lock()
        
        # translated
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None
        
        # translated
        self._total_activities = 0  # translated
        self._total_sent = 0        # translatedZeptranslated
        self._total_items_sent = 0  # translatedZeptranslated
        self._failed_count = 0      # translated
        self._skipped_count = 0     # translated（DO_NOTHING）
        
        logger.info(f"ZepGraphMemoryUpdater translated: graph_id={graph_id}, batch_size={self.BATCH_SIZE}")
    
    def _get_platform_display_name(self, platform: str) -> str:
        """translated"""
        return self.PLATFORM_DISPLAY_NAMES.get(platform.lower(), platform)
    
    def start(self):
        """translated"""
        if self._running:
            return
        
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name=f"ZepMemoryUpdater-{self.graph_id[:8]}"
        )
        self._worker_thread.start()
        logger.info(f"ZepGraphMemoryUpdater translated: graph_id={self.graph_id}")
    
    def stop(self):
        """translated"""
        self._running = False
        
        # translated
        self._flush_remaining()
        
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=10)
        
        logger.info(f"ZepGraphMemoryUpdater translated: graph_id={self.graph_id}, "
                   f"total_activities={self._total_activities}, "
                   f"batches_sent={self._total_sent}, "
                   f"items_sent={self._total_items_sent}, "
                   f"failed={self._failed_count}, "
                   f"skipped={self._skipped_count}")
    
    def add_activity(self, activity: AgentActivity):
        """
        translatedagenttranslated
        
        translated，translated：
        - CREATE_POST（translated）
        - CREATE_COMMENT（translated）
        - QUOTE_POST（translated）
        - SEARCH_POSTS（translated）
        - SEARCH_USER（translated）
        - LIKE_POST/DISLIKE_POST（translated/translated）
        - REPOST（translated）
        - FOLLOW（translated）
        - MUTE（translated）
        - LIKE_COMMENT/DISLIKE_COMMENT（translated/translated）
        
        action_argstranslated（translated、translated）。
        
        Args:
            activity: Agenttranslated
        """
        # translatedDO_NOTHINGtranslated
        if activity.action_type == "DO_NOTHING":
            self._skipped_count += 1
            return
        
        self._activity_queue.put(activity)
        self._total_activities += 1
        logger.debug(f"translatedZeptranslated: {activity.agent_name} - {activity.action_type}")
    
    def add_activity_from_dict(self, data: Dict[str, Any], platform: str):
        """
        translated
        
        Args:
            data: translatedactions.jsonltranslated
            platform: translated (twitter/reddit)
        """
        # translated
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
        """translated - translatedZep"""
        while self._running or not self._activity_queue.empty():
            try:
                # translated（translated1translated）
                try:
                    activity = self._activity_queue.get(timeout=1)
                    
                    # translated
                    platform = activity.platform.lower()
                    with self._buffer_lock:
                        if platform not in self._platform_buffers:
                            self._platform_buffers[platform] = []
                        self._platform_buffers[platform].append(activity)
                        
                        # translated
                        if len(self._platform_buffers[platform]) >= self.BATCH_SIZE:
                            batch = self._platform_buffers[platform][:self.BATCH_SIZE]
                            self._platform_buffers[platform] = self._platform_buffers[platform][self.BATCH_SIZE:]
                            # translated
                            self._send_batch_activities(batch, platform)
                            # translated，translated
                            time.sleep(self.SEND_INTERVAL)
                    
                except Empty:
                    pass
                    
            except Exception as e:
                logger.error(f"translated: {e}")
                time.sleep(1)
    
    def _send_batch_activities(self, activities: List[AgentActivity], platform: str):
        """
        translatedZeptranslated（translated）
        
        Args:
            activities: Agenttranslated
            platform: translated
        """
        if not activities:
            return
        
        # translated，translated
        episode_texts = [activity.to_episode_text() for activity in activities]
        combined_text = "\n".join(episode_texts)
        
        # translated
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
                logger.info(f"translated {len(activities)} translated{display_name}translated {self.graph_id}")
                logger.debug(f"translated: {combined_text[:200]}...")
                return
                
            except Exception as e:
                if attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"translatedZeptranslated (translated {attempt + 1}/{self.MAX_RETRIES}): {e}")
                    time.sleep(self.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"translatedZeptranslated，translated{self.MAX_RETRIES}translated: {e}")
                    self._failed_count += 1
    
    def _flush_remaining(self):
        """translated"""
        # translated，translated
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
        
        # translated（translatedBATCH_SIZEtranslated）
        with self._buffer_lock:
            for platform, buffer in self._platform_buffers.items():
                if buffer:
                    display_name = self._get_platform_display_name(platform)
                    logger.info(f"translated{display_name}translated {len(buffer)} translated")
                    self._send_batch_activities(buffer, platform)
            # translated
            for platform in self._platform_buffers:
                self._platform_buffers[platform] = []
    
    def get_stats(self) -> Dict[str, Any]:
        """translated"""
        with self._buffer_lock:
            buffer_sizes = {p: len(b) for p, b in self._platform_buffers.items()}
        
        return {
            "graph_id": self.graph_id,
            "batch_size": self.BATCH_SIZE,
            "total_activities": self._total_activities,  # translated
            "batches_sent": self._total_sent,            # translated
            "items_sent": self._total_items_sent,        # translated
            "failed_count": self._failed_count,          # translated
            "skipped_count": self._skipped_count,        # translated（DO_NOTHING）
            "queue_size": self._activity_queue.qsize(),
            "buffer_sizes": buffer_sizes,                # translated
            "running": self._running,
        }


class ZepGraphMemoryManager:
    """
    translatedZeptranslated
    
    translated
    """
    
    _updaters: Dict[str, ZepGraphMemoryUpdater] = {}
    _lock = threading.Lock()
    
    @classmethod
    def create_updater(cls, simulation_id: str, graph_id: str) -> ZepGraphMemoryUpdater:
        """
        translated
        
        Args:
            simulation_id: translatedID
            graph_id: ZeptranslatedID
            
        Returns:
            ZepGraphMemoryUpdatertranslated
        """
        with cls._lock:
            # translated，translated
            if simulation_id in cls._updaters:
                cls._updaters[simulation_id].stop()
            
            updater = ZepGraphMemoryUpdater(graph_id)
            updater.start()
            cls._updaters[simulation_id] = updater
            
            logger.info(f"translated: simulation_id={simulation_id}, graph_id={graph_id}")
            return updater
    
    @classmethod
    def get_updater(cls, simulation_id: str) -> Optional[ZepGraphMemoryUpdater]:
        """translated"""
        return cls._updaters.get(simulation_id)
    
    @classmethod
    def stop_updater(cls, simulation_id: str):
        """translated"""
        with cls._lock:
            if simulation_id in cls._updaters:
                cls._updaters[simulation_id].stop()
                del cls._updaters[simulation_id]
                logger.info(f"translated: simulation_id={simulation_id}")
    
    # translated stop_all translated
    _stop_all_done = False
    
    @classmethod
    def stop_all(cls):
        """translated"""
        # translated
        if cls._stop_all_done:
            return
        cls._stop_all_done = True
        
        with cls._lock:
            if cls._updaters:
                for simulation_id, updater in list(cls._updaters.items()):
                    try:
                        updater.stop()
                    except Exception as e:
                        logger.error(f"translated: simulation_id={simulation_id}, error={e}")
                cls._updaters.clear()
            logger.info("translated")
    
    @classmethod
    def get_all_stats(cls) -> Dict[str, Dict[str, Any]]:
        """translated"""
        return {
            sim_id: updater.get_stats() 
            for sim_id, updater in cls._updaters.items()
        }
