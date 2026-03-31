"""
Job Roles Module — SkillScope AI
- Job role auto-detection from JD
- Interview question bank (per skill)
- Cover letter generator (template-based)
- Resume bullet point analyzer
- Letter grade + competitive percentile
"""

# ── Job Role Detection ─────────────────────────────────────────────────────────
JOB_ROLE_PATTERNS = {
    "AI/ML Research Scientist": {
        "keywords": ["research", "deep learning", "neural networks", "nlp", "transformers",
                     "llm", "generative ai", "bert", "pytorch", "paper", "arxiv"],
        "icon": "🧠", "color": "#7C3AED",
        "focus": "Deep learning research, NLP, LLMs, model architecture",
    },
    "Machine Learning Engineer": {
        "keywords": ["machine learning", "model deployment", "mlops", "tensorflow", "pytorch",
                     "feature engineering", "model training", "pipeline", "inference"],
        "icon": "🤖", "color": "#6366f1",
        "focus": "ML pipelines, model deployment, MLOps, production ML",
    },
    "Data Scientist": {
        "keywords": ["data science", "statistical", "predictive modeling", "python", "r",
                     "pandas", "sklearn", "hypothesis", "experimentation", "a/b testing"],
        "icon": "🔬", "color": "#7C3AED",
        "focus": "ML models, statistical analysis, Python/R, experimentation",
    },
    "Data Analyst": {
        "keywords": ["data analysis", "sql", "tableau", "power bi", "reporting",
                     "dashboards", "excel", "business intelligence", "kpi", "metrics"],
        "icon": "📊", "color": "#00F5FF",
        "focus": "SQL, BI tools, reporting, dashboards, KPIs",
    },
    "Data Engineer": {
        "keywords": ["etl", "data pipeline", "spark", "kafka", "airflow",
                     "data warehouse", "bigquery", "redshift", "snowflake", "dbt"],
        "icon": "🔧", "color": "#f59e0b",
        "focus": "Data pipelines, ETL, Spark, cloud data warehouses",
    },
    "DevOps Engineer": {
        "keywords": ["devops", "docker", "kubernetes", "ci/cd", "aws", "azure",
                     "infrastructure", "pipeline", "terraform", "ansible", "linux"],
        "icon": "🚀", "color": "#ef4444",
        "focus": "CI/CD, cloud infrastructure, containers, automation",
    },
    "Cloud Engineer": {
        "keywords": ["aws", "azure", "gcp", "cloud", "serverless", "terraform",
                     "infrastructure as code", "ec2", "lambda", "s3"],
        "icon": "☁️", "color": "#0ea5e9",
        "focus": "Cloud platforms (AWS/Azure/GCP), IaC, serverless",
    },
    "Full Stack Developer": {
        "keywords": ["full stack", "frontend", "backend", "react", "nodejs",
                     "api", "database", "end-to-end", "fullstack"],
        "icon": "🔄", "color": "#10b981",
        "focus": "Full-stack web development, APIs, databases, UI",
    },
    "Backend Developer": {
        "keywords": ["backend", "api", "rest", "server", "nodejs", "python",
                     "java", "spring", "django", "flask", "fastapi", "microservices"],
        "icon": "⚙️", "color": "#6366f1",
        "focus": "APIs, databases, server-side logic, performance",
    },
    "Frontend Developer": {
        "keywords": ["react", "angular", "vue", "html", "css", "javascript",
                     "typescript", "ui", "ux", "frontend", "responsive"],
        "icon": "🎨", "color": "#f59e0b",
        "focus": "React/Vue, responsive design, JavaScript/TypeScript",
    },
    "Cybersecurity Analyst": {
        "keywords": ["security", "cybersecurity", "penetration", "vulnerability",
                     "firewall", "siem", "threat", "owasp", "ethical hacking"],
        "icon": "🛡️", "color": "#dc2626",
        "focus": "Security audits, threat analysis, vulnerability management",
    },
    "Mobile Developer": {
        "keywords": ["android", "ios", "flutter", "react native", "swift",
                     "kotlin", "mobile app", "jetpack", "swiftui"],
        "icon": "📱", "color": "#8b5cf6",
        "focus": "iOS/Android, Flutter/React Native, mobile UX",
    },
}


