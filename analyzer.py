"""Pure-Python (standard library only) telecom log analysis."""
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from catalog import CATALOGS, ACCEPTED_GTP, SEVERITY_ORDER

SIP_RE = re.compile(r"\bSIP(?:/2\.0)?[\s:_-]*([4-6]\d{2})\b", re.I)
GTP_RE = re.compile(r"\bGTP\w*\b.*?\bcause(?:[\s_]*(?:code|value))?\s*[:=]?\s*(\d{1,3})\b", re.I)
DIA_RE = re.compile(r"\b(?:Experimental-)?Result-Code\s*[:=]?\s*(\d{4})\b", re.I)
TS_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2}:\d{2})")
IP_RE = re.compile(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b")
UNKNOWN = ("Unknown code", "Minor", "Uncategorised",
           "Code not in knowledge base.", "Consult the relevant 3GPP/IETF specification.")
MAX_EVENTS = 5000


def _hits(line):
    for m in SIP_RE.finditer(line):
        yield "SIP", int(m.group(1))
    m = GTP_RE.search(line)
    if m and int(m.group(1)) not in ACCEPTED_GTP:
        yield "GTP", int(m.group(1))
    m = DIA_RE.search(line)
    if m and int(m.group(1)) >= 3000:
        yield "Diameter", int(m.group(1))


def _timeline(events):
    stamps = [(e["_dt"], e["protocol"]) for e in events if e["_dt"]]
    if not stamps:
        return None
    lo = min(s for s, _ in stamps)
    hi = max(s for s, _ in stamps)
    span = max((hi - lo).total_seconds() / 60, 1)
    step = next((s for s in (1, 5, 10, 15, 30, 60, 180, 360, 1440) if span / s <= 120), 1440)
    base = lo.replace(second=0, microsecond=0)
    buckets = defaultdict(Counter)
    for dt, proto in stamps:
        idx = int((dt - base).total_seconds() // 60 // step)
        buckets[idx][proto] += 1
    out = []
    for i in range(max(buckets) + 1):
        t = base + timedelta(minutes=i * step)
        out.append({"t": t.strftime("%Y-%m-%d %H:%M"), "counts": dict(buckets.get(i, {}))})
    return {"step_minutes": step, "buckets": out}


def analyze(data: bytes) -> dict:
    lines = data.decode("utf-8", errors="replace").splitlines()
    events = []
    for n, line in enumerate(lines, 1):
        for proto, code in _hits(line):
            name, sev, cat, meaning, action = CATALOGS[proto].get(code, UNKNOWN)
            ts = TS_RE.search(line)
            ip = IP_RE.search(line)
            dt = None
            if ts:
                try:
                    dt = datetime.strptime(f"{ts.group(1)} {ts.group(2)}", "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    pass
            events.append({
                "line": n, "_dt": dt, "ts": f"{ts.group(1)} {ts.group(2)}" if ts else "",
                "protocol": proto, "code": f"{proto} {code}", "name": name,
                "severity": sev, "category": cat, "meaning": meaning,
                "action": action, "ip": ip.group(1) if ip else "",
                "raw": line.strip()[:300],
            })

    by_code = Counter(e["code"] for e in events)
    info = {}
    for e in events:
        info.setdefault(e["code"], {k: e[k] for k in
                        ("code", "protocol", "name", "severity", "category", "meaning", "action")})
    diagnosis = [dict(info[c], count=n) for c, n in by_code.most_common()]

    result = {
        "total_lines": len(lines),
        "total_events": len(events),
        "distinct_codes": len(by_code),
        "severity_order": SEVERITY_ORDER,
        "by_severity": dict(Counter(e["severity"] for e in events)),
        "by_protocol": dict(Counter(e["protocol"] for e in events)),
        "by_category": dict(Counter(e["category"] for e in events).most_common()),
        "by_ip": dict(Counter(e["ip"] for e in events if e["ip"]).most_common(10)),
        "diagnosis": diagnosis,
        "timeline": _timeline(events),
        "events": [{k: v for k, v in e.items() if k != "_dt"} for e in events[:MAX_EVENTS]],
        "events_truncated": len(events) > MAX_EVENTS,
    }
    return result
