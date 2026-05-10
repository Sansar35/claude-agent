"""
MULTI-AI TEAM
====================
Lider:  Claude Opus 4.7  (Claude Max abonelik, KEY GEREKMEZ — claude-agent-sdk)
Worker: Claude Sonnet 4.6 + Haiku 4.5 (yine abonelik) + diger AI'lar (key ile)

Akis:
  1. Lider (Opus) projeyi parcalar, ekibe gorev dagitir
  2. Worker'lar PARALEL calisir (asyncio.gather)
  3. Lider tum ciktilari sentezler ve son halini verir

Kullanim:
  python team.py "FastAPI ile JWT login API yaz"
"""
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# .env (sablon) + .env.local (gercek key'ler, override) yukle
try:
    from dotenv import load_dotenv
    _here = Path(__file__).parent
    load_dotenv(_here / ".env")                      # bos sablon (GitHub'da)
    load_dotenv(_here / ".env.local", override=True) # gercek key'ler (lokal, .gitignore'da)
except ImportError:
    pass

from claude_agent_sdk import query, ClaudeAgentOptions
import litellm

# Sessiz mod — litellm log spam yapmasin
litellm.suppress_debug_info = True
os.environ.setdefault("LITELLM_LOG", "ERROR")

# =====================================================================
# OBSERVABILITY — gercek zamanli istek goz takibi
# =====================================================================
VERBOSE = os.environ.get("TEAM_VERBOSE", "1") == "1"   # default ACIK
LOG_DIR = Path(__file__).parent / "runs"
LOG_DIR.mkdir(exist_ok=True)
RUN_ID = datetime.now().strftime("%Y%m%d-%H%M%S")
LOG_FILE = LOG_DIR / f"run-{RUN_ID}.jsonl"

# Provider URL haritasi — "litellm model string" → gercek API endpoint
PROVIDER_URLS = {
    "openai/":          "https://api.openai.com/v1/chat/completions",
    "gemini/":          "https://generativelanguage.googleapis.com/v1beta/models",
    "deepseek/":        "https://api.deepseek.com/v1/chat/completions",
    "mistral/":         "https://api.mistral.ai/v1/chat/completions",
    "groq/":            "https://api.groq.com/openai/v1/chat/completions",
    "cerebras/":        "https://api.cerebras.ai/v1/chat/completions",
    "together_ai/":     "https://api.together.xyz/v1/chat/completions",
    "fireworks_ai/":    "https://api.fireworks.ai/inference/v1/chat/completions",
    "xai/":             "https://api.x.ai/v1/chat/completions",
    "cohere/":          "https://api.cohere.com/v2/chat",
    "hyperbolic/":      "https://api.hyperbolic.xyz/v1/chat/completions",
    "sambanova/":       "https://api.sambanova.ai/v1/chat/completions",
    "nvidia_nim/":      "https://integrate.api.nvidia.com/v1/chat/completions",
    "deepinfra/":       "https://api.deepinfra.com/v1/openai/chat/completions",
    "openrouter/":      "https://openrouter.ai/api/v1/chat/completions",
    "azure/":           "https://<azure-endpoint>/openai/deployments/<model>/chat/completions",
    "bedrock/":         "https://bedrock-runtime.<region>.amazonaws.com/model/<id>/invoke",
    "vertex_ai/":       "https://<region>-aiplatform.googleapis.com/v1/projects/<project>/locations/<region>/publishers",
    "watsonx/":         "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat",
    "databricks/":      "https://<workspace>.databricks.com/serving-endpoints/<model>/invocations",
    "snowflake/":       "https://<account>.snowflakecomputing.com/api/v2/cortex/inference:complete",
    "replicate/":       "https://api.replicate.com/v1/predictions",
    "anyscale/":        "https://api.endpoints.anyscale.com/v1/chat/completions",
    "baseten/":         "https://app.baseten.co/models/<id>/predict",
    "octoai/":          "https://text.octoai.run/v1/chat/completions",
    "lepton/":          "https://<model>.lepton.run/api/v1/chat/completions",
    "siliconflow/":     "https://api.siliconflow.cn/v1/chat/completions",
    "novita/":          "https://api.novita.ai/v3/openai/chat/completions",
    "kluster/":         "https://api.kluster.ai/v1/chat/completions",
    "lambda/":          "https://api.lambdalabs.com/v1/chat/completions",
    "friendliai/":      "https://inference.friendli.ai/v1/chat/completions",
    "aimlapi/":         "https://api.aimlapi.com/v1/chat/completions",
    "nscale/":          "https://inference.api.nscale.com/v1/chat/completions",
    "featherless_ai/":  "https://api.featherless.ai/v1/chat/completions",
    "netmind/":         "https://api.netmind.ai/v1/chat/completions",
    # Cin saglayicilari
    # Niche
    "ai21/":            "https://api.ai21.com/studio/v1/chat/completions",
    "writer/":          "https://api.writer.com/v1/chat",
    "voyage/":          "https://api.voyageai.com/v1/embeddings",
    "jina/":            "https://api.jina.ai/v1/embeddings",
    "anthropic-claude-code": "claude-agent-sdk (Claude Max abonelik — local OAuth)",
}

def _resolve_url(model: str) -> str:
    for prefix, url in PROVIDER_URLS.items():
        if model.startswith(prefix):
            return url
    return f"<bilinmeyen-provider:{model.split('/')[0]}>"

