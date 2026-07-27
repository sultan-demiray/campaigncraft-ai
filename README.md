# Ainnova AI Marketing Agent

Ainnova AI Marketing Agent, Google Gemini API tabanlı çok aşamalı bir dijital pazarlama içerik üretim sistemidir.

Agent Core; kullanıcı isteğini analiz eder, yapılandırılmış bir kampanya planı oluşturur, plana uygun içerik üretir, üretilen içeriği marka ve güvenlik kurallarına göre inceler ve gerekli olduğunda içeriği bir kez otomatik olarak revize eder.

## Özellikler

- Google Gemini API ile içerik üretimi
- Campaign Planner Agent
- Content Generator
- Brand Reviewer Agent
- Agent Orchestrator
- Tek seferlik otomatik revizyon
- Revizyon sonrasında ikinci Reviewer kontrolü
- Pydantic tabanlı yapılandırılmış veri modelleri
- Agent adım ve deneme takibi
- Session ve Agent Run kimlikleri
- Girdi ve çıktı token kullanım takibi
- Geçici API hatalarında yeniden deneme
- Kontrollü hata yönetimi
- Türkçe ve İngilizce içerik desteği
- Platforma, marka tonuna ve hedef kitleye uygun içerik üretimi

## Desteklenen Platformlar

- LinkedIn
- X
- Instagram
- Blog
- E-posta

## Kullanılan Teknolojiler

- Python 3.12
- Google Gemini API
- Google GenAI Python SDK
- Pydantic
- python-dotenv

## Proje Yapısı

```text
Ainnova-agent/
├── agent_service/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── planner_agent.py
│   │   └── reviewer_agent.py
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── orchestrator.py
│   ├── prompts.py
│   ├── schemas.py
│   └── state.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── test_agent.py
├── test_agent_flow.py
├── test_planner.py
├── test_reviewer.py
└── test_revision_flow.py
```

## Agent Core Mimarisi

Agent Core, içerik üretimini tek bir model çağrısıyla gerçekleştirmek yerine farklı sorumluluklara sahip bileşenler üzerinden yürütür.

Normal Agent akışı:

```text
ContentGenerationRequest
        ↓
Campaign Planner Agent
        ↓
Content Generator
        ↓
Brand Reviewer Agent
        ↓
AgentResponse
```

Reviewer içeriğin revize edilmesini isterse aşağıdaki akış çalışır:

```text
Campaign Planner Agent
        ↓
Content Generator — attempt 1
        ↓
Brand Reviewer Agent — attempt 1
        ↓
Content Generator — attempt 2
        ↓
Brand Reviewer Agent — attempt 2
        ↓
AgentResponse
```

Agent Core sonsuz revizyon döngüsünü önlemek için en fazla bir otomatik revizyon gerçekleştirir.

## Campaign Planner Agent

Campaign Planner Agent, kullanıcı tarafından gönderilen içerik isteğini analiz ederek yapılandırılmış bir kampanya planı oluşturur.

Kampanya planı şu bilgileri içerir:

- Kampanya amacı
- Hedef kitle
- Platform
- İçerik türü
- İletişim tonu
- Temel mesajlar
- CTA stratejisi
- İçerik sınırlamaları

Örnek kampanya planı:

```json
{
  "objective": "Yapay zekânın klinik karar destek süreçlerindeki rolü hakkında farkındalık oluşturmak.",
  "target_audience": "Hekimler ve hastane yöneticileri",
  "platform": "linkedin",
  "content_type": "linkedin_post",
  "tone": "bilimsel ve profesyonel",
  "key_messages": [
    "Yapay zekâ, klinik karar süreçlerinde hekimleri destekleyebilir.",
    "Teknoloji, insan uzmanlığının yerine geçen bir sistem olarak konumlandırılmamalıdır.",
    "Veriye dayalı yaklaşımlar ek bir değerlendirme perspektifi sağlayabilir."
  ],
  "cta_strategy": "Kullanıcıları görüşlerini yorumlarda paylaşmaya davet etmek.",
  "constraints": [
    "Doğrulanmamış başarı oranları kullanılmamalıdır.",
    "Kesin sonuç veya garanti verilmemelidir."
  ]
}
```

Campaign Planner Agent aşağıdaki kurallara göre çalışır:

- Kullanıcı tarafından belirtilmeyen ürün veya hizmetleri oluşturmaz.
- Uydurma istatistik, başarı oranı veya akademik kaynak eklemez.
- Var olmayan web sitesi, demo veya teknik dokümana yönlendirme yapmaz.
- Doğrulanmamış iletişim veya sosyal medya hesabı kullanmaz.
- Hassas alanlarda kesin sonuç veya garanti vadetmez.
- Doğrulanmış ölçüm veya kaynak bulunmadığında ölçülü ifadeler kullanır.
- Yapay zekâyı insan uzmanlığının yerine geçen bir sistem olarak konumlandırmaz.

