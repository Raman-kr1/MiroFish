"""
Ontology Generation Service
Interface 1: Analyzes text content and generates entity and relationship type definitions suitable for social simulation
"""

import json
from typing import Dict, Any, List, Optional
from ..utils.llm_client import LLMClient


# System prompt for ontology generation
ONTOLOGY_SYSTEM_PROMPT = """translated。translated，translated**translated**translated。

**translated：translatedJSONtranslated，translated。**

## translated

translated**translated**。translated：
- translated、translated、translated"translated"translated"translated"
- translated、translated、translated、translated
- translated

translated，**translated、translated**：

**translated**：
- translated（translated、translated、translated、translated、translated）
- translated、translated（translated）
- translated（translated、translated、NGO、translated）
- translated、translated
- translated（translated、translated、translated、translated）
- translated
- translated（translated、translated、translated）

**translated**：
- translated（translated"translated"、"translated"、"translated"）
- translated/translated（translated"translated"、"translated"）
- translated/translated（translated"translated"、"translated"）

## translated

translatedJSONtranslated，translated：

```json
{
    "entity_types": [
        {
            "name": "translated（translated，PascalCase）",
            "description": "translated（translated，translated100translated）",
            "attributes": [
                {
                    "name": "translated（translated，snake_case）",
                    "type": "text",
                    "description": "translated"
                }
            ],
            "examples": ["translated1", "translated2"]
        }
    ],
    "edge_types": [
        {
            "name": "translated（translated，UPPER_SNAKE_CASE）",
            "description": "translated（translated，translated100translated）",
            "source_targets": [
                {"source": "translated", "target": "translated"}
            ],
            "attributes": []
        }
    ],
    "analysis_summary": "translated（translated）"
}
```

## translated（translated！）

### 1. translated - translated

**translated：translated10translated**

**translated（translated）**：

translated10translated：

A. **translated（translated，translated2translated）**：
   - `Person`: translated。translated，translated。
   - `Organization`: translated。translated，translated。

B. **translated（8translated，translated）**：
   - translated，translated
   - translated：translated，translated `Student`, `Professor`, `University`
   - translated：translated，translated `Company`, `CEO`, `Employee`

**translated**：
- translated，translated"translated"、"translated"、"translated"
- translated，translated `Person`
- translated，translated、translated `Organization`

**translated**：
- translated
- translated，translated
- description translated

### 2. translated

- translated：6-10translated
- translated
- translated source_targets translated

### 3. translated

- translated1-3translated
- **translated**：translated `name`、`uuid`、`group_id`、`created_at`、`summary`（translated）
- translated：`full_name`, `title`, `role`, `position`, `location`, `description` translated

## translated

**translated（translated）**：
- Student: translated
- Professor: translated/translated
- Journalist: translated
- Celebrity: translated/translated
- Executive: translated
- Official: translated
- Lawyer: translated
- Doctor: translated

**translated（translated）**：
- Person: translated（translated）

**translated（translated）**：
- University: translated
- Company: translated
- GovernmentAgency: translated
- MediaOutlet: translated
- Hospital: translated
- School: translated
- NGO: translated

**translated（translated）**：
- Organization: translated（translated）

## translated

- WORKS_FOR: translated
- STUDIES_AT: translated
- AFFILIATED_WITH: translated
- REPRESENTS: translated
- REGULATES: translated
- REPORTS_ON: translated
- COMMENTS_ON: translated
- RESPONDS_TO: translated
- SUPPORTS: translated
- OPPOSES: translated
- COLLABORATES_WITH: translated
- COMPETES_WITH: translated
"""


