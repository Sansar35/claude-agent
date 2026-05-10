"""
JARVIZ DEMO - Paralelligi GOZLE GOSTERIR
=========================================
Aktif tum worker'lara ayni kisa soruyu sorar, her birinin
basladi/bitti zamanini ASCII grafiginde cizer.

Kullanim:
  python demo.py
  python demo.py "Python'da Fibonacci fonksiyonu yaz"
"""
import asyncio
import os
import sys
import time
from pathlib import Path

# Windows cp1254 -> UTF-8 zorla
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
os.environ["PYTHONIOENCODING"] = "utf-8"

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

from team import build_workers, claude_call

DEFAULT_Q = "Python'da fizzbuzz fonksiyonu yaz. SADECE kod, 5 satiri gecme."


async def demo(question: str):
    workers = build_workers()
    all_agents = [{
        "name": "opus-lider",
        "role": "[*] Claude Opus 4.7 (LIDER)",
        "fn": lambda p, s: claude_call(p, "claude-opus-4-7", s),
        "system": "Be concise.",
    }] + workers

    n = len(all_agents)
    print()
    print("=" * 78)
    print(f"  JARVIZ PARALELLIK DEMO  -  {n} AI motoru AYNI ANDA calisiyor")
    print("=" * 78)
    print(f"  Soru: {question}")
    print("=" * 78)
    print()
    print("  ZAMAN     AJAN")
    print("  --------  ------------------------------------------------------------")
    sys.stdout.flush()

    t0 = time.time()

    async def run(agent):
        s = time.time() - t0
        print(f"  +{s:6.2f}s  >> {agent['role'][:55]:55s}  BASLADI")
        sys.stdout.flush()
        try:
            r = await agent["fn"](question, agent["system"])
            e = time.time() - t0
            d = e - s
            print(f"  +{e:6.2f}s  OK  {agent['role'][:55]:55s}  BITTI ({d:5.2f}s)")
            sys.stdout.flush()
            return {"name": agent["name"], "role": agent["role"], "start": s, "end": e, "dur": d, "result": r, "error": False}
        except Exception as ex:
            e = time.time() - t0
            d = e - s
            print(f"  +{e:6.2f}s  XX  {agent['role'][:55]:55s}  HATA: {str(ex)[:30]}")
            sys.stdout.flush()
            return {"name": agent["name"], "role": agent["role"], "start": s, "end": e, "dur": d, "result": f"[HATA: {ex}]", "error": True}

    results = await asyncio.gather(*(run(a) for a in all_agents), return_exceptions=False)
    total = time.time() - t0
    sequential = sum(r["dur"] for r in results)
    saved = sequential - total
    pct = (saved / sequential * 100) if sequential else 0

    # Bar grafik
    print()
    print("=" * 78)
    print("  ZAMAN CIZGISI (her ajan ne zaman calisti, # = aktif)")
    print("=" * 78)
    if total > 0:
        scale = 60.0 / total
        for r in sorted(results, key=lambda x: x["start"]):
            s_cells = int(r["start"] * scale)
            d_cells = max(1, int(r["dur"] * scale))
            bar = " " * s_cells + ("#" * d_cells)
            marker = "XX" if r.get("error") else "OK"
            print(f"  {marker} {r['role'][:32]:32s} |{bar:60s}| {r['dur']:5.2f}s")
        print(f"     {'':32s} 0s{'-' * 56}{total:.1f}s")

    # Paralellik analizi
    print()
    print("=" * 78)
    print("  PARALELLIK ANALIZI")
    print("=" * 78)
    print(f"    Aktif AI sayisi      : {n}")
    print(f"    Paralel toplam sure  : {total:.2f}s   <- gercekte bekledigin")
    print(f"    Sirayla yapilsaydi   : {sequential:.2f}s")
    print(f"    KAZANC               : {saved:.2f}s   ({pct:.0f}% daha hizli)")
    if saved > total * 0.5:
        print(f"    SONUC                : >>> HEPSI PARALEL CALISTI <<<")
    elif saved > 0:
        print(f"    SONUC                : >>> KISMI PARALEL <<<")
    else:
        print(f"    SONUC                : !!! SIRALI CALISIYOR (sorun var) !!!")
    print()

    # Cevap onizlemeleri
    print("=" * 78)
    print("  CEVAP ONIZLEME (her ajan ilk 90 karakter)")
    print("=" * 78)
    for r in results:
        marker = "XX" if r.get("error") else "OK"
        preview = r["result"][:90].replace('\n', ' / ').replace('\r', '')
        print(f"  {marker} [{r['name']:18s}] {preview}")
    print()


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else DEFAULT_Q
    asyncio.run(demo(q))
