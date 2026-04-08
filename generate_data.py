import os
import json
import shutil
from subject_paths import iter_subject_dirs


def generate_data():
    output_base_dir = "frontend/public/data"

    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)
    os.makedirs(output_base_dir, exist_ok=True)

    subjects = []

    # Iterate through subject directories inside question_bank/
    for subject_dir in iter_subject_dirs():
        subject_id = subject_dir.name
        subject_json_dir = subject_dir / "json"

        json_files = [f for f in os.listdir(subject_json_dir) if f.endswith(".json")]
        json_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]) if '_' in x else x)

        questions_manifest = []
        subject_name = subject_id

        os.makedirs(os.path.join(output_base_dir, subject_id), exist_ok=True)

        for json_file in json_files:
            file_path = subject_json_dir / json_file
            with open(file_path, "r") as f:
                try:
                    data = json.load(f)

                    questions_manifest.append({
                        "id": data.get("id", json_file.split('_')[1].split('.')[0]),
                        "short_text": data.get("question_short_text", "Question " + str(data.get("id"))),
                        "file": json_file
                    })

                    shutil.copy(file_path, os.path.join(output_base_dir, subject_id, json_file))
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

        subjects.append({
            "id": subject_id,
            "name": subject_name,
            "count": len(questions_manifest)
        })

        manifest_data = {
            "name": subject_name,
            "questions": questions_manifest
        }
        with open(os.path.join(output_base_dir, subject_id, "manifest.json"), "w") as f:
            json.dump(manifest_data, f, indent=2)

    # Save global subjects manifest
    with open(os.path.join(output_base_dir, "subjects.json"), "w") as f:
        json.dump(subjects, f, indent=2)

    print(f"Data generation complete. Found {len(subjects)} subjects.")


if __name__ == "__main__":
    generate_data()
