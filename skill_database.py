"""
Skill Database — Extended & Weighted
Comprehensive skill registry with importance weights (1-10) and recommendations.
"""

# ── Skill DB: { category: [(skill_name, weight)] } ──────────────────────────
SKILLS_DB = {
    "Programming Languages": [
        ("python", 10), ("java", 9), ("javascript", 9), ("typescript", 8),
        ("c++", 8), ("c#", 8), ("c", 7), ("r", 8), ("golang", 7), ("go", 7),
        ("rust", 7), ("swift", 7), ("kotlin", 7), ("scala", 7), ("ruby", 6),
        ("php", 6), ("matlab", 6), ("bash", 6), ("shell scripting", 5),
        ("perl", 5), ("dart", 6), ("lua", 5), ("haskell", 5), ("vba", 4),
        ("assembly", 4), ("cobol", 3), ("fortran", 3), ("julia", 6),
    ],
    "Web Development": [
        ("react", 9), ("angular", 8), ("vue", 8), ("nextjs", 8), ("nodejs", 9),
        ("express", 7), ("django", 8), ("flask", 8), ("fastapi", 8),
        ("spring boot", 8), ("spring", 7), ("html", 7), ("css", 7),
        ("html5", 7), ("css3", 7), ("rest api", 9), ("graphql", 8),
        ("bootstrap", 6), ("tailwind css", 7), ("sass", 6), ("webpack", 6),
        ("vite", 6), ("redux", 7), ("svelte", 7), ("nuxtjs", 7),
        ("jquery", 5), ("asp.net", 7), ("laravel", 7), ("rails", 6),
        ("websocket", 7), ("oauth", 7), ("jwt", 7), ("microservices", 9),
    ],
    "Data Science & ML": [
        ("machine learning", 10), ("deep learning", 10), ("neural networks", 9),
        ("natural language processing", 9), ("nlp", 9), ("computer vision", 9),
        ("reinforcement learning", 8), ("scikit-learn", 9), ("tensorflow", 9),
        ("pytorch", 9), ("keras", 8), ("xgboost", 8), ("lightgbm", 8),
        ("pandas", 9), ("numpy", 9), ("scipy", 8), ("matplotlib", 7),
        ("seaborn", 7), ("plotly", 7), ("data analysis", 9),
        ("feature engineering", 9), ("model evaluation", 8),
        ("hyperparameter tuning", 8), ("cross validation", 8),
        ("regression", 8), ("classification", 8), ("clustering", 8),
        ("time series", 8), ("anomaly detection", 7), ("bert", 9), ("gpt", 9),
        ("transformers", 9), ("hugging face", 8), ("langchain", 8),
        ("llm", 9), ("generative ai", 9), ("rag", 8), ("opencv", 8),
        ("yolo", 8), ("object detection", 8), ("statistics", 8),
        ("probability", 7), ("linear algebra", 7), ("calculus", 6),
        ("a/b testing", 7), ("data visualization", 8), ("tableau", 7),
        ("power bi", 7),
    ],
    "Databases": [
        ("sql", 10), ("mysql", 8), ("postgresql", 8), ("mongodb", 8),
        ("redis", 8), ("elasticsearch", 8), ("cassandra", 7), ("dynamodb", 7),
        ("sqlite", 6), ("oracle", 7), ("sql server", 7), ("firestore", 7),
        ("neo4j", 6), ("influxdb", 6), ("database design", 8),
        ("query optimization", 7), ("stored procedures", 6), ("orm", 7),
        ("sqlalchemy", 7), ("nosql", 8), ("vector database", 8),
        ("pinecone", 7), ("chroma", 6),
    ],
    "Cloud & DevOps": [
        ("aws", 10), ("azure", 9), ("gcp", 9), ("google cloud", 9),
        ("docker", 10), ("kubernetes", 9), ("ci/cd", 9), ("devops", 9),
        ("terraform", 8), ("ansible", 7), ("jenkins", 8), ("helm", 7),
        ("prometheus", 7), ("grafana", 7), ("linux", 8), ("nginx", 7),
        ("apache", 6), ("serverless", 8), ("lambda", 7), ("ec2", 7),
        ("s3", 7), ("github actions", 8), ("gitlab ci", 8), ("circleci", 7),
        ("azure devops", 8), ("load balancing", 7), ("cdn", 6),
        ("cloudwatch", 6), ("iam", 6),
    ],
    "Data Engineering": [
        ("apache spark", 9), ("kafka", 9), ("airflow", 9), ("dbt", 8),
        ("etl", 9), ("data pipeline", 9), ("data warehouse", 8),
        ("data lake", 8), ("bigquery", 8), ("redshift", 8), ("snowflake", 8),
        ("databricks", 8), ("hadoop", 7), ("hive", 7), ("flink", 7),
        ("data modeling", 8), ("data architecture", 8), ("nifi", 6),
    ],
    "Tools & Platforms": [
        ("git", 9), ("github", 9), ("gitlab", 8), ("docker compose", 8),
        ("jira", 6), ("confluence", 5), ("postman", 7), ("swagger", 7),
        ("jupyter", 8), ("vs code", 6), ("linux", 8), ("excel", 6),
        ("google analytics", 6), ("figma", 5), ("bitbucket", 6), ("npm", 6),
        ("yarn", 5), ("poetry", 5), ("conda", 6), ("pip", 5),
    ],
    "Cybersecurity": [
        ("cybersecurity", 9), ("network security", 8), ("ethical hacking", 8),
        ("penetration testing", 8), ("vulnerability assessment", 8),
        ("cryptography", 7), ("ssl", 7), ("tls", 7), ("firewall", 7),
        ("siem", 7), ("threat intelligence", 7), ("zero trust", 7),
        ("soc", 7), ("owasp", 7), ("burp suite", 7),
    ],
    "Mobile Development": [
        ("android", 8), ("ios", 8), ("react native", 8), ("flutter", 8),
        ("swift", 7), ("kotlin", 7), ("xamarin", 6), ("ionic", 6),
        ("jetpack compose", 7), ("swiftui", 7), ("pwa", 6),
    ],
    "Soft Skills": [
        ("communication", 8), ("leadership", 8), ("teamwork", 8),
        ("problem solving", 9), ("critical thinking", 8), ("agile", 8),
        ("scrum", 7), ("project management", 8), ("mentoring", 7),
        ("time management", 7), ("collaboration", 8), ("adaptability", 7),
    ],
}

