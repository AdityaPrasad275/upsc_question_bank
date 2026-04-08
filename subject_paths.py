from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
QUESTION_BANK_DIR = REPO_ROOT / "question_bank"


def get_subject_dir(subject: str) -> Path:
    return QUESTION_BANK_DIR / subject


def iter_subject_dirs():
    if not QUESTION_BANK_DIR.exists():
        return []

    return sorted(
        path
        for path in QUESTION_BANK_DIR.iterdir()
        if path.is_dir() and (path / "json").exists()
    )
