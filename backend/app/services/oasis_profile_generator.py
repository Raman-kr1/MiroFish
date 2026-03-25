"""
OASIS Agent Profileconverted
convertedZepconvertedOASISconvertedAgent Profileconverted

details：
1. convertedZepconverted
2. details
3. details
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
    """OASIS Agent Profileconverted"""
    # details
    user_id: int
    user_name: str
    name: str
    bio: str
    persona: str
    
    # details - Redditconverted
    karma: int = 1000
    
    # details - Twitterconverted
    friend_count: int = 100
    follower_count: int = 150
    statuses_count: int = 500
    
    # details
    age: Optional[int] = None
    gender: Optional[str] = None
    mbti: Optional[str] = None
    country: Optional[str] = None
    profession: Optional[str] = None
    interested_topics: List[str] = field(default_factory=list)
    
    # details
    source_entity_uuid: Optional[str] = None
    source_entity_type: Optional[str] = None
    
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    def to_reddit_format(self) -> Dict[str, Any]:
        """convertedRedditconverted"""
        profile = {
            "user_id": self.user_id,
            "username": self.user_name,  # OASIS details username（details）
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "karma": self.karma,
            "created_at": self.created_at,
        }
        
        # details（details）
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
        """convertedTwitterconverted"""
        profile = {
            "user_id": self.user_id,
            "username": self.user_name,  # OASIS details username（details）
            "name": self.name,
            "bio": self.bio,
            "persona": self.persona,
            "friend_count": self.friend_count,
            "follower_count": self.follower_count,
            "statuses_count": self.statuses_count,
            "created_at": self.created_at,
        }
        
        # details
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
        """details"""
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
    OASIS Profileconverted
    
    convertedZepconvertedOASISconvertedAgent Profile
    
    details：
    1. convertedZepconverted
    2. details（details、details、details、details）
    3. details
    """
    
    # MBTIconverted
    MBTI_TYPES = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP"
    ]
    
    # details
    COUNTRIES = [
        "China", "US", "UK", "Japan", "Germany", "France", 
        "Canada", "Australia", "Brazil", "India", "South Korea"
    ]
    
    # details（details）
    INDIVIDUAL_ENTITY_TYPES = [
        "student", "alumni", "professor", "person", "publicfigure", 
        "expert", "faculty", "official", "journalist", "activist"
    ]
    
    # details/details（details）
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
            raise ValueError("LLM_API_KEY details")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # Zepconverted
        self.zep_api_key = zep_api_key or Config.ZEP_API_KEY
        self.zep_client = None
        self.graph_id = graph_id
        
        if self.zep_api_key:
            try:
                self.zep_client = Zep(api_key=self.zep_api_key)
            except Exception as e:
                logger.warning(f"Zepconverted: {e}")
    
    def generate_profile_from_entity(
        self, 
        entity: EntityNode, 
        user_id: int,
        use_llm: bool = True
    ) -> OasisAgentProfile:
        """
        convertedZepconvertedOASIS Agent Profile
        
        Args:
            entity: Zepconverted
            user_id: convertedID（convertedOASIS）
            use_llm: convertedLLMconverted
            
        Returns:
            OasisAgentProfile
        """
        entity_type = entity.get_entity_type() or "Entity"
        
        # details
        name = entity.name
        user_name = self._generate_username(name)
        
        # details
        context = self._build_entity_context(entity)
        
        if use_llm:
            # convertedLLMconverted
            profile_data = self._generate_profile_with_llm(
                entity_name=name,
                entity_type=entity_type,
                entity_summary=entity.summary,
                entity_attributes=entity.attributes,
                context=context
            )
        else:
            # details
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
        """details"""
        # details，details
        username = name.lower().replace(" ", "_")
        username = ''.join(c for c in username if c.isalnum() or c == '_')
        
        # details
        suffix = random.randint(100, 999)
        return f"{username}_{suffix}"
    
    def _search_zep_for_entity(self, entity: EntityNode) -> Dict[str, Any]:
        """
        convertedZepconverted
        
        Zepconverted，convertededgesconvertednodesconverted。
        details，details。
        
        Args:
            entity: details
            
        Returns:
            convertedfacts, node_summaries, contextconverted
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
        
        # convertedgraph_idconverted
        if not self.graph_id:
            logger.debug(f"convertedZepconverted：convertedgraph_id")
            return results
        
        comprehensive_query = f"details{entity_name}details、details、details、details"
        
        def search_edges():
            """details（details/details）- details"""
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
                        logger.debug(f"Zepconverted {attempt + 1} details: {str(e)[:80]}, details...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.debug(f"Zepconverted {max_retries} details: {e}")
            return None
        
        def search_nodes():
            """details（details）- details"""
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
                        logger.debug(f"Zepconverted {attempt + 1} details: {str(e)[:80]}, details...")
                        time.sleep(delay)
                        delay *= 2
                    else:
                        logger.debug(f"Zepconverted {max_retries} details: {e}")
            return None
        
        try:
            # convertededgesconvertednodesconverted
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                edge_future = executor.submit(search_edges)
                node_future = executor.submit(search_nodes)
                
                # details
                edge_result = edge_future.result(timeout=30)
                node_result = node_future.result(timeout=30)
            
            # details
            all_facts = set()
            if edge_result and hasattr(edge_result, 'edges') and edge_result.edges:
                for edge in edge_result.edges:
                    if hasattr(edge, 'fact') and edge.fact:
                        all_facts.add(edge.fact)
            results["facts"] = list(all_facts)
            
            # details
            all_summaries = set()
            if node_result and hasattr(node_result, 'nodes') and node_result.nodes:
                for node in node_result.nodes:
                    if hasattr(node, 'summary') and node.summary:
                        all_summaries.add(node.summary)
                    if hasattr(node, 'name') and node.name and node.name != entity_name:
                        all_summaries.add(f"details: {node.name}")
            results["node_summaries"] = list(all_summaries)
            
            # details
            context_parts = []
            if results["facts"]:
                context_parts.append("details:\n" + "\n".join(f"- {f}" for f in results["facts"][:20]))
            if results["node_summaries"]:
                context_parts.append("details:\n" + "\n".join(f"- {s}" for s in results["node_summaries"][:10]))
            results["context"] = "\n\n".join(context_parts)
            
            logger.info(f"Zepconverted: {entity_name}, details {len(results['facts'])} details, {len(results['node_summaries'])} details")
            
        except concurrent.futures.TimeoutError:
            logger.warning(f"Zepconverted ({entity_name})")
        except Exception as e:
            logger.warning(f"Zepconverted ({entity_name}): {e}")
        
        return results
    
    def _build_entity_context(self, entity: EntityNode) -> str:
        """
        details
        
        details：
        1. details（details）
        2. details
        3. Zepconverted
        """
        context_parts = []
        
        # 1. details
        if entity.attributes:
            attrs = []
            for key, value in entity.attributes.items():
                if value and str(value).strip():
                    attrs.append(f"- {key}: {value}")
            if attrs:
                context_parts.append("### details\n" + "\n".join(attrs))
        
        # 2. details（details/details）
        existing_facts = set()
        if entity.related_edges:
            relationships = []
            for edge in entity.related_edges:  # details
                fact = edge.get("fact", "")
                edge_name = edge.get("edge_name", "")
                direction = edge.get("direction", "")
                
                if fact:
                    relationships.append(f"- {fact}")
                    existing_facts.add(fact)
                elif edge_name:
                    if direction == "outgoing":
                        relationships.append(f"- {entity.name} --[{edge_name}]--> (details)")
                    else:
                        relationships.append(f"- (details) --[{edge_name}]--> {entity.name}")
            
            if relationships:
                context_parts.append("### details\n" + "\n".join(relationships))
        
        # 3. details
        if entity.related_nodes:
            related_info = []
            for node in entity.related_nodes:  # details
                node_name = node.get("name", "")
                node_labels = node.get("labels", [])
                node_summary = node.get("summary", "")
                
                # details
                custom_labels = [l for l in node_labels if l not in ["Entity", "Node"]]
                label_str = f" ({', '.join(custom_labels)})" if custom_labels else ""
                
                if node_summary:
                    related_info.append(f"- **{node_name}**{label_str}: {node_summary}")
                else:
                    related_info.append(f"- **{node_name}**{label_str}")
            
            if related_info:
                context_parts.append("### details\n" + "\n".join(related_info))
        
        # 4. convertedZepconverted
        zep_results = self._search_zep_for_entity(entity)
        
        if zep_results.get("facts"):
            # details：details
            new_facts = [f for f in zep_results["facts"] if f not in existing_facts]
            if new_facts:
                context_parts.append("### Zepconverted\n" + "\n".join(f"- {f}" for f in new_facts[:15]))
        
        if zep_results.get("node_summaries"):
            context_parts.append("### Zepconverted\n" + "\n".join(f"- {s}" for s in zep_results["node_summaries"][:10]))
        
        return "\n\n".join(context_parts)
    
    def _is_individual_entity(self, entity_type: str) -> bool:
        """details"""
        return entity_type.lower() in self.INDIVIDUAL_ENTITY_TYPES
    
    def _is_group_entity(self, entity_type: str) -> bool:
        """details/details"""
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
        convertedLLMconverted
        
        details：
        - details：details
        - details/details：details
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

        # details，details
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
                    temperature=0.7 - (attempt * 0.1)  # details
                    # convertedmax_tokens，convertedLLMconverted
                )
                
                content = response.choices[0].message.content
                
                # details（finish_reasonconverted'stop'）
                finish_reason = response.choices[0].finish_reason
                if finish_reason == 'length':
                    logger.warning(f"LLMconverted (attempt {attempt+1}), details...")
                    content = self._fix_truncated_json(content)
                
                # convertedJSON
                try:
                    result = json.loads(content)
                    
                    # details
                    if "bio" not in result or not result["bio"]:
                        result["bio"] = entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}"
                    if "persona" not in result or not result["persona"]:
                        result["persona"] = entity_summary or f"{entity_name}details{entity_type}。"
                    
                    return result
                    
                except json.JSONDecodeError as je:
                    logger.warning(f"JSONconverted (attempt {attempt+1}): {str(je)[:80]}")
                    
                    # convertedJSON
                    result = self._try_fix_json(content, entity_name, entity_type, entity_summary)
                    if result.get("_fixed"):
                        del result["_fixed"]
                        return result
                    
                    last_error = je
                    
            except Exception as e:
                logger.warning(f"LLMconverted (attempt {attempt+1}): {str(e)[:80]}")
                last_error = e
                import time
                time.sleep(1 * (attempt + 1))  # details
        
        logger.warning(f"LLMconverted（{max_attempts}details）: {last_error}, details")
        return self._generate_profile_rule_based(
            entity_name, entity_type, entity_summary, entity_attributes
        )
    
    def _fix_truncated_json(self, content: str) -> str:
        """convertedJSON（convertedmax_tokensconverted）"""
        import re
        
        # convertedJSONconverted，details
        content = content.strip()
        
        # details
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        # details
        # details：details，details
        if content and content[-1] not in '",}]':
            # details
            content += '"'
        
        # details
        content += ']' * open_brackets
        content += '}' * open_braces
        
        return content
    
    def _try_fix_json(self, content: str, entity_name: str, entity_type: str, entity_summary: str = "") -> Dict[str, Any]:
        """convertedJSON"""
        import re
        
        # 1. details
        content = self._fix_truncated_json(content)
        
        # 2. convertedJSONconverted
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            json_str = json_match.group()
            
            # 3. details
            # details
            def fix_string_newlines(match):
                s = match.group(0)
                # details
                s = s.replace('\n', ' ').replace('\r', ' ')
                # details
                s = re.sub(r'\s+', ' ', s)
                return s
            
            # convertedJSONconverted
            json_str = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', fix_string_newlines, json_str)
            
            # 4. details
            try:
                result = json.loads(json_str)
                result["_fixed"] = True
                return result
            except json.JSONDecodeError as e:
                # 5. details，details
                try:
                    # details
                    json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                    # details
                    json_str = re.sub(r'\s+', ' ', json_str)
                    result = json.loads(json_str)
                    result["_fixed"] = True
                    return result
                except:
                    pass
        
        # 6. details
        bio_match = re.search(r'"bio"\s*:\s*"([^"]*)"', content)
        persona_match = re.search(r'"persona"\s*:\s*"([^"]*)', content)  # details
        
        bio = bio_match.group(1) if bio_match else (entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}")
        persona = persona_match.group(1) if persona_match else (entity_summary or f"{entity_name}details{entity_type}。")
        
        # details，details
        if bio_match or persona_match:
            logger.info(f"convertedJSONconverted")
            return {
                "bio": bio,
                "persona": persona,
                "_fixed": True
            }
        
        # 7. details，details
        logger.warning(f"JSONconverted，details")
        return {
            "bio": entity_summary[:200] if entity_summary else f"{entity_type}: {entity_name}",
            "persona": entity_summary or f"{entity_name}details{entity_type}。"
        }
    
    def _get_system_prompt(self, is_individual: bool) -> str:
        """details"""
        base_prompt = "details。details、details,details。convertedJSONconverted，details。details。"
        return base_prompt
    
    def _build_individual_persona_prompt(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any],
        context: str
    ) -> str:
        """details"""
        
        attrs_str = json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "details"
        context_str = context[:3000] if context else "details"
        
        return f"""details,details。