# ── Flat skill list with weights ─────────────────────────────────────────────
ALL_SKILLS_WEIGHTED = {}  # { normalized_skill: (display_name, weight, category) }
for category, skill_list in SKILLS_DB.items():
    for skill_name, weight in skill_list:
        key = skill_name.lower().strip()
        ALL_SKILLS_WEIGHTED[key] = (skill_name, weight, category)

# ── Aliases ──────────────────────────────────────────────────────────────────
SKILL_ALIASES = {
    "ml":               "machine learning",
    "dl":               "deep learning",
    "ai":               "artificial intelligence",
    "cv":               "computer vision",
    "nlp":              "natural language processing",
    "js":               "javascript",
    "ts":               "typescript",
    "py":               "python",
    "k8s":              "kubernetes",
    "tf":               "tensorflow",
    "pt":               "pytorch",
    "rl":               "reinforcement learning",
    "gcp":              "google cloud",
    "gen ai":           "generative ai",
    "genai":            "generative ai",
    "node":             "nodejs",
    "node.js":          "nodejs",
    "next.js":          "nextjs",
    "vue.js":           "vue",
    "postgres":         "postgresql",
    "psql":             "postgresql",
    "sklearn":          "scikit-learn",
    "hf":               "hugging face",
    "gh actions":       "github actions",
    "ci cd":            "ci/cd",
    "rest":             "rest api",
    "restful":          "rest api",
    "restful api":      "rest api",
    "spring":           "spring boot",
    "fast api":         "fastapi",
    "power bi":         "power bi",
    "ms sql":           "sql server",
    "mssql":            "sql server",
    "spark":            "apache spark",
    "rdbms":            "sql",
    "llms":             "llm",
    "large language models": "llm",
}

