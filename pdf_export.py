"""
PDF Export — SkillScope AI
Generates a downloadable PDF report using reportlab (if available)
or falls back to a rich HTML report for download.
"""

import io
import re
from datetime import datetime


def _duration_to_weeks(duration_str: str) -> float:
    """Parse '2-3 weeks' or '3-5 days' into an avg week float."""
    s = duration_str.lower().strip()
    nums = re.findall(r"[\d.]+", s)
    if not nums:
        return 2.0
    avg = sum(float(n) for n in nums) / len(nums)
    if "day" in s:
        avg /= 7
    return avg


def build_weekly_plan(missing_skills: list, get_rec_fn) -> list:
    """
    Build a week-by-week plan from missing skills.
    Returns list of dicts: {week_start, week_end, skill, task, resource}
    """
    plan = []
    current_week = 1
    for skill_info in missing_skills:
        skill_name = skill_info["display"]
        rec = get_rec_fn(skill_name)
        duration = rec.get("duration", "1–2 weeks")
        weeks = max(1, round(_duration_to_weeks(duration)))
        courses = rec.get("courses", [])
        projects = rec.get("projects", [])
        resources = rec.get("resources", [])

        plan.append({
            "week_start": current_week,
            "week_end": current_week + weeks - 1,
            "skill": skill_name.title(),
            "duration": duration,
            "difficulty": rec.get("difficulty", "Intermediate"),
            "weight": skill_info.get("weight", 5),
            "course": courses[0] if courses else f"Search '{skill_name}' on Coursera",
            "course2": courses[1] if len(courses) > 1 else "",
            "project": projects[0] if projects else f"Build a demo with {skill_name}",
            "resource": resources[0] if resources else f"{skill_name} official docs",
        })
        current_week += weeks
    return plan


def generate_html_report(
    resume_name: str,
    gap: dict,
    ats: dict,
    sem: float,
    plan: list,
    missing_skills: list,
    matched_skills: list,
) -> bytes:
    """Generate a styled HTML report as bytes for download."""

    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    total_weeks = plan[-1]["week_end"] if plan else 0

    # Build skill rows
    missing_rows = ""
    for s in missing_skills:
        badge = "🔴 Critical" if s.get("weight", 0) >= 8 else "🟡 Nice-to-have"
        missing_rows += f"<tr><td>{s['display'].title()}</td><td>{s.get('weight',5)}/10</td><td>{badge}</td></tr>"

    matched_rows = ""
    for s in matched_skills[:15]:
        matched_rows += f"<tr><td>{s['display'].title()}</td><td>{s.get('weight',5)}/10</td><td>✅ Matched</td></tr>"

    # Build plan rows
    plan_rows = ""
    for p in plan:
        wk = f"Week {p['week_start']}" if p['week_start'] == p['week_end'] else f"Week {p['week_start']}–{p['week_end']}"
        plan_rows += f"""
        <tr>
            <td><strong>{wk}</strong></td>
            <td>{p['skill']}</td>
            <td>{p['difficulty']}</td>
            <td>{p['course']}</td>
            <td>{p['project']}</td>
            <td>{p['resource']}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SkillScope AI — Resume Analysis Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #0B1020;
    color: #E6E9F2;
    padding: 40px;
    font-size: 14px;
    line-height: 1.6;
  }}
  .header {{
    background: linear-gradient(135deg, #7C3AED, #00F5FF);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 32px;
    color: white;
  }}
  .header h1 {{ font-size: 2rem; font-weight: 800; margin-bottom: 4px; }}
  .header p {{ opacity: 0.85; font-size: 0.9rem; }}
  .scores {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }}
  .score-card {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 20px 16px;
    text-align: center;
  }}
  .score-card .val {{
    font-size: 1.8rem;
    font-weight: 800;
    color: #00F5FF;
  }}
  .score-card .lbl {{
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6B7280;
    margin-top: 4px;
  }}
  h2 {{
    font-size: 1.15rem;
    font-weight: 700;
    color: #00F5FF;
    margin: 32px 0 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0,245,255,0.2);
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 24px;
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    overflow: hidden;
  }}
  th {{
    background: rgba(124,58,237,0.25);
    color: #00F5FF;
    padding: 10px 14px;
    text-align: left;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  td {{
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    color: #B8C1EC;
    font-size: 0.85rem;
  }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(0,245,255,0.03); }}
  .footer {{
    margin-top: 40px;
    text-align: center;
    color: #4B5563;
    font-size: 0.75rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    padding-top: 20px;
  }}
  .pill {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
  }}
  .pill-good {{ background: rgba(0,245,255,0.15); color: #00F5FF; border: 1px solid rgba(0,245,255,0.3); }}
  .pill-warn {{ background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }}
</style>
</head>
<body>

<div class="header">
  <h1>⚡ SkillScope AI — Resume Analysis Report</h1>
  <p>Resume: <strong>{resume_name}</strong> &nbsp;|&nbsp; Generated: {now}</p>
  <p style="margin-top:6px;">ATS Grade: <strong>{ats.get('grade','—')}</strong> &nbsp;|&nbsp;
     Resume Length: <strong>{ats.get('word_count',0)} words</strong> &nbsp;|&nbsp;
     {ats.get('length_status','')}</p>
</div>

<div class="scores">
  <div class="score-card"><div class="val">{gap['weighted_score']}%</div><div class="lbl">Weighted Score</div></div>
  <div class="score-card"><div class="val">{gap['total_matched']}</div><div class="lbl">Matched Skills</div></div>
  <div class="score-card"><div class="val">{gap['total_missing']}</div><div class="lbl">Missing Skills</div></div>
  <div class="score-card"><div class="val">{ats['ats_score']}%</div><div class="lbl">ATS Score</div></div>
  <div class="score-card"><div class="val">{sem}%</div><div class="lbl">Text Similarity</div></div>
</div>

<h2>🔴 Missing Skills — Gap Analysis</h2>
<table>
  <tr><th>Skill</th><th>Importance</th><th>Priority</th></tr>
  {missing_rows or "<tr><td colspan='3' style='text-align:center;color:#6B7280;'>No missing skills — great match!</td></tr>"}
</table>

<h2>✅ Matched Skills (Top 15)</h2>
<table>
  <tr><th>Skill</th><th>Weight</th><th>Status</th></tr>
  {matched_rows or "<tr><td colspan='3' style='text-align:center;color:#6B7280;'>No matches found.</td></tr>"}
</table>

<h2>📅 Weekly Study Plan — {total_weeks} Weeks Total</h2>
<table>
  <tr><th>Timeline</th><th>Skill</th><th>Level</th><th>Course</th><th>Project</th><th>Resource</th></tr>
  {plan_rows or "<tr><td colspan='6' style='text-align:center;color:#6B7280;'>No plan generated.</td></tr>"}
</table>

<h2>💡 ATS Improvement Tips</h2>
<ul style="padding-left:20px;color:#B8C1EC;line-height:2;">
  {''.join(f'<li>{tip}</li>' for tip in ats.get('tips', []))}
</ul>

<div class="footer">
  ⚡ SkillScope AI &nbsp;|&nbsp; AI-Powered Resume Skill Gap Analyzer &nbsp;|&nbsp;
  Empowering students to close skill gaps and land their dream job
</div>

</body>
</html>"""

    return html.encode("utf-8")