def _log_event(event: dict):
    """JSONL append — her satir tek event. Run sonu pivot icin yeterli."""
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

def _vprint(line: str):
    if VERBOSE:
        print(line, flush=True)


# =====================================================================
# DINAMIK ROUTING — Hata alan ajanlari oturum boyunca skip et
# =====================================================================
_FAILED_WORKERS: dict[str, str] = {}  # {worker_name: error_msg}

def _mark_failed(worker_name: str, error: str):
    """Bu oturumda fail eden worker'i kaydet — sonraki cagrida skip edilir."""
    _FAILED_WORKERS[worker_name] = error
    _log_event({"ts": time.time(), "phase": "worker_marked_failed",
                "worker": worker_name, "error": error[:200]})

def _get_failed_workers() -> set[str]:
    """Hata cache'i — develop() bunu okuyup skip listesi olusturur."""
    return set(_FAILED_WORKERS.keys())

def _reset_failed():
    """Manuel reset — sonraki develop() cagrisinda tum worker'lara tekrar sans ver."""
    _FAILED_WORKERS.clear()

# =====================================================================
# ANTHROPIC KATMANI (subscription, key gerekmez)
# =====================================================================
async def claude_call(prompt: str, model: str = "claude-opus-4-7", system: str = "") -> str:
    """Claude Max aboneligi uzerinden Claude'i cagirir. KEY YOK."""
    t0 = time.time()
    url = PROVIDER_URLS["anthropic-claude-code"]
    _vprint(f"  [REQ] {model:32s} -> {url}  (prompt={len(prompt)}c)")
    _log_event({"ts": t0, "phase": "request", "model": model, "url": url, "prompt_chars": len(prompt)})

    options = ClaudeAgentOptions(
        model=model,
        system_prompt=system if system else None,
        max_turns=1,
    )
    parts = []
    try:
        async for msg in query(prompt=prompt, options=options):
            content = getattr(msg, "content", None)
            if isinstance(content, list):
                for block in content:
                    txt = getattr(block, "text", None)
                    if txt:
                        parts.append(txt)
            elif isinstance(content, str):
                parts.append(content)
        out = "".join(parts).strip() or "[bos cevap]"
        dt = time.time() - t0
        _vprint(f"  [RES] {model:32s} <- OK  ({len(out)}c, {dt:.1f}s)")
        _log_event({"ts": time.time(), "phase": "response", "model": model, "url": url,
                    "ok": True, "response_chars": len(out), "duration_s": round(dt, 2)})
        return out
    except Exception as e:
        dt = time.time() - t0
        _vprint(f"  [ERR] {model:32s} <- FAIL ({e}, {dt:.1f}s)")
        _log_event({"ts": time.time(), "phase": "response", "model": model, "url": url,
                    "ok": False, "error": str(e), "duration_s": round(dt, 2)})
        return f"[HATA {model}: {e}]"

# =====================================================================
# DIGER AI KATMANI (LiteLLM, key ile)
# =====================================================================
async def litellm_call(model: str, prompt: str, api_key: str, system: str = "") -> str:
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    t0 = time.time()
    url = _resolve_url(model)
    key_mask = (api_key[:6] + "..." + api_key[-3:]) if api_key else "(no-key)"
    _vprint(f"  [REQ] {model:48s} -> {url}  (key={key_mask}, prompt={len(prompt)}c)")
    _log_event({"ts": t0, "phase": "request", "model": model, "url": url,
                "key_masked": key_mask, "prompt_chars": len(prompt)})
    try:
        resp = await litellm.acompletion(
            model=model,
            messages=msgs,
            api_key=api_key,
            timeout=180,
        )
        out = (resp.choices[0].message.content or "").strip() or "[bos cevap]"
        dt = time.time() - t0
        # Token kullanimi (litellm response.usage)
        usage = getattr(resp, "usage", None)
        usage_dict = {}
        if usage:
            usage_dict = {
                "prompt_tokens":     getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens":      getattr(usage, "total_tokens", None),
            }
        _vprint(f"  [RES] {model:48s} <- OK  ({len(out)}c, {dt:.1f}s, tok={usage_dict.get('total_tokens', '?')})")
        _log_event({"ts": time.time(), "phase": "response", "model": model, "url": url,
                    "ok": True, "response_chars": len(out), "duration_s": round(dt, 2),
                    "usage": usage_dict})
        return out
    except Exception as e:
        dt = time.time() - t0
        _vprint(f"  [ERR] {model:48s} <- FAIL ({type(e).__name__}: {str(e)[:80]}, {dt:.1f}s)")
        _log_event({"ts": time.time(), "phase": "response", "model": model, "url": url,
                    "ok": False, "error": f"{type(e).__name__}: {str(e)[:200]}", "duration_s": round(dt, 2)})
        return f"[HATA {model}: {e}]"

# =====================================================================
# EKIP HAVUZU
# =====================================================================
def _key(env_name: str) -> str:
    return os.environ.get(env_name, "").strip()