details: {entity_name}
details: {entity_type}
details: {entity_summary}
details: {attrs_str}

details:
{context_str}

convertedJSON，details:

1. bio: details，200converted
2. persona: details（2000converted），details:
   - details（details、details、details、details）
   - details（details、details、details）
   - details（MBTIconverted、details、details）
   - details（details、details、details、details）
   - details（details、details/details）
   - details（details、details、details）
   - details（details，details，details）
3. age: details（details）
4. gender: details，details: "male" details "female"
5. mbti: MBTIconverted（convertedINTJ、ENFPconverted）
6. country: details（details，details"details"）
7. profession: details
8. interested_topics: details

details:
- details，details
- personaconverted
- details（convertedgenderconvertedmale/female）
- details
- ageconverted，genderconverted"male"details"female"
"""

    def _build_group_persona_prompt(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any],
        context: str
    ) -> str:
        """details/details"""
        
        attrs_str = json.dumps(entity_attributes, ensure_ascii=False) if entity_attributes else "details"
        context_str = context[:3000] if context else "details"
        
        return f"""details/details,details。

details: {entity_name}
details: {entity_type}
details: {entity_summary}
details: {attrs_str}

details:
{context_str}

convertedJSON，details:

1. bio: details，200converted，details
2. persona: details（2000converted），details:
   - details（details、details、details、details）
   - details（details、details、details）
   - details（details、details、details）
   - details（details、details、details）
   - details（details、details）
   - details（details、details）
   - details（details，details，details）
