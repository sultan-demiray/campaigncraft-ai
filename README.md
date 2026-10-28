# CampaignCraft — AI İçerik Üretim Sistemi

CampaignCraft, Google Gemini API kullanarak farklı dijital platformlar için yapılandırılmış pazarlama içerikleri üreten bir Python projesidir.

Proje; marka adı, sektör, içerik brief'i, platform, dil, ton ve hedef kitle bilgilerini kullanarak Gemini modeline istek gönderir. Dönen yanıt Pydantic ile doğrulanır ve standart bir agent yanıt yapısına dönüştürülür.

## Özellikler

- Google Gemini API ile pazarlama içeriği üretimi
- Türkçe ve İngilizce içerik desteği
- LinkedIn, X, Instagram, blog ve e-posta platformları için içerik üretimi
- Marka tonu ve hedef kitleye göre özelleştirilmiş çıktı
- Başlık, ana metin, CTA ve hashtag üretimi
- Riskli veya doğrulanması gereken ifadeler için uyarı listesi
- Yapılandırılmış JSON yanıt
- Pydantic ile istek ve yanıt doğrulaması
- Geçici API ve bağlantı hatalarında otomatik yeniden deneme
- Girdi ve çıktı token kullanımının raporlanması

## Proje Yapısı

```text
campaigncraft-ai/
├── agent_service/
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── prompts.py
│   └── schemas.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── test_agent.py
```

## Kullanılan Teknolojiler

- Python 3.12
- Google Gemini API
- Google GenAI Python SDK
- Pydantic
- python-dotenv

## Kurulum

### 1. Sanal ortam oluşturma

Windows PowerShell üzerinde aşağıdaki komutları sırasıyla çalıştırın:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 2. Bağımlılıkları yükleme

```powershell
pip install -r requirements.txt
```

### 3. Gemini API anahtarını tanımlama

Proje kökünde `.env` adında bir dosya oluşturun ve API anahtarınızı ekleyin:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Paylaşılabilir örnek yapı `.env.example` dosyasında bulunur:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## Çalıştırma

Agent testini çalıştırmak için:

```powershell
python test_agent.py
```

Test dosyası bir `ContentGenerationRequest` oluşturur ve isteği `GeminiClient` üzerinden Gemini API'ye gönderir.

## İstek Yapısı

Agent aşağıdaki bilgileri kabul eder:

- `brand_name`: Marka adı
- `vertical`: Marka veya ürünün faaliyet alanı
- `brief`: Üretilecek içeriğin açıklaması
- `platform`: İçeriğin yayınlanacağı platform
- `language`: İçerik dili
- `tone`: İçerik tonu
- `target_audience`: Hedef kitle

Örnek istek:

```python
from agent_service.schemas import ContentGenerationRequest

request = ContentGenerationRequest(
    brand_name="Demo Marka",
    vertical="Sağlık ve Tıp Teknolojileri",
    brief=(
        "Yapay zekânın sağlık alanındaki karar destek "
        "süreçlerine katkısını anlatan bir LinkedIn gönderisi hazırla."
    ),
    platform="linkedin",
    language="tr",
    tone="bilimsel ve profesyonel",
    target_audience="hekimler ve hastane yöneticileri",
)
```

## Yanıt Yapısı

Başarılı bir istekte agent aşağıdaki bilgileri döndürür:

- İşlem durumu
- Açıklama mesajı
- Üretilen içerik artifact'i
- İçerik başlığı
- Ana içerik metni
- CTA
- Hashtag listesi
- Uyarı listesi
- Agent adımı ve durumu
- Girdi ve çıktı token sayıları

Örnek yanıt:

```json
{
  "status": "completed",
  "message": "İçerik başarıyla üretildi.",
  "artifacts": [
    {
      "type": "linkedin_content",
      "title": "Örnek içerik başlığı",
      "content": {
        "title": "Örnek içerik başlığı",
        "body": "Üretilen içerik metni",
        "cta": "Harekete geçirici mesaj",
        "hashtags": [
          "#YapayZeka",
          "#DijitalPazarlama"
        ],
        "warnings": []
      }
    }
  ],
  "sources": [],
  "steps": [
    {
      "agent": "content_generator",
      "status": "completed"
    }
  ],
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

Token değerleri örnek olarak verilmiştir; gerçek kullanımda API yanıtına göre değişir.

## İçerik Üretim Akışı

1. `ContentGenerationRequest` ile istek oluşturulur.
2. İstek bilgilerine göre prompt hazırlanır.
3. Gemini API'ye istek gönderilir.
4. Dönen yanıt Pydantic ile doğrulanır.
5. Sonuç, standart `AgentResponse` yapısında döndürülür.
