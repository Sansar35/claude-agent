"""
JARVIZ Team Run Summary
=======================
runs/<id>.jsonl dosyasini okur ve provider/model basina ozetler:
  - kac istek atildi
  - kac OK / kac FAIL
  - toplam token (varsa)
  - ortalama duration

Kullanim:
  python summary.py                        # en son run
  python summary.py run-20260509-143022    # belirli run
  python summary.py runs/run-...jsonl      # tam yol
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
RUNS_DIR = ROOT / "runs"


def find_log(arg: str | None) -> Path:
    if arg:
        p = Path(arg)
        if p.is_file():
            return p
        p2 = RUNS_DIR / arg
        if p2.is_file():
            return p2
        p3 = RUNS_DIR / f"{arg}.jsonl"
        if p3.is_file():
            return p3
        sys.exit(f"Log bulunamadi: {arg}")
    files = sorted(RUNS_DIR.glob("run-*.jsonl"))
    if not files:
        sys.exit("Hic run yok. Once `python team.py '...'` ile bir oturum baslat.")
    return files[-1]


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    logf = find_log(arg)

    print("=" * 78)
    print(f"JARVIZ TEAM RUN SUMMARY  —  {logf.name}")
    print("=" * 78)

    events = []
    with logf.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    session = next((e for e in events if e.get("phase") == "session_start"), {})
    if session:
        print(f"\nMode: {session.get('mode', '?').upper()}")
        print(f"Lider: {session.get('lead', '?')}")
        print(f"Worker: {session.get('worker_count', '?')}")
        print(f"Brief: {session.get('brief', '?')[:120]}")

    # Provider basina pivot
    by_provider = defaultdict(lambda: {
        "requests": 0, "ok": 0, "fail": 0,
        "total_chars_in": 0, "total_chars_out": 0,
        "total_tokens": 0, "durations": [],
        "models": set(),
    })

    pending_req = {}  # ts → event (request)
    for e in events:
        phase = e.get("phase")
        url = e.get("url", "<bilinmeyen>")
        # Provider isim cikar (ornek: "https://api.openai.com/..." → "openai")
        prov = url.split("//")[-1].split("/")[0].replace("api.", "").replace(".com", "").replace(".ai", "").replace(".xyz", "")
        if "anthropic" in prov or "claude" in prov.lower() or "claude-agent-sdk" in url:
            prov = "anthropic"

        model = e.get("model", "?")
        rec = by_provider[prov]
        rec["models"].add(model)

        if phase == "request":
            rec["requests"] += 1
            rec["total_chars_in"] += e.get("prompt_chars", 0) or 0
        elif phase == "response":
            if e.get("ok"):
                rec["ok"] += 1
                rec["total_chars_out"] += e.get("response_chars", 0) or 0
                u = e.get("usage") or {}
                if u.get("total_tokens"):
                    rec["total_tokens"] += u["total_tokens"]
            else:
                rec["fail"] += 1
            d = e.get("duration_s")
            if d is not None:
                rec["durations"].append(d)

    # Cikti
    print("\n" + "=" * 78)
    print(f"{'PROVIDER':18s} {'MODEL#':>6s} {'REQ':>5s} {'OK':>4s} {'FAIL':>5s} {'OUT_CHAR':>10s} {'TOKEN':>8s} {'AVG_S':>6s}")
    print("-" * 78)
    grand = {"requests": 0, "ok": 0, "fail": 0, "tokens": 0, "out": 0}
    for prov, r in sorted(by_provider.items(), key=lambda x: -x[1]["requests"]):
        avg = sum(r["durations"]) / len(r["durations"]) if r["durations"] else 0
        print(f"{prov:18s} {len(r['models']):>6d} {r['requests']:>5d} {r['ok']:>4d} {r['fail']:>5d} "
              f"{r['total_chars_out']:>10d} {r['total_tokens']:>8d} {avg:>6.1f}")
        grand["requests"] += r["requests"]
        grand["ok"] += r["ok"]
        grand["fail"] += r["fail"]
        grand["tokens"] += r["total_tokens"]
        grand["out"] += r["total_chars_out"]
    print("-" * 78)
    print(f"{'TOPLAM':18s} {'':>6s} {grand['requests']:>5d} {grand['ok']:>4d} {grand['fail']:>5d} "
          f"{grand['out']:>10d} {grand['tokens']:>8d}")
    print("=" * 78)


if __name__ == "__main__":
    main()