## Content Generator

Content Generator, kullanıcı isteğine ve Campaign Planner tarafından hazırlanan kampanya planına göre platforma uygun içerik üretir.

Üretilen içerik şu alanlardan oluşur:

- `title`: İçerik başlığı
- `body`: Ana içerik metni
- `cta`: Harekete geçirici mesaj
- `hashtags`: İçerikle ilgili hashtag listesi
- `warnings`: Kaynak, doğrulama veya insan kontrolü gerektiren uyarılar

Örnek içerik çıktısı:

```json
{
  "title": "Klinik Karar Destek Süreçlerinde Yapay Zekâ",
  "body": "Yapay zekâ tabanlı sistemler, klinik karar süreçlerinde hekimlere yardımcı bir değerlendirme perspektifi sunabilir.",
  "cta": "Konu hakkındaki görüşlerinizi yorumlarda paylaşabilirsiniz.",
  "hashtags": [
    "AINNOVA",
    "YapayZeka",
    "DijitalSağlık",
    "KlinikKararDestek"
  ],
  "warnings": [
    "Nihai klinik karar her zaman hekim sorumluluğundadır."
  ]
}
```

Content Generator aşağıdaki güvenlik ve kalite kurallarına göre çalışır:

- Kullanıcı briefinde bulunmayan ürün, hizmet veya özellikleri uydurmaz.
- Uydurma istatistik, akademik kaynak veya bağlantı oluşturmaz.
- Kesin başarı, doğruluk, hız veya verimlilik iddiası kullanmaz.
- Sağlık, hukuk ve finans gibi hassas alanlarda garanti vermez.
- Doğrulanmamış iletişim kanallarına yönlendirme yapmaz.
- Kullanıcı tarafından belirtilmeyen demo, doküman veya web sayfası oluşturmaz.
- Yapay zekâyı insan uzmanlığının alternatifi olarak göstermez.
- Kaynak veya insan kontrolü gerektiren durumları `warnings` alanında belirtir.

## Brand Reviewer Agent

Brand Reviewer Agent, üretilen içeriği kalite, marka uyumu ve güvenlik açısından kontrol eder.

Reviewer aşağıdaki kriterleri inceler:

- Kullanıcı briefine uygunluk
- Kampanya planına uygunluk
- Marka tonuna uygunluk
- Hedef kitle uyumu
- Platform uyumu
- Dil bilgisi ve anlatım bütünlüğü
- CTA ve hashtag uygunluğu
- Uydurma veya doğrulanmamış bilgi kullanımı
- Doğrulanmamış başarı, doğruluk, hız veya verimlilik iddiaları
- Hassas sektör riskleri
- İnsan uzmanlığının doğru konumlandırılması

Reviewer çıktısı:

```json
{
  "approved": true,
  "requires_revision": false,
  "feedback": [
    "İçerik marka tonuna ve hedef kitleye uygundur."
  ],
  "warnings": [
    "İçerik yayınlanmadan önce alan uzmanı tarafından kontrol edilmelidir."
  ]
}
```

Alanların anlamları:

- `approved`: İçeriğin kullanılabilir durumda olup olmadığını belirtir.
- `requires_revision`: İçeriğin yeniden düzenlenmesi gerekip gerekmediğini belirtir.
- `feedback`: İçeriği geliştirmek için uygulanabilir öneriler içerir.
- `warnings`: Kaynak, mevzuat, etik veya insan kontrolü gerektiren riskleri içerir.

`approved` ve `requires_revision` alanlarının birbiriyle çelişmemesi Pydantic doğrulamasıyla kontrol edilir.

## Otomatik Revizyon Akışı

Reviewer önemli bir sorun tespit ederse şu sonucu döndürür:

```json
{
  "approved": false,
  "requires_revision": true
}
```

Bu durumda Agent Orchestrator:

1. Reviewer geri bildirimlerini alır.
2. Mevcut içeriği geri bildirimlerle birlikte Content Generator’a gönderir.
3. İçeriği geri bildirimlere göre bir kez revize eder.
4. Revize edilen içeriği Brand Reviewer Agent’a tekrar gönderir.
5. İkinci incelemeden sonra nihai sonucu oluşturur.

Revizyon sırasında:

- Kampanya planındaki temel mesajlar korunur.
- Riskli veya aşırı kesin ifadeler ölçülü hâle getirilir.
- Kullanıcı briefinde bulunmayan yeni ürün, hizmet, kaynak veya bağlantı eklenmez.
- İç sistem uyarıları içerik gövdesine veya CTA metnine taşınmaz.
- Briefin kapsamını gereksiz şekilde genişletecek öneriler uygulanmaz.

