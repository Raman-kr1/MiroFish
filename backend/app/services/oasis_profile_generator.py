"""
OASIS Agent Profiletranslated
translatedZeptranslatedOASIStranslatedAgent Profiletranslated

translated：
1. translatedZeptranslated
2. translated
3. translated
"""

import json
import random
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from openai import OpenAI
from zep_cloud.client import Zep

from ..config import Config
from ..utils.logger import get_logger
from .zep_entity_reader import EntityNode, ZepEntityReader

logger = get_logger('mirofish.oasis_profile')


@dataclass
class OasisAgentProfile:
    """OASIS Agent Profiletranslated"""
    # translated
    user_id: int
    user_name: str
    name: str
    bio: str
    persona: str
    
    # translated - Reddittranslated
    karma: int = 1000
    
    # translated - Twittertranslated
    friend_count: int = 100
    follower_count: int = 150
    statuses_count: int = 500
    
    # translated
    age: Optional[int] = None
    gender: Optional[str] = None
    mbti: Optional[str] = None
    country: Optional[str] = None
    profession: Optional[str] = None
    interested_topics: List[str] = field(default_factory=list)
    
    # translated
    source_entity_uuid: Optional[str] = None
    source_entity_type: Optional[str] = None
    
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    def to_reddit_format(self) -> Dict[str, Any]:
        """translatedReddittranslated"""
        profile = {
            "user_id": self.user_id,
            "username": self.user_name,  # OASIS translated username（translated）
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "karma": self.karma,
            "created_at": self.created_at,
        }
        
        # translated（translated）
        if self.age:
            profile["age"] = self.age
        if self.gender:
            profile["gender"] = self.gender
        if self.mbti:
            profile["mbti"] = self.mbti
        if self.country:
            profile["country"] = self.country
        if self.profession:
            profile["profession"] = self.profession
        if self.interested_topics:
            profile["interested_topics"] = self.interested_topics
        
        return profile
    
    def to_twitter_format(self) -> Dict[str, Any]:
        """translatedTwittertranslated"""
        profile = {
            "user_id": self.user_id,
            "username": self.user_name,  # OASIS translated username（translated）
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "friend_count": self.friend_count,
            "follower_count": self.follower_count,
            "statuses_count": self.statuses_count,
            "created_at": self.created_at,
        }
        
        # translated
        if self.age:
            profile["age"] = self.age
        if self.gender:
            profile["gender"] = self.gender
        if self.mbti:
            profile["mbti"] = self.mbti
        if self.country:
            profile["country"] = self.country
        if self.profession:
            profile["profession"] = self.profession
        if self.interested_topics:
            profile["interested_topics"] = self.interested_topics
        
        return profile
    
    def to_dict(self) -> Dict[str, Any]:
        """translated"""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "karma": self.karma,
            "friend_count": self.friend_count,
            "follower_count": self.follower_count,
            "statuses_count": self.statuses_count,
            "age": self.age,
            "gender": self.gender,
            "mbti": self.mbti,
            "country": self.country,
            "profession": self.profession,
            "interested_topics": self.interested_topics,
            "source_entity_uuid": self.source_entity_uuid,
            "source_entity_type": self.source_entity_type,
            "created_at": self.created_at,
        }


