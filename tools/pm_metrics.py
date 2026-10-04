"""
pm_metrics.py — คำนวณตัวเลขบริหารโครงการ (ENGSE202) จากข้อมูลจริงในที่เดียว

อ่าน   docs/data/project_metrics.json      ตัวเลขแผน/ชั่วโมง/กันชน/เครื่องมือ/ROI
       docs/data/github_pull_requests.json ไทม์ไลน์ PR จริงจาก GitHub API
เขียน  docs/data/metrics_summary.md        ตาราง EVM · Reserve · Velocity · Flow · ROI
       docs/images/*.png                   Burnup · CFD · Velocity · EVM

รัน:  python tools/pm_metrics.py
ต้องมี matplotlib (pip install matplotlib) — ใช้เฉพาะตอนสร้างเอกสาร ไม่ใช่ dependency ของโปรแกรม
"""

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "data"
IMAGES = ROOT / "docs" / "images"
BANGKOK = timezone(timedelta(hours=7))

# PR ที่ไม่ใช่งานจริง: sync สาขา (#12 #16 #17) และ PR ที่ปิดโดยไม่ merge (#7 #13 #18)
NON_WORK_PRS = {12, 16, 17}


def load():
    metrics = json.loads((DATA / "project_metrics.json").read_text(encoding="utf-8"))
    prs = json.loads((DATA / "github_pull_requests.json").read_text(encoding="utf-8"))
    return metrics, prs


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(BANGKOK)


def thb(value):
    return f"{value:,.0f}"


# ── EVM ──────────────────────────────────────────────────────────────

def evm_rows(metrics):
    rate = metrics["labor_rate_thb_per_hour"]["value"]
    tools = sum(t["actual_thb"] for t in metrics["tools"])
    rows = []
    for s in metrics["sprints"]:
        scope = s["committed_issues"] + s["added_issues"]
        pv = (s["planned_hours"] + s["reserve_hours"]) * rate
        ev = pv * s["completed_issues"] / scope
        ac = s["actual_hours"]["value"] * rate
        delay = (date.fromisoformat(s["actual_end"]) - date.fromisoformat(s["planned_end"])).days
        rows.append({"name": s["name"], "pv": pv, "ev": ev, "ac": ac, "delay_days": delay,
                     "scope": scope, "done": s["completed_issues"],
                     "committed": s["committed_issues"],
                     "ev_at_planned_end": pv * s["completed_by_planned_end"] / scope,
                     "planned_end": s["planned_end"]})
    total = {k: sum(r[k] for r in rows) for k in ("pv", "ev", "ac")}
    total["ac"] += tools
    total["name"] = "รวม 3 Sprints"
    return rows, total


def indices(row):
    return {
        "sv": row["ev"] - row["pv"], "cv": row["ev"] - row["ac"],
        "spi": row["ev"] / row["pv"], "cpi": row["ev"] / row["ac"],
    }


# ── Contingency reserve ──────────────────────────────────────────────

def reserve_ledger(metrics):
    rate = metrics["labor_rate_thb_per_hour"]["value"]
    balance = metrics["contingency_reserve"]["initial_hours"]
    lines = [("ยอดตั้งต้น", "", 0.0, balance)]
    for d in metrics["contingency_reserve"]["draws"]:
        balance -= d["hours"]
        lines.append((d["id"], d["item"], d["hours"], balance))
    return lines, balance, balance * rate


# ── Flow metrics from GitHub PRs ─────────────────────────────────────

def work_prs(prs):
    return [p for p in prs if p["merged_at"] and p["number"] not in NON_WORK_PRS]


def flow_stats(prs):
    stats = []
    for p in work_prs(prs):
        start, opened, merged = ts(p["first_commit_at"]), ts(p["created_at"]), ts(p["merged_at"])
        stats.append({
            "number": p["number"], "head": p["head"], "user": p["user"],
            "lead_min": (merged - start).total_seconds() / 60,
            "review_min": (merged - opened).total_seconds() / 60,
            "merged": merged,
        })
    return stats


def max_review_wip(prs):
    """จำนวน PR ที่ค้างอยู่ในสถานะ Review พร้อมกันมากที่สุด และเวลาที่เกิด"""
    events = []
    for p in work_prs(prs):
        events.append((ts(p["created_at"]), 1))
        events.append((ts(p["merged_at"]), -1))
    events.sort(key=lambda e: (e[0], e[1]))
    wip, peak, when = 0, 0, None
    for moment, delta in events:
        wip += delta
        if wip > peak:
            peak, when = wip, moment
    return peak, when


# ── ROI ──────────────────────────────────────────────────────────────

