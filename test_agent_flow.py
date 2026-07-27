import json

from agent_service.orchestrator import AgentOrchestrator
from agent_service.schemas import ContentGenerationRequest


request = ContentGenerationRequest(
    brand_name="AINNOVA",
    vertical="Sağlık ve Tıp Teknolojileri",
    brief=(
        "Yapay zekânın klinik karar destek süreçlerine katkısını anlat."
    ),
    platform="linkedin",
    language="tr",
    tone="bilimsel ve profesyonel",
    target_audience=(
        "hekimler ve hastane yöneticileri"
    ),
)

orchestrator = AgentOrchestrator()

response = orchestrator.run(request)

print(
    json.dumps(
        response.model_dump(),
        ensure_ascii=False,
        indent=2,
    )
)