def detect_job_role(jd_text: str) -> dict:
    """Detect the most likely job role from a JD using keyword scoring."""
    jd_lower = jd_text.lower()
    scores = {}
    for role, data in JOB_ROLE_PATTERNS.items():
        score = sum(1 for kw in data["keywords"] if kw in jd_lower)
        if score > 0:
            scores[role] = score
    if not scores:
        return {"role": "Software Engineer", "icon": "💻", "color": "#6B7280",
                "focus": "General software engineering", "confidence": 50}
    best_role = max(scores, key=scores.get)
    return {
        "role": best_role,
        "icon": JOB_ROLE_PATTERNS[best_role]["icon"],
        "color": JOB_ROLE_PATTERNS[best_role]["color"],
        "focus": JOB_ROLE_PATTERNS[best_role]["focus"],
        "confidence": min(99, scores[best_role] * 14),
    }


# ── Interview Question Bank ────────────────────────────────────────────────────
INTERVIEW_QUESTIONS = {
    "python": [
        "What are Python decorators and how have you used them in production?",
        "Explain the difference between a list, tuple, set, and dictionary.",
        "How does Python's GIL affect multithreaded programs?",
        "What is the difference between `__init__` and `__new__`?",
        "Explain list comprehensions vs generator expressions and when to use each.",
    ],
    "machine learning": [
        "Explain the bias-variance tradeoff with a real example.",
        "When would you use Random Forest over XGBoost, and vice versa?",
        "How do you handle class imbalance in a classification problem?",
        "Explain cross-validation and why k-fold is preferred over hold-out.",
        "What metrics would you choose to evaluate a regression vs. classification model?",
    ],
    "sql": [
        "What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN?",
        "Explain window functions: ROW_NUMBER, RANK, and DENSE_RANK with an example.",
        "How would you find duplicate rows and remove them from a table?",
        "What is query optimization and how do indexes speed up queries?",
        "Write a query to find the top 3 highest salaries per department.",
    ],
    "deep learning": [
        "Explain the vanishing gradient problem and common solutions (BatchNorm, ReLU, ResNet).",
        "What is the difference between CNN, RNN, LSTM, and Transformer architectures?",
        "When would you use dropout regularization and how does it work?",
        "What is batch normalization and why does it speed up training?",
        "How does the attention mechanism work in transformers?",
    ],
    "aws": [
        "What is the difference between EC2 (IaaS), Lambda (FaaS), and ECS (CaaS)?",
        "How does S3 ensure 99.999999999% durability?",
        "Explain VPC, subnets, NAT gateways, and security groups.",
        "What is the difference between SQS (queue) and SNS (pub/sub)?",
        "How would you architect a highly available, scalable web app on AWS?",
    ],
    "docker": [
        "What is the difference between a Docker image and a running container?",
        "How does Docker networking work (bridge, host, overlay)?",
        "Explain multi-stage builds and their benefits for production images.",
        "What is Docker Compose and when would you use it vs Kubernetes?",
        "How do you persist data in Docker containers (volumes vs bind mounts)?",
    ],
    "kubernetes": [
        "What is the difference between a Pod, Deployment, StatefulSet, and DaemonSet?",
        "How does Kubernetes handle rolling updates and rollbacks?",
        "Explain Horizontal Pod Autoscaler (HPA) and how it works.",
        "What is the difference between ConfigMap and Secret in Kubernetes?",
        "How do liveness probes and readiness probes differ in their purpose?",
    ],
    "react": [
        "Explain the difference between state and props in React.",
        "What are React hooks and why were they introduced over class components?",
        "How does the virtual DOM work and why is reconciliation important?",
        "When would you use useCallback vs useMemo? Give an example.",
        "How do you handle side effects in React (useEffect, cleanup)?",
    ],
    "java": [
        "What is the difference between HashMap and ConcurrentHashMap?",
        "Explain Java's garbage collection mechanisms (G1, ZGC, Shenandoah).",
        "What is the difference between abstract class and interface in Java 8+?",
        "How does Java handle multithreading with ExecutorService and CompletableFuture?",
        "What are Java generics, wildcards (? extends, ? super), and their use cases?",
    ],
    "r": [
        "What is the difference between a data.frame and a tibble in tidyverse?",
        "Explain the apply family (apply, lapply, sapply, vapply) with use cases.",
        "How does ggplot2's grammar of graphics work (aesthetics, geoms, scales)?",
        "What is the difference between `<-` and `=` for assignment in R?",
        "How do you handle missing values (NA) effectively in R?",
    ],
    "c": [
        "Explain the difference between stack and heap memory allocation in C.",
        "What are pointers and how do you avoid pointer arithmetic errors?",
        "What causes a segmentation fault and how do you debug it?",
        "Explain the difference between `malloc`, `calloc`, and `realloc`.",
        "What is a memory leak and how do tools like Valgrind help detect them?",
    ],
    "c++": [
        "What is RAII (Resource Acquisition Is Initialization) and why is it important?",
        "Explain the Rule of Three/Five/Zero in C++.",
        "What is the difference between stack unwinding and exception handling?",
        "How do smart pointers (unique_ptr, shared_ptr) differ from raw pointers?",
        "What is template metaprogramming and when would you use it?",
    ],
    "data analysis": [
        "Walk me through your data cleaning process for a raw, messy dataset.",
        "How do you detect and handle outliers in a dataset?",
        "What is the difference between correlation and causation? Give an example.",
        "How do you choose the right visualization for a given dataset type?",
        "Describe a project where you found a surprising or counter-intuitive insight.",
    ],
    "nlp": [
        "Explain TF-IDF and when you'd use it over word embeddings.",
        "What is the difference between stemming and lemmatization? When to use each?",
        "How does BERT differ from GPT and what are each best suited for?",
        "Explain named entity recognition (NER) and how you'd build an NER system.",
        "How would you build a text classification pipeline from scratch?",
    ],
    "tensorflow": [
        "What is the difference between eager execution and graph mode in TF2?",
        "How do you save and load a TensorFlow model (SavedModel vs HDF5)?",
        "Explain the purpose of tf.data and how it optimizes training pipelines.",
        "How do you implement a custom training loop using GradientTape?",
        "What is tf.function and how does it improve performance?",
    ],
    "pytorch": [
        "What is autograd and how does PyTorch's computational graph work?",
        "Explain the difference between .detach() and torch.no_grad().",
        "How do you implement a custom loss function in PyTorch?",
        "What is DataLoader and how does num_workers affect performance?",
        "How do you distribute training across multiple GPUs in PyTorch?",
    ],
    "git": [
        "What is the difference between git rebase and git merge?",
        "How do you resolve a merge conflict step by step?",
        "Explain GitFlow vs Trunk-Based Development. When to use each?",
        "What does `git stash` do and when is it useful?",
        "How do you revert a commit that has already been pushed to remote?",
    ],
    "statistics": [
        "What is the Central Limit Theorem and why is it fundamental in statistics?",
        "Explain Type I (false positive) and Type II (false negative) errors.",
        "What is a p-value? What does p < 0.05 actually mean?",
        "When would you use a t-test vs chi-squared test vs ANOVA?",
        "What is the difference between Bayesian and frequentist inference?",
    ],
    "ci/cd": [
        "What is the difference between Continuous Integration, Delivery, and Deployment?",
        "How do you handle secrets and credentials securely in a CI/CD pipeline?",
        "What is a rollback strategy and how do you implement it safely?",
        "Explain blue-green deployment and canary releases.",
        "What types of tests should run at each stage of a CI/CD pipeline?",
    ],
    "pandas": [
        "What is the difference between .loc (label-based) and .iloc (integer-based)?",
        "How do you efficiently merge two large DataFrames without running out of memory?",
        "What is vectorization in pandas and why is it faster than for loops?",
        "How do you handle datetime data and time zones in pandas?",
        "Explain groupby + agg and give a real-world use case.",
    ],
    "mongodb": [
        "When would you choose MongoDB over a relational database like PostgreSQL?",
        "Explain the MongoDB aggregation pipeline with an example.",
        "How does MongoDB handle multi-document transactions?",
        "What is sharding in MongoDB and when would you use it?",
        "How do you design indexes for read-heavy vs write-heavy workloads?",
    ],
    "golang": [
        "What are goroutines and how do channels enable communication between them?",
        "How does Go handle error handling differently from exceptions in other languages?",
        "Explain interfaces in Go and how they enable duck typing.",
        "What is the `defer` keyword and how does it work with stack unwinding?",
        "How does Go's garbage collector work and how do you minimize GC pressure?",
    ],
    "llm": [
        "What is RAG (Retrieval Augmented Generation) and how does it reduce hallucinations?",
        "How do you fine-tune an LLM using LoRA or QLoRA?",
        "What is prompt engineering? Explain chain-of-thought and few-shot prompting.",
        "How do you evaluate the output quality of an LLM application?",
        "What is the difference between zero-shot, few-shot, and fine-tuning?",
    ],
    "generative ai": [
        "What is the difference between GANs, VAEs, and Diffusion models?",
        "How do you handle and reduce hallucinations in LLM responses?",
        "What is the role of temperature and top-k/top-p in LLM text generation?",
        "How would you build a production-grade RAG pipeline?",
        "What are the safety and ethical concerns in deploying generative AI?",
    ],
    "docker": [
        "What is the difference between a Docker image and container?",
        "How does Docker networking (bridge, host, overlay) work?",
        "Explain multi-stage builds and why they reduce image size.",
        "What is Docker Compose used for vs Kubernetes?",
        "How do you persist data in Docker containers (volumes vs tmpfs)?",
    ],
    "kubernetes": [
        "What is the difference between a Pod, Deployment, and Service?",
        "How does Kubernetes handle rolling updates and rollbacks?",
        "Explain Horizontal Pod Autoscaling and how it works.",
        "What is ConfigMap vs Secret in Kubernetes?",
        "How do liveness and readiness probes work?",
    ],
}