class OntologyGenerator:
    """
    Ontology generator
    Analyzes text content and generates entity and relationship type definitions
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def generate(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate ontology definition
        
        Args:
            document_texts: List of document texts
            simulation_requirement: Description of the simulation requirement
            additional_context: Additional context
            
        Returns:
            Ontology definition (entity_types, edge_types, etc.)
        """
        # Build user message
        user_message = self._build_user_message(
            document_texts, 
            simulation_requirement,
            additional_context
        )
        
        messages = [
            {"role": "system", "content": ONTOLOGY_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
        
        # Call LLM
        result = self.llm_client.chat_json(
            messages=messages,
            temperature=0.3,
            max_tokens=4096
        )
        
        # Validate and post-process
        result = self._validate_and_process(result)
        
        return result
    
    # Maximum text length to send to LLM (50,000 characters)
    MAX_TEXT_LENGTH_FOR_LLM = 50000
    
    def _build_user_message(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str]
    ) -> str:
        """Build user message"""
        
        # Merge texts
        combined_text = "\n\n---\n\n".join(document_texts)
        original_length = len(combined_text)
        
        # If text exceeds 50,000 characters, truncate (only affects content sent to LLM, not graph construction)
        if len(combined_text) > self.MAX_TEXT_LENGTH_FOR_LLM:
            combined_text = combined_text[:self.MAX_TEXT_LENGTH_FOR_LLM]
            combined_text += f"\n\n...(translated{original_length}translated，translated{self.MAX_TEXT_LENGTH_FOR_LLM}translated)..."
        
        message = f"""## translated

{simulation_requirement}

## translated

{combined_text}
"""
        
        if additional_context:
            message += f"""
## translated

{additional_context}
"""
        
        message += """
translated，translated。

**translated**：
1. translated10translated
2. translated2translated：Person（translated）translated Organization（translated）
3. translated8translated
4. translated，translated
5. translated name、uuid、group_id translated，translated full_name、org_name translated
"""
        
        return message
    
    def _validate_and_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and post-process result"""
        
        # Ensure required fields exist
        if "entity_types" not in result:
            result["entity_types"] = []
        if "edge_types" not in result:
            result["edge_types"] = []
        if "analysis_summary" not in result:
            result["analysis_summary"] = ""
        
        # Validate entity types
        for entity in result["entity_types"]:
            if "attributes" not in entity:
                entity["attributes"] = []
            if "examples" not in entity:
                entity["examples"] = []
            # Ensure description does not exceed 100 characters
            if len(entity.get("description", "")) > 100:
                entity["description"] = entity["description"][:97] + "..."
        
        # Validate relationship types
        for edge in result["edge_types"]:
            if "source_targets" not in edge:
                edge["source_targets"] = []
            if "attributes" not in edge:
                edge["attributes"] = []
            if len(edge.get("description", "")) > 100:
                edge["description"] = edge["description"][:97] + "..."
        
        # Zep API limit: max 10 custom entity types, max 10 custom edge types
        MAX_ENTITY_TYPES = 10
        MAX_EDGE_TYPES = 10
        
        # Fallback type definitions
        person_fallback = {
            "name": "Person",
            "description": "Any individual person not fitting other specific person types.",
            "attributes": [
                {"name": "full_name", "type": "text", "description": "Full name of the person"},
                {"name": "role", "type": "text", "description": "Role or occupation"}
            ],
            "examples": ["ordinary citizen", "anonymous netizen"]
        }
        
        organization_fallback = {
            "name": "Organization",
            "description": "Any organization not fitting other specific organization types.",
            "attributes": [
                {"name": "org_name", "type": "text", "description": "Name of the organization"},
                {"name": "org_type", "type": "text", "description": "Type of organization"}
            ],
            "examples": ["small business", "community group"]
        }
        
        # Check if fallback types already exist
        entity_names = {e["name"] for e in result["entity_types"]}
        has_person = "Person" in entity_names
        has_organization = "Organization" in entity_names
        
        # Fallback types to add
        fallbacks_to_add = []
        if not has_person:
            fallbacks_to_add.append(person_fallback)
        if not has_organization:
            fallbacks_to_add.append(organization_fallback)
        
        if fallbacks_to_add:
            current_count = len(result["entity_types"])
            needed_slots = len(fallbacks_to_add)
            
            # If adding would exceed 10, remove some existing types
            if current_count + needed_slots > MAX_ENTITY_TYPES:
                # Calculate how many to remove
                to_remove = current_count + needed_slots - MAX_ENTITY_TYPES
                # Remove from the end (preserving more important specific types at the front)
                result["entity_types"] = result["entity_types"][:-to_remove]
            
            # Add fallback types
            result["entity_types"].extend(fallbacks_to_add)
        
        # Final check to not exceed the limit (defensive programming)
        if len(result["entity_types"]) > MAX_ENTITY_TYPES:
            result["entity_types"] = result["entity_types"][:MAX_ENTITY_TYPES]
        
        if len(result["edge_types"]) > MAX_EDGE_TYPES:
            result["edge_types"] = result["edge_types"][:MAX_EDGE_TYPES]
        
        return result
    
    def generate_python_code(self, ontology: Dict[str, Any]) -> str:
        """
        Convert ontology definition to Python code (similar to ontology.py)
        
        Args:
            ontology: Ontology definition
            
        Returns:
            Python code string
        """
        code_lines = [
            '"""',
            'Custom entity type definitions',
            'Auto-generated by MiroFish for social opinion simulation',
            '"""',
            '',
            'from pydantic import Field',
            'from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel',
            '',
            '',
            '# ============== Entity Type Definitions ==============',
            '',
        ]
        
        # Generate entity types
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            desc = entity.get("description", f"A {name} entity.")
            
            code_lines.append(f'class {name}(EntityModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = entity.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        code_lines.append('# ============== Relationship Type Definitions ==============')
        code_lines.append('')
        
        # Generate relationship types
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            # Convert to PascalCase class name
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            desc = edge.get("description", f"A {name} relationship.")
            
            code_lines.append(f'class {class_name}(EdgeModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = edge.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        # Generate type dictionaries
        code_lines.append('# ============== Type Configuration ==============')
        code_lines.append('')
        code_lines.append('ENTITY_TYPES = {')
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            code_lines.append(f'    "{name}": {name},')
        code_lines.append('}')
        code_lines.append('')
        code_lines.append('EDGE_TYPES = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            code_lines.append(f'    "{name}": {class_name},')
        code_lines.append('}')
        code_lines.append('')
        
        # Generate edge source_targets mapping
        code_lines.append('EDGE_SOURCE_TARGETS = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            source_targets = edge.get("source_targets", [])
            if source_targets:
                st_list = ', '.join([
                    f'{{"source": "{st.get("source", "Entity")}", "target": "{st.get("target", "Entity")}"}}'
                    for st in source_targets
                ])
                code_lines.append(f'    "{name}": [{st_list}],')
        code_lines.append('}')
        
        return '\n'.join(code_lines)

