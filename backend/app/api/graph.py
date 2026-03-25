"""
translatedAPItranslated
translated，translated
"""

import os
import traceback
import threading
from flask import request, jsonify

from . import graph_bp
from ..config import Config
from ..services.ontology_generator import OntologyGenerator
from ..services.graph_builder import GraphBuilderService
from ..services.text_processor import TextProcessor
from ..utils.file_parser import FileParser
from ..utils.logger import get_logger
from ..models.task import TaskManager, TaskStatus
from ..models.project import ProjectManager, ProjectStatus

# translated
logger = get_logger('mirofish.api')


def allowed_file(filename: str) -> bool:
    """translated"""
    if not filename or '.' not in filename:
        return False
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    return ext in Config.ALLOWED_EXTENSIONS


# ============== translated ==============

@graph_bp.route('/project/<project_id>', methods=['GET'])
def get_project(project_id: str):
    """
    translated
    """
    project = ProjectManager.get_project(project_id)
    
    if not project:
        return jsonify({
            "success": False,
            "error": f"translated: {project_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "data": project.to_dict()
    })


@graph_bp.route('/project/list', methods=['GET'])
def list_projects():
    """
    translated
    """
    limit = request.args.get('limit', 50, type=int)
    projects = ProjectManager.list_projects(limit=limit)
    
    return jsonify({
        "success": True,
        "data": [p.to_dict() for p in projects],
        "count": len(projects)
    })


@graph_bp.route('/project/<project_id>', methods=['DELETE'])
def delete_project(project_id: str):
    """
    translated
    """
    success = ProjectManager.delete_project(project_id)
    
    if not success:
        return jsonify({
            "success": False,
            "error": f"translated: {project_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "message": f"translated: {project_id}"
    })


@graph_bp.route('/project/<project_id>/reset', methods=['POST'])
def reset_project(project_id: str):
    """
    translated（translated）
    """
    project = ProjectManager.get_project(project_id)
    
    if not project:
        return jsonify({
            "success": False,
            "error": f"translated: {project_id}"
        }), 404
    
    # translated
    if project.ontology:
        project.status = ProjectStatus.ONTOLOGY_GENERATED
    else:
        project.status = ProjectStatus.CREATED
    
    project.graph_id = None
    project.graph_build_task_id = None
    project.error = None
    ProjectManager.save_project(project)
    
    return jsonify({
        "success": True,
        "message": f"translated: {project_id}",
        "data": project.to_dict()
    })


# ============== translated1：translated ==============

