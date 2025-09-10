"""
Schemas for agents data structures
"""
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass


@dataclass
class AgentMessage:
    """Schema for agent messages"""
    text: str
    agent: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class QuizChoice:
    """Schema for quiz choices"""
    text: str
    value: str
    cost: float
    description: Optional[str] = None