Başarılı bir revizyon akışında adımlar şu sırada oluşur:

```text
campaign_planner — attempt 1
content_generator — attempt 1
brand_reviewer — attempt 1
content_generator — attempt 2
brand_reviewer — attempt 2
```

## Agent Orchestrator

`AgentOrchestrator`, bütün Agent bileşenlerinin çalışma sırasını yöneten ana sınıftır.

Başlıca görevleri:

- Benzersiz bir `session_id` oluşturmak
- Benzersiz bir `agent_run_id` oluşturmak
- Campaign Planner Agent’ı çalıştırmak
- Content Generator’ı çalıştırmak
- Brand Reviewer Agent’ı çalıştırmak
- Gerekirse içeriği bir kez revize etmek
- Revizyon sonrasında ikinci Reviewer kontrolünü çalıştırmak
- Agent adımlarını ve deneme numaralarını kaydetmek
- Token kullanımlarını birleştirmek
- Kontrollü hataları ortak bir yapıda toplamak
- Nihai `AgentResponse` sonucunu oluşturmak

## Yapılandırılmış Veri Modelleri

Agent bileşenleri arasındaki veri aktarımı Pydantic modelleriyle gerçekleştirilir.

Temel veri modelleri:

- `ContentGenerationRequest`
- `CampaignPlan`
- `GeneratedContent`
- `ReviewResult`
- `ContentArtifact`
- `AgentStep`
- `TokenUsage`
- `AgentError`
- `AgentResponse`

### ContentGenerationRequest

Kullanıcı tarafından gönderilen içerik üretim isteğini temsil eder.

Başlıca alanları:

- `brand_name`
- `vertical`
- `brief`
- `platform`
- `language`
- `tone`
- `target_audience`

### CampaignPlan

Campaign Planner Agent tarafından oluşturulan yapılandırılmış kampanya planını temsil eder.

### GeneratedContent

Content Generator tarafından oluşturulan başlık, içerik gövdesi, CTA, hashtag ve uyarıları temsil eder.

### ReviewResult

Brand Reviewer Agent tarafından oluşturulan onay, revizyon, geri bildirim ve uyarı sonucunu temsil eder.

### AgentStep

Agent akışı sırasında çalışan her bileşenin durumunu ve deneme numarasını tutar.

```json
{
  "agent": "content_generator",
  "status": "completed",
  "message": "Kampanya planına uygun içerik üretildi.",
  "attempt": 1
}
```

### TokenUsage

Gemini API isteklerinde kullanılan input ve output token miktarlarını tutar.

### AgentError

Agent çalışması sırasında oluşan kontrollü hataları ortak bir yapıda saklar.

### AgentResponse

Bütün Agent çalışmasının nihai sonucunu temsil eder.

Örnek:

