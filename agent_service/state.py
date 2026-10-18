from typing import TypedDict

from agent_service.schemas import (
    AgentError,
    AgentStep,
    CampaignPlan,
    ContentGenerationRequest,
    GeneratedContent,
    ReviewResult,
    TokenUsage,
)


class AgentState(TypedDict):
    """Agent adımları arasında taşınan ortak çalışma durumu."""

    session_id: str

    agent_run_id: str

    request: ContentGenerationRequest

    campaign_plan: CampaignPlan | None

    generated_content: GeneratedContent | None

    review_result: ReviewResult | None

    steps: list[AgentStep]

    errors: list[AgentError]

    usage: TokenUsage

    revision_count: int