def build_workers(mode: str = "heavy") -> list[dict]:
    """Hangi key'ler girildiyse o ajanlar aktive olur.

    mode:
      - 'light' = sadece Anthropic 3'lu (Sonnet + Haiku worker, Opus lider).
                  Kucuk isler icin, ucuz, hizli, abonelik kaynakli.
      - 'heavy' = tum aktif key'li provider'lar dahil olur. Buyuk / agir isler icin.
    """
    workers: list[dict] = []

    # === 1) ANTHROPIC (subscription, her zaman aktif) ===
    workers.append({
        "name":   "claude-sonnet",
        "role":   "Senior Yazilim Mimari (Claude Sonnet 4.6)",
        "system": "Senior software architect. Clean code, SOLID, design patterns. Terse output.",
        "fn":     lambda p, s: claude_call(p, "claude-sonnet-4-6", s),
    })
    workers.append({
        "name":   "claude-haiku",
        "role":   "Hizli Yardimci (Claude Haiku 4.5)",
        "system": "Quick utility coder. Small tasks, refactors, regex, type fixes.",
        "fn":     lambda p, s: claude_call(p, "claude-haiku-4-5", s),
    })

    # LIGHT MODE: sadece Anthropic, key-bazli provider'lara hic gecme
    if mode == "light":
        return workers

    # === 2) OPENROUTER (tek key ile coklu model) ===
    OR = _key("OPENROUTER_API_KEY")
    if OR:
        for model, name, role in [
            ("openrouter/openai/gpt-5",                          "gpt-5",     "Frontend Uzmani (GPT-5)"),
            ("openrouter/google/gemini-2.5-pro",                 "gemini",    "Code Reviewer (Gemini 2.5 Pro)"),
            ("openrouter/deepseek/deepseek-chat",                "deepseek",  "ML / AI Mimari (DeepSeek V3.2)"),
            ("openrouter/meta-llama/llama-3.3-70b-instruct",     "llama",     "QA Test Yazici (Llama 3.3 70B)"),
            ("openrouter/qwen/qwen-2.5-72b-instruct",            "qwen",      "Backend Specialist (Qwen 2.5 72B)"),
            ("openrouter/mistralai/mistral-large",               "mistral",   "Dokuman Yazari (Mistral Large)"),
            ("openrouter/x-ai/grok-3",                           "grok",      "Performance Optimizer (Grok 3)"),
        ]:
            workers.append({
                "name": name, "role": role,
                "system": f"You are {role}. Output concise, code-focused, production-grade.",
                "fn":     lambda p, s, m=model, k=OR: litellm_call(m, p, k, s),
            })

    # === 3) DIREKT PROVIDERLAR — HER KEY ICIN COKLU MODEL ===
    # Her satir = ayri agent. Tek key, birden fazla model = birden fazla paralel ajan.
    DIRECTS = [
        # ---------- OpenAI (GPT ailesi — 8 ajan) ----------
        ("OPENAI_API_KEY",      "openai/gpt-5",                                                      "openai-gpt5",        "OpenAI GPT-5 (flagship)"),
        ("OPENAI_API_KEY",      "openai/gpt-5-mini",                                                 "openai-gpt5mini",    "OpenAI GPT-5 Mini (hizli/ucuz)"),
        ("OPENAI_API_KEY",      "openai/gpt-4o",                                                     "openai-4o",          "OpenAI GPT-4o (multimodal)"),
        ("OPENAI_API_KEY",      "openai/gpt-4o-mini",                                                "openai-4omini",      "OpenAI GPT-4o Mini"),
        ("OPENAI_API_KEY",      "openai/o1",                                                         "openai-o1",          "OpenAI o1 (reasoning)"),
        ("OPENAI_API_KEY",      "openai/o1-mini",                                                    "openai-o1mini",      "OpenAI o1 Mini"),
        ("OPENAI_API_KEY",      "openai/o3",                                                         "openai-o3",          "OpenAI o3 (advanced reasoning)"),
        ("OPENAI_API_KEY",      "openai/o3-mini",                                                    "openai-o3mini",      "OpenAI o3 Mini"),

        # ---------- Google Gemini (5 ajan) — GEMINI_API_KEY ----------
        ("GEMINI_API_KEY",      "gemini/gemini-2.5-pro",                                             "gemini-25pro",       "Gemini 2.5 Pro (uzun context)"),
        ("GEMINI_API_KEY",      "gemini/gemini-2.5-flash",                                           "gemini-25flash",     "Gemini 2.5 Flash (hizli)"),
        ("GEMINI_API_KEY",      "gemini/gemini-2.0-flash",                                           "gemini-20flash",     "Gemini 2.0 Flash"),
        ("GEMINI_API_KEY",      "gemini/gemini-1.5-pro",                                             "gemini-15pro",       "Gemini 1.5 Pro"),
        ("GEMINI_API_KEY",      "gemini/gemini-1.5-flash",                                           "gemini-15flash",     "Gemini 1.5 Flash"),

        # ---------- Google alt key (GOOGLE_API_KEY) — bos ise atlanir ----------
        ("GOOGLE_API_KEY",      "gemini/gemini-2.5-pro",                                             "google-25pro",       "Google Gemini 2.5 Pro (alt key)"),
        ("GOOGLE_API_KEY",      "gemini/gemini-2.5-flash",                                           "google-25flash",     "Google Gemini 2.5 Flash (alt key)"),

        # ---------- DeepSeek (2 ajan) ----------
        ("DEEPSEEK_API_KEY",    "deepseek/deepseek-chat",                                            "deepseek-chat",      "DeepSeek V3 Chat (genel)"),
        ("DEEPSEEK_API_KEY",    "deepseek/deepseek-reasoner",                                        "deepseek-r1",        "DeepSeek R1 (reasoning)"),

        # ---------- Mistral (6 ajan) ----------
        ("MISTRAL_API_KEY",     "mistral/mistral-large-latest",                                      "mistral-large",      "Mistral Large (flagship)"),
        ("MISTRAL_API_KEY",     "mistral/mistral-medium-latest",                                     "mistral-medium",     "Mistral Medium"),
        ("MISTRAL_API_KEY",     "mistral/mistral-small-latest",                                      "mistral-small",      "Mistral Small"),
        ("MISTRAL_API_KEY",     "mistral/codestral-latest",                                          "mistral-codestral",  "Mistral Codestral (code)"),
        ("MISTRAL_API_KEY",     "mistral/ministral-8b-latest",                                       "mistral-ministral",  "Mistral Ministral 8B"),
        ("MISTRAL_API_KEY",     "mistral/pixtral-large-latest",                                      "mistral-pixtral",    "Mistral Pixtral (vision)"),

        # ---------- Groq (8 ajan — ucuz/hizli) ----------
        ("GROQ_API_KEY",        "groq/llama-3.3-70b-versatile",                                      "groq-llama33",       "Groq Llama 3.3 70B (versatile)"),
        ("GROQ_API_KEY",        "groq/llama-3.1-8b-instant",                                         "groq-llama31",       "Groq Llama 3.1 8B (instant)"),
        ("GROQ_API_KEY",        "groq/llama-3.2-90b-vision-preview",                                 "groq-llama-vision",  "Groq Llama 3.2 90B Vision"),
        ("GROQ_API_KEY",        "groq/qwen-2.5-32b",                                                 "groq-qwen",          "Groq Qwen 2.5 32B"),
        ("GROQ_API_KEY",        "groq/deepseek-r1-distill-llama-70b",                                "groq-r1distill",     "Groq DeepSeek R1 Distill 70B"),
        ("GROQ_API_KEY",        "groq/gemma2-9b-it",                                                 "groq-gemma2",        "Groq Gemma2 9B"),
        ("GROQ_API_KEY",        "groq/mistral-saba-24b",                                             "groq-saba",          "Groq Mistral Saba 24B"),
        ("GROQ_API_KEY",        "groq/llama3-70b-8192",                                              "groq-llama3-70",     "Groq Llama 3 70B (8K)"),

        # ---------- Cerebras (4 ajan — ultra hizli) ----------
        ("CEREBRAS_API_KEY",    "cerebras/qwen-3-235b-a22b-instruct-2507",                           "cerebras-qwen235",   "Cerebras Qwen 3 235B MoE"),
        ("CEREBRAS_API_KEY",    "cerebras/llama-3.3-70b",                                            "cerebras-llama33",   "Cerebras Llama 3.3 70B"),
        ("CEREBRAS_API_KEY",    "cerebras/llama-4-scout-17b-16e-instruct",                           "cerebras-llama4",    "Cerebras Llama 4 Scout 17B"),
        ("CEREBRAS_API_KEY",    "cerebras/llama3.1-8b",                                              "cerebras-llama31",   "Cerebras Llama 3.1 8B"),

        # ---------- Together (6 ajan) ----------
        ("TOGETHER_API_KEY",    "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",               "together-llama33",   "Together Llama 3.3 70B Turbo"),
        ("TOGETHER_API_KEY",    "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",         "together-llama405",  "Together Llama 3.1 405B Turbo"),
        ("TOGETHER_API_KEY",    "together_ai/Qwen/Qwen2.5-72B-Instruct-Turbo",                       "together-qwen72",    "Together Qwen 2.5 72B Turbo"),
        ("TOGETHER_API_KEY",    "together_ai/mistralai/Mixtral-8x22B-Instruct-v0.1",                 "together-mixtral",   "Together Mixtral 8x22B"),
        ("TOGETHER_API_KEY",    "together_ai/deepseek-ai/DeepSeek-V3",                               "together-dsv3",      "Together DeepSeek V3"),
        ("TOGETHER_API_KEY",    "together_ai/Qwen/QwQ-32B-Preview",                                  "together-qwq",       "Together QwQ 32B (reasoning)"),

        # ---------- Fireworks (5 ajan) ----------
        ("FIREWORKS_API_KEY",   "fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct",    "fireworks-llama33",  "Fireworks Llama 3.3 70B"),
        ("FIREWORKS_API_KEY",   "fireworks_ai/accounts/fireworks/models/llama-v3p1-405b-instruct",   "fireworks-llama405", "Fireworks Llama 3.1 405B"),
        ("FIREWORKS_API_KEY",   "fireworks_ai/accounts/fireworks/models/qwen2p5-72b-instruct",       "fireworks-qwen72",   "Fireworks Qwen 2.5 72B"),
        ("FIREWORKS_API_KEY",   "fireworks_ai/accounts/fireworks/models/deepseek-v3",                "fireworks-dsv3",     "Fireworks DeepSeek V3"),
        ("FIREWORKS_API_KEY",   "fireworks_ai/accounts/fireworks/models/mixtral-8x22b-instruct",     "fireworks-mixtral",  "Fireworks Mixtral 8x22B"),

        # ---------- xAI (3 ajan) ----------
        ("XAI_API_KEY",         "xai/grok-3",                                                        "xai-grok3",          "xAI Grok 3"),
        ("XAI_API_KEY",         "xai/grok-3-mini",                                                   "xai-grok3mini",      "xAI Grok 3 Mini"),
        ("XAI_API_KEY",         "xai/grok-2-vision-1212",                                            "xai-grok2vision",    "xAI Grok 2 Vision"),

        # ---------- Cohere (4 ajan) — model adlari 2025-09-15 sonrasi guncel ----------
        ("COHERE_API_KEY",      "cohere/command-a-03-2025",                                          "cohere-a",           "Cohere Command A (flagship 03-2025)"),
        ("COHERE_API_KEY",      "cohere/command-r-plus-08-2024",                                     "cohere-rplus",       "Cohere Command R+ (08-2024)"),
        ("COHERE_API_KEY",      "cohere/command-r-08-2024",                                          "cohere-r",           "Cohere Command R (08-2024)"),
        ("COHERE_API_KEY",      "cohere/command-r7b-12-2024",                                        "cohere-r7b",         "Cohere Command R7B (12-2024)"),

        # ---------- Hyperbolic (5 ajan) ----------
        ("HYPERBOLIC_API_KEY",  "hyperbolic/meta-llama/Meta-Llama-3.1-405B-Instruct",                "hyper-llama405",     "Hyperbolic Llama 3.1 405B"),
        ("HYPERBOLIC_API_KEY",  "hyperbolic/meta-llama/Meta-Llama-3.1-70B-Instruct",                 "hyper-llama70",      "Hyperbolic Llama 3.1 70B"),
        ("HYPERBOLIC_API_KEY",  "hyperbolic/meta-llama/Meta-Llama-3.3-70B-Instruct",                 "hyper-llama33",      "Hyperbolic Llama 3.3 70B"),
        ("HYPERBOLIC_API_KEY",  "hyperbolic/Qwen/Qwen2.5-72B-Instruct",                              "hyper-qwen72",       "Hyperbolic Qwen 2.5 72B"),
        ("HYPERBOLIC_API_KEY",  "hyperbolic/deepseek-ai/DeepSeek-V3",                                "hyper-dsv3",         "Hyperbolic DeepSeek V3"),

        # ---------- SambaNova (4 ajan) ----------
        ("SAMBANOVA_API_KEY",   "sambanova/Meta-Llama-3.3-70B-Instruct",                             "samba-llama33",      "SambaNova Llama 3.3 70B"),
        ("SAMBANOVA_API_KEY",   "sambanova/Meta-Llama-3.1-405B-Instruct",                            "samba-llama405",     "SambaNova Llama 3.1 405B"),
        ("SAMBANOVA_API_KEY",   "sambanova/Qwen2.5-72B-Instruct",                                    "samba-qwen72",       "SambaNova Qwen 2.5 72B"),
        ("SAMBANOVA_API_KEY",   "sambanova/DeepSeek-V3-0324",                                        "samba-dsv3",         "SambaNova DeepSeek V3"),

        # ---------- NVIDIA NIM (3 ajan) — bos ise atlanir ----------
        ("NVIDIA_API_KEY",      "nvidia_nim/meta/llama-3.3-70b-instruct",                            "nvidia-llama33",     "NVIDIA Llama 3.3 70B"),
        ("NVIDIA_API_KEY",      "nvidia_nim/meta/llama-3.1-405b-instruct",                           "nvidia-llama405",    "NVIDIA Llama 3.1 405B"),
        ("NVIDIA_API_KEY",      "nvidia_nim/qwen/qwen2.5-72b-instruct",                              "nvidia-qwen72",      "NVIDIA Qwen 2.5 72B"),

        # ---------- DeepInfra (4 ajan) — bos ise atlanir ----------
        ("DEEPINFRA_API_KEY",   "deepinfra/deepseek-ai/DeepSeek-V3",                                 "deepinfra-dsv3",     "DeepInfra DeepSeek V3"),
        ("DEEPINFRA_API_KEY",   "deepinfra/meta-llama/Meta-Llama-3.3-70B-Instruct",                  "deepinfra-llama33",  "DeepInfra Llama 3.3 70B"),
        ("DEEPINFRA_API_KEY",   "deepinfra/Qwen/Qwen2.5-72B-Instruct",                               "deepinfra-qwen72",   "DeepInfra Qwen 2.5 72B"),
        ("DEEPINFRA_API_KEY",   "deepinfra/mistralai/Mixtral-8x22B-Instruct-v0.1",                   "deepinfra-mixtral",  "DeepInfra Mixtral 8x22B"),

        # ---------- AWS Bedrock (4 ajan) — Claude/Llama/Mistral/Cohere ----------
        ("AWS_BEDROCK_ACCESS_KEY", "bedrock/anthropic.claude-opus-4-7-20251201-v1:0",                "bedrock-opus",       "Bedrock Claude Opus 4.7"),
        ("AWS_BEDROCK_ACCESS_KEY", "bedrock/meta.llama3-3-70b-instruct-v1:0",                        "bedrock-llama33",    "Bedrock Llama 3.3 70B"),
        ("AWS_BEDROCK_ACCESS_KEY", "bedrock/mistral.mistral-large-2407-v1:0",                        "bedrock-mistral",    "Bedrock Mistral Large"),
        ("AWS_BEDROCK_ACCESS_KEY", "bedrock/cohere.command-r-plus-v1:0",                             "bedrock-cohere",     "Bedrock Cohere Command R+"),

        # ---------- Azure OpenAI (3 ajan) — endpoint .env'den ----------
        ("AZURE_OPENAI_API_KEY",   "azure/gpt-5",                                                    "azure-gpt5",         "Azure OpenAI GPT-5"),
        ("AZURE_OPENAI_API_KEY",   "azure/gpt-4o",                                                   "azure-4o",           "Azure OpenAI GPT-4o"),
        ("AZURE_OPENAI_API_KEY",   "azure/o3",                                                       "azure-o3",           "Azure OpenAI o3"),

        # ---------- Google Vertex AI (3 ajan) ----------
        ("VERTEX_AI_PROJECT_ID",   "vertex_ai/gemini-2.5-pro",                                       "vertex-25pro",       "Vertex AI Gemini 2.5 Pro"),
        ("VERTEX_AI_PROJECT_ID",   "vertex_ai/claude-opus-4-7",                                      "vertex-opus",        "Vertex AI Claude Opus 4.7"),
        ("VERTEX_AI_PROJECT_ID",   "vertex_ai/meta/llama-3.3-70b-instruct",                          "vertex-llama33",     "Vertex AI Llama 3.3 70B"),

        # ---------- IBM WatsonX (2 ajan) ----------
        ("WATSONX_API_KEY",        "watsonx/meta-llama/llama-3-3-70b-instruct",                      "watsonx-llama33",    "WatsonX Llama 3.3 70B"),
        ("WATSONX_API_KEY",        "watsonx/ibm/granite-3-8b-instruct",                              "watsonx-granite",    "WatsonX IBM Granite 3 8B"),

        # ---------- Databricks (2 ajan) ----------
        ("DATABRICKS_API_KEY",     "databricks/databricks-meta-llama-3-3-70b-instruct",              "dbrx-llama33",       "Databricks Llama 3.3 70B"),
        ("DATABRICKS_API_KEY",     "databricks/databricks-dbrx-instruct",                            "dbrx-dbrx",          "Databricks DBRX Instruct"),

        # ---------- Replicate (3 ajan — Llama/FLUX) ----------
        ("REPLICATE_API_TOKEN",    "replicate/meta/meta-llama-3-70b-instruct",                       "rep-llama70",        "Replicate Llama 3 70B"),
        ("REPLICATE_API_TOKEN",    "replicate/meta/meta-llama-3.1-405b-instruct",                    "rep-llama405",       "Replicate Llama 3.1 405B"),
        ("REPLICATE_API_TOKEN",    "replicate/mistralai/mixtral-8x7b-instruct-v0.1",                 "rep-mixtral",        "Replicate Mixtral 8x7B"),

        # ---------- AnyScale (3 ajan) ----------
        ("ANYSCALE_API_KEY",       "anyscale/meta-llama/Meta-Llama-3.1-70B-Instruct",                "any-llama70",        "AnyScale Llama 3.1 70B"),
        ("ANYSCALE_API_KEY",       "anyscale/meta-llama/Meta-Llama-3.1-405B-Instruct",               "any-llama405",       "AnyScale Llama 3.1 405B"),
        ("ANYSCALE_API_KEY",       "anyscale/mistralai/Mixtral-8x22B-Instruct-v0.1",                 "any-mixtral",        "AnyScale Mixtral 8x22B"),

        # ---------- OctoAI (2 ajan) ----------
        ("OCTOAI_API_KEY",         "octoai/meta-llama-3.1-70b-instruct",                             "octo-llama70",       "OctoAI Llama 3.1 70B"),
        ("OCTOAI_API_KEY",         "octoai/mixtral-8x22b-instruct",                                  "octo-mixtral",       "OctoAI Mixtral 8x22B"),

        # ---------- SiliconFlow (4 ajan — Cin OS cloud) ----------
        ("SILICONFLOW_API_KEY",    "siliconflow/deepseek-ai/DeepSeek-V3",                            "sf-dsv3",            "SiliconFlow DeepSeek V3"),
        ("SILICONFLOW_API_KEY",    "siliconflow/Qwen/Qwen2.5-72B-Instruct",                          "sf-qwen72",          "SiliconFlow Qwen 2.5 72B"),
        ("SILICONFLOW_API_KEY",    "siliconflow/meta-llama/Meta-Llama-3.1-405B-Instruct",            "sf-llama405",        "SiliconFlow Llama 3.1 405B"),
        ("SILICONFLOW_API_KEY",    "siliconflow/01-ai/Yi-1.5-34B-Chat",                              "sf-yi34",            "SiliconFlow Yi 1.5 34B"),

        # ---------- Novita AI (3 ajan) ----------
        ("NOVITA_API_KEY",         "novita/meta-llama/llama-3.3-70b-instruct",                       "nov-llama33",        "Novita Llama 3.3 70B"),
        ("NOVITA_API_KEY",         "novita/qwen/qwen-2.5-72b-instruct",                              "nov-qwen72",         "Novita Qwen 2.5 72B"),
        ("NOVITA_API_KEY",         "novita/deepseek/deepseek-v3",                                    "nov-dsv3",           "Novita DeepSeek V3"),

        # ---------- Lambda Labs (2 ajan) ----------
        ("LAMBDALABS_API_KEY",     "lambda/llama3.3-70b-instruct-fp8",                               "lam-llama33",        "Lambda Llama 3.3 70B FP8"),
        ("LAMBDALABS_API_KEY",     "lambda/llama3.1-405b-instruct-fp8",                              "lam-llama405",       "Lambda Llama 3.1 405B FP8"),

        # ---------- Friendli AI (2 ajan) ----------
        ("FRIENDLI_API_KEY",       "friendliai/meta-llama-3.3-70b-instruct",                         "fri-llama33",        "Friendli Llama 3.3 70B"),
        ("FRIENDLI_API_KEY",       "friendliai/mixtral-8x22b-instruct-v0-1",                         "fri-mixtral",        "Friendli Mixtral 8x22B"),

        # ---------- Aimlapi (3 ajan — multi-provider proxy) ----------
        ("AIMLAPI_API_KEY",        "aimlapi/gpt-4o",                                                 "aiml-gpt4o",         "AIMLAPI GPT-4o"),
        ("AIMLAPI_API_KEY",        "aimlapi/meta-llama/Llama-3.3-70B-Instruct",                      "aiml-llama33",       "AIMLAPI Llama 3.3 70B"),
        ("AIMLAPI_API_KEY",        "aimlapi/deepseek-v3",                                            "aiml-dsv3",          "AIMLAPI DeepSeek V3"),

        # ---------- Lepton, Baseten, Kluster, NScale, NetMind, Featherless (1'er) ----------
        ("LEPTON_API_KEY",         "lepton/llama3-3-70b",                                            "lep-llama33",        "Lepton Llama 3.3 70B"),
        ("BASETEN_API_KEY",        "baseten/llama-3-3-70b-instruct",                                 "bas-llama33",        "Baseten Llama 3.3 70B"),
        ("KLUSTER_API_KEY",        "kluster/meta-llama/Llama-3.3-70B-Instruct",                      "klu-llama33",        "Kluster Llama 3.3 70B"),
        ("NSCALE_API_KEY",         "nscale/meta-llama/Llama-3.3-70B-Instruct",                       "nsc-llama33",        "NScale Llama 3.3 70B"),
        ("NETMIND_API_KEY",        "netmind/meta-llama/Llama-3.3-70B-Instruct",                      "net-llama33",        "NetMind Llama 3.3 70B"),
        ("FEATHERLESS_API_KEY",    "featherless_ai/meta-llama/Meta-Llama-3.1-70B-Instruct",          "fea-llama70",        "Featherless Llama 3.1 70B"),
        ("TARGON_API_KEY",         "openai/llama-3.3-70b",                                           "tar-llama33",        "Targon Llama 3.3 70B"),
        ("INFERENCE_NET_API_KEY",  "openai/meta-llama/Meta-Llama-3.1-70B-Instruct",                  "inf-llama70",        "Inference.net Llama 3.1 70B"),

        # ---------- NICHE / OZEL ----------
        ("AI21_API_KEY",           "ai21/jamba-1.5-large",                                           "ai21-jamba",         "AI21 Jamba 1.5 Large"),
        ("WRITER_API_KEY",         "writer/palmyra-x-004",                                           "writer-palmyra",     "Writer Palmyra X 004"),
        ("INFLECTION_API_KEY",     "openai/Pi-3.0",                                                  "inflection-pi",      "Inflection Pi 3.0"),
        ("ALEPH_ALPHA_API_KEY",    "openai/luminous-supreme",                                        "aleph-luminous",     "Aleph Alpha Luminous Supreme"),
    ]
    # Duplicate koruma: ayni (key, model) ikilisini iki kez ekleme
    seen = set()
    for env_name, model, name, role in DIRECTS:
        k = _key(env_name)
        if not k:
            continue
        sig = (k, model)
        if sig in seen:
            continue
        seen.add(sig)
        workers.append({
            "name": name, "role": role,
            "system": f"You are {role}. Output concise, code-focused, production-grade.",
            "fn":     lambda p, s, m=model, kk=k: litellm_call(m, p, kk, s),
        })

    return workers

