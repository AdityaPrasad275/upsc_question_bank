import os
import json
import shutil

def generate_data():
    base_dir = "."
    output_base_dir = "frontend/public/data"
    
    if os.path.exists(output_base_dir):
        shutil.rmtree(output_base_dir)
    os.makedirs(output_base_dir, exist_ok=True)
    
    subjects = []
    
    # Iterate through directories in the root
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "json")):
            subject_id = item
            subject_json_dir = os.path.join(item_path, "json")
            
            # List all json files in the subject's json directory
            json_files = [f for f in os.listdir(subject_json_dir) if f.endswith(".json")]
            # Sort them numerically if possible
            json_files.sort(key=lambda x: int(x.split('_')[1].split('.')[0]) if '_' in x else x)
            
            questions_manifest = []
            # Use exact folder name as subject name
            subject_name = subject_id
            
            # Create directory for subject in public/data
            os.makedirs(os.path.join(output_base_dir, subject_id), exist_ok=True)
            
            for json_file in json_files:
                file_path = os.path.join(subject_json_dir, json_file)
                with open(file_path, 'r') as f:
                    try:
                        data = json.load(f)
                        
                        questions_manifest.append({
                            "id": data.get("id", json_file.split('_')[1].split('.')[0]),
                            "short_text": data.get("question_short_text", "Question " + str(data.get("id"))),
                            "file": json_file
                        })
                        
                        # Copy the json file to the public/data/<subject_id>/ directory
                        shutil.copy(file_path, os.path.join(output_base_dir, subject_id, json_file))
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
            
            subjects.append({
                "id": subject_id,
                "name": subject_name,
                "count": len(questions_manifest)
            })
            
            # Save subject manifest
            manifest_data = {
                "name": subject_name,
                "questions": questions_manifest
            }
            with open(os.path.join(output_base_dir, subject_id, "manifest.json"), 'w') as f:
                json.dump(manifest_data, f, indent=2)
                
    # Save global subjects manifest
    with open(os.path.join(output_base_dir, "subjects.json"), 'w') as f:
        json.dump(subjects, f, indent=2)
    
    print(f"Data generation complete. Found {len(subjects)} subjects.")

if __name__ == "__main__":
    generate_data()
