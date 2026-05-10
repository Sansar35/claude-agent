"""
TEAM VERIFY — Her ajanin GERCEKTEN site'ye istek attigini KANITLAR
=====================================================================
Cikti orneği:
  OK  Groq      | api.groq.com           | 0.42s | "pong" | 12 tokens
  OK  Mistral   | api.mistral.ai         | 1.20s | "pong" | 8  tokens
  ...

Latency 0'dan farkli + token sayisi varsa = GERCEK HTTP istek atildi.
LiteLLM verbose modunda full URL + headers da goruluyor.

Kullanim:
  python verify.py            # normal mod
  python verify.py --verbose  # LiteLLM full HTTP debug
"""
import asyncio
import os
import sys
import time
from pathlib import Path

# UTF-8 zorla
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

import litellm

# Verbose mod (full HTTP URL + headers)
if "--verbose" in sys.argv or "-v" in sys.argv:
    litellm.set_verbose = True
    os.environ["LITELLM_LOG"] = "DEBUG"
else:
    litellm._logging._disable_debugging()
    os.environ["LITELLM_LOG"] = "ERROR"


PING_PROMPT = "Say only the word: pong"


async def ping_http(name: str, env_var: str, model: str, endpoint_url: str):
    """LiteLLM uzerinden minik HTTP cagrisi. Gercekten istek gitti mi gor."""
    key = os.environ.get(env_var, "").strip()
    if not key:
        return {"name": name, "env": env_var, "endpoint": endpoint_url,
                "status": "SKIP", "reason": "key yok"}

    t0 = time.time()
    try:
        resp = await litellm.acompletion(
            model=model,
            messages=[{"role": "user", "content": PING_PROMPT}],
            api_key=key,
            max_tokens=10,
            timeout=25,
        )
        latency = time.time() - t0
        content = (resp.choices[0].message.content or "").strip()[:30]
        tokens = resp.usage.total_tokens if getattr(resp, "usage", None) else 0
        actual_model = getattr(resp, "model", model)
        return {
            "name": name, "env": env_var, "endpoint": endpoint_url,
            "status": "OK", "latency": latency, "tokens": tokens,
            "response": content, "actual_model": actual_model,
        }
    except Exception as e:
        latency = time.time() - t0
        msg = str(e)
        # Hatadan endpoint cikar (litellm bazen URL atiyor exception'a)
        return {
            "name": name, "env": env_var, "endpoint": endpoint_url,
            "status": "FAIL", "latency": latency,
            "error": msg[:120],
        }


async def ping_claude(label: str, model: str):
    """Anthropic katmani (claude-agent-sdk subprocess)."""
    from team import claude_call
    t0 = time.time()
    try:
        r = await claude_call(PING_PROMPT, model, "Be terse.")
        latency = time.time() - t0
        return {
            "name": f"Claude {label}", "env": "(abonelik)",
            "endpoint": "claude.exe subprocess",
            "status": "OK", "latency": latency,
            "response": r[:30].replace("\n", " "),
            "tokens": "n/a (subprocess)",
        }
    except Exception as e:
        return {
            "name": f"Claude {label}", "env": "(abonelik)",
            "endpoint": "claude.exe subprocess",
            "status": "FAIL", "latency": time.time() - t0,
            "error": str(e)[:120],
        }


