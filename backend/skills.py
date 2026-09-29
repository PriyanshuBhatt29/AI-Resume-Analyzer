import re
from collections import OrderedDict


SKILL_ALIASES = OrderedDict({
    "Python": [r"\bpython\b"],
    "C++": [r"\bc\+\+\b", r"cpp"],
    "Java": [r"\bjava\b"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b"],
    "TypeScript": [r"\btypescript\b"],
    "SQL": [r"\bsql\b"],
    "HTML": [r"\bhtml5?\b"],
    "CSS": [r"\bcss3?\b"],
    "React": [r"\breact(?:\.js)?\b"],
    "Node.js": [r"\bnode(?:\.js)?\b", r"\bnodejs\b"],
    "FastAPI": [r"\bfastapi\b"],
    "Flask": [r"\bflask\b"],
    "Django": [r"\bdjango\b"],
    "Docker": [r"\bdocker\b"],
    "Kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "AWS": [r"\baws\b", r"amazon web services"],
    "Azure": [r"\bazure\b"],
    "GCP": [r"\bgcp\b", r"google cloud"],
    "Git": [r"\bgit\b"],
    "GitHub": [r"\bgithub\b"],
    "Linux": [r"\blinux\b"],
    "TensorFlow": [r"\btensorflow\b"],
    "PyTorch": [r"\bpytorch\b"],
    "Keras": [r"\bkeras\b"],
    "Scikit-learn": [r"\bscikit[- ]learn\b", r"\bsklearn\b"],
    "Pandas": [r"\bpandas\b"],
    "NumPy": [r"\bnumpy\b"],
    "OpenCV": [r"\bopencv\b", r"open cv"],
    "NLP": [r"\bnatural language processing\b", r"\bnlp\b"],
    "Computer Vision": [r"\bcomputer vision\b"],
    "Machine Learning": [r"\bmachine learning\b"],
    "Deep Learning": [r"\bdeep learning\b"],
    "Transformers": [r"\btransformers?\b"],
    "LLM": [r"\bllms?\b", r"large language models?"],
    "Hugging Face": [r"hugging ?face"],
    "REST API": [r"\brest(?:ful)?\s+(?:api|apis)\b"],
    "MongoDB": [r"\bmongodb\b"],
    "MySQL": [r"\bmysql\b"],
    "PostgreSQL": [r"\bpostgres(?:ql)?\b"],
])


def extract_skills(text: str) -> list[str]:
    found = []
    lowered = text.lower()
    for skill, patterns in SKILL_ALIASES.items():
        if any(re.search(pattern, lowered, re.IGNORECASE) for pattern in patterns):
            found.append(skill)
    return found
