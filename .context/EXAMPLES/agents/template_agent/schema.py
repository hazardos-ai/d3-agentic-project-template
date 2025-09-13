"""
Pydantic schemas for a generic agent (template).
Replace names/fields as needed for your concrete agent.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class Section(BaseModel):
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    sources: List[str] = Field(default_factory=list, description="IDs or URLs of sources")
    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Section score or relevance")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata")


class TaskInput(BaseModel):
    """Generic input schema for any agent's task."""
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Candidate items (e.g., retrieved docs)")
    query: Optional[str] = Field(default=None, description="Optional user/system query")
    params: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters")
    max_output_length: int = Field(default=4000, ge=500, le=20000, description="Max characters for output assembly")


class TaskOutput(BaseModel):
    """Generic output schema for any agent's task."""
    text: str = Field(..., description="Primary text output (assembled or generated)")
    sections: List[Section] = Field(default_factory=list, description="Structured sections used to build text")
    status: str = Field(default="ok", description="ok|error|partial")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Scores and runtime statistics")
    attachments: List[Dict[str, Any]] = Field(default_factory=list, description="Any extra artifacts produced")

    model_config = ConfigDict(use_enum_values=True)