def roi(metrics, total_ac):
    rate = metrics["labor_rate_thb_per_hour"]["value"]
    months = metrics["roi"]["horizon_months"]
    b1, b2, b3 = metrics["roi"]["benefits"]
    benefits = {
        "B1": (b1["hours_before_per_month"] - b1["hours_after_per_month"]) * months * rate,
        "B2": b2["minutes_saved_per_run"] / 60 * b2["runs_per_month"] * months * rate,
        "B3": b3["thb_per_month"] * months,
    }
    yearly = sum(benefits.values())
    monthly = yearly / months
    return {
        "benefits": benefits, "yearly": yearly,
        "roi_1y": (yearly - total_ac) / total_ac,
        "roi_3y": (yearly * 3 - total_ac) / total_ac,
        "payback_months": total_ac / monthly,
    }


# ── Charts ───────────────────────────────────────────────────────────

def draw_charts(metrics, prs, rows):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    IMAGES.mkdir(parents=True, exist_ok=True)

    # Burnup — ระดับโครงการ (นับจำนวน issue เพราะ Jira ยังไม่เปิด Story Points)
    points = [
        ("2026-06-29", 16, 0), ("2026-07-06", 16, 2), ("2026-07-13", 16, 4),
        ("2026-08-03", 16, 16), ("2026-08-10", 30, 16), ("2026-09-06", 30, 16),
        ("2026-09-07", 35, 35), ("2026-09-08", 44, 35), ("2026-10-04", 44, 35),
        ("2026-10-05", 45, 45), ("2026-10-07", 45, 45),
    ]
    days = [date.fromisoformat(p[0]) for p in points]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.step(days, [p[1] for p in points], where="post", label="Total scope (issues)",
            color="#2563eb", linewidth=2)
    ax.step(days, [p[2] for p in points], where="post", label="Completed (issues)",
            color="#dc2626", linewidth=2)
    for label, when, y in [("CR-01 + CR-02 + 3 defects", "2026-09-07", 35),
                           ("Sprint 3 planned", "2026-09-08", 44),
                           ("UAT-DEF-01", "2026-10-05", 45)]:
        ax.annotate(label, (date.fromisoformat(when), y), textcoords="offset points",
                    xytext=(-10, 8), ha="right", fontsize=8)
    ax.set_title("Project Burnup — scope vs completed (source: Jira dates + git)")
    ax.set_ylabel("Issues")
    ax.set_ylim(0, 50)
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    fig.tight_layout()
    fig.savefig(IMAGES / "burnup_project.png", dpi=120)
    plt.close(fig)

    # CFD — คืนวันที่ 12→13 ก.ค. (Sprint 1) ความละเอียด 5 นาที
    sprint1 = [p for p in work_prs(prs) if p["number"] <= 11]
    start = datetime(2026, 7, 12, 22, 0, tzinfo=BANGKOK)
    grid = [start + timedelta(minutes=5 * i) for i in range(int(5 * 60 / 5) + 1)]
    progress, review, done = [], [], []
    for t in grid:
        d = sum(1 for p in sprint1 if ts(p["merged_at"]) <= t)
        r = sum(1 for p in sprint1 if ts(p["created_at"]) <= t < ts(p["merged_at"]))
        i = sum(1 for p in sprint1 if ts(p["first_commit_at"]) <= t < ts(p["created_at"]))
        done.append(d)
        review.append(r)
        progress.append(i)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(grid, done, review, progress,
                 labels=["Done (PR merged)", "In Review (PR open)", "In Progress (committing)"],
                 colors=["#16a34a", "#f59e0b", "#3b82f6"], alpha=0.85)
    ax.set_title("Cumulative Flow — Sprint 1 PRs merged on the night of 12→13 Jul 2026 (Bangkok)")
    ax.set_ylabel("Pull requests")
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=BANGKOK))
    fig.tight_layout()
    fig.savefig(IMAGES / "cfd_sprint1_night.png", dpi=120)
    plt.close(fig)

    # Velocity — committed vs completed
    names = [r["name"] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    xs = range(len(rows))
    ax.bar([x - 0.2 for x in xs], [r["committed"] for r in rows], 0.4,
           label="Commitment", color="#94a3b8")
    ax.bar([x + 0.2 for x in xs], [r["done"] for r in rows], 0.4,
           label="Completed", color="#16a34a")
    for x, r in zip(xs, rows):
        ax.text(x + 0.2, r["done"] + 0.3, str(r["done"]), ha="center", fontsize=9)
    ax.set_xticks(list(xs))
    ax.set_xticklabels(names)
    ax.set_ylabel("Issues")
    ax.set_title("Velocity Chart (issue count)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES / "velocity_3_sprints.png", dpi=120)
    plt.close(fig)

    # EVM cumulative PV / EV / AC ณ วันจบแต่ละ sprint
    cum = {"pv": [], "ev": [], "ac": []}
    run = {"pv": 0, "ev": 0, "ac": 0}
    for r in rows:
        for k in run:
            run[k] += r[k]
            cum[k].append(run[k])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(names, cum["pv"], marker="o", label="PV", color="#2563eb")
    ax.plot(names, cum["ev"], marker="s", label="EV", color="#16a34a", linestyle="--")
    ax.plot(names, cum["ac"], marker="^", label="AC", color="#dc2626")
    ax.set_ylabel("THB (cumulative)")
    ax.set_title("Earned Value at sprint completion")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(IMAGES / "evm_cumulative.png", dpi=120)
    plt.close(fig)


# ── Report ───────────────────────────────────────────────────────────

def build_summary(metrics, prs):
    rows, total = evm_rows(metrics)
    out = ["# Metrics Summary (สร้างอัตโนมัติจาก tools/pm_metrics.py — ห้ามแก้ไฟล์นี้ด้วยมือ)", ""]
    rate = metrics["labor_rate_thb_per_hour"]

    out += ["## EVM ณ วันเสร็จจริงของแต่ละ Sprint", "",
            f"อัตราค่าแรง {rate['value']} บาท/ชม. ({rate['status']})", "",
            "| Sprint | PV | EV | AC | SV | CV | SPI | CPI | ส่งช้า (วัน) |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in rows + [total]:
        i = indices(r)
        delay = r.get("delay_days", "")
        out.append(f"| {r['name']} | {thb(r['pv'])} | {thb(r['ev'])} | {thb(r['ac'])} | "
                   f"{thb(i['sv'])} | {thb(i['cv'])} | {i['spi']:.2f} | {i['cpi']:.3f} | "
                   f"{delay} |")

    out += ["", "## SPI ณ วันสิ้นสุดตามแผนของแต่ละ Sprint (มุมมองที่ไม่บอด)", "",
            "| Sprint | วันสิ้นสุดตามแผน | PV | EV ณ วันนั้น | SPI |", "|---|---|---:|---:|---:|"]
    for r in rows:
        out.append(f"| {r['name']} | {r['planned_end']} | {thb(r['pv'])} | "
                   f"{thb(r['ev_at_planned_end'])} | {r['ev_at_planned_end'] / r['pv']:.2f} |")

    lines, balance_h, balance_thb = reserve_ledger(metrics)
    out += ["", "## Contingency Reserve", "", "| รายการ | เรื่อง | เบิก (ชม.) | คงเหลือ (ชม.) |",
            "|---|---|---:|---:|"]
    out += [f"| {a} | {b} | {c:.1f} | {d:.1f} |" for a, b, c, d in lines]
    out += ["", f"คงเหลือสุทธิ **{balance_h:.1f} ชม. = {thb(balance_thb)} บาท**"]

    stats = flow_stats(prs)
    peak, when = max_review_wip(prs)
    s1 = [s for s in stats if s["number"] <= 11]
    s2 = [s for s in stats if s["number"] >= 23]
    out += ["", "## Flow (จาก GitHub PR)", "",
            "| PR | สาขา | ผู้เปิด | Lead time (นาที) | Review (นาที) |",
            "|---|---|---|---:|---:|"]
    out += [f"| #{s['number']} | {s['head']} | {s['user']} | {s['lead_min']:.0f} | "
            f"{s['review_min']:.0f} |" for s in stats]
    for label, group in (("Sprint 1 (#1–#11)", s1), ("Sprint 2 (#23–#26)", s2)):
        avg_review = sum(s["review_min"] for s in group) / len(group)
        avg_lead = sum(s["lead_min"] for s in group) / len(group)
        out.append(f"\n{label}: เฉลี่ย Lead time {avg_lead:.0f} นาที · "
                   f"Review {avg_review:.0f} นาที")
    out.append(f"\nWIP สูงสุดในช่อง Review = **{peak} PR** เมื่อ {when:%Y-%m-%d %H:%M} (เวลาไทย)")

    r = roi(metrics, total["ac"])
    out += ["", "## ROI", "", "| ผลประโยชน์ | บาท/ปี |", "|---|---:|"]
    out += [f"| {k} | {thb(v)} |" for k, v in r["benefits"].items()]
    out += [f"| **รวม** | **{thb(r['yearly'])}** |", "",
            f"ต้นทุน (AC รวม) {thb(total['ac'])} บาท · ROI ปีแรก {r['roi_1y']:+.1%} · "
            f"ROI 3 ปี {r['roi_3y']:+.1%} · คืนทุน {r['payback_months']:.1f} เดือน"]
    return "\n".join(out) + "\n", rows


def main():
    metrics, prs = load()
    summary, rows = build_summary(metrics, prs)
    (DATA / "metrics_summary.md").write_text(summary, encoding="utf-8")
    draw_charts(metrics, prs, rows)
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows เป็น cp1252
    print(summary)


if __name__ == "__main__":
    main()
