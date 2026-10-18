import os
import random
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent_service.prompts import (
    REVIEWER_SYSTEM_PROMPT,
    build_reviewer_prompt,
)
from agent_service.schemas import (
    AgentError,
    AgentStep,
    CampaignPlan,
    ContentGenerationRequest,
    GeneratedContent,
    ReviewResult,
    TokenUsage,
)


load_dotenv()


class ReviewerAgentResult:
    """Reviewer Agent çalışmasının kontrollü sonucu."""

    def __init__(
        self,
        review: ReviewResult | None,
        step: AgentStep,
        usage: TokenUsage,
        error: AgentError | None = None,
    ) -> None:
        self.review = review
        self.step = step
        self.usage = usage
        self.error = error


class ReviewerAgent:
    """Üretilen içeriği marka ve risk açısından kontrol eden agent."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY bulunamadı. "
                "Proje kökündeki .env dosyasını kontrol et."
            )

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-flash-lite",
        )

        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                timeout=30_000,
            ),
        )

    def run(
        self,
        request: ContentGenerationRequest,
        campaign_plan: CampaignPlan,
        generated_content: GeneratedContent,
        attempt_number: int = 1,
    ) -> ReviewerAgentResult:
        try:
            response = None
            last_error: Exception | None = None

            for attempt in range(2):
                print(
                    "Reviewer Agent isteği gönderiliyor. "
                    f"Deneme: {attempt + 1}"
                )

                try:
                    response = (
                        self.client.models.generate_content(
                            model=self.model_name,
                            contents=build_reviewer_prompt(
                                request=request,
                                campaign_plan=campaign_plan,
                                generated_content=generated_content,
                            ),
                            config=types.GenerateContentConfig(
                                system_instruction=(
                                    REVIEWER_SYSTEM_PROMPT
                                ),
                                response_mime_type=(
                                    "application/json"
                                ),
                                response_schema=ReviewResult,
                            ),
                        )
                    )
                    break

                except Exception as exc:
                    last_error = exc
                    error_message = str(exc).lower()

                    is_temporary_error = any(
                        value in error_message
                        for value in (
                            "429",
                            "500",
                            "502",
                            "503",
                            "504",
                            "unavailable",
                            "resource_exhausted",
                            "server disconnected",
                            "connection reset",
                            "connection error",
                            "timeout",
                            "timed out",
                        )
                    )

                    if not is_temporary_error:
                        raise

                    if attempt == 1:
                        raise

                    delay = (
                        2**attempt
                    ) + random.uniform(0, 1)

                    time.sleep(delay)

            if response is None:
                raise RuntimeError(
                    "Reviewer Agent isteği tamamlanamadı: "
                    f"{last_error}"
                )

            generated_text = (
                response.text or ""
            ).strip()

            if not generated_text:
                raise RuntimeError(
                    "Reviewer Agent boş cevap döndürdü."
                )

            review_result = (
                ReviewResult.model_validate_json(
                    generated_text
                )
            )

            usage_metadata = response.usage_metadata

            input_tokens = (
                getattr(
                    usage_metadata,
                    "prompt_token_count",
                    0,
                )
                or 0
            )

            output_tokens = (
                getattr(
                    usage_metadata,
                    "candidates_token_count",
                    0,
                )
                or 0
            )

            return ReviewerAgentResult(
                review=review_result,
                step=AgentStep(
                    agent="brand_reviewer",
                    status="completed",
                    message=(
                        "İçerik incelemesi başarıyla tamamlandı."
                    ),
                    attempt=attempt_number,
                ),
                usage=TokenUsage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                ),
            )

        except Exception as exc:
            return ReviewerAgentResult(
                review=None,
                step=AgentStep(
                    agent="brand_reviewer",
                    status="failed",
                    message=(
                        "İçerik incelemesi tamamlanamadı."
                    ),
                    attempt=attempt_number,
                ),
                usage=TokenUsage(),
                error=AgentError(
                    agent="brand_reviewer",
                    message=str(exc),
                    error_type=type(exc).__name__,
                    retryable=False,
                ),
            )