# ── Recommendations ───────────────────────────────────────────────────────────
SKILL_RECOMMENDATIONS = {
    # ── Programming Languages ──────────────────────────────────────────────────
    "python": {
        "courses": ["Python for Everybody – U of Michigan (Coursera, free)", "Automate the Boring Stuff with Python (book, free online)"],
        "projects": ["Web Scraper with BeautifulSoup", "CLI Task Manager", "Data Analysis Dashboard"],
        "duration": "1–2 weeks",
        "resources": ["python.org/docs", "Real Python (realpython.com)", "W3Schools Python"],
        "difficulty": "Beginner",
    },
    "r": {
        "courses": ["R Programming – Johns Hopkins (Coursera)", "R for Data Science – Hadley Wickham (free online book)"],
        "projects": ["EDA with ggplot2 on a Kaggle dataset", "Linear Regression Analysis", "Shiny Dashboard App"],
        "duration": "2–3 weeks",
        "resources": ["r-project.org", "RStudio Education (education.rstudio.com)", "CRAN Task Views"],
        "difficulty": "Beginner",
    },
    "java": {
        "courses": ["Java Programming Masterclass – Udemy (Tim Buchalka)", "Java for Complete Beginners – freeCodeCamp (YouTube)"],
        "projects": ["CRUD REST API with Spring Boot", "Bank Account System (OOP)", "Multithreaded File Downloader"],
        "duration": "3–4 weeks",
        "resources": ["docs.oracle.com/java", "Baeldung.com", "Effective Java (book)"],
        "difficulty": "Intermediate",
    },
    "javascript": {
        "courses": ["JavaScript Algorithms & Data Structures – freeCodeCamp (free)", "The Modern JavaScript Tutorial (javascript.info)"],
        "projects": ["Vanilla JS Quiz App", "Weather App using Fetch API", "To-Do List with LocalStorage"],
        "duration": "2–3 weeks",
        "resources": ["MDN Web Docs", "javascript.info", "You Don't Know JS (free book)"],
        "difficulty": "Beginner",
    },
    "typescript": {
        "courses": ["Understanding TypeScript – Udemy (Maximilian Schwarzmüller)", "TypeScript Handbook – Official (free)"],
        "projects": ["REST API with TypeScript + Express", "Type-safe React App", "CLI Tool in TypeScript"],
        "duration": "1–2 weeks",
        "resources": ["typescriptlang.org/docs", "Total TypeScript (totaltypescript.com)", "Type Challenges on GitHub"],
        "difficulty": "Intermediate",
    },
    "c++": {
        "courses": ["C++ Tutorial for Complete Beginners – freeCodeCamp (YouTube)", "Learn C++ – learncpp.com (free)"],
        "projects": ["Student Management System", "Linked List Implementation", "Simple Game with SFML"],
        "duration": "3–5 weeks",
        "resources": ["cppreference.com", "learncpp.com", "C++ Primer (book)"],
        "difficulty": "Intermediate",
    },
    "c": {
        "courses": ["C Programming for Beginners – Udemy", "CS50 (Harvard, free) — starts with C"],
        "projects": ["Command-line Calculator", "Memory Allocator", "Simple Shell Implementation"],
        "duration": "2–3 weeks",
        "resources": ["cppreference.com (C section)", "CS50 course materials", "The C Programming Language (K&R book)"],
        "difficulty": "Intermediate",
    },
    "c#": {
        "courses": ["C# Fundamentals – Pluralsight", "foundational C# with Microsoft – freeCodeCamp (free certification)"],
        "projects": ["ASP.NET Core REST API", "Console Bank App", "Unity 2D Game"],
        "duration": "2–3 weeks",
        "resources": ["learn.microsoft.com/dotnet/csharp", "C# Corner (c-sharpcorner.com)"],
        "difficulty": "Intermediate",
    },
    "golang": {
        "courses": ["Go: The Complete Developer's Guide – Udemy (Stephen Grider)", "Tour of Go – official (go.dev/tour, free)"],
        "projects": ["REST API with Gin framework", "CLI File Organizer", "Concurrent Web Crawler"],
        "duration": "2–3 weeks",
        "resources": ["go.dev/doc", "Go by Example (gobyexample.com)", "Effective Go (free)"],
        "difficulty": "Intermediate",
    },
    "go": {
        "courses": ["Go: The Complete Developer's Guide – Udemy (Stephen Grider)", "Tour of Go – official (go.dev/tour, free)"],
        "projects": ["REST API with Gin framework", "CLI File Organizer", "Concurrent Web Crawler"],
        "duration": "2–3 weeks",
        "resources": ["go.dev/doc", "Go by Example (gobyexample.com)", "Effective Go (free)"],
        "difficulty": "Intermediate",
    },
    "rust": {
        "courses": ["The Rust Programming Language (book, free — doc.rust-lang.org)", "Rust for Beginners – freeCodeCamp (YouTube)"],
        "projects": ["CLI Tool (e.g., file finder)", "HTTP Server from scratch", "WebAssembly module with Rust"],
        "duration": "4–6 weeks",
        "resources": ["doc.rust-lang.org/book", "Rustlings exercises (GitHub)", "Rust by Example (free)"],
        "difficulty": "Advanced",
    },
    "scala": {
        "courses": ["Functional Programming in Scala – EPFL (Coursera)", "Scala & Spark for Big Data – Udemy (Jose Portilla)"],
        "projects": ["Spark Data Processing Pipeline", "REST API with Akka HTTP", "Functional Data Transformer"],
        "duration": "3–5 weeks",
        "resources": ["scala-lang.org/docs", "Scala Exercises (scala-exercises.org)", "Alvin Alexander Scala book (free)"],
        "difficulty": "Advanced",
    },
    "ruby": {
        "courses": ["The Odin Project – Ruby Path (free)", "Learn Ruby on Rails – Michael Hartl (free book)"],
        "projects": ["Blog App with Rails", "REST API with Sinatra", "CLI Budget Tracker"],
        "duration": "2–3 weeks",
        "resources": ["ruby-lang.org/docs", "The Odin Project (theodinproject.com)", "RubyGems.org"],
        "difficulty": "Beginner",
    },
    "kotlin": {
        "courses": ["Kotlin for Java Developers – JetBrains (Coursera, free)", "Android Development with Kotlin – Udacity (free)"],
        "projects": ["Android To-Do App with Jetpack Compose", "REST Client with Ktor", "Command-line Exercise Tracker"],
        "duration": "2–3 weeks",
        "resources": ["kotlinlang.org/docs", "Android Developer Guides", "Kotlin Koans (kotlinlang.org/koans)"],
        "difficulty": "Intermediate",
    },
    "swift": {
        "courses": ["100 Days of SwiftUI – Paul Hudson (free)", "iOS App Development with Swift – University of Toronto (Coursera)"],
        "projects": ["To-Do App with SwiftUI", "Weather App (iOS)", "Simple Photo Gallery App"],
        "duration": "3–4 weeks",
        "resources": ["developer.apple.com/swift", "Hacking with Swift (hackingwithswift.com)", "Swift Playgrounds"],
        "difficulty": "Intermediate",
    },
    "julia": {
        "courses": ["Introduction to Julia – MIT OpenCourseWare (free)", "Julia Scientific Programming – Coursera"],
        "projects": ["Numerical Methods Solver", "Data Visualization with Plots.jl", "ML Model from scratch"],
        "duration": "2–3 weeks",
        "resources": ["docs.julialang.org", "JuliaAcademy (juliaacademy.com)", "Julia Observer"],
        "difficulty": "Intermediate",
    },
    "matlab": {
        "courses": ["MATLAB Programming for Engineers – MathWorks (free)", "Signal Processing with MATLAB – Coursera"],
        "projects": ["Image Processing Pipeline", "Numerical ODE Solver", "Control System Simulation"],
        "duration": "2–3 weeks",
        "resources": ["mathworks.com/help/matlab", "MATLAB Central (File Exchange)", "MATLAB Onramp (free)"],
        "difficulty": "Intermediate",
    },
    # ── Web & Frameworks ───────────────────────────────────────────────────────
    "react": {
        "courses": ["The Complete React Developer – Zero to Mastery", "Full Stack Open – University of Helsinki (free)"],
        "projects": ["Todo App with Redux", "E-Commerce Frontend with Cart", "Portfolio Website"],
        "duration": "2–3 weeks",
        "resources": ["react.dev (official docs)", "Scrimba React (free)", "egghead.io React"],
        "difficulty": "Intermediate",
    },
    "nodejs": {
        "courses": ["The Complete Node.js Developer Course – Udemy (Andrew Mead)", "Node.js Tutorial – The Odin Project (free)"],
        "projects": ["REST API with Express.js & MongoDB", "Real-time Chat App with Socket.io", "CLI File System Tool"],
        "duration": "2–3 weeks",
        "resources": ["nodejs.org/docs", "nodeschool.io (free)", "Express.js docs"],
        "difficulty": "Intermediate",
    },
    "django": {
        "courses": ["Django for Beginners – William S. Vincent (book, free chapters)", "Tweetme Django – freeCodeCamp (YouTube)"],
        "projects": ["Blog with User Auth", "E-Commerce Store", "REST API with Django REST Framework"],
        "duration": "2–3 weeks",
        "resources": ["docs.djangoproject.com", "Django REST Framework docs", "William Vincent's blog"],
        "difficulty": "Intermediate",
    },
    "flask": {
        "courses": ["Flask Mega-Tutorial – Miguel Grinberg (free)", "REST APIs with Flask – Udemy (Jose Salvatierra)"],
        "projects": ["URL Shortener API", "Authentication System with JWT", "Portfolio API"],
        "duration": "1–2 weeks",
        "resources": ["flask.palletsprojects.com", "Miguel Grinberg's blog", "TestDriven.io Flask"],
        "difficulty": "Beginner",
    },
    "fastapi": {
        "courses": ["FastAPI Full Course – freeCodeCamp (YouTube)", "Building APIs with FastAPI – TestDriven.io"],
        "projects": ["CRUD API with SQLAlchemy", "ML Model Serving API", "Authentication API with OAuth2"],
        "duration": "1–2 weeks",
        "resources": ["fastapi.tiangolo.com (official docs)", "TestDriven.io FastAPI", "FastAPI GitHub examples"],
        "difficulty": "Intermediate",
    },
    "spring boot": {
        "courses": ["Spring Boot 3 – Amigoscode (YouTube, free)", "Building Microservices with Spring Boot – Udemy"],
        "projects": ["CRUD REST API with JPA", "Microservices with Eureka & Gateway", "Spring Security OAuth2 App"],
        "duration": "3–4 weeks",
        "resources": ["spring.io/guides", "Baeldung.com/Spring", "Start.spring.io"],
        "difficulty": "Intermediate",
    },
    # ── Data & ML ──────────────────────────────────────────────────────────────
    "machine learning": {
        "courses": ["Machine Learning Specialization – Andrew Ng (Coursera)", "Machine Learning A-Z – Udemy (Hadelin de Ponteves)"],
        "projects": ["House Price Predictor (Regression)", "Customer Churn Classifier", "Movie Recommendation System"],
        "duration": "3–5 weeks",
        "resources": ["Kaggle Learn (kaggle.com/learn)", "scikit-learn docs", "fast.ai"],
        "difficulty": "Intermediate",
    },
    "deep learning": {
        "courses": ["Deep Learning Specialization – deeplearning.ai (Coursera)", "Practical Deep Learning – fast.ai (free)"],
        "projects": ["MNIST Digit Recognizer (CNN)", "Image Classifier", "Text Generation with RNN"],
        "duration": "4–6 weeks",
        "resources": ["d2l.ai (free book)", "PyTorch Tutorials", "TensorFlow Hub"],
        "difficulty": "Advanced",
    },
    "natural language processing": {
        "courses": ["NLP Specialization – deeplearning.ai (Coursera)", "Hugging Face NLP Course (free)"],
        "projects": ["Sentiment Analyzer", "Named Entity Recognizer", "Question-Answering Bot"],
        "duration": "3–4 weeks",
        "resources": ["huggingface.co/learn", "spaCy 101 (spacy.io)", "NLTK Book (free, nltk.org)"],
        "difficulty": "Advanced",
    },
    "nlp": {
        "courses": ["NLP Specialization – deeplearning.ai (Coursera)", "Hugging Face NLP Course (free)"],
        "projects": ["Sentiment Analyzer", "Named Entity Recognizer", "Question-Answering Bot"],
        "duration": "3–4 weeks",
        "resources": ["huggingface.co/learn", "spaCy 101 (spacy.io)", "NLTK Book (free)"],
        "difficulty": "Advanced",
    },
    "tensorflow": {
        "courses": ["TensorFlow Developer Certificate – deeplearning.ai (Coursera)", "TensorFlow 2.x Official Tutorial (free)"],
        "projects": ["Image Classifier (CNN)", "Text Sentiment Model", "Time Series Forecaster"],
        "duration": "2–4 weeks",
        "resources": ["tensorflow.org/tutorials", "TF Playground (playground.tensorflow.org)"],
        "difficulty": "Intermediate",
    },
    "pytorch": {
        "courses": ["PyTorch for Deep Learning – freeCodeCamp (YouTube, free)", "Practical Deep Learning – fast.ai (free)"],
        "projects": ["CIFAR-10 CNN Classifier", "Fine-tune BERT for Sentiment", "GAN for image generation"],
        "duration": "2–4 weeks",
        "resources": ["pytorch.org/tutorials", "Papers with Code (paperswithcode.com)"],
        "difficulty": "Intermediate",
    },
    "pandas": {
        "courses": ["Data Analysis with Python – IBM (Coursera, free audit)", "Pandas Documentation Tutorials (free)"],
        "projects": ["EDA on any Kaggle Dataset", "COVID-19 Data Analysis", "Financial Stock Analyzer"],
        "duration": "1 week",
        "resources": ["pandas.pydata.org/docs", "Kaggle Learn: Pandas (free)", "Real Python Pandas tutorials"],
        "difficulty": "Beginner",
    },
    "data analysis": {
        "courses": ["Google Data Analytics Certificate (Coursera)", "Data Analysis with Python – IBM (Coursera, free audit)"],
        "projects": ["EDA Report on Kaggle dataset", "Retail Sales Dashboard", "Sports Stats Analysis"],
        "duration": "2–3 weeks",
        "resources": ["Kaggle (kaggle.com)", "DataCamp (free tier)", "The Pudding (pudding.cool) for inspiration"],
        "difficulty": "Beginner",
    },
    "data visualization": {
        "courses": ["Data Visualization with Python – IBM (Coursera)", "Fundamentals of Data Visualization – Claus Wilke (free book)"],
        "projects": ["Interactive Dashboard with Plotly/Dash", "Matplotlib Data Story", "D3.js Chart"],
        "duration": "1–2 weeks",
        "resources": ["plotly.com/examples", "matplotlib.org/gallery", "fundamentalsofdatavisualization.com (free)"],
        "difficulty": "Beginner",
    },
    "tableau": {
        "courses": ["Tableau Desktop Specialist – Tableau eLearning (free trial)", "Data Visualization with Tableau – UC Davis (Coursera)"],
        "projects": ["COVID-19 Dashboard", "E-commerce Performance Dashboard", "HR Analytics Report"],
        "duration": "1–2 weeks",
        "resources": ["public.tableau.com", "Tableau Community Forums", "Tableau Help docs"],
        "difficulty": "Beginner",
    },
    "power bi": {
        "courses": ["Microsoft Power BI – Microsoft Learn (free)", "Power BI A-Z – Udemy (Kirill Eremenko)"],
        "projects": ["Sales KPI Dashboard", "HR Analytics Report", "Social Media Analytics Dashboard"],
        "duration": "1–2 weeks",
        "resources": ["learn.microsoft.com/power-bi", "SQLBI.com", "Guy in a Cube (YouTube)"],
        "difficulty": "Beginner",
    },
    "statistics": {
        "courses": ["Statistics with Python – University of Michigan (Coursera)", "Khan Academy Statistics & Probability (free)"],
        "projects": ["Hypothesis Testing on a real dataset", "A/B Test Simulation", "Regression Analysis Report"],
        "duration": "2–3 weeks",
        "resources": ["Khan Academy (khanacademy.org)", "StatQuest with Josh Starmer (YouTube)", "OpenIntro Statistics (free book)"],
        "difficulty": "Beginner",
    },
    "generative ai": {
        "courses": ["Generative AI with LLMs – AWS + deeplearning.ai (Coursera)", "LangChain for LLM Apps – deeplearning.ai (free short course)"],
        "projects": ["RAG-based PDF Q&A Bot", "AI Writing Assistant", "Code Review Bot with GPT API"],
        "duration": "3–5 weeks",
        "resources": ["platform.openai.com/docs", "huggingface.co", "LangChain docs (langchain.com)"],
        "difficulty": "Advanced",
    },
    "llm": {
        "courses": ["Generative AI with LLMs – deeplearning.ai", "Building LLM Apps – LangChain Academy (free)"],
        "projects": ["Document Q&A with RAG", "Fine-tune a small LLM (LoRA)", "Chatbot with conversation memory"],
        "duration": "3–5 weeks",
        "resources": ["huggingface.co/learn", "langchain.com/docs", "Andrej Karpathy's makemore (YouTube)"],
        "difficulty": "Advanced",
    },
    # ── Databases ──────────────────────────────────────────────────────────────
    "sql": {
        "courses": ["SQL for Data Science – UC Davis (Coursera, free audit)", "Mode SQL Tutorial (mode.com/sql-tutorial, free)"],
        "projects": ["Sales Analytics with Complex Queries", "User Retention Funnel Analysis", "Library Management System DB"],
        "duration": "1–2 weeks",
        "resources": ["SQLZoo (sqlzoo.net)", "LeetCode SQL problems", "W3Schools SQL"],
        "difficulty": "Beginner",
    },
    "mongodb": {
        "courses": ["MongoDB Atlas – MongoDB University (free)", "Node.js & MongoDB: Full Stack – freeCodeCamp (YouTube)"],
        "projects": ["Blog REST API (Node + Express + MongoDB)", "Product Catalog with Aggregation", "Real-time Analytics Store"],
        "duration": "1–2 weeks",
        "resources": ["mongodb.com/docs", "MongoDB University (university.mongodb.com)", "Mongoose.js docs"],
        "difficulty": "Beginner",
    },
    "postgresql": {
        "courses": ["PostgreSQL Tutorial – postgresqltutorial.com (free)", "PostgreSQL for Beginners – Udemy"],
        "projects": ["E-Commerce Database Design", "Full-Text Search System", "Time-Series Data Store"],
        "duration": "1–2 weeks",
        "resources": ["postgresql.org/docs", "pgExercises.com (free)", "Use-the-index-luke.com"],
        "difficulty": "Intermediate",
    },
    # ── Cloud & DevOps ─────────────────────────────────────────────────────────
    "aws": {
        "courses": ["AWS Cloud Practitioner Essentials – AWS Skill Builder (free)", "AWS Certified Solutions Architect – A Cloud Guru"],
        "projects": ["Deploy a Flask App on EC2", "Serverless Image Resizer (Lambda + S3)", "Static Site on S3 + CloudFront"],
        "duration": "3–4 weeks",
        "resources": ["AWS Free Tier", "AWS Skill Builder (skillbuilder.aws, free)", "CloudGuru"],
        "difficulty": "Intermediate",
    },
    "docker": {
        "courses": ["Docker & Kubernetes: The Complete Guide – Udemy (Bret Fisher)", "KodeKloud Docker Labs (free)"],
        "projects": ["Containerize your Python/Flask App", "Multi-service App with Docker Compose", "CI/CD Pipeline with Docker"],
        "duration": "1–2 weeks",
        "resources": ["docs.docker.com", "Play with Docker (labs.play-with-docker.com, free)", "Docker Hub"],
        "difficulty": "Intermediate",
    },
    "kubernetes": {
        "courses": ["Kubernetes for Beginners – KodeKloud (free tier)", "CKAD Exam Prep – Linux Foundation"],
        "projects": ["Deploy Microservice on local K8s (minikube)", "Rolling Update & HPA Demo", "Helm Chart Deployment"],
        "duration": "2–3 weeks",
        "resources": ["kubernetes.io/docs", "Killercoda K8s Sandbox (killercoda.com, free)", "K9s terminal UI"],
        "difficulty": "Advanced",
    },
    "ci/cd": {
        "courses": ["DevOps with GitHub Actions – GitHub Learning Lab (free)", "GitLab CI/CD for Beginners – KodeKloud"],
        "projects": ["Auto-deploy a Python App with GitHub Actions", "Build & push Docker image on PR", "Automated Test Pipeline"],
        "duration": "1–2 weeks",
        "resources": ["docs.github.com/actions", "GitLab CI/CD docs", "CircleCI getting-started guide"],
        "difficulty": "Intermediate",
    },
    "git": {
        "courses": ["Version Control with Git – Atlassian/Coursera (free)", "Git & GitHub Crash Course – Traversy Media (YouTube, free)"],
        "projects": ["Contribute to an open-source project on GitHub", "Create a GitHub portfolio with README", "Git branching strategy demo"],
        "duration": "3–5 days",
        "resources": ["git-scm.com/docs", "learngitbranching.js.org (interactive, free)", "Oh Shit Git! (ohshitgit.com)"],
        "difficulty": "Beginner",
    },
    "linux": {
        "courses": ["Linux Command Line Basics – Udacity (free)", "The Linux Command Line – William Shotts (free online book)"],
        "projects": ["Automate backups with Bash scripts", "Set up a LAMP stack on Ubuntu VM", "Write a system monitoring script"],
        "duration": "1–2 weeks",
        "resources": ["linuxcommand.org (free)", "OverTheWire Wargames (free, learn by hacking)", "ss64.com command reference"],
        "difficulty": "Beginner",
    },
    # ── Data Engineering ───────────────────────────────────────────────────────
    "apache spark": {
        "courses": ["Apache Spark with Python (PySpark) – Udemy (Frank Kane)", "Spark by Example – Databricks Academy (free)"],
        "projects": ["Log Analytics Pipeline with PySpark", "Batch ETL Job on Parquet files", "Spark Streaming from Kafka"],
        "duration": "2–4 weeks",
        "resources": ["spark.apache.org/docs", "Databricks Community Edition (free)", "Spark: The Definitive Guide (book)"],
        "difficulty": "Advanced",
    },
    "kafka": {
        "courses": ["Apache Kafka Series – Stéphane Maarek (Udemy)", "Kafka 101 – Confluent Developer (free)"],
        "projects": ["Real-time Order Processing Pipeline", "Log Aggregation System", "Event-Driven Microservice Demo"],
        "duration": "2–3 weeks",
        "resources": ["kafka.apache.org/docs", "developer.confluent.io (free labs)", "Kafka: The Definitive Guide (free PDF)"],
        "difficulty": "Advanced",
    },
    "airflow": {
        "courses": ["The Complete Hands-on Apache Airflow – Marc Lamberti (Udemy)", "Astronomer Learn Airflow (free)"],
        "projects": ["Scheduled Data Pipeline with Airflow DAGs", "ETL Workflow with PythonOperator", "Daily Report Generator"],
        "duration": "2–3 weeks",
        "resources": ["airflow.apache.org/docs", "astronomer.io/learn (free)", "Airflow GitHub examples"],
        "difficulty": "Intermediate",
    },
    "etl": {
        "courses": ["Data Engineering with Python – DataCamp", "ETL & Data Pipelines with Shell, Airflow & Kafka – IBM (Coursera)"],
        "projects": ["Extract-Transform-Load CSV to PostgreSQL", "Incremental Data Sync Pipeline", "Data Quality Validation Framework"],
        "duration": "2–3 weeks",
        "resources": ["AWS Glue documentation", "dbt docs (getdbt.com)", "Great Expectations docs"],
        "difficulty": "Intermediate",
    },
    # ── Security / Tools ───────────────────────────────────────────────────────
    "cybersecurity": {
        "courses": ["Google Cybersecurity Certificate (Coursera, free audit)", "CompTIA Security+ – Professor Messer (YouTube, free)"],
        "projects": ["Vulnerability Scanner (Nmap + Python)", "Password Manager CLI", "CTF challenges on HackTheBox"],
        "duration": "4–6 weeks",
        "resources": ["TryHackMe (tryhackme.com, free tier)", "HackTheBox (hackthebox.com)", "OWASP Top 10 guide"],
        "difficulty": "Intermediate",
    },
    # ── Mobile ─────────────────────────────────────────────────────────────────
    "flutter": {
        "courses": ["The Complete Flutter Development Bootcamp – Dr. Angela Yu (Udemy)", "Flutter & Dart – Official docs codelabs (free)"],
        "projects": ["Cross-Platform To-Do App", "Weather App (Android + iOS)", "E-Commerce Mobile App"],
        "duration": "3–4 weeks",
        "resources": ["flutter.dev/docs", "pub.dev (package repository)", "Flutter by Google (YouTube playlist)"],
        "difficulty": "Intermediate",
    },
    "react native": {
        "courses": ["React Native – The Practical Guide – Udemy (Maximilian Schwarzmüller)", "Expo React Native Docs (free)"],
        "projects": ["Cross-Platform To-Do App", "Fitness Tracker with SQLite", "Photo Gallery App with Camera API"],
        "duration": "3–4 weeks",
        "resources": ["reactnative.dev/docs", "expo.dev/docs", "Snack by Expo (free online editor)"],
        "difficulty": "Intermediate",
    },
}