@graph_bp.route('/ontology/generate', methods=['POST'])
def generate_ontology():
    """
    translated1：translated，translated
    
    translated：multipart/form-data
    
    translated：
        files: translated（PDF/MD/TXT），translated
        simulation_requirement: translated（translated）
        project_name: translated（translated）
        additional_context: translated（translated）
        
    translated：
        {
            "success": true,
            "data": {
                "project_id": "proj_xxxx",
                "ontology": {
                    "entity_types": [...],
                    "edge_types": [...],
                    "analysis_summary": "..."
                },
                "files": [...],
                "total_text_length": 12345
            }
        }
    """
    try:
        logger.info("=== translated ===")
        
        # translated
        simulation_requirement = request.form.get('simulation_requirement', '')
        project_name = request.form.get('project_name', 'Unnamed Project')
        additional_context = request.form.get('additional_context', '')
        
        logger.debug(f"translated: {project_name}")
        logger.debug(f"translated: {simulation_requirement[:100]}...")
        
        if not simulation_requirement:
            return jsonify({
                "success": False,
                "error": "translated (simulation_requirement)"
            }), 400
        
        # translated
        uploaded_files = request.files.getlist('files')
        if not uploaded_files or all(not f.filename for f in uploaded_files):
            return jsonify({
                "success": False,
                "error": "translated"
            }), 400
        
        # translated
        project = ProjectManager.create_project(name=project_name)
        project.simulation_requirement = simulation_requirement
        logger.info(f"translated: {project.project_id}")
        
        # translated
        document_texts = []
        all_text = ""
        
        for file in uploaded_files:
            if file and file.filename and allowed_file(file.filename):
                # translated
                file_info = ProjectManager.save_file_to_project(
                    project.project_id, 
                    file, 
                    file.filename
                )
                project.files.append({
                    "filename": file_info["original_filename"],
                    "size": file_info["size"]
                })
                
                # translated
                text = FileParser.extract_text(file_info["path"])
                text = TextProcessor.preprocess_text(text)
                document_texts.append(text)
                all_text += f"\n\n=== {file_info['original_filename']} ===\n{text}"
        
        if not document_texts:
            ProjectManager.delete_project(project.project_id)
            return jsonify({
                "success": False,
                "error": "translated，translated"
            }), 400
        
        # translated
        project.total_text_length = len(all_text)
        ProjectManager.save_extracted_text(project.project_id, all_text)
        logger.info(f"translated，translated {len(all_text)} translated")
        
        # translated
        logger.info("translated LLM translated...")
        generator = OntologyGenerator()
        ontology = generator.generate(
            document_texts=document_texts,
            simulation_requirement=simulation_requirement,
            additional_context=additional_context if additional_context else None
        )
        
        # translated
        entity_count = len(ontology.get("entity_types", []))
        edge_count = len(ontology.get("edge_types", []))
        logger.info(f"translated: {entity_count} translated, {edge_count} translated")
        
        project.ontology = {
            "entity_types": ontology.get("entity_types", []),
            "edge_types": ontology.get("edge_types", [])
        }
        project.analysis_summary = ontology.get("analysis_summary", "")
        project.status = ProjectStatus.ONTOLOGY_GENERATED
        ProjectManager.save_project(project)
        logger.info(f"=== translated === translatedID: {project.project_id}")
        
        return jsonify({
            "success": True,
            "data": {
                "project_id": project.project_id,
                "project_name": project.name,
                "ontology": project.ontology,
                "analysis_summary": project.analysis_summary,
                "files": project.files,
                "total_text_length": project.total_text_length
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


# ============== translated2：translated ==============

@graph_bp.route('/build', methods=['POST'])
def build_graph():
    """
    translated2：translatedproject_idtranslated
    
    translated（JSON）：
        {
            "project_id": "proj_xxxx",  // translated，translated1
            "graph_name": "translated",    // translated
            "chunk_size": 500,          // translated，translated500
            "chunk_overlap": 50         // translated，translated50
        }
        
    translated：
        {
            "success": true,
            "data": {
                "project_id": "proj_xxxx",
                "task_id": "task_xxxx",
                "message": "translated"
            }
        }
    """
    try:
        logger.info("=== translated ===")
        
        # translated
        errors = []
        if not Config.ZEP_API_KEY:
            errors.append("ZEP_API_KEYtranslated")
        if errors:
            logger.error(f"translated: {errors}")
            return jsonify({
                "success": False,
                "error": "translated: " + "; ".join(errors)
            }), 500
        
        # translated
        data = request.get_json() or {}
        project_id = data.get('project_id')
        logger.debug(f"translated: project_id={project_id}")
        
        if not project_id:
            return jsonify({
                "success": False,
                "error": "translated project_id"
            }), 400
        
        # translated
        project = ProjectManager.get_project(project_id)
        if not project:
            return jsonify({
                "success": False,
                "error": f"translated: {project_id}"
            }), 404
        
        # translated
        force = data.get('force', False)  # translated
        
        if project.status == ProjectStatus.CREATED:
            return jsonify({
                "success": False,
                "error": "translated，translated /ontology/generate"
            }), 400
        
        if project.status == ProjectStatus.GRAPH_BUILDING and not force:
            return jsonify({
                "success": False,
                "error": "translated，translated。translated，translated force: true",
                "task_id": project.graph_build_task_id
            }), 400
        
        # translated，translated
        if force and project.status in [ProjectStatus.GRAPH_BUILDING, ProjectStatus.FAILED, ProjectStatus.GRAPH_COMPLETED]:
            project.status = ProjectStatus.ONTOLOGY_GENERATED
            project.graph_id = None
            project.graph_build_task_id = None
            project.error = None
        
        # translated
        graph_name = data.get('graph_name', project.name or 'MiroFish Graph')
        chunk_size = data.get('chunk_size', project.chunk_size or Config.DEFAULT_CHUNK_SIZE)
        chunk_overlap = data.get('chunk_overlap', project.chunk_overlap or Config.DEFAULT_CHUNK_OVERLAP)
        
        # translated
        project.chunk_size = chunk_size
        project.chunk_overlap = chunk_overlap
        
        # translated
        text = ProjectManager.get_extracted_text(project_id)
        if not text:
            return jsonify({
                "success": False,
                "error": "translated"
            }), 400
        
        # translated
        ontology = project.ontology
        if not ontology:
            return jsonify({
                "success": False,
                "error": "translated"
            }), 400
        
        # translated
        task_manager = TaskManager()
        task_id = task_manager.create_task(f"translated: {graph_name}")
        logger.info(f"translated: task_id={task_id}, project_id={project_id}")
        
        # translated
        project.status = ProjectStatus.GRAPH_BUILDING
        project.graph_build_task_id = task_id
        ProjectManager.save_project(project)
        
        # translated
        def build_task():
            build_logger = get_logger('mirofish.build')
            try:
                build_logger.info(f"[{task_id}] translated...")
                task_manager.update_task(
                    task_id, 
                    status=TaskStatus.PROCESSING,
                    message="translated..."
                )
                
                # translated
                builder = GraphBuilderService(api_key=Config.ZEP_API_KEY)
                
                # translated
                task_manager.update_task(
                    task_id,
                    message="translated...",
                    progress=5
                )
                chunks = TextProcessor.split_text(
                    text, 
                    chunk_size=chunk_size, 
                    overlap=chunk_overlap
                )
                total_chunks = len(chunks)
                
                # translated
                task_manager.update_task(
                    task_id,
                    message="translatedZeptranslated...",
                    progress=10
                )
                graph_id = builder.create_graph(name=graph_name)
                
                # translatedgraph_id
                project.graph_id = graph_id
                ProjectManager.save_project(project)
                
                # translated
                task_manager.update_task(
                    task_id,
                    message="translated...",
                    progress=15
                )
                builder.set_ontology(graph_id, ontology)
                
                # translated（progress_callback translated (msg, progress_ratio)）
                def add_progress_callback(msg, progress_ratio):
                    progress = 15 + int(progress_ratio * 40)  # 15% - 55%
                    task_manager.update_task(
                        task_id,
                        message=msg,
                        progress=progress
                    )
                
                task_manager.update_task(
                    task_id,
                    message=f"translated {total_chunks} translated...",
                    progress=15
                )
                
                episode_uuids = builder.add_text_batches(
                    graph_id, 
                    chunks,
                    batch_size=3,
                    progress_callback=add_progress_callback
                )
                
                # translatedZeptranslated（translatedepisodetranslatedprocessedtranslated）
                task_manager.update_task(
                    task_id,
                    message="translatedZeptranslated...",
                    progress=55
                )
                
                def wait_progress_callback(msg, progress_ratio):
                    progress = 55 + int(progress_ratio * 35)  # 55% - 90%
                    task_manager.update_task(
                        task_id,
                        message=msg,
                        progress=progress
                    )
                
                builder._wait_for_episodes(episode_uuids, wait_progress_callback)
                
                # translated
                task_manager.update_task(
                    task_id,
                    message="translated...",
                    progress=95
                )
                graph_data = builder.get_graph_data(graph_id)
                
                # translated
                project.status = ProjectStatus.GRAPH_COMPLETED
                ProjectManager.save_project(project)
                
                node_count = graph_data.get("node_count", 0)
                edge_count = graph_data.get("edge_count", 0)
                build_logger.info(f"[{task_id}] translated: graph_id={graph_id}, translated={node_count}, translated={edge_count}")
                
                # translated
                task_manager.update_task(
                    task_id,
                    status=TaskStatus.COMPLETED,
                    message="translated",
                    progress=100,
                    result={
                        "project_id": project_id,
                        "graph_id": graph_id,
                        "node_count": node_count,
                        "edge_count": edge_count,
                        "chunk_count": total_chunks
                    }
                )
                
            except Exception as e:
                # translated
                build_logger.error(f"[{task_id}] translated: {str(e)}")
                build_logger.debug(traceback.format_exc())
                
                project.status = ProjectStatus.FAILED
                project.error = str(e)
                ProjectManager.save_project(project)
                
                task_manager.update_task(
                    task_id,
                    status=TaskStatus.FAILED,
                    message=f"translated: {str(e)}",
                    error=traceback.format_exc()
                )
        
        # translated
        thread = threading.Thread(target=build_task, daemon=True)
        thread.start()
        
        return jsonify({
            "success": True,
            "data": {
                "project_id": project_id,
                "task_id": task_id,
                "message": "translated，translated /task/{task_id} translated"
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


# ============== translated ==============

@graph_bp.route('/task/<task_id>', methods=['GET'])
def get_task(task_id: str):
    """
    translated
    """
    task = TaskManager().get_task(task_id)
    
    if not task:
        return jsonify({
            "success": False,
            "error": f"translated: {task_id}"
        }), 404
    
    return jsonify({
        "success": True,
        "data": task.to_dict()
    })


@graph_bp.route('/tasks', methods=['GET'])
def list_tasks():
    """
    translated
    """
    tasks = TaskManager().list_tasks()
    
    return jsonify({
        "success": True,
        "data": [t.to_dict() for t in tasks],
        "count": len(tasks)
    })


# ============== translated ==============

@graph_bp.route('/data/<graph_id>', methods=['GET'])
def get_graph_data(graph_id: str):
    """
    translated（translated）
    """
    try:
        if not Config.ZEP_API_KEY:
            return jsonify({
                "success": False,
                "error": "ZEP_API_KEYtranslated"
            }), 500
        
        builder = GraphBuilderService(api_key=Config.ZEP_API_KEY)
        graph_data = builder.get_graph_data(graph_id)
        
        return jsonify({
            "success": True,
            "data": graph_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500


@graph_bp.route('/delete/<graph_id>', methods=['DELETE'])
def delete_graph(graph_id: str):
    """
    translatedZeptranslated
    """
    try:
        if not Config.ZEP_API_KEY:
            return jsonify({
                "success": False,
                "error": "ZEP_API_KEYtranslated"
            }), 500
        
        builder = GraphBuilderService(api_key=Config.ZEP_API_KEY)
        builder.delete_graph(graph_id)
        
        return jsonify({
            "success": True,
            "message": f"translated: {graph_id}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
