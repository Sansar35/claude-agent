"""
Hangi ajanlar aktif gorur. API cagrisi YAPMAZ — sadece konfigurasyon ozeti.
Kullanim: python test.py
"""
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from team import build_workers

print("=" * 60)
print("MULTI-AI TEAM — SMOKE TEST")
print("=" * 60)
print("\n* LIDER (ANA MERKEZ): claude-opus-4-7  (Claude Max abonelik, key gerekmez)")
print("  Workers/ajanlar yardimci rolde -- Opus plan yapar, sentezler, final cikar.\n")

workers_light = build_workers(mode="light")
workers_heavy = build_workers(mode="heavy")

print("\n--- LIGHT MODE (kucuk isler — sadece Anthropic 3lu) ---")
print(f"Worker sayisi: {len(workers_light)}  (+ Lider Opus = toplam {len(workers_light)+1} AI)")
for i, w in enumerate(workers_light, 1):
    print(f"  {i:2d}. [{w['name']:18s}] {w['role']}")

print("\n--- HEAVY MODE (buyuk isler — tum aktif provider) ---")
print(f"Worker sayisi: {len(workers_heavy)}  (+ Lider Opus = toplam {len(workers_heavy)+1} AI)")
for i, w in enumerate(workers_heavy, 1):
    print(f"  {i:2d}. [{w['name']:18s}] {w['role']}")

print("\n" + "=" * 60)
print("KEY DURUMU (.env'den okundu)")
print("=" * 60)
keys = [
    # Onerilen
    "OPENROUTER_API_KEY",
    # Ana cloud
    "OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY",
    "DEEPSEEK_API_KEY", "MISTRAL_API_KEY", "GROQ_API_KEY", "CEREBRAS_API_KEY",
    "TOGETHER_API_KEY", "FIREWORKS_API_KEY", "XAI_API_KEY", "COHERE_API_KEY",
    "DEEPINFRA_API_KEY", "NVIDIA_API_KEY",
    "HYPERBOLIC_API_KEY", "SAMBANOVA_API_KEY",
    "PERPLEXITY_API_KEY", "HUGGINGFACE_API_KEY",
    # Ek premium / enterprise
    "ANTHROPIC_API_KEY", "AZURE_OPENAI_API_KEY", "AWS_BEDROCK_ACCESS_KEY",
    "VERTEX_AI_PROJECT_ID", "WATSONX_API_KEY", "DATABRICKS_API_KEY",
    "SNOWFLAKE_API_KEY", "CLOUDFLARE_API_KEY", "VERCEL_AI_GATEWAY_KEY",
    "GITHUB_TOKEN",
    # Acik kaynak host
    "REPLICATE_API_TOKEN", "ANYSCALE_API_KEY", "BASETEN_API_KEY",
    "OCTOAI_API_KEY", "LEPTON_API_KEY", "SILICONFLOW_API_KEY",
    "NOVITA_API_KEY", "KLUSTER_API_KEY", "LAMBDALABS_API_KEY",
    "TARGON_API_KEY", "LATITUDE_API_KEY", "INFERENCE_NET_API_KEY",
    "FRIENDLI_API_KEY", "AIMLAPI_API_KEY", "NSCALE_API_KEY",
    "GOOSEAI_API_KEY", "NETMIND_API_KEY", "FEATHERLESS_API_KEY",
    # Cin
    "ZHIPU_API_KEY", "MOONSHOT_API_KEY", "YI_API_KEY", "BAICHUAN_API_KEY",
    "QIANWEN_API_KEY", "DASHSCOPE_API_KEY", "BAIDU_API_KEY",
    "SENSENOVA_API_KEY", "MINIMAX_API_KEY", "SPARK_API_KEY",
    "VOLCENGINE_API_KEY", "HUNYUAN_API_KEY",
    # Niche / ozel
    "AI21_API_KEY", "ALEPH_ALPHA_API_KEY", "INFLECTION_API_KEY",
    "WRITER_API_KEY", "CHARACTER_AI_KEY", "NLPCLOUD_API_KEY",
    "VOYAGE_API_KEY", "JINA_API_KEY", "BAAI_API_KEY",
]
for k in keys:
    val = os.environ.get(k, "").strip()
    status = "[VAR]  " if val else "[bos]  "
    masked = val[:8] + "..." if val else "(girilmedi)"
    print(f"  {status} {k:25s} {masked}")

print()
print("Calistirmak icin: python team.py 'proje aciklamasi'")
