
from enum import Enum

from pydantic import BaseModel, Field

class PromptCategory(Enum):
    CODING = "coding"
    DATA_ANALYSIS = "data_analysis"
    CHAT = "chat"
    REASONING = "reasoning"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"
    RESEARCH = "research"
    AUTOMATION = "automation"

class PromptComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class PromptAnalysis(BaseModel):
    category: PromptCategory
    complexity: PromptComplexity
    requires_reasoning: bool
    requires_tools: bool
    domain: str
    confidence: float = Field(ge=0.0, le=1.0)