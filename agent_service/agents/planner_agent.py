import os
import random
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent_service.prompts import (
    PLANNER_SYSTEM_PROMPT,
    build_planner_prompt,
)
from agent_service.schemas import (
    AgentError,
    AgentStep,
    CampaignPlan,
    ContentGenerationRequest,
    TokenUsage,
)


load_dotenv()


class PlannerAgentResult:
    """Planner Agent çalışmasının kontrollü sonucu."""

    def __init__(
        self,
        plan: CampaignPlan | None,
        step: AgentStep,
        usage: TokenUsage,
        error: AgentError | None = None,
    ) -> None:
        self.plan = plan
        self.step = step
        self.usage = usage
        self.error = error


class PlannerAgent:
    """Kullanıcı briefinden kampanya planı oluşturan agent."""

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
    ) -> PlannerAgentResult:
        try:
            response = None
            last_error: Exception | None = None

            for attempt in range(2):
                print(
                    "Planner Agent isteği gönderiliyor. "
                    f"Deneme: {attempt + 1}"
                )

                try:
                    response = (
                        self.client.models.generate_content(
                            model=self.model_name,
                            contents=build_planner_prompt(
                                request
                            ),
                            config=types.GenerateContentConfig(
                                system_instruction=(
                                    PLANNER_SYSTEM_PROMPT
                                ),
                                response_mime_type=(
                                    "application/json"
                                ),
                                response_schema=CampaignPlan,
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
                    "Planner Agent isteği tamamlanamadı: "
                    f"{last_error}"
                )

            generated_text = (
                response.text or ""
            ).strip()

            if not generated_text:
                raise RuntimeError(
                    "Planner Agent boş cevap döndürdü."
                )

            campaign_plan = (
                CampaignPlan.model_validate_json(
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

            return PlannerAgentResult(
                plan=campaign_plan,
                step=AgentStep(
                    agent="campaign_planner",
                    status="completed",
                    message=(
                        "Kampanya planı başarıyla oluşturuldu."
                    ),
                ),
                usage=TokenUsage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                ),
            )

        except Exception as exc:
            return PlannerAgentResult(
                plan=None,
                step=AgentStep(
                    agent="campaign_planner",
                    status="failed",
                    message=(
                        "Kampanya planı oluşturulamadı."
                    ),
                ),
                usage=TokenUsage(),
                error=AgentError(
                    agent="campaign_planner",
                    message=str(exc),
                    error_type=type(exc).__name__,
                    retryable=False,
                ),
            )