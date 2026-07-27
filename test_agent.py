from agent_service.gemini_client import GeminiClient
from agent_service.schemas import ContentGenerationRequest


def main() -> None:
    request = ContentGenerationRequest(
        brand_name="AINNOVA",
        vertical="Sağlık ve Tıp Teknolojileri",
        brief=(
            "Yapay zekânın sağlık alanındaki karar destek süreçlerine katkısını anlatan bir LinkedIn gönderisi hazırla."
        ),
        platform="linkedin",
        language="tr",
        tone="bilimsel ve profesyonel",
        target_audience="hekimler ve hastane yöneticileri",
    )

    client = GeminiClient()
    result = client.generate_content(request)

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()