def get_interview_questions(skill: str) -> list:
    """Get interview questions for a skill."""
    key = skill.lower().strip()
    if key in INTERVIEW_QUESTIONS:
        return INTERVIEW_QUESTIONS[key]
    for q_key in INTERVIEW_QUESTIONS:
        if len(q_key) > 2 and (q_key in key or key in q_key):
            return INTERVIEW_QUESTIONS[q_key]
    return [
        f"Explain the core concepts of {skill} and how you've used it in a project.",
        f"Describe the most challenging problem you solved using {skill}.",
        f"What are the main advantages and limitations of {skill}?",
        f"How does {skill} compare to similar tools/technologies?",
        f"How do you stay updated with the latest developments in {skill}?",
    ]


# ── Letter Grade ───────────────────────────────────────────────────────────────
def get_letter_grade(weighted_score: float, ats_score: float, sem: float) -> dict:
    """Calculate an overall letter grade."""
    avg = (weighted_score * 0.5) + (ats_score * 0.3) + (sem * 0.2)
    if avg >= 85:
        return {"grade": "A+", "label": "Exceptional Match", "color": "#00F5FF",
                "bg": "rgba(0,245,255,0.12)",
                "advice": "Outstanding! You're a top-tier candidate for this role."}
    elif avg >= 75:
        return {"grade": "A",  "label": "Strong Match",      "color": "#34d399",
                "bg": "rgba(52,211,153,0.12)",
                "advice": "Great profile! Minor gaps can be closed in 1–2 weeks."}
    elif avg >= 65:
        return {"grade": "B+", "label": "Good Match",        "color": "#a78bfa",
                "bg": "rgba(167,139,250,0.12)",
                "advice": "Solid candidate. Filling 2–3 key skills will boost your chances significantly."}
    elif avg >= 55:
        return {"grade": "B",  "label": "Fair Match",        "color": "#fbbf24",
                "bg": "rgba(251,191,36,0.12)",
                "advice": "Decent foundation. Focus on the critical missing skills first."}
    elif avg >= 40:
        return {"grade": "C",  "label": "Partial Match",     "color": "#f97316",
                "bg": "rgba(249,115,22,0.12)",
                "advice": "Skill gaps present. Follow the weekly learning roadmap to improve."}
    else:
        return {"grade": "D",  "label": "Needs Work",        "color": "#f87171",
                "bg": "rgba(248,113,113,0.12)",
                "advice": "Significant gaps detected. Consider this role as a 3–6 month learning goal."}