class OasisProfileGenerator:
    """
    OASIS Profiletranslated
    
    translatedZeptranslatedOASIStranslatedAgent Profile
    
    translated：
    1. translatedZeptranslated
    2. translated（translated、translated、translated、translated）
    3. translated
    """
    
    # MBTItranslated
    MBTI_TYPES = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ]
    
    # translated
    COUNTRIES = [
        "China", "US", "UK", "Japan", "Germany", "France", 
        "Canada", "Australia", "Brazil", "India", "South Korea"
    ]
    
    # translated（translated）
    INDIVIDUAL_ENTITY_TYPES = [
        "student", "alumni", "professor", "person", "publicfigure", 
        "expert", "faculty", "official", "journalist", "activist"
    ]
    
    # translated/translated（translated）
    GROUP_ENTITY_TYPES = [
        "university", "governmentagency", "organization", "ngo", 
        "mediaoutlet", "company", "institution", "group", "community"
    ]
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        zep_api_key: Optional[str] = None,
        graph_id: Optional[str] = None
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
        
        # Zeptranslated
        self.zep_api_key = zep_api_key or Config.ZEP_API_KEY
        self.zep_client = None
        self.graph_id = graph_id
        
        if self.zep_api_key:
            try:
                self.zep_client = Zep(api_key=self.zep_api_key)
            except Exception as e:
                logger.warning(f"Zeptranslated: {e}")
    
    def generate_profile_from_entity(
        self, 
        entity: EntityNode, 
        user_id: int,
        use_llm: bool = True
    ) -> OasisAgentProfile:
        """
        translatedZeptranslatedOASIS Agent Profile
        
        Args:
            entity: Zeptranslated
            user_id: translatedID（translatedOASIS）
            use_llm: translatedLLMtranslated
            
        Returns:
            OasisAgentProfile
        """
        entity_type = entity.get_entity_type() or "Entity"
        
        # translated
        name = entity.name
        user_name = self._generate_username(name)
        
        # translated
        context = self._build_entity_context(entity)
        
        if use_llm:
            # translatedLLMtranslated
            profile_data = self._generate_profile_with_llm(
                entity_name=name,
                entity_type=entity_type,
                entity_summary=entity.summary,
                entity_attributes=entity.attributes,
                context=context
            )
        else:
            # translated
            profile_data = self._generate_profile_rule_based(
                entity_name=name,
                entity_type=entity_type,
                entity_summary=entity.summary,
                entity_attributes=entity.attributes
            )
        
        return OasisAgentProfile(
            user_id=user_id,
            user_name=user_name,
            name=name,
            bio=profile_data.get("bio", f"{entity_type}: {name}"),
            persona=profile_data.get("persona", entity.summary or f"A {entity_type} named {name}."),
            karma=profile_data.get("karma", random.randint(500, 5000)),
            friend_count=profile_data.get("friend_count", random.randint(50, 500)),
            follower_count=profile_data.get("follower_count", random.randint(100, 1000)),
            statuses_count=profile_data.get("statuses_count", random.randint(100, 2000)),
            age=profile_data.get("age"),
            gender=profile_data.get("gender"),
            mbti=profile_data.get("mbti"),
            country=profile_data.get("country"),
            profession=profile_data.get("profession"),
            interested_topics=profile_data.get("interested_topics", []),
            source_entity_uuid=entity.uuid,
            source_entity_type=entity_type,
        )
    
    def _generate_username(self, name: str) -> str:
        """translated"""
        # translated，translated
        username = name.lower().replace(" ", "_")
        username = ''.join(c for c in username if c.isalnum() or c == '_')
        
        # translated
        suffix = random.randint(100, 999)
        return f"{username}_{suffix}"
    
    def _search_zep_for_entity(self, entity: EntityNode) -> Dict[str, Any]:
        """
        translatedZeptranslated
        
        Zeptranslated，translatededgestranslatednodestranslated。
        translated，translated。
        
        Args:
            entity: translated
            
        Returns:
            translatedfacts, node_summaries, contexttranslated
        """
        import concurrent.futures
        
        if not self.zep_client:
            return {"facts": [], "node_summaries": [], "context": ""}
        
        entity_name = entity.name
        
        results = {
            "facts": [],
            "node_summaries": [],
            "context": ""
        }
        
        # translatedgraph_idtranslated
        if not self.graph_id:
            logger.debug(f"translatedZeptranslated：translatedgraph_id")
            return results
        
        comprehensive_query = f"translated{entity_name}translated、translated、translated、translated"
        
        def search_edges():
            """translated（translated/translated）- translated"""
            max_retries = 3
            last_exception = None
            delay = 2.0
            
            for attempt in range(max_retries):
                try:
                    return self.zep_client.graph.search(
                        query=comprehensive_query,
                        graph_id=self.graph_id,
                        limit=30,
                        scope="edges",
                        reranker="rrf"
                    )
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.debug(f"Zeptranslated {attempt + 1} translated: {str(e)[:80]}, translated...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.debug(f"Zeptranslated {max_retries} translated: {e}")
            return None
        
        def search_nodes():
            """translated（translated）- translated"""
            max_retries = 3
            last_exception = None
            delay = 2.0
            
            for attempt in range(max_retries):
                try:
                    return self.zep_client.graph.search(
                        query=comprehensive_query,
                        graph_id=self.graph_id,
                        limit=20,
                        scope="nodes",
                        reranker="rrf"
                    )
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.debug(f"Zeptranslated {attempt + 1} translated: {str(e)[:80]}, translated...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.debug(f"Zeptranslated {max_retries} translated: {e}")
            return None
        
        try:
            # translatededgestranslatednodestranslated
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                edge_future = executor.submit(search_edges)
                node_future = executor.submit(search_nodes)
                
                # translated
                edge_result = edge_future.result(timeout=30)
                node_result = node_future.result(timeout=30)
            
            # translated
            all_facts = set()
            if edge_result and hasattr(edge_result, 'edges') and edge_result.edges:
                for edge in edge_result.edges:
                    if hasattr(edge, 'fact') and edge.fact:
                        all_facts.add(edge.fact)
            results["facts"] = list(all_facts)
            
            # translated
            all_summaries = set()
            if node_result and hasattr(node_result, 'nodes') and node_result.nodes:
                for node in node_result.nodes:
                    if hasattr(node, 'summary') and node.summary:
                        all_summaries.add(node.summary)
                    if hasattr(node, 'name') and node.name and node.name != entity_name:
                        all_summaries.add(f"translated: {node.name}")
            results["node_summaries"] = list(all_summaries)
            
            # translated
            context_parts = []
            if results["facts"]:
                context_parts.append("translated:\n" + "\n".join(f"- {f}" for f in results["facts"][:20]))
            if results["node_summaries"]:
                context_parts.append("translated:\n" + "\n".join(f"- {s}" for s in results["node_summaries"][:10]))
            results["context"] = "\n\n".join(context_parts)
            
            logger.info(f"Zeptranslated: {entity_name}, translated {len(results['facts'])} translated, {len(results['node_summaries'])} translated")
            
        except concurrent.futures.TimeoutError:
            logger.warning(f"Zeptranslated ({entity_name})")
        except Exception as e:
            logger.warning(f"Zeptranslated ({entity_name}): {e}")
        
        return results
    
    def _build_entity_context(self, entity: EntityNode) -> str:
        """
        translated
        
        translated：
        1. translated（translated）
        2. translated
        3. Zeptranslated
        """
        context_parts = []
        
        # 1. translated
        if entity.attributes:
            attrs = []
            for key, value in entity.attributes.items():
                if value and str(value).strip():
                    attrs.append(f"- {key}: {value}")
            if attrs:
                context_parts.append("### translated\n" + "\n".join(attrs))
        
        # 2. translated（translated/translated）
        existing_facts = set()
        if entity.related_edges:
            relationships = []
            for edge in entity.related_edges:  # translated
                fact = edge.get("fact", "")
                edge_name = edge.get("edge_name", "")
                direction = edge.get("direction", "")
                
                if fact:
                    relationships.append(f"- {fact}")
                    existing_facts.add(fact)
                elif edge_name:
                    if direction == "outgoing":
                        relationships.append(f"- {entity.name} --[{edge_name}]--> (translated)")
                    else:
                        relationships.append(f"- (translated) --[{edge_name}]--> {entity.name}")
            
            if relationships:
                context_parts.append("### translated\n" + "\n".join(relationships))
        
        # 3. translated
        if entity.related_nodes:
            related_info = []
            for node in entity.related_nodes:  # translated
                node_name = node.get("name", "")
                node_labels = node.get("labels", [])
                node_summary = node.get("summary", "")
                
                # translated
                custom_labels = [l for l in node_labels if l not in ["Entity", "Node"]]
                label_str = f" ({', '.join(custom_labels)})" if custom_labels else ""
                
                if node_summary:
                    related_info.append(f"- **{node_name}**{label_str}: {node_summary}")
                else:
                    related_info.append(f"- **{node_name}**{label_str}")
            
            if related_info:
                context_parts.append("### translated\n" + "\n".join(related_info))
        
        # 4. translatedZeptranslated
        zep_results = self._search_zep_for_entity(entity)
        
        if zep_results.get("facts"):
            # translated：translated
            new_facts = [f for f in zep_results["facts"] if f not in existing_facts]
            if new_facts:
                context_parts.append("### Zeptranslated\n" + "\n".join(f"- {f}" for f in new_facts[:15]))
        
        if zep_results.get("node_summaries"):
            context_parts.append("### Zeptranslated\n" + "\n".join(f"- {s}" for s in zep_results["node_summaries"][:10]))
        
        return "\n\n".join(context_parts)
    
    def _is_individual_entity(self, entity_type: str) -> bool:
        """translated"""
        return entity_type.lower() in self.INDIVIDUAL_ENTITY_TYPES
    
    def _is_group_entity(self, entity_type: str) -> bool:
        """translated/translated"""
        return entity_type.lower() in self.GROUP_ENTITY_TYPES
    
    def _generate_profile_with_llm(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any],
        context: str
    ) -> Dict[str, Any]:
        """
        translatedLLMtranslated
        
        translated：
        - translated：translated
        - translated/translated：translated
        """
        
        is_individual = self._is_individual_entity(entity_type)
        
        if is_individual:
            prompt = self._build_individual_persona_prompt(
                entity_name, entity_type, entity_summary, entity_attributes, context
            )
        else:
            prompt = self._build_group_persona_prompt(
                entity_name, entity_type, entity_summary, entity_attributes, context
            )

        # translated，translated
        max_attempts = 3
        last_error = None
        
        for attempt in range(max_attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self._get_system_prompt(is_individual)},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.7 - (attempt * 0.1)  # translated
                    # translatedmax_tokens，translatedLLMtranslated
                )
                
                content = response.choices[0].message.content
                
                # translated（finish_reasontranslated'stop'）
                finish_reason = response.choices[0].finish_reason
                if finish_reason == 'length':
                    logger.warning(f"LLMtranslated (attempt {attempt+1}), translated...")
                    content = self._fix_truncated_json(content)
                
                # translatedJSON
                try:
                    result = json.loads(content)
                    
                    # translated
                    if "bio" not in result or not result["bio"]:
                        result["bio"] = entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}"
                    if "persona" not in result or not result["persona"]:
                        result["persona"] = entity_summary or f"{entity_name}translated{entity_type}。"
                    
                    return result
                    
                except json.JSONDecodeError as je:
                    logger.warning(f"JSONtranslated (attempt {attempt+1}): {str(je)[:80]}")
                    
                    # translatedJSON
                    result = self._try_fix_json(content, entity_name, entity_type, entity_summary)
                    if result.get("_fixed"):
                        del result["_fixed"]
                        return result
                    
                    last_error = je
                    
            except Exception as e:
                logger.warning(f"LLMtranslated (attempt {attempt+1}): {str(e)[:80]}")
                last_error = e
                import time
                time.sleep(1 * (attempt + 1))  # translated
        
        logger.warning(f"LLMtranslated（{max_attempts}translated）: {last_error}, translated")
        return self._generate_profile_rule_based(
            entity_name, entity_type, entity_summary, entity_attributes
        )
    
    def _fix_truncated_json(self, content: str) -> str:
        """translatedJSON（translatedmax_tokenstranslated）"""
        import re
        
        # translatedJSONtranslated，translated
        content = content.strip()
        
        # translated
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        # translated
        # translated：translated，translated
        if content and content[-1] not in '",}]':
            # translated
            content += '"'
        
        # translated
        content += ']' * open_brackets
        content += '}' * open_braces
        
        return content
    
    def _try_fix_json(self, content: str, entity_name: str, entity_type: str, entity_summary: str = "") -> Dict[str, Any]:
        """translatedJSON"""
        import re
        
        # 1. translated
        content = self._fix_truncated_json(content)
        
        # 2. translatedJSONtranslated
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group()
            
            # 3. translated
            # translated
            def fix_string_newlines(match):
                s = match.group(0)
                # translated
                s = s.replace('\n', ' ').replace('\r', ' ')
                # translated
                s = re.sub(r'\s+', ' ', s)
                return s
            
            # translatedJSONtranslated
            json_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', fix_string_newlines, json_str)
            
            # 4. translated
            try:
                result = json.loads(json_str)
                result["_fixed"] = True
                return result
            except json.JSONDecodeError as e:
                # 5. translated，translated
                try:
                    # translated
                    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                    # translated
                    json_str = re.sub(r'\s+', ' ', json_str)
                    result = json.loads(json_str)
                    result["_fixed"] = True
                    return result
                except:
                    pass
        
        # 6. translated
        bio_match = re.search(r'"bio"\s*:\s*"([^"]*)"', content)
        persona_match = re.search(r'"persona"\s*:\s*"([^"]*)', content)  # translated
        
        bio = bio_match.group(1) if bio_match else (entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}")
        persona = persona_match.group(1) if persona_match else (entity_summary or f"{entity_name}translated{entity_type}。")
        
        # translated，translated
        if bio_match or persona_match:
            logger.info(f"translatedJSONtranslated")
            return {
                "bio": bio,
                "persona": persona,
                "_fixed": True
            }
        
        # 7. translated，translated
        logger.warning(f"JSONtranslated，translated")
        return {
            "bio": entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}",
            "persona": entity_summary or f"{entity_name}translated{entity_type}。"
        }
    
    def _get_system_prompt(self, is_individual: bool) -> str:
        """translated"""
        base_prompt = "translated。translated、translated,translated。translatedJSONtranslated，translated。translated。"
        return base_prompt
    
    def _build_individual_persona_prompt(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any],
        context: str
    ) -> str:
        """translated"""
        
        attrs_str = json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "translated"
        context_str = context[:3000] if context else "translated"
        
        return f"""translated,translated。

translated: {entity_name}
translated: {entity_type}
translated: {entity_summary}
translated: {attrs_str}

translated:
{context_str}

translatedJSON，translated:

1. bio: translated，200translated
2. persona: translated（2000translated），translated:
   - translated（translated、translated、translated、translated）
   - translated（translated、translated、translated）
   - translated（MBTItranslated、translated、translated）
   - translated（translated、translated、translated、translated）
   - translated（translated、translated/translated）
   - translated（translated、translated、translated）
   - translated（translated，translated，translated）
3. age: translated（translated）
4. gender: translated，translated: "male" translated "female"
5. mbti: MBTItranslated（translatedINTJ、ENFPtranslated）
6. country: translated（translated，translated"translated"）
7. profession: translated
8. interested_topics: translated

translated:
- translated，translated
- personatranslated
- translated（translatedgendertranslatedmale/female）
- translated
- agetranslated，gendertranslated"male"translated"female"
"""

    def _build_group_persona_prompt(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any],
        context: str
    ) -> str:
        """translated/translated"""
        
        attrs_str = json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "translated"
        context_str = context[:3000] if context else "translated"
        
        return f"""translated/translated,translated。

translated: {entity_name}
translated: {entity_type}
translated: {entity_summary}
translated: {attrs_str}

translated:
{context_str}

translatedJSON，translated:

1. bio: translated，200translated，translated
2. persona: translated（2000translated），translated:
   - translated（translated、translated、translated、translated）
   - translated（translated、translated、translated）
   - translated（translated、translated、translated）
   - translated（translated、translated、translated）
   - translated（translated、translated）
   - translated（translated、translated）
   - translated（translated，translated，translated）
3. age: translated30（translated）
4. gender: translated"other"（translatedothertranslated）
5. mbti: MBTItranslated，translated，translatedISTJtranslated
6. country: translated（translated，translated"translated"）
7. profession: translated
8. interested_topics: translated

translated:
- translated，translatednulltranslated
- personatranslated，translated
- translated（translatedgendertranslated"other"）
- agetranslated30，gendertranslated"other"
- translated"""
    
    def _generate_profile_rule_based(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """translated"""
        
        # translated
        entity_type_lower = entity_type.lower()
        
        if entity_type_lower in ["student", "alumni"]:
            return {
                "bio": f"{entity_type} with interests in academics and social issues.",
                "persona": f"{entity_name} is a {entity_type.lower()} who is actively engaged in academic and social discussions. They enjoy sharing perspectives and connecting with peers.",
                "age": random.randint(18, 30),
                "gender": random.choice(["male", "female"]),
                "mbti": random.choice(self.MBTI_TYPES),
                "country": random.choice(self.COUNTRIES),
                "profession": "Student",
                "interested_topics": ["Education", "Social Issues", "Technology"],
            }
        
        elif entity_type_lower in ["publicfigure", "expert", "faculty"]:
            return {
                "bio": f"Expert and thought leader in their field.",
                "persona": f"{entity_name} is a recognized {entity_type.lower()} who shares insights and opinions on important matters. They are known for their expertise and influence in public discourse.",
                "age": random.randint(35, 60),
                "gender": random.choice(["male", "female"]),
                "mbti": random.choice(["ENTJ", "INTJ", "ENTP", "INTP"]),
                "country": random.choice(self.COUNTRIES),
                "profession": entity_attributes.get("occupation", "Expert"),
                "interested_topics": ["Politics", "Economics", "Culture & Society"],
            }
        
        elif entity_type_lower in ["mediaoutlet", "socialmediaplatform"]:
            return {
                "bio": f"Official account for {entity_name}. News and updates.",
                "persona": f"{entity_name} is a media entity that reports news and facilitates public discourse. The account shares timely updates and engages with the audience on current events.",
                "age": 30,  # translated
                "gender": "other",  # translatedother
                "mbti": "ISTJ",  # translated：translated
                "country": "translated",
                "profession": "Media",
                "interested_topics": ["General News", "Current Events", "Public Affairs"],
            }
        
        elif entity_type_lower in ["university", "governmentagency", "ngo", "organization"]:
            return {
                "bio": f"Official account of {entity_name}.",
                "persona": f"{entity_name} is an institutional entity that communicates official positions, announcements, and engages with stakeholders on relevant matters.",
                "age": 30,  # translated
                "gender": "other",  # translatedother
                "mbti": "ISTJ",  # translated：translated
                "country": "translated",
                "profession": entity_type,
                "interested_topics": ["Public Policy", "Community", "Official Announcements"],
            }
        
        else:
            # translated
            return {
                "bio": entity_summary[:150] if entity_summary else f"{entity_type}: {entity_name}",
                "persona": entity_summary or f"{entity_name} is a {entity_type.lower()} participating in social discussions.",
                "age": random.randint(25, 50),
                "gender": random.choice(["male", "female"]),
                "mbti": random.choice(self.MBTI_TYPES),
                "country": random.choice(self.COUNTRIES),
                "profession": entity_type,
                "interested_topics": ["General", "Social Issues"],
            }
    
    def set_graph_id(self, graph_id: str):
        """translatedIDtranslatedZeptranslated"""
        self.graph_id = graph_id
    
    def generate_profiles_from_entities(
        self,
        entities: List[EntityNode],
        use_llm: bool = True,
        progress_callback: Optional[callable] = None,
        graph_id: Optional[str] = None,
        parallel_count: int = 5,
        realtime_output_path: Optional[str] = None,
        output_platform: str = "reddit"
    ) -> List[OasisAgentProfile]:
        """
        translatedAgent Profile（translated）
        
        Args:
            entities: translated
            use_llm: translatedLLMtranslated
            progress_callback: translated (current, total, message)
            graph_id: translatedID，translatedZeptranslated
            parallel_count: translated，translated5
            realtime_output_path: translated（translated，translated）
            output_platform: translated ("reddit" translated "twitter")
            
        Returns:
            Agent Profiletranslated
        """
        import concurrent.futures
        from threading import Lock
        
        # translatedgraph_idtranslatedZeptranslated
        if graph_id:
            self.graph_id = graph_id
        
        total = len(entities)
        profiles = [None] * total  # translated
        completed_count = [0]  # translated
        lock = Lock()
        
        # translated
        def save_profiles_realtime():
            """translated profiles translated"""
            if not realtime_output_path:
                return
            
            with lock:
                # translated profiles
                existing_profiles = [p for p in profiles if p is not None]
                if not existing_profiles:
                    return
                
                try:
                    if output_platform == "reddit":
                        # Reddit JSON translated
                        profiles_data = [p.to_reddit_format() for p in existing_profiles]
                        with open(realtime_output_path, 'w', encoding='utf-8') as f:
                            json.dump(profiles_data, f, ensure_ascii=False, indent=2)
                    else:
                        # Twitter CSV translated
                        import csv
                        profiles_data = [p.to_twitter_format() for p in existing_profiles]
                        if profiles_data:
                            fieldnames = list(profiles_data[0].keys())
                            with open(realtime_output_path, 'w', encoding='utf-8', newline='') as f:
                                writer = csv.DictWriter(f, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerows(profiles_data)
                except Exception as e:
                    logger.warning(f"translated profiles translated: {e}")
        
        def generate_single_profile(idx: int, entity: EntityNode) -> tuple:
            """translatedprofiletranslated"""
            entity_type = entity.get_entity_type() or "Entity"
            
            try:
                profile = self.generate_profile_from_entity(
                    entity=entity,
                    user_id=idx,
                    use_llm=use_llm
                )
                
                # translated
                self._print_generated_profile(entity.name, entity_type, profile)
                
                return idx, profile, None
                
            except Exception as e:
                logger.error(f"translated {entity.name} translated: {str(e)}")
                # translatedprofile
                fallback_profile = OasisAgentProfile(
                    user_id=idx,
                    user_name=self._generate_username(entity.name),
                    name=entity.name,
                    bio=f"{entity_type}: {entity.name}",
                    persona=entity.summary or f"A participant in social discussions.",
                    source_entity_uuid=entity.uuid,
                    source_entity_type=entity_type,
                )
                return idx, fallback_profile, str(e)
        
        logger.info(f"translated {total} translatedAgenttranslated（translated: {parallel_count}）...")
        print(f"\n{'='*60}")
        print(f"translatedAgenttranslated - translated {total} translated，translated: {parallel_count}")
        print(f"{'='*60}\n")
        
        # translated
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_count) as executor:
            # translated
            future_to_entity = {
                executor.submit(generate_single_profile, idx, entity): (idx, entity)
                for idx, entity in enumerate(entities)
            }
            
            # translated
            for future in concurrent.futures.as_completed(future_to_entity):
                idx, entity = future_to_entity[future]
                entity_type = entity.get_entity_type() or "Entity"
                
                try:
                    result_idx, profile, error = future.result()
                    profiles[result_idx] = profile
                    
                    with lock:
                        completed_count[0] += 1
                        current = completed_count[0]
                    
                    # translated
                    save_profiles_realtime()
                    
                    if progress_callback:
                        progress_callback(
                            current, 
                            total, 
                            f"translated {current}/{total}: {entity.name}（{entity_type}）"
                        )
                    
                    if error:
                        logger.warning(f"[{current}/{total}] {entity.name} translated: {error}")
                    else:
                        logger.info(f"[{current}/{total}] translated: {entity.name} ({entity_type})")
                        
                except Exception as e:
                    logger.error(f"translated {entity.name} translated: {str(e)}")
                    with lock:
                        completed_count[0] += 1
                    profiles[idx] = OasisAgentProfile(
                        user_id=idx,
                        user_name=self._generate_username(entity.name),
                        name=entity.name,
                        bio=f"{entity_type}: {entity.name}",
                        persona=entity.summary or "A participant in social discussions.",
                        source_entity_uuid=entity.uuid,
                        source_entity_type=entity_type,
                    )
                    # translated（translated）
                    save_profiles_realtime()
        
        print(f"\n{'='*60}")
        print(f"translated！translated {len([p for p in profiles if p])} translatedAgent")
        print(f"{'='*60}\n")
        
        return profiles
    
    def _print_generated_profile(self, entity_name: str, entity_type: str, profile: OasisAgentProfile):
        """translated（translated，translated）"""
        separator = "-" * 70
        
        # translated（translated）
        topics_str = ', '.join(profile.interested_topics) if profile.interested_topics else 'translated'
        
        output_lines = [
            f"\n{separator}",
            f"[translated] {entity_name} ({entity_type})",
            f"{separator}",
            f"translated: {profile.user_name}",
            f"",
            f"【translated】",
            f"{profile.bio}",
            f"",
            f"【translated】",
            f"{profile.persona}",
            f"",
            f"【translated】",
            f"translated: {profile.age} | translated: {profile.gender} | MBTI: {profile.mbti}",
            f"translated: {profile.profession} | translated: {profile.country}",
            f"translated: {topics_str}",
            separator
        ]
        
        output = "\n".join(output_lines)
        
        # translated（translated，loggertranslated）
        print(output)
    
    def save_profiles(
        self,
        profiles: List[OasisAgentProfile],
        file_path: str,
        platform: str = "reddit"
    ):
        """
        translatedProfiletranslated（translated）
        
        OASIStranslated：
        - Twitter: CSVtranslated
        - Reddit: JSONtranslated
        
        Args:
            profiles: Profiletranslated
            file_path: translated
            platform: translated ("reddit" translated "twitter")
        """
        if platform == "twitter":
            self._save_twitter_csv(profiles, file_path)
        else:
            self._save_reddit_json(profiles, file_path)
    
    def _save_twitter_csv(self, profiles: List[OasisAgentProfile], file_path: str):
        """
        translatedTwitter ProfiletranslatedCSVtranslated（translatedOASIStranslated）
        
        OASIS TwittertranslatedCSVtranslated：
        - user_id: translatedID（translatedCSVtranslated0translated）
        - name: translated
        - username: translated
        - user_char: translated（translatedLLMtranslated，translatedAgenttranslated）
        - description: translated（translated）
        
        user_char vs description translated：
        - user_char: translated，LLMtranslated，translatedAgenttranslated
        - description: translated，translated
        """
        import csv
        
        # translated.csv
        if not file_path.endswith('.csv'):
            file_path = file_path.replace('.json', '.csv')
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # translatedOASIStranslated
            headers = ['user_id', 'name', 'username', 'user_char', 'description']
            writer.writerow(headers)
            
            # translated
            for idx, profile in enumerate(profiles):
                # user_char: translated（bio + persona），translatedLLMtranslated
                user_char = profile.bio
                if profile.persona and profile.persona != profile.bio:
                    user_char = f"{profile.bio} {profile.persona}"
                # translated（CSVtranslated）
                user_char = user_char.replace('\n', ' ').replace('\r', ' ')
                
                # description: translated，translated
                description = profile.bio.replace('\n', ' ').replace('\r', ' ')
                
                row = [
                    idx,                    # user_id: translated0translatedID
                    profile.name,           # name: translated
                    profile.user_name,      # username: translated
                    user_char,              # user_char: translated（translatedLLMtranslated）
                    description             # description: translated（translated）
                ]
                writer.writerow(row)
        
        logger.info(f"translated {len(profiles)} translatedTwitter Profiletranslated {file_path} (OASIS CSVtranslated)")
    
    def _normalize_gender(self, gender: Optional[str]) -> str:
        """
        translatedgendertranslatedOASIStranslated
        
        OASIStranslated: male, female, other
        """
        if not gender:
            return "other"
        
        gender_lower = gender.lower().strip()
        
        # translated
        gender_map = {
            "translated": "male",
            "translated": "female",
            "translated": "other",
            "translated": "other",
            # translated
            "male": "male",
            "female": "female",
            "other": "other",
        }
        
        return gender_map.get(gender_lower, "other")
    
    def _save_reddit_json(self, profiles: List[OasisAgentProfile], file_path: str):
        """
        translatedReddit ProfiletranslatedJSONtranslated
        
        translated to_reddit_format() translated，translated OASIS translated。
        translated user_id translated，translated OASIS agent_graph.get_agent() translated！
        
        translated：
        - user_id: translatedID（translated，translated initial_posts translated poster_agent_id）
        - username: translated
        - name: translated
        - bio: translated
        - persona: translated
        - age: translated（translated）
        - gender: "male", "female", translated "other"
        - mbti: MBTItranslated
        - country: translated
        """
        data = []
        for idx, profile in enumerate(profiles):
            # translated to_reddit_format() translated
            item = {
                "user_id": profile.user_id if profile.user_id is not None else idx,  # translated：translated user_id
                "username": profile.user_name,
                "name": profile.name,
                "bio": profile.bio[:150] if profile.bio else f"{profile.name}",
                "persona": profile.persona or f"{profile.name} is a participant in social discussions.",
                "karma": profile.karma if profile.karma else 1000,
                "created_at": profile.created_at,
                # OASIStranslated - translated
                "age": profile.age if profile.age else 30,
                "gender": self._normalize_gender(profile.gender),
                "mbti": profile.mbti if profile.mbti else "ISTJ",
                "country": profile.country if profile.country else "translated",
            }
            
            # translated
            if profile.profession:
                item["profession"] = profile.profession
            if profile.interested_topics:
                item["interested_topics"] = profile.interested_topics
            
            data.append(item)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"translated {len(profiles)} translatedReddit Profiletranslated {file_path} (JSONtranslated，translateduser_idtranslated)")
    
    # translated，translated
    def save_profiles_to_json(
        self,
        profiles: List[OasisAgentProfile],
        file_path: str,
        platform: str = "reddit"
    ):
        """[translated] translated save_profiles() translated"""
        logger.warning("save_profiles_to_jsontranslated，translatedsave_profilestranslated")
        self.save_profiles(profiles, file_path, platform)