```json
{
  "session_id": "session-uuid",
  "agent_run_id": "agent-run-uuid",
  "status": "completed",
  "message": "Kampanya planı, içerik üretimi ve marka incelemesi başarıyla tamamlandı.",
  "campaign_plan": {
    "objective": "Kampanya amacı",
    "target_audience": "Hedef kitle",
    "platform": "linkedin",
    "content_type": "linkedin_post",
    "tone": "bilimsel ve profesyonel",
    "key_messages": [
      "Temel mesaj 1",
      "Temel mesaj 2"
    ],
    "cta_strategy": "Platform içi CTA yaklaşımı",
    "constraints": [
      "Doğrulanmamış bilgi kullanılmamalıdır."
    ]
  },
  "review_result": {
    "approved": true,
    "requires_revision": false,
    "feedback": [],
    "warnings": []
  },
  "artifacts": [
    {
      "type": "linkedin_content",
      "title": "İçerik başlığı",
      "content": {
        "title": "İçerik başlığı",
        "body": "Üretilen içerik metni",
        "cta": "Görüşlerinizi yorumlarda paylaşabilirsiniz.",
        "hashtags": [
          "AINNOVA",
          "YapayZeka"
        ],
        "warnings": []
      }
    }
  ],
  "sources": [],
  "steps": [
    {
      "agent": "campaign_planner",
      "status": "completed",
      "message": "Kampanya planı başarıyla oluşturuldu.",
      "attempt": 1
    },
    {
      "agent": "content_generator",
      "status": "completed",
      "message": "Kampanya planına uygun içerik üretildi.",
      "attempt": 1
    },
    {
      "agent": "brand_reviewer",
      "status": "completed",
      "message": "İçerik incelemesi başarıyla tamamlandı.",
      "attempt": 1
    }
  ],
  "errors": [],
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

## Token Kullanım Takibi

Her Gemini çağrısında şu bilgiler kaydedilir:

- Input token miktarı
- Output token miktarı

Bütün Agent çağrılarının toplam token kullanımı nihai `AgentResponse.usage` alanında döndürülür.

```json
{
  "input_tokens": 3500,
  "output_tokens": 900
}
```

## Hata Yönetimi

Agent bileşenlerinde kontrollü hata yönetimi uygulanmıştır.

Sistem:

- Geçici Gemini API hatalarında isteği yeniden deneyebilir.
- Başarısız Agent adımını `failed` olarak işaretler.
- Hata bilgisini `AgentError` yapısında saklar.
- Tamamlanan Agent adımlarını kaydeder.
- Token kullanımını başarılı çağrılar üzerinden toplar.
- Nihai sonucu ortak `AgentResponse` yapısıyla döndürür.

## İçerik Güvenliği Kuralları

Agent promptları aşağıdaki riskleri azaltacak şekilde hazırlanmıştır:

- Uydurma ürün veya hizmet oluşturma
- Var olmayan web sitesi, demo veya teknik dokümana yönlendirme
- Doğrulanmamış iletişim veya sosyal medya kanalı kullanma
- Uydurma istatistik veya akademik kaynak üretme
- Kesin başarı, doğruluk, hız veya verimlilik iddiası oluşturma
- Sağlık, hukuk ve finans gibi hassas sektörlerde kesin sonuç veya garanti verme
- Yapay zekâyı insan uzmanlığının yerine geçen bir sistem olarak sunma
- İç sistem uyarılarını yayınlanacak içerik metniyle karıştırma
- Kullanıcı istemediği hâlde görsel, video veya medya önerme
- Briefte bulunmayan yeni iddiaları Reviewer geri bildirimi olarak önerme
- Sonsuz otomatik revizyon döngüsü oluşturma

Sağlık, hukuk, finans ve regülasyon gibi hassas alanlarda üretilen içerikler yayınlanmadan önce insan ve alan uzmanı kontrolünden geçirilmelidir.

## Kurulum

### 1. Sanal ortam oluşturma

Windows PowerShell üzerinde:

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 2. Bağımlılıkları yükleme

```powershell
pip install -r requirements.txt
```

### 3. Ortam değişkenlerini tanımlama

Proje kökünde `.env.example` dosyası örnek alınarak `.env` dosyası oluşturulmalıdır.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.1-flash-lite
```

## Testler

### Content Generator testi

```powershell
python test_agent.py
```

Content Generator bileşenini bağımsız olarak çalıştırır ve yapılandırılmış içerik çıktısının oluşturulduğunu doğrular.

Başarılı sonuçta:

```json
{
  "status": "completed",
  "errors": []
}
```

dönmesi beklenir.

### Campaign Planner testi

```powershell
python test_planner.py
```

Campaign Planner Agent’ın kullanıcı isteğine göre yapılandırılmış bir kampanya planı oluşturduğunu doğrular.

Başarılı sonuçta:

```json
{
  "step": {
    "agent": "campaign_planner",
    "status": "completed",
    "attempt": 1
  },
  "error": null
}
```

dönmesi beklenir.

### Brand Reviewer testi

```powershell
python test_reviewer.py
```

Brand Reviewer Agent’ın üretilen içeriği inceleyerek yapılandırılmış bir `ReviewResult` oluşturduğunu doğrular.

Başarılı sonuçta:

```json
{
  "review": {
    "approved": true,
    "requires_revision": false
  },
  "error": null
}
```

benzeri bir sonuç dönmesi beklenir.

### Normal Agent akışı testi

```powershell
python test_agent_flow.py
```

Şu akışı çalıştırır:

```text
Campaign Planner
        ↓
Content Generator
        ↓
Brand Reviewer
        ↓
AgentResponse
```

Beklenen Agent adımları:

```text
campaign_planner — attempt 1
content_generator — attempt 1
brand_reviewer — attempt 1
```

Başarılı sonuçta:

```json
{
  "status": "completed",
  "errors": []
}
```

dönmesi beklenir.

### Zorunlu revizyon akışı testi

```powershell
python test_revision_flow.py
```

İlk Brand Reviewer sonucunu kontrollü biçimde revizyon gerektirir hâle getirerek Agent Orchestrator’ın revizyon dalını doğrular.

Test sırasında şu akış çalıştırılır:

```text
Campaign Planner
        ↓
Content Generator — attempt 1
        ↓
Brand Reviewer — attempt 1
        ↓
Content Generator — attempt 2
        ↓
Brand Reviewer — attempt 2
        ↓
AgentResponse
```

Beklenen Agent adımları:

```text
campaign_planner — attempt 1
content_generator — attempt 1
brand_reviewer — attempt 1
content_generator — attempt 2
brand_reviewer — attempt 2
```

Başarılı sonuçta:

```json
{
  "status": "completed",
  "review_result": {
    "approved": true,
    "requires_revision": false
  },
  "errors": []
}
```

dönmesi beklenir.