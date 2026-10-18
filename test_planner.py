import json

from agent_service.agents.planner_agent import (
    PlannerAgent,
)
from agent_service.schemas import (
    ContentGenerationRequest,
)


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

planner = PlannerAgent()

result = planner.run(request)

output = {
    "plan": (
        result.plan.model_dump()
        if result.plan
        else None
    ),
    "step": result.step.model_dump(),
    "usage": result.usage.model_dump(),
    "error": (
        result.error.model_dump()
        if result.error
        else None
    ),
}

print(
    json.dumps(
        output,
        ensure_ascii=False,
        indent=2,
    )
)