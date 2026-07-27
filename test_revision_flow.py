import json

from agent_service.agents.reviewer_agent import (
    ReviewerAgentResult,
)
from agent_service.orchestrator import AgentOrchestrator
from agent_service.schemas import (
    AgentStep,
    ContentGenerationRequest,
    ReviewResult,
    TokenUsage,
)


request = ContentGenerationRequest(
    brand_name="AINNOVA",
    vertical="Sağlık ve Tıp Teknolojileri",
    brief=(
        "Yapay zekânın klinik karar destek "
        "süreçlerine katkısını anlat."
    ),
    platform="linkedin",
    language="tr",
    tone="bilimsel ve profesyonel",
    target_audience=(
        "hekimler ve hastane yöneticileri"
    ),
)


orchestrator = AgentOrchestrator()

original_reviewer_run = orchestrator.reviewer.run

review_call_count = 0


def controlled_reviewer_run(
    request,
    campaign_plan,
    generated_content,
    attempt_number=1,
):
    """
    İlk kontrolde revizyon ister.
    İkinci kontrolde gerçek Reviewer Agent çalışır.
    """

    global review_call_count
    review_call_count += 1

    if review_call_count == 1:
        return ReviewerAgentResult(
            review=ReviewResult(
                approved=False,
                requires_revision=True,
                feedback=[
                    (
                        "İçerikteki kesin başarı ve verimlilik ifadelerini daha ölçülü hale getir."
                    ),
                    (
                        "Hekimin nihai karar verici olduğunu daha açık biçimde vurgula."
                    ),
                ],
                warnings=[
                    (
                        "Sağlık alanındaki iddialar klinik validasyon gerektirir."
                    ),
                ],
            ),
            step=AgentStep(
                agent="brand_reviewer",
                status="completed",
                message=(
                    "Test amacıyla ilk incelemede revizyon istendi."
                ),
                attempt=attempt_number,
            ),
            usage=TokenUsage(),
            error=None,
        )

    return original_reviewer_run(
        request=request,
        campaign_plan=campaign_plan,
        generated_content=generated_content,
        attempt_number=attempt_number,
    )


orchestrator.reviewer.run = controlled_reviewer_run

response = orchestrator.run(request)

print(
    json.dumps(
        response.model_dump(),
        ensure_ascii=False,
        indent=2,
    )
)