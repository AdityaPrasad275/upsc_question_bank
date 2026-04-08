#!/usr/bin/env python3
"""
taking question_bank/<subject>/input/questions.md

like question_bank/economy_1/input/questions.md

and split the md based on "---"

theres a --- after first question, second...and so on till last
so n quesitons, n ---

splitting one large into smaller indivisual mds
"""

import os
import sys
from subject_paths import get_subject_dir

if len(sys.argv) != 2:
    print("Usage: python splitter.py <subject>")
    sys.exit(1)

subject = sys.argv[1]
subject_dir = get_subject_dir(subject)
input_file = subject_dir / "input" / "questions.md"

if not os.path.exists(input_file):
    print(f"File {input_file} not found")
    sys.exit(1)

with open(input_file, "r") as f:
    content = f.read()

sections = content.split("---")

output_dir = subject_dir / "questions"
os.makedirs(output_dir, exist_ok=True)

for i, section in enumerate(sections, 1):
    section = section.strip()
    if section:  # skip empty sections
        output_file = output_dir / f"question_{i}.md"
        with open(output_file, "w") as f:
            f.write(section)

print(f"Split into {len([s for s in sections if s.strip()])} questions")
