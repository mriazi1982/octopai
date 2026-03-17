"""
Octopai Integration API - High-Level External Integration

This module provides a standardized, high-level API for integrating
Octopai's proprietary skill development platform with external applications.
Features async task management and status tracking.
"""

import uuid
import threading
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, Future
from enum import Enum

from octopai import Octopai
from octopai.core.pipeline import PipelineStage, PipelineResult
from octopai.core.skill_factory import SkillType
from octopai.api_integration.schemas import (
    CreateSkillFromURLRequest,
    CreateSkillFromFilesRequest,
    CreateSkillFromPromptRequest,
    OptimizeSkillRequest,
    PipelineStatusResponse,
    SkillInfoResponse,
    SkillListResponse,
    SkillSearchQuery,
    ErrorResponse,
    IntegrationPipelineStage,
    UpdateSkillMetadataRequest,
    CreateCollectionRequest,
    CollectionResponse,
    CollectionListResponse,
    AddRatingRequest,
    RatingResponse,
    VersionDiffRequest,
    VersionDiffResponse,
    RollbackRequest,
    PublishSkillRequest,
    ContextSlotSchema,
    CreateCompositionRequest,
    CompositionResponse,
    CompositionListResponse,
    BindSkillRequest,
    SemanticSearchQuery,
    SemanticSearchResult,
    SemanticSearchResponse
)
from octopai.core.skill_hub import SkillStatus, SkillVisibility