def get_recommendation(skill: str) -> dict:
    """Get recommendation for a skill — exact match first, then safe partial match, then fallback."""
    key = skill.lower().strip()
    # Resolve alias
    key = SKILL_ALIASES.get(key, key)
    # 1. Exact match
    if key in SKILL_RECOMMENDATIONS:
        return SKILL_RECOMMENDATIONS[key]
    # 2. Safe partial — only match if rec_key is a multi-word substring of key
    #    (prevents single-char mismatches like "r" matching "reinforcement learning")
    if len(key) > 2:
        for rec_key, rec in SKILL_RECOMMENDATIONS.items():
            if len(rec_key) > 2 and rec_key in key:
                return rec
    # 3. Generic but informative fallback
    return {
        "courses": [
            f"Search \"{skill}\" on Coursera, Udemy, or YouTube",
            f"freeCodeCamp has free tutorials — search \"{skill}\" on freeCodeCamp.org",
        ],
        "projects": [
            f"Build a small demo project using {skill}",
            f"Find a beginner {skill} project on GitHub and replicate it",
        ],
        "duration": "1–3 weeks",
        "resources": [
            f"Official {skill} documentation / website",
            "dev.to — search for beginner articles",
            "Reddit r/learnprogramming for community advice",
        ],
        "difficulty": "Varies",
    }


def get_skill_weight(skill: str) -> int:
    """Return importance weight of a skill (1–10)."""
    key = skill.lower().strip()
    if key in ALL_SKILLS_WEIGHTED:
        return ALL_SKILLS_WEIGHTED[key][1]
    return 5  # default



