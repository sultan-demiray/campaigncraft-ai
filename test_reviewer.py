import json

from agent_service.agents.reviewer_agent import (
    ReviewerAgent,
)
from agent_service.schemas import (
    CampaignPlan,
    ContentGenerationRequest,
    GeneratedContent,
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

campaign_plan = CampaignPlan(
    objective=(
        "Klinik karar destek sistemleri hakkında bilgilendirme ve marka bilinirliği oluşturmak."
    ),
    target_audience=(
        "Hekimler ve hastane yöneticileri"
    ),
    platform="linkedin",
    content_type="linkedin_post",
    tone="bilimsel ve profesyonel",
    key_messages=[
        (
            "Yapay zekâ hekimlerin karar süreçlerini destekleyen tamamlayıcı bir teknolojidir."
        ),
        (
            "Sistemler insan denetimiyle kullanılmalıdır."
        ),
    ],
    cta_strategy=(
        "Kullanıcıyı konu hakkında daha fazla bilgi almaya davet etmek."
    ),
    constraints=[
        "Kesin teşhis veya başarı garantisi verilmemelidir.",
        "Doğrulanmamış istatistik kullanılmamalıdır.",
    ],
)

generated_content = GeneratedContent(
    title=(
        "Klinik Karar Destek Süreçlerinde "
        "Yapay Zekânın Rolü"
    ),
    body=(
        "Yapay zekâ tabanlı klinik karar destek sistemleri, hekimlerin verileri daha düzenli değerlendirmesine yardımcı olan tamamlayıcı teknolojilerdir."
        "Bu sistemler uzman kararının yerine geçmez ve insan denetimiyle kullanılmalıdır."
    ),
    cta=(
        "Klinik teknolojiler hakkında daha fazla bilgi almak için bizimle iletişime geçin."
    ),
    hashtags=[
        "AINNOVA",
        "YapayZeka",
        "DijitalSağlık",
    ],
    warnings=[],
)

reviewer = ReviewerAgent()

result = reviewer.run(
    request=request,
    campaign_plan=campaign_plan,
    generated_content=generated_content,
)

output = {
    "review": (
        result.review.model_dump()
        if result.review
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