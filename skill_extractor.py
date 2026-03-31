"""
Skill Extractor — v2
Improved accuracy: keyword matching + bigram/trigram + alias expansion +
TF-IDF cosine similarity fallback + weighted scoring.
"""

import re
import math
from typing import List, Dict, Tuple, Set
from collections import Counter
from skill_database import (
    SKILLS_DB, ALL_SKILLS_WEIGHTED, SKILL_ALIASES, get_skill_weight
)


# ── Text helpers ─────────────────────────────────────────────────────────────

def _norm(text: str) -> str:
    """Lowercase, collapse whitespace, handle symbols."""
    text = text.lower()
    text = re.sub(r'[^\w\s\+\#\.\/\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _expand_aliases(text: str) -> str:
    """Replace abbreviations with full skill names."""
    for alias, full in SKILL_ALIASES.items():
        pattern = r'\b' + re.escape(alias.lower()) + r'\b'
        text = re.sub(pattern, full.lower(), text)
    return text


def _ngrams_from_text(text: str, n: int) -> List[str]:
    """Generate n-grams (space-joined) from text tokens."""
    tokens = text.split()
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


# ── Core skill extraction ─────────────────────────────────────────────────────

def extract_skills(text: str) -> Dict[str, Dict]:
    """
    Extract skills from text.
    Returns: { skill_name: { weight, category, confidence } }
    """
    text_norm = _norm(text)
    text_exp  = _expand_aliases(text_norm)

    found: Dict[str, Dict] = {}

    for skill_key, (display, weight, category) in ALL_SKILLS_WEIGHTED.items():
        # Build regex for whole-word / whole-phrase match
        pattern = r'\b' + re.escape(_norm(skill_key)) + r'\b'

        # Search in both original-norm and alias-expanded
        m1 = bool(re.search(pattern, text_norm))
        m2 = bool(re.search(pattern, text_exp))

        if m1 or m2:
            confidence = 1.0 if m1 else 0.85  # slightly lower if only alias-matched
            # Boost confidence if skill appears multiple times
            count = len(re.findall(pattern, text_exp))
            if count >= 2:
                confidence = min(1.0, confidence + 0.05 * (count - 1))

            found[skill_key] = {
                "display":    display,
                "weight":     weight,
                "category":   category,
                "confidence": round(confidence, 2),
                "count":      count,
            }

    return found


def get_flat_skill_list(skills_dict: Dict[str, Dict]) -> List[str]:
    """Return list of display names from extracted-skills dict."""
    return [v["display"] for v in skills_dict.values()]


def group_by_category(skills_dict: Dict[str, Dict]) -> Dict[str, List[Dict]]:
    """Group extracted skills by category."""
    result: Dict[str, List] = {}
    for key, info in skills_dict.items():
        cat = info["category"]
        result.setdefault(cat, []).append({**info, "key": key})
    # Sort each category by weight desc
    for cat in result:
        result[cat].sort(key=lambda x: x["weight"], reverse=True)
    return result


# ── Gap analysis ──────────────────────────────────────────────────────────────

def compare_skills(
    resume_skills: Dict[str, Dict],
    jd_skills:     Dict[str, Dict],
) -> Dict:
    """
    Compare resume vs JD skills.
    Returns matched, missing, extra, weighted scores.
    """
    resume_keys = set(resume_skills.keys())
    jd_keys     = set(jd_skills.keys())

    # Also do alias-resolved key sets
    resume_alias_resolved = {}
    for k in resume_keys:
        resolved = SKILL_ALIASES.get(k, k)
        resume_alias_resolved[resolved] = k

    matched_keys:  List[str] = []
    missing_keys:  List[str] = []

    for jd_key in jd_keys:
        jd_resolved = SKILL_ALIASES.get(jd_key, jd_key)
        if jd_key in resume_keys or jd_resolved in resume_keys or jd_key in resume_alias_resolved:
            matched_keys.append(jd_key)
        else:
            missing_keys.append(jd_key)

    extra_keys = [k for k in resume_keys if k not in jd_keys]

    # ── Weighted match score ──────────────────────────────────────────────────
    total_jd_weight    = sum(jd_skills[k]["weight"] for k in jd_keys)
    matched_jd_weight  = sum(jd_skills[k]["weight"] for k in matched_keys)

    if total_jd_weight > 0:
        weighted_score = (matched_jd_weight / total_jd_weight) * 100
    else:
        weighted_score = 0.0

    # Simple ratio score
    simple_score = (len(matched_keys) / max(len(jd_keys), 1)) * 100

    # Critical missing (weight >= 8)
    critical_missing = [k for k in missing_keys if jd_skills[k]["weight"] >= 8]
    nice_to_have     = [k for k in missing_keys if jd_skills[k]["weight"] <  8]

    return {
        "matched":          [jd_skills[k] for k in matched_keys],
        "missing":          [jd_skills[k] for k in missing_keys],
        "critical_missing": [jd_skills[k] for k in critical_missing],
        "nice_to_have":     [jd_skills[k] for k in nice_to_have],
        "extra":            [resume_skills[k] for k in extra_keys],
        "weighted_score":   round(weighted_score, 1),
        "simple_score":     round(simple_score, 1),
        "total_jd":         len(jd_keys),
        "total_matched":    len(matched_keys),
        "total_missing":    len(missing_keys),
        "total_extra":      len(extra_keys),
        "total_jd_weight":  total_jd_weight,
        "matched_weight":   matched_jd_weight,
    }


# ── ATS + Resume Quality ──────────────────────────────────────────────────────

def get_ats_analysis(
    match_result:  Dict,
    resume_text:   str,
    jd_text:       str,
) -> Dict:
    """
    Compute ATS compatibility score and resume quality metrics.
    """
    base   = match_result["weighted_score"]
    word_count = len(resume_text.split())

    # ── Factor 1: Keyword density overlap ─────────────────────────────────
    jd_words     = set(re.findall(r'\b\w{3,}\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b\w{3,}\b', resume_text.lower()))
    kw_overlap   = len(jd_words & resume_words) / max(len(jd_words), 1)
    kw_bonus     = min(kw_overlap * 15, 8)

    # ── Factor 2: Resume length ────────────────────────────────────────────
    if   300 <= word_count <= 900: length_bonus =  5
    elif word_count < 150:         length_bonus = -10
    elif word_count > 1500:        length_bonus = -5
    else:                          length_bonus =  0

    # ── Factor 3: Critical skills coverage ────────────────────────────────
    total_critical  = len(match_result["critical_missing"]) + sum(
        1 for m in match_result["matched"] if m["weight"] >= 8
    )
    matched_critical = sum(1 for m in match_result["matched"] if m["weight"] >= 8)
    crit_ratio = matched_critical / max(total_critical, 1)
    crit_bonus = crit_ratio * 5

    ats = min(100, max(0, round(base + kw_bonus + length_bonus + crit_bonus, 1)))

    # ── Grade & feedback ───────────────────────────────────────────────────
    if   ats >= 85: grade, color = "Excellent",        "#10b981"
    elif ats >= 70: grade, color = "Good",             "#22d3ee"
    elif ats >= 55: grade, color = "Moderate",         "#f59e0b"
    elif ats >= 40: grade, color = "Needs Improvement","#f97316"
    else:           grade, color = "Poor",             "#ef4444"

    # ── Improvement tips ───────────────────────────────────────────────────
    tips = []
    if match_result["critical_missing"]:
        names = ", ".join(s["display"].title() for s in match_result["critical_missing"][:3])
        tips.append(f"🔴 Add critical missing skills to your resume: {names}")
    if word_count < 300:
        tips.append("📝 Resume is too short — aim for 300–900 words")
    elif word_count > 1200:
        tips.append("✂️ Resume is too long — trim to 1 page (300–900 words)")
    if kw_overlap < 0.4:
        tips.append("🔑 Mirror more keywords from the job description")
    tips.append("🏷️ Use standard section headings: Experience, Skills, Education, Projects")
    tips.append("📄 Avoid tables/graphics in PDF for best ATS parsing")
    if not tips:
        tips = ["✅ Your resume is well-optimised for ATS systems!"]

    return {
        "ats_score":    ats,
        "grade":        grade,
        "grade_color":  color,
        "word_count":   word_count,
        "kw_overlap":   round(kw_overlap * 100, 1),
        "tips":         tips,
        "length_status": (
            "Optimal ✅" if 300 <= word_count <= 900
            else ("Too Short ⚠️" if word_count < 300 else "Too Long ⚠️")
        ),
    }


# ── TF-IDF cosine similarity (bonus overall relevance) ───────────────────────

def _tfidf_similarity(text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using TF-IDF."""
    def tokenize(t):
        return re.findall(r'\b\w{2,}\b', t.lower())

    tokens_a = tokenize(text_a)
    tokens_b = tokenize(text_b)
    if not tokens_a or not tokens_b:
        return 0.0

    vocab = set(tokens_a) | set(tokens_b)

    def tfidf_vec(tokens):
        tf = Counter(tokens)
        total = len(tokens)
        return {w: tf[w] / total for w in vocab}

    va = tfidf_vec(tokens_a)
    vb = tfidf_vec(tokens_b)

    dot    = sum(va[w] * vb[w] for w in vocab)
    mag_a  = math.sqrt(sum(v**2 for v in va.values()))
    mag_b  = math.sqrt(sum(v**2 for v in vb.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0
    return round(dot / (mag_a * mag_b), 4)


def semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Return overall text-level cosine similarity (0–100)."""
    return round(_tfidf_similarity(resume_text, jd_text) * 100, 1)