# =====================================================================
# ORCHESTRATION
# =====================================================================
async def develop(brief: str, lead_model: str = "", mode: str = "heavy") -> str:
    lead = lead_model or _key("LEAD_MODEL") or "claude-opus-4-7"
    workers = build_workers(mode=mode)

    print(f"\n[TEAM] Mode: {mode.upper()}  ({'sadece Anthropic 3lu' if mode == 'light' else 'tum aktif provider'})")
    print(f"[TEAM] Lider: {lead} (subscription)")
    print(f"[TEAM] Worker sayisi: {len(workers)}")
    print(f"[TEAM] Verbose istek izleme: {'ACIK' if VERBOSE else 'KAPALI'}  (env TEAM_VERBOSE=0 ile kapatabilirsin)")
    print(f"[TEAM] Run log: {LOG_FILE}")
    print(f"[TEAM] Pivot ozet: python summary.py {LOG_FILE.name}\n")
    for w in workers:
        print(f"  - {w['role']}")
    _log_event({"ts": time.time(), "phase": "session_start", "mode": mode, "lead": lead,
                "worker_count": len(workers), "brief": brief[:200]})

    # === ADIM 1: LIDER PLAN YAPSIN ===
    print("\n[ADIM 1] Lider (Opus) projeyi parcaliyor...")
    plan_prompt = f"""PROJE ISTEGI:
{brief}

EKIP UZMANLARI:
{chr(10).join(f'- [{w["name"]}] {w["role"]}' for w in workers)}

GOREVIN:
1. Bu projeyi {len(workers)} alt-goreve bol — her uzmana 1 alt-gorev.
2. Her alt-gorevi 2-3 cumlede acikla.
3. Cikti formati ZORUNLU:
GOREV [uzman-name]: aciklama metni
GOREV [uzman-name]: aciklama metni
...
"""
    plan = await claude_call(
        plan_prompt,
        model=lead,
        system="Sen Hive Mind lidersin. Project Manager + Architect rolunde dusun. Net ve dagitilabilir plan cikar.",
    )
    print("\n--- LIDER PLANI ---")
    print(plan)
    print("--- /PLAN ---\n")

    # === ADIM 2: WORKER'LAR PARALEL CALISSIN — DINAMIK ROUTING ===
    # Filtre: daha onceki cagrida fail olan worker'lar bu turn da CONNECTION_BROKEN listesinde ise skip edilir.
    skip_list = _get_failed_workers()
    active_workers = [w for w in workers if w["name"] not in skip_list]
    skipped_count = len(workers) - len(active_workers)
    if skipped_count > 0:
        print(f"[ADIM 2] {len(active_workers)} aktif worker (oturumda hata almis {skipped_count} ajan ATLANDI)")
    else:
        print(f"[ADIM 2] {len(workers)} worker PARALEL calisiyor (asyncio.gather)...")

    async def _run(w):
        sub = f"""ANA PROJE: {brief}

LIDER PLANI:
{plan}

SENIN GOREVIN: Plan icinde "[{w['name']}]" olarak senden istenen kismi tamamla.
Sadece kendi alaninda uretim yap. Kisa aciklama + asil cikti (kod/dok/test).
"""
        try:
            r = await w["fn"](sub, w["system"])
            # Bos response veya HATA isareti = fail say
            if not r or r.startswith("[HATA") or r.startswith("[bos cevap"):
                _mark_failed(w["name"], "empty/hata response")
                print(f"  [FAIL] {w['name']:18s} bos/hata response")
                return {"name": w["name"], "role": w["role"], "result": None, "ok": False}
            print(f"  [OK]   {w['name']:18s} ({len(r)} char)")
            return {"name": w["name"], "role": w["role"], "result": r, "ok": True}
        except Exception as e:
            _mark_failed(w["name"], str(e)[:80])
            print(f"  [FAIL] {w['name']:18s} {type(e).__name__}: {str(e)[:60]}")
            return {"name": w["name"], "role": w["role"], "result": None, "ok": False}

    all_results = await asyncio.gather(*(_run(w) for w in active_workers))

    # Basarili ve fail ayikla
    success = [r for r in all_results if r["ok"]]
    failed  = [r for r in all_results if not r["ok"]]
    print(f"\n[ROUTING] BASARILI: {len(success)} ajan  |  FAIL: {len(failed)} ajan  |  SKIP: {skipped_count} (onceden hata)")
    if failed:
        print(f"[ROUTING] Fail eden ajanlar (bu oturumda artik atlanir): {', '.join(r['name'] for r in failed)}")

    # === ADIM 3: LIDER SENTEZLESIN — sadece basarililari kullan ===
    print(f"\n[ADIM 3] Lider (Opus) {len(success)} basarili ciktiyi sentezliyor (fail/skip olanlar dahil edilmedi)...")
    if not success:
        return "[HATA] Hicbir worker basarili response uretmedi. .env.local key'lerini kontrol et veya provider servisleri uzgun olabilir."

    synth = "\n\n".join(
        f"### {r['role']} ({r['name']})\n{r['result']}" for r in success
    )
    fail_note = ""
    if failed or skipped_count > 0:
        fail_note = f"\n\nNOT: {len(failed)} ajan bu istekte hata aldi, {skipped_count} ajan onceki hatalardan skip edildi. Final cikti sadece {len(success)} basarili ajan uzerinden hazirlandi."
    synth_prompt = f"""PROJE: {brief}

EKIBIN URETTIKLERI ({len(success)} ajan):
{synth}{fail_note}

GOREVIN:
- Tum basarili ciktilari birlestir, celiskileri coz, son halini ver
- Eksik parcalar varsa kendi tamamla
- Tutarsizliklari duzelt
- Calistirilabilir / yayinlanabilir final teslimat ver
- Turkce yorum/aciklama, kod ingilizce kalir
"""
    final = await claude_call(
        synth_prompt,
        model=lead,
        system="Sen Lidersin. Sentezci, kararli, eksiksiz. Final cikti uret.",
    )
    return final

def main():
    args = list(sys.argv[1:])
    mode = "heavy"

    # --light / --heavy flag parse
    if "--light" in args:
        mode = "light"
        args.remove("--light")
    if "--heavy" in args:
        mode = "heavy"
        args.remove("--heavy")
    if "--mode=light" in args:
        mode = "light"
        args.remove("--mode=light")
    if "--mode=heavy" in args:
        mode = "heavy"
        args.remove("--mode=heavy")

    if not args:
        print(__doc__)
        print("\nKULLANIM:")
        print("  python team.py 'proje aciklamasi'              # default = heavy")
        print("  python team.py 'kucuk fix' --light             # sadece Claude 3lu")
        print("  python team.py 'agir feature' --heavy          # tum keyli AI'lar")
        sys.exit(1)

    brief = " ".join(args)
    result = asyncio.run(develop(brief, mode=mode))
    print("\n" + "=" * 72)
    print(f"FINAL CIKTI (Lider Sentezi — Mode: {mode.upper()})")
    print("=" * 72)
    print(result)

if __name__ == "__main__":
    main()