# ── Competitive Score ──────────────────────────────────────────────────────────
def get_competitive_score(weighted_score: float) -> dict:
    """Estimate candidate competitive percentile."""
    if weighted_score >= 85:
        return {"percentile": 95, "label": "Top 5% of candidates 🏆", "color": "#00F5FF"}
    elif weighted_score >= 70:
        return {"percentile": 80, "label": "Top 20% of candidates 🥇", "color": "#34d399"}
    elif weighted_score >= 55:
        return {"percentile": 60, "label": "Top 40% of candidates 📈", "color": "#a78bfa"}
    elif weighted_score >= 40:
        return {"percentile": 40, "label": "Average candidate 📊",     "color": "#fbbf24"}
    else:
        return {"percentile": 15, "label": "Below average — follow the roadmap 📚", "color": "#f87171"}


# ── Cover Letter Generator ─────────────────────────────────────────────────────
def generate_cover_letter(
    candidate_name: str,
    job_role: str,
    matched_skills: list,
    missing_skills: list,
    company: str = "your company",
) -> str:
    """Generate a personalized cover letter template."""
    top_matched = [s["display"].title() for s in matched_skills[:5]]
    top_missing = [s["display"].title() for s in missing_skills[:2]]
    matched_str = ", ".join(top_matched) if top_matched else "a range of technical skills"
    learning_str = (
        f" I am also actively enhancing my proficiency in {' and '.join(top_missing)}, "
        "which I understand are key requirements for this role."
    ) if top_missing else ""

    return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_role} position at {company}. After carefully reviewing the role requirements, I am confident that my technical expertise and drive for continuous learning make me a strong candidate.