# Her provider icin: (label, env_var, litellm_model_id, gercek_endpoint_url)
HTTP_PROVIDERS = [
    ("Gemini",       "GEMINI_API_KEY",     "gemini/gemini-2.5-pro",
        "generativelanguage.googleapis.com"),
    ("Google",       "GOOGLE_API_KEY",     "gemini/gemini-2.5-pro",
        "generativelanguage.googleapis.com"),
    ("Mistral",      "MISTRAL_API_KEY",    "mistral/mistral-large-latest",
        "api.mistral.ai"),
    ("Groq",         "GROQ_API_KEY",       "groq/llama-3.3-70b-versatile",
        "api.groq.com"),
    ("Cerebras",     "CEREBRAS_API_KEY",   "cerebras/qwen-3-235b-a22b-instruct-2507",
        "api.cerebras.ai"),
    ("Together",     "TOGETHER_API_KEY",
        "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "api.together.xyz"),
    ("OpenRouter",   "OPENROUTER_API_KEY", "openrouter/meta-llama/llama-3.3-70b-instruct",
        "openrouter.ai"),
    ("OpenAI",       "OPENAI_API_KEY",     "openai/gpt-4o-mini",
        "api.openai.com"),
    ("DeepSeek",     "DEEPSEEK_API_KEY",   "deepseek/deepseek-chat",
        "api.deepseek.com"),
    ("xAI Grok",     "XAI_API_KEY",        "xai/grok-3",
        "api.x.ai"),
    ("Cohere",       "COHERE_API_KEY",     "cohere/command-a-03-2025",
        "api.cohere.com"),
    ("Perplexity",   "PERPLEXITY_API_KEY", "perplexity/sonar",
        "api.perplexity.ai"),
    ("Fireworks",    "FIREWORKS_API_KEY",
        "fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct",
        "api.fireworks.ai"),
    ("DeepInfra",    "DEEPINFRA_API_KEY",  "deepinfra/deepseek-ai/DeepSeek-V3",
        "api.deepinfra.com"),
    ("NVIDIA",       "NVIDIA_API_KEY",     "nvidia_nim/meta/llama-3.3-70b-instruct",
        "integrate.api.nvidia.com"),
    ("HuggingFace",  "HUGGINGFACE_API_KEY","huggingface/meta-llama/Llama-3.3-70B-Instruct",
        "api-inference.huggingface.co"),
    ("Hyperbolic",   "HYPERBOLIC_API_KEY", "hyperbolic/meta-llama/Meta-Llama-3.1-70B-Instruct",
        "api.hyperbolic.xyz"),
    ("SambaNova",    "SAMBANOVA_API_KEY",  "sambanova/Meta-Llama-3.3-70B-Instruct",
        "api.sambanova.ai"),
]


async def main():
    print()
    print("=" * 88)
    print("  TEAM VERIFY  -  Her ajanin GERCEKTEN siteye HTTP istek attigini kanitlar")
    print("=" * 88)
    print()

    print("[ANTHROPIC KATMANI - claude-agent-sdk subprocess]")
    print("  " + "-" * 84)
    sys.stdout.flush()

    claude_tasks = [
        ping_claude("Opus 4.7",   "claude-opus-4-7"),
        ping_claude("Sonnet 4.6", "claude-sonnet-4-6"),
        ping_claude("Haiku 4.5",  "claude-haiku-4-5"),
    ]
    claude_results = await asyncio.gather(*claude_tasks)
    for r in claude_results:
        if r["status"] == "OK":
            print(f"  OK   {r['name']:18s} | {r['endpoint']:30s} | {r['latency']:5.2f}s | resp: {r['response']}")
        else:
            print(f"  FAIL {r['name']:18s} | {r['endpoint']:30s} | {r.get('error','')}")
    sys.stdout.flush()

    print()
    print("[DIS PROVIDERLAR - LiteLLM uzerinden HTTP]")
    print("  " + "-" * 84)
    sys.stdout.flush()

    # Sadece key girilmis olanlari paralel calistir
    seen_envs = set()
    http_tasks = []
    skipped = []
    for label, env, model, endpoint in HTTP_PROVIDERS:
        if env in seen_envs:
            continue
        seen_envs.add(env)
        if not os.environ.get(env, "").strip():
            skipped.append((label, env))
            continue
        http_tasks.append(ping_http(label, env, model, endpoint))

    if http_tasks:
        http_results = await asyncio.gather(*http_tasks)
        for r in http_results:
            if r["status"] == "OK":
                print(f"  OK   {r['name']:18s} | {r['endpoint']:30s} | {r['latency']:5.2f}s | resp: {r['response']:15s} | {r['tokens']} tokens")
            else:
                err = r.get("error", "")[:60]
                print(f"  FAIL {r['name']:18s} | {r['endpoint']:30s} | {r['latency']:5.2f}s | HATA: {err}")

    if skipped:
        print()
        print("  [Atlanan - key girilmemis]")
        for label, env in skipped:
            print(f"    -- {label:18s} ({env})")

    sys.stdout.flush()

    # Ozet
    total_ok = sum(1 for r in claude_results if r["status"] == "OK")
    total_ok += sum(1 for r in http_results if r["status"] == "OK") if http_tasks else 0
    total_fail = sum(1 for r in claude_results if r["status"] == "FAIL")
    total_fail += sum(1 for r in http_results if r["status"] == "FAIL") if http_tasks else 0

    print()
    print("=" * 88)
    print(f"  KANIT: {total_ok} ajan GERCEKTEN siteye HTTP istek atti (latency > 0, response geldi)")
    if total_fail:
        print(f"  HATA: {total_fail} ajan istek atti ama hata aldi (rate limit, model adi, vs.)")
    print(f"  Atlandi: {len(skipped)} ajan (key girilmemis)")
    print("=" * 88)
    print()
    print("  Ek kanit istersen: 'python verify.py --verbose' ile LiteLLM full HTTP URL'leri yazsin")
    print("  Veya: Resource Monitor (Win+R 'resmon') -> Network -> bu komutu calistir,")
    print("  api.groq.com / api.mistral.ai / generativelanguage.googleapis.com")
    print("  domainlerine giden eszamanli paketleri canli gor.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