3. age: converted30（details）
4. gender: details"other"（convertedotherconverted）
5. mbti: MBTIconverted，details，convertedISTJconverted
6. country: details（details，details"details"）
7. profession: details
8. interested_topics: details

details:
- details，convertednullconverted
- personaconverted，details
- details（convertedgenderconverted"other"）
- ageconverted30，genderconverted"other"
- details"""
    
    def _generate_profile_rule_based(
        self,
        entity_name: str,
        entity_type: str,
        entity_summary: str,
        entity_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """details"""
        
        # details
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
                "age": 30,  # details
                "gender": "other",  # convertedother
                "mbti": "ISTJ",  # details：details
                "country": "details",
                "profession": "Media",
                "interested_topics": ["General News", "Current Events", "Public Affairs"],
            }
        
        elif entity_type_lower in ["university", "governmentagency", "ngo", "organization"]:
            return {
                "bio": f"Official account of {entity_name}.",
                "persona": f"{entity_name} is an institutional entity that communicates official positions, announcements, and engages with stakeholders on relevant matters.",
                "age": 30,  # details
                "gender": "other",  # convertedother
                "mbti": "ISTJ",  # details：details
                "country": "details",
                "profession": entity_type,
                "interested_topics": ["Public Policy", "Community", "Official Announcements"],
            }
        
        else:
            # details
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
        """convertedIDconvertedZepconverted"""
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
        convertedAgent Profile（details）
        
        Args:
            entities: details
            use_llm: convertedLLMconverted
            progress_callback: details (current, total, message)
            graph_id: convertedID，convertedZepconverted
            parallel_count: details，converted5
            realtime_output_path: details（details，details）
            output_platform: details ("reddit" details "twitter")
            
        Returns:
            Agent Profileconverted
        """
        import concurrent.futures
        from threading import Lock
        
        # convertedgraph_idconvertedZepconverted
        if graph_id:
            self.graph_id = graph_id
        
        total = len(entities)
        profiles = [None] * total  # details
        completed_count = [0]  # details
        lock = Lock()
        
        # details
        def save_profiles_realtime():
            """details profiles details"""
            if not realtime_output_path:
                return
            
            with lock:
                # details profiles
                existing_profiles = [p for p in profiles if p is not None]
                if not existing_profiles:
                    return
                
                try:
                    if output_platform == "reddit":
                        # Reddit JSON details
                        profiles_data = [p.to_reddit_format() for p in existing_profiles]
                        with open(realtime_output_path, 'w', encoding='utf-8') as f:
                            json.dump(profiles_data, f, ensure_ascii=False, indent=2)
                    else:
                        # Twitter CSV details
                        import csv
                        profiles_data = [p.to_twitter_format() for p in existing_profiles]
                        if profiles_data:
                            fieldnames = list(profiles_data[0].keys())
                            with open(realtime_output_path, 'w', encoding='utf-8', newline='') as f:
                                writer = csv.DictWriter(f, fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerows(profiles_data)
                except Exception as e:
                    logger.warning(f"details profiles details: {e}")
        
        def generate_single_profile(idx: int, entity: EntityNode) -> tuple:
            """convertedprofileconverted"""
            entity_type = entity.get_entity_type() or "Entity"
            
            try:
                profile = self.generate_profile_from_entity(
                    entity=entity,
                    user_id=idx,
                    use_llm=use_llm
                )
                
                # details
                self._print_generated_profile(entity.name, entity_type, profile)
                
                return idx, profile, None
                
            except Exception as e:
                logger.error(f"details {entity.name} details: {str(e)}")
                # convertedprofile
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
        
        logger.info(f"details {total} convertedAgentconverted（details: {parallel_count}）...")
        print(f"\n{'='*60}")
        print(f"convertedAgentconverted - details {total} details，details: {parallel_count}")
        print(f"{'='*60}\n")
        
        # details
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallel_count) as executor:
            # details
            future_to_entity = {
                executor.submit(generate_single_profile, idx, entity): (idx, entity)
                for idx, entity in enumerate(entities)
            }
            
            # details
            for future in concurrent.futures.as_completed(future_to_entity):
                idx, entity = future_to_entity[future]
                entity_type = entity.get_entity_type() or "Entity"
                
                try:
                    result_idx, profile, error = future.result()
                    profiles[result_idx] = profile
                    
                    with lock:
                        completed_count[0] += 1
                        current = completed_count[0]
                    
                    # details
                    save_profiles_realtime()
                    
                    if progress_callback:
                        progress_callback(
                            current, 
                            total, 
                            f"details {current}/{total}: {entity.name}（{entity_type}）"
                        )
                    
                    if error:
                        logger.warning(f"[{current}/{total}] {entity.name} details: {error}")
                    else:
                        logger.info(f"[{current}/{total}] details: {entity.name} ({entity_type})")
                        
                except Exception as e:
                    logger.error(f"details {entity.name} details: {str(e)}")
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
                    # details（details）
                    save_profiles_realtime()
        
        print(f"\n{'='*60}")
        print(f"details！details {len([p for p in profiles if p])} convertedAgent")
        print(f"{'='*60}\n")
        
        return profiles
    
    def _print_generated_profile(self, entity_name: str, entity_type: str, profile: OasisAgentProfile):
        """details（details，details）"""
        separator = "-" * 70
        
        # details（details）
        topics_str = ', '.join(profile.interested_topics) if profile.interested_topics else 'details'
        
        output_lines = [
            f"\n{separator}",
            f"[details] {entity_name} ({entity_type})",
            f"{separator}",
            f"details: {profile.user_name}",
            f"",
            f"【details】",
            f"{profile.bio}",
            f"",
            f"【details】",
            f"{profile.persona}",
            f"",
            f"【details】",
            f"details: {profile.age} | details: {profile.gender} | MBTI: {profile.mbti}",
            f"details: {profile.profession} | details: {profile.country}",
            f"details: {topics_str}",
            separator
        ]
        
        output = "\n".join(output_lines)
        
        # details（details，loggerconverted）
        print(output)
    
    def save_profiles(
        self,
        profiles: List[OasisAgentProfile],
        file_path: str,
        platform: str = "reddit"
    ):
        """
        convertedProfileconverted（details）
        
        OASISconverted：
        - Twitter: CSVconverted
        - Reddit: JSONconverted
        
        Args:
            profiles: Profileconverted
            file_path: details
            platform: details ("reddit" details "twitter")
        """
        if platform == "twitter":
            self._save_twitter_csv(profiles, file_path)
        else:
            self._save_reddit_json(profiles, file_path)
    
    def _save_twitter_csv(self, profiles: List[OasisAgentProfile], file_path: str):
        """
        convertedTwitter ProfileconvertedCSVconverted（convertedOASISconverted）
        
        OASIS TwitterconvertedCSVconverted：
        - user_id: convertedID（convertedCSVconverted0converted）
        - name: details
        - username: details
        - user_char: details（convertedLLMconverted，convertedAgentconverted）
        - description: details（details）
        
        user_char vs description details：
        - user_char: details，LLMconverted，convertedAgentconverted
        - description: details，details
        """
        import csv
        
        # details.csv
        if not file_path.endswith('.csv'):
            file_path = file_path.replace('.json', '.csv')
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # convertedOASISconverted
            headers = ['user_id', 'name', 'username', 'user_char', 'description']
            writer.writerow(headers)
            
            # details
            for idx, profile in enumerate(profiles):
                # user_char: details（bio + persona），convertedLLMconverted
                user_char = profile.bio
                if profile.persona and profile.persona != profile.bio:
                    user_char = f"{profile.bio} {profile.persona}"
                # details（CSVconverted）
                user_char = user_char.replace('\n', ' ').replace('\r', ' ')
                
                # description: details，details
                description = profile.bio.replace('\n', ' ').replace('\r', ' ')
                
                row = [
                    idx,                    # user_id: converted0convertedID
                    profile.name,           # name: details
                    profile.user_name,      # username: details
                    user_char,              # user_char: details（convertedLLMconverted）
                    description             # description: details（details）
                ]
                writer.writerow(row)
        
        logger.info(f"details {len(profiles)} convertedTwitter Profileconverted {file_path} (OASIS CSVconverted)")
    
    def _normalize_gender(self, gender: Optional[str]) -> str:
        """
        convertedgenderconvertedOASISconverted
        
        OASISconverted: male, female, other
        """
        if not gender:
            return "other"
        
        gender_lower = gender.lower().strip()
        
        # details
        gender_map = {
            "details": "male",
            "details": "female",
            "details": "other",
            "details": "other",
            # details
            "male": "male",
            "female": "female",
            "other": "other",
        }
        
        return gender_map.get(gender_lower, "other")
    
    def _save_reddit_json(self, profiles: List[OasisAgentProfile], file_path: str):
        """
        convertedReddit ProfileconvertedJSONconverted
        
        details to_reddit_format() details，details OASIS details。
        details user_id details，details OASIS agent_graph.get_agent() details！
        
        details：
        - user_id: convertedID（details，details initial_posts details poster_agent_id）
        - username: details
        - name: details
        - bio: details
        - persona: details
        - age: details（details）
        - gender: "male", "female", details "other"
        - mbti: MBTIconverted
        - country: details
        """
        data = []
        for idx, profile in enumerate(profiles):
            # details to_reddit_format() details
            item = {
                "user_id": profile.user_id if profile.user_id is not None else idx,  # details：details user_id
                "username": profile.user_name,
                "name": profile.name,
                "bio": profile.bio[:150] if profile.bio else f"{profile.name}",
                "persona": profile.persona or f"{profile.name} is a participant in social discussions.",
                "karma": profile.karma if profile.karma else 1000,
                "created_at": profile.created_at,
                # OASISconverted - details
                "age": profile.age if profile.age else 30,
                "gender": self._normalize_gender(profile.gender),
                "mbti": profile.mbti if profile.mbti else "ISTJ",
                "country": profile.country if profile.country else "details",
            }
            
            # details
            if profile.profession:
                item["profession"] = profile.profession
            if profile.interested_topics:
                item["interested_topics"] = profile.interested_topics
            
            data.append(item)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"details {len(profiles)} convertedReddit Profileconverted {file_path} (JSONconverted，converteduser_idconverted)")
    
    # details，details
    def save_profiles_to_json(
        self,
        profiles: List[OasisAgentProfile],
        file_path: str,
        platform: str = "reddit"
    ):
        """[details] details save_profiles() details"""
        logger.warning("save_profiles_to_jsonconverted，convertedsave_profilesconverted")
        self.save_profiles(profiles, file_path, platform)