My core competencies include {matched_str}, which directly align with the technical requirements outlined in your job description.{learning_str}

Throughout my career, I have consistently delivered measurable results by applying these skills to solve real-world challenges. I thrive in fast-paced, collaborative environments and am energised by technical problems that demand both analytical depth and creative thinking.

I am particularly excited about this opportunity at {company} because it aligns with my professional goal of contributing to impactful, scalable solutions. I am confident I can deliver immediate value to your team while continuing to grow in this role.

I would welcome the chance to discuss how my background and skills can contribute to your team's success. Thank you for considering my application — I look forward to speaking with you.

Warm regards,
{candidate_name if candidate_name.strip() else '[Your Name]'}
"""


# ── Resume Bullet Analyzer ─────────────────────────────────────────────────────
WEAK_PHRASES = [
    ("responsible for",   "Replace 'responsible for' with a strong action verb: 'Led', 'Owned', 'Delivered'"),
    ("worked on",         "Replace 'worked on' with 'Engineered', 'Developed', 'Built', or 'Architected'"),
    ("helped with",       "Replace 'helped with' — show your direct contribution instead"),
    ("was involved in",   "Replace 'was involved in' with direct action verbs and ownership language"),
    ("tasked with",       "Replace 'tasked with' with 'Spearheaded', 'Executed', or 'Delivered'"),
    ("assisted",          "Replace 'assisted' with 'Collaborated on' or a direct-ownership verb"),
    ("good knowledge of", "Replace 'good knowledge of' with a concrete achievement or years of experience"),
    ("familiar with",     "Replace 'familiar with' — only list skills you can confidently demonstrate"),
    ("etc.",              "Avoid 'etc.' — be specific about every relevant item"),
    ("team player",       "Avoid generic phrases like 'team player' — show teamwork via achievements"),
    ("hard worker",       "Replace 'hard worker' — show it through accomplishments, not adjectives"),
]


def analyze_bullets(resume_text: str) -> list:
    """Scan resume text for weak phrases and suggest improvements."""
    suggestions = []
    text_lower = resume_text.lower()

    for phrase, fix in WEAK_PHRASES:
        if phrase in text_lower:
            suggestions.append({
                "type": "⚠️ Weak Phrase",
                "issue": f"Found: \"{phrase}\"",
                "fix": fix,
            })

    has_numbers = any(c.isdigit() for c in resume_text)
    if not has_numbers:
        suggestions.append({
            "type": "📊 Missing Metrics",
            "issue": "No quantified results found in your resume",
            "fix": "Add numbers wherever possible: '↑ API latency by 40%', 'Led team of 5', 'Processed 1M+ records/day'",
        })

    word_count = len(resume_text.split())
    if word_count < 200:
        suggestions.append({
            "type": "📝 Too Short",
            "issue": f"Resume is only ~{word_count} words — may lack detail",
            "fix": "A strong resume should be 400–800 words. Expand your project descriptions.",
        })
    elif word_count > 1200:
        suggestions.append({
            "type": "📝 Too Long",
            "issue": f"Resume is ~{word_count} words — may be too verbose",
            "fix": "Aim for 1–2 pages max. Remove older or irrelevant experience.",
        })

    if not suggestions:
        suggestions.append({
            "type": "✅ No Issues",
            "issue": "No major resume writing issues detected",
            "fix": "Keep bullet points concise, action-verb-led, and achievement-focused.",
        })

    return suggestions