class TaskStatus(Enum):
    """Status of an async task"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AsyncTask:
    """Represents an asynchronous task"""
    task_id: str
    status: TaskStatus
    task_type: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    future: Optional[Future] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "task_type": self.task_type,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error
        }


class OctopaiIntegrationAPI:
    """
    Octopai Integration API - Standardized Interface for External Applications
    
    Provides async task management, status tracking, and
    standardized data formats for external application integration.
    """
    
    def __init__(
        self,
        skill_output_dir: str = "./skills",
        skill_hub_dir: str = "./SkillHub",
        experience_dir: str = "./experiences",
        max_workers: int = 4
    ):
        """
        Initialize Octopai Web API
        
        Args:
            skill_output_dir: Directory for skill output
            skill_hub_dir: Directory for SkillHub storage
            experience_dir: Directory for experience tracking
            max_workers: Maximum number of concurrent tasks
        """
        self.octopai = Octopai(
            skill_output_dir=skill_output_dir,
            skill_hub_dir=skill_hub_dir,
            experience_dir=experience_dir
        )
        
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks: Dict[str, AsyncTask] = {}
        self._lock = threading.Lock()
        
        self._setup_pipeline_callbacks()
    
    def _setup_pipeline_callbacks(self):
        """Setup callbacks for pipeline stage updates"""
        
        def on_stage_complete(result: PipelineResult):
            """Callback for pipeline stage completion"""
            pass
        
        self.octopai.pipeline.register_callback(PipelineStage.CREATION, on_stage_complete)
        self.octopai.pipeline.register_callback(PipelineStage.OPTIMIZATION, on_stage_complete)
        self.octopai.pipeline.register_callback(PipelineStage.PACKAGING, on_stage_complete)
        self.octopai.pipeline.register_callback(PipelineStage.VALIDATION, on_stage_complete)
    
    def create_skill_from_url_async(
        self,
        request: CreateSkillFromURLRequest
    ) -> str:
        """
        Start async task to create a skill from a URL
        
        Args:
            request: Create skill from URL request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_url",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.octopai.create_from_url(
                    url=request.url,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type)
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def create_skill_from_files_async(
        self,
        request: CreateSkillFromFilesRequest
    ) -> str:
        """
        Start async task to create a skill from files
        
        Args:
            request: Create skill from files request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_files",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.octopai.create_from_files(
                    file_paths=request.files,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type)
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def create_skill_from_prompt_async(
        self,
        request: CreateSkillFromPromptRequest
    ) -> str:
        """
        Start async task to create a skill from a prompt
        
        Args:
            request: Create skill from prompt request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="create_from_prompt",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.octopai.create_from_prompt(
                    prompt=request.prompt,
                    name=request.name,
                    description=request.description,
                    tags=request.tags,
                    category=request.category,
                    author=request.author,
                    skill_type=SkillType(request.skill_type),
                    resources=request.resources
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def optimize_skill_async(
        self,
        request: OptimizeSkillRequest
    ) -> str:
        """
        Start async task to optimize a skill
        
        Args:
            request: Optimize skill request
            
        Returns:
            Task ID for tracking
        """
        task_id = str(uuid.uuid4())
        
        with self._lock:
            task = AsyncTask(
                task_id=task_id,
                status=TaskStatus.PENDING,
                task_type="optimize_skill",
                created_at=datetime.now().isoformat()
            )
            self.tasks[task_id] = task
        
        def _execute():
            try:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.RUNNING
                    self.tasks[task_id].started_at = datetime.now().isoformat()
                
                result = self.octopai.optimize_skill(
                    skill_dir=request.skill_dir
                )
                
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.COMPLETED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].result = result
                
            except Exception as e:
                with self._lock:
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].completed_at = datetime.now().isoformat()
                    self.tasks[task_id].error = str(e)
        
        future = self.executor.submit(_execute)
        
        with self._lock:
            self.tasks[task_id].future = future
        
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[AsyncTask]:
        """
        Get status of an async task
        
        Args:
            task_id: Task ID to query
            
        Returns:
            AsyncTask object or None if not found
        """
        with self._lock:
            return self.tasks.get(task_id)
    
    def get_pipeline_status_from_task(self, task_id: str) -> Optional[PipelineStatusResponse]:
        """
        Get pipeline status from a task
        
        Args:
            task_id: Task ID to query
            
        Returns:
            PipelineStatusResponse or None
        """
        task = self.get_task_status(task_id)
        if not task:
            return None
        
        web_status = self._map_task_status_to_integration(task.status)
        
        response = PipelineStatusResponse(
            request_id=task_id,
            status=web_status,
            started_at=task.created_at
        )
        
        if task.started_at:
            response.started_at = task.started_at
        
        if task.completed_at:
            response.completed_at = task.completed_at
        
        if task.error:
            response.errors = [task.error]
        
        if task.result and isinstance(task.result, PipelineResult):
            result = task.result
            response.skill_id = result.skill_id
            response.skill_dir = result.skill_dir
            response.errors = result.errors
            response.warnings = result.warnings
            response.metrics = result.metrics
            
            if result.success:
                response.status = IntegrationPipelineStage.COMPLETED
            else:
                response.status = IntegrationPipelineStage.FAILED
        
        return response
    
    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[AsyncTask]:
        """
        List all tasks, optionally filtered by status
        
        Args:
            status: Optional status filter
            
        Returns:
            List of AsyncTask objects
        """
        with self._lock:
            if status:
                return [t for t in self.tasks.values() if t.status == status]
            return list(self.tasks.values())
    
    def get_skill_info(self, skill_id: str) -> Optional[SkillInfoResponse]:
        """
        Get information about a skill
        
        Args:
            skill_id: Skill ID to query
            
        Returns:
            SkillInfoResponse or None
        """
        skill = self.octopai.get_skill_from_hub(skill_id)
        if not skill:
            return None
        
        experience = self.octopai.get_skill_experience(skill_id)
        
        response = SkillInfoResponse(
            skill_id=skill_id,
            name=skill.name,
            description=getattr(skill, 'description', ''),
            skill_type='general',
            tags=getattr(skill, 'tags', []),
            path=getattr(skill, 'path', None)
        )
        
        if experience:
            response.usage_count = experience.total_interactions
            response.success_rate = experience.success_rate
        
        return response
    
    def list_skills(
        self,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> SkillListResponse:
        """
        List skills with pagination
        
        Args:
            category: Optional category filter
            tags: Optional tag filter
            limit: Maximum number of results
            offset: Offset for pagination
            
        Returns:
            SkillListResponse
        """
        skills = self.octopai.list_skills_in_hub(category, tags, limit + offset)
        
        skill_infos = []
        for skill in skills[offset:offset + limit]:
            info = self.get_skill_info(skill.skill_id if hasattr(skill, 'skill_id') else skill.name)
            if info:
                skill_infos.append(info)
        
        return SkillListResponse(
            skills=skill_infos,
            total=len(skills),
            page=(offset // limit) + 1,
            page_size=limit
        )
    
    def search_skills(self, query: SkillSearchQuery) -> SkillListResponse:
        """
        Search for skills
        
        Args:
            query: Search query
            
        Returns:
            SkillListResponse
        """
        skills = self.octopai.search_skills_in_hub(
            query=query.query,
            tags=query.tags,
            category=query.category,
            limit=query.limit
        )
        
        skill_infos = []
        for skill in skills:
            info = self.get_skill_info(skill.skill_id if hasattr(skill, 'skill_id') else skill.name)
            if info:
                skill_infos.append(info)
        
        return SkillListResponse(
            skills=skill_infos,
            total=len(skill_infos),
            page=1,
            page_size=query.limit
        )
    
    def get_insights(self, skill_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get experience insights
        
        Args:
            skill_id: Optional specific skill to analyze
            
        Returns:
            Dictionary of insights
        """
        return self.octopai.get_experience_insights(skill_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending or running task
        
        Args:
            task_id: Task ID to cancel
            
        Returns:
            True if successful
        """
        with self._lock:
            task = self.tasks.get(task_id)
            if not task:
                return False
            
            if task.future and not task.future.done():
                task.future.cancel()
                task.status = TaskStatus.FAILED
                task.error = "Task cancelled by user"
                return True
            
            return False
    
    def cleanup_completed_tasks(self, older_than_hours: int = 24):
        """
        Clean up old completed tasks
        
        Args:
            older_than_hours: Remove tasks older than this
        """
        from datetime import timedelta
        
        cutoff = datetime.now() - timedelta(hours=older_than_hours)
        
        with self._lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task.completed_at:
                    completed = datetime.fromisoformat(task.completed_at)
                    if completed < cutoff:
                        to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.tasks[task_id]
    
    def _map_task_status_to_integration(self, status: TaskStatus) -> IntegrationPipelineStage:
        """Map internal task status to integration API status"""
        mapping = {
            TaskStatus.PENDING: IntegrationPipelineStage.PENDING,
            TaskStatus.RUNNING: IntegrationPipelineStage.CREATION,
            TaskStatus.COMPLETED: IntegrationPipelineStage.COMPLETED,
            TaskStatus.FAILED: IntegrationPipelineStage.FAILED
        }
        return mapping.get(status, IntegrationPipelineStage.PENDING)
    
    def update_skill_metadata(
        self,
        request: UpdateSkillMetadataRequest
    ) -> Optional[SkillInfoResponse]:
        """
        Update skill metadata
        
        Args:
            request: Update metadata request
            
        Returns:
            Updated SkillInfoResponse or None
        """
        status = SkillStatus(request.status) if request.status else None
        visibility = SkillVisibility(request.visibility) if request.visibility else None
        
        skill = self.octopai.update_skill_metadata_in_hub(
            skill_id=request.skill_id,
            name=request.name,
            description=request.description,
            tags=request.tags,
            category=request.category,
            status=status,
            visibility=visibility,
            author=request.author,
            keywords=request.keywords,
            related_skills=request.related_skills,
            skill_type=request.skill_type,
            custom_fields=request.custom_fields
        )
        
        if not skill:
            return None
        
        return self.get_skill_info(skill.metadata.skill_id)
    
    def create_collection(
        self,
        request: CreateCollectionRequest
    ) -> CollectionResponse:
        """
        Create a skill collection
        
        Args:
            request: Create collection request
            
        Returns:
            Created CollectionResponse
        """
        collection = self.octopai.create_collection_in_hub(
            name=request.name,
            description=request.description,
            skill_ids=request.skill_ids,
            tags=request.tags,
            author=request.author
        )
        
        return CollectionResponse(
            collection_id=collection.collection_id,
            name=collection.name,
            description=collection.description,
            skill_ids=collection.skill_ids,
            tags=collection.tags,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            author=collection.author
        )
    
    def add_skill_to_collection(
        self,
        collection_id: str,
        skill_id: str
    ) -> bool:
        """
        Add a skill to a collection
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID
            
        Returns:
            True if successful
        """
        return self.octopai.add_skill_to_collection_in_hub(collection_id, skill_id)
    
    def remove_skill_from_collection(
        self,
        collection_id: str,
        skill_id: str
    ) -> bool:
        """
        Remove a skill from a collection
        
        Args:
            collection_id: Collection ID
            skill_id: Skill ID
            
        Returns:
            True if successful
        """
        return self.octopai.remove_skill_from_collection_in_hub(collection_id, skill_id)
    
    def get_collection(
        self,
        collection_id: str
    ) -> Optional[CollectionResponse]:
        """
        Get a collection by ID
        
        Args:
            collection_id: Collection ID
            
        Returns:
            CollectionResponse or None
        """
        collection = self.octopai.get_collection_from_hub(collection_id)
        if not collection:
            return None
        
        return CollectionResponse(
            collection_id=collection.collection_id,
            name=collection.name,
            description=collection.description,
            skill_ids=collection.skill_ids,
            tags=collection.tags,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
            author=collection.author
        )
    
    def list_collections(self) -> CollectionListResponse:
        """
        List all collections
        
        Returns:
            CollectionListResponse
        """
        collections = self.octopai.list_collections_in_hub()
        responses = []
        for collection in collections:
            responses.append(CollectionResponse(
                collection_id=collection.collection_id,
                name=collection.name,
                description=collection.description,
                skill_ids=collection.skill_ids,
                tags=collection.tags,
                created_at=collection.created_at,
                updated_at=collection.updated_at,
                author=collection.author
            ))
        
        return CollectionListResponse(
            collections=responses,
            total=len(responses)
        )
    
    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection
        
        Args:
            collection_id: Collection ID
            
        Returns:
            True if successful
        """
        return self.octopai.delete_collection_from_hub(collection_id)
    
    def add_rating(
        self,
        request: AddRatingRequest
    ) -> Optional[RatingResponse]:
        """
        Add a rating to a skill
        
        Args:
            request: Add rating request
            
        Returns:
            RatingResponse or None
        """
        rating = self.octopai.add_rating_to_skill_in_hub(
            skill_id=request.skill_id,
            rating=request.rating,
            feedback=request.feedback,
            reviewer=request.reviewer
        )
        
        if not rating:
            return None
        
        return RatingResponse(
            rating_id=rating.rating_id,
            skill_id=rating.skill_id,
            rating=rating.rating,
            feedback=rating.feedback,
            reviewer=rating.reviewer,
            created_at=rating.created_at
        )
    
    def get_ratings(
        self,
        skill_id: str
    ) -> List[RatingResponse]:
        """
        Get all ratings for a skill
        
        Args:
            skill_id: Skill ID
            
        Returns:
            List of RatingResponse
        """
        ratings = self.octopai.get_ratings_from_hub(skill_id)
        return [
            RatingResponse(
                rating_id=r.rating_id,
                skill_id=r.skill_id,
                rating=r.rating,
                feedback=r.feedback,
                reviewer=r.reviewer,
                created_at=r.created_at
            )
            for r in ratings
        ]
    
    def compute_version_diff(
        self,
        request: VersionDiffRequest
    ) -> Optional[VersionDiffResponse]:
        """
        Compute version diff
        
        Args:
            request: Version diff request
            
        Returns:
            VersionDiffResponse or None
        """
        diff = self.octopai.compute_version_diff_in_hub(
            skill_id=request.skill_id,
            from_version=request.from_version,
            to_version=request.to_version
        )
        
        if not diff:
            return None
        
        return VersionDiffResponse(
            diff_id=diff.diff_id,
            skill_id=diff.skill_id,
            from_version=diff.from_version,
            to_version=diff.to_version,
            additions=diff.additions,
            deletions=diff.deletions,
            modifications=diff.modifications,
            created_at=diff.created_at
        )
    
    def rollback_skill(
        self,
        request: RollbackRequest
    ) -> Optional[SkillInfoResponse]:
        """
        Rollback a skill
        
        Args:
            request: Rollback request
            
        Returns:
            Updated SkillInfoResponse or None
        """
        skill = self.octopai.rollback_skill_in_hub(
            skill_id=request.skill_id,
            version=request.version,
            author=request.author
        )
        
        if not skill:
            return None
        
        return self.get_skill_info(skill.metadata.skill_id)
    
    def publish_skill(
        self,
        request: PublishSkillRequest
    ) -> Optional[SkillInfoResponse]:
        """
        Publish a skill
        
        Args:
            request: Publish request
            
        Returns:
            Updated SkillInfoResponse or None
        """
        visibility = SkillVisibility(request.visibility)
        skill = self.octopai.publish_skill_in_hub(
            skill_id=request.skill_id,
            visibility=visibility
        )
        
        if not skill:
            return None
        
        return self.get_skill_info(skill.metadata.skill_id)
    
    def deprecate_skill(self, skill_id: str) -> Optional[SkillInfoResponse]:
        """
        Deprecate a skill
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Updated SkillInfoResponse or None
        """
        skill = self.octopai.deprecate_skill_in_hub(skill_id)
        if not skill:
            return None
        return self.get_skill_info(skill.metadata.skill_id)
    
    def archive_skill(self, skill_id: str) -> Optional[SkillInfoResponse]:
        """
        Archive a skill
        
        Args:
            skill_id: Skill ID
            
        Returns:
            Updated SkillInfoResponse or None
        """
        skill = self.octopai.archive_skill_in_hub(skill_id)
        if not skill:
            return None
        return self.get_skill_info(skill.metadata.skill_id)
    
    def create_composition(
        self,
        request: CreateCompositionRequest
    ) -> CompositionResponse:
        """
        Create a context composition
        
        Args:
            request: Create composition request
            
        Returns:
            Created CompositionResponse
        """
        slots = None
        if request.slots:
            from octopai.core.skill_hub import ContextSlot
            slots = {
                k: ContextSlot(
                    slot_id=v.slot_id,
                    name=v.name,
                    description=v.description,
                    required=v.required,
                    default_skill_id=v.default_skill_id,
                    allowed_skill_types=v.allowed_skill_types
                )
                for k, v in request.slots.items()
            }
        
        composition = self.octopai.create_composition_in_hub(
            name=request.name,
            description=request.description,
            slots=slots
        )
        
        response_slots = {
            k: ContextSlotSchema(
                slot_id=v.slot_id,
                name=v.name,
                description=v.description,
                required=v.required,
                default_skill_id=v.default_skill_id,
                allowed_skill_types=v.allowed_skill_types
            )
            for k, v in composition.slots.items()
        }
        
        return CompositionResponse(
            composition_id=composition.composition_id,
            name=composition.name,
            description=composition.description,
            slots=response_slots,
            bindings=composition.bindings,
            created_at=composition.created_at,
            updated_at=composition.updated_at
        )
    
    def add_slot_to_composition(
        self,
        composition_id: str,
        slot: ContextSlotSchema
    ) -> bool:
        """
        Add a slot to a composition
        
        Args:
            composition_id: Composition ID
            slot: Slot to add
            
        Returns:
            True if successful
        """
        from octopai.core.skill_hub import ContextSlot
        context_slot = ContextSlot(
            slot_id=slot.slot_id,
            name=slot.name,
            description=slot.description,
            required=slot.required,
            default_skill_id=slot.default_skill_id,
            allowed_skill_types=slot.allowed_skill_types
        )
        return self.octopai.add_slot_to_composition_in_hub(composition_id, context_slot)
    
    def bind_skill_to_slot(
        self,
        request: BindSkillRequest
    ) -> bool:
        """
        Bind a skill to a slot
        
        Args:
            request: Bind request
            
        Returns:
            True if successful
        """
        return self.octopai.bind_skill_to_slot_in_hub(
            request.composition_id,
            request.slot_id,
            request.skill_id
        )
    
    def get_composition(
        self,
        composition_id: str
    ) -> Optional[CompositionResponse]:
        """
        Get a composition by ID
        
        Args:
            composition_id: Composition ID
            
        Returns:
            CompositionResponse or None
        """
        composition = self.octopai.get_composition_from_hub(composition_id)
        if not composition:
            return None
        
        response_slots = {
            k: ContextSlotSchema(
                slot_id=v.slot_id,
                name=v.name,
                description=v.description,
                required=v.required,
                default_skill_id=v.default_skill_id,
                allowed_skill_types=v.allowed_skill_types
            )
            for k, v in composition.slots.items()
        }
        
        return CompositionResponse(
            composition_id=composition.composition_id,
            name=composition.name,
            description=composition.description,
            slots=response_slots,
            bindings=composition.bindings,
            created_at=composition.created_at,
            updated_at=composition.updated_at
        )
    
    def list_compositions(self) -> CompositionListResponse:
        """
        List all compositions
        
        Returns:
            CompositionListResponse
        """
        compositions = self.octopai.list_compositions_in_hub()
        responses = []
        
        for comp in compositions:
            response_slots = {
                k: ContextSlotSchema(
                    slot_id=v.slot_id,
                    name=v.name,
                    description=v.description,
                    required=v.required,
                    default_skill_id=v.default_skill_id,
                    allowed_skill_types=v.allowed_skill_types
                )
                for k, v in comp.slots.items()
            }
            
            responses.append(CompositionResponse(
                composition_id=comp.composition_id,
                name=comp.name,
                description=comp.description,
                slots=response_slots,
                bindings=comp.bindings,
                created_at=comp.created_at,
                updated_at=comp.updated_at
            ))
        
        return CompositionListResponse(
            compositions=responses,
            total=len(responses)
        )
    
    def delete_composition(self, composition_id: str) -> bool:
        """
        Delete a composition
        
        Args:
            composition_id: Composition ID
            
        Returns:
            True if successful
        """
        return self.octopai.delete_composition_from_hub(composition_id)
    
    def semantic_search(
        self,
        query: SemanticSearchQuery
    ) -> SemanticSearchResponse:
        """
        Enhanced semantic search
        
        Args:
            query: Semantic search query
            
        Returns:
            SemanticSearchResponse
        """
        status = SkillStatus(query.status) if query.status else None
        results = self.octopai.semantic_search_in_hub(
            query=query.query,
            tags=query.tags,
            category=query.category,
            status=status,
            limit=query.limit
        )
        
        search_results = []
        for skill, score in results:
            info = self.get_skill_info(skill.metadata.skill_id)
            if info:
                search_results.append(SemanticSearchResult(
                    skill=info,
                    score=score
                ))
        
        return SemanticSearchResponse(
            results=search_results,
            total=len(search_results)
        )
    
    def shutdown(self, wait: bool = True):
        """
        Shutdown the executor
        
        Args:
            wait: Whether to wait for running tasks
        """
        self.executor.shutdown(wait=wait)
