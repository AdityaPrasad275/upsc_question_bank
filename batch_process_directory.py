#!/usr/bin/env python3
"""
Processes a whole directory of questions using the Anthropic Message Batches API
for maximum cost-efficiency.

Usage:
python3 batch_process_directory.py <subject>

Example:
python3 batch_process_directory.py economy_1

This script will:
1. Find all question_*.md files in the <subject>/questions directory.
2. Check which questions have already been processed (i.e., a corresponding .json file exists).
3. Create a batch request for all unprocessed questions.
4. Use Prompt Caching within the batch to further reduce costs.
5. Submit the batch, poll for completion, and retrieve the results.
6. Save each result to its corresponding question_*.json file.
"""

import os
import sys
import json
import glob
import time
from anthropic import Anthropic
from dotenv import load_dotenv

def main(subject):
    load_dotenv()

    # Set up client
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    model_name = os.getenv("ANTHROPIC_MODEL", "claude-3.5-sonnet-20240620")

    # --- 1. Read System Prompt ---
    try:
        with open("prompts/question-builder.md", "r") as f:
            system_prompt = f.read()
    except FileNotFoundError:
        print("Error: prompts/question-builder.md not found.")
        sys.exit(1)
        
    # The JSON schema for the output
    output_schema = {
        "type": "object",
        "properties": {
            "subject": {"type": "string"},
            "year": {"type": ["integer", "null"]},
            "theme": {"type": "string"},
            "question_short_text": {"type": "string"},
            "text": {"type": "string"},
            "options": {
                "type": "array",
                "items": {"type": "string"}
            },
            "answerIndex": {"type": "integer"},
            "answerText": {"type": "string"},
            "explanation": {"type": "string"},
            "research": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "facts": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                                "whyUsed": {"type": "string"}
                            },
                            "required": ["title", "url", "whyUsed"],
                            "additionalProperties": False
                        }
                    },
                    "searchMeta": {
                        "type": "object",
                        "properties": {
                            "usedWebSearch": {"type": "boolean"},
                            "searchQueries": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "confidence": {"type": "string"}
                        },
                        "required": ["usedWebSearch", "searchQueries", "confidence"],
                        "additionalProperties": False
                    }
                },
                "required": ["summary", "facts", "sources", "searchMeta"],
                "additionalProperties": False
            }
        },
        "required": ["subject", "year", "theme", "question_short_text", "text", "options", "answerIndex", "answerText", "explanation", "research"],
        "additionalProperties": False
    }


    # --- 2. Find Unprocessed Questions ---
    questions_dir = os.path.join(subject, "questions")
    json_dir = os.path.join(subject, "json")
    os.makedirs(json_dir, exist_ok=True)

    question_files = glob.glob(os.path.join(questions_dir, "question_*.md"))
    
    requests_to_process = []
    if not question_files:
        print(f"No question markdown files found in {questions_dir}")
        return

    for q_file in question_files:
        question_number = os.path.basename(q_file).replace("question_", "").replace(".md", "")
        json_file = os.path.join(json_dir, f"question_{question_number}.json")

        if not os.path.exists(json_file):
            with open(q_file, "r") as f:
                question_content = f.read()

            custom_id = f"question_{question_number}"

            request = {
                "custom_id": custom_id,
                "params": {
                    "model": model_name,
                    "max_tokens": 8000,
                    # This is the key part for caching the system prompt!
                    "system": [
                        {
                            "type": "text",
                            "text": system_prompt,
                            "cache_control": {"type": "ephemeral"}
                        }
                    ],
                    "messages": [{"role": "user", "content": question_content}],
                    "tools": [{"type": "web_search_20250305", "name": "web_search"}],
                    "output_config": {
                        "format": {
                            "type": "json_schema",
                            "schema": output_schema
                        }
                    }
                }
            }
            requests_to_process.append(request)

    if not requests_to_process:
        print("All questions have already been processed.")
        return

    print(f"Found {len(requests_to_process)} questions to process.")

    # --- 3. Create and Submit Batch ---
    try:
        batch = anthropic_client.beta.messages.batches.create(
            requests=requests_to_process
        )
        print(f"Batch {batch.id} created. Status: {batch.processing_status}")
    except Exception as e:
        print(f"Error creating batch: {e}")
        sys.exit(1)

    # --- 4. Poll for Completion ---
    while True:
        try:
            retrieved_batch = anthropic_client.beta.messages.batches.retrieve(batch.id)
            print(f"Polling batch {retrieved_batch.id}... Status: {retrieved_batch.processing_status}")
            print(f"Request counts: {retrieved_batch.request_counts}")
        except Exception as e:
            print(f"Error retrieving batch status: {e}")
            time.sleep(60)
            continue

        if retrieved_batch.processing_status == "ended":
            print("Batch processing complete.")
            break
        elif retrieved_batch.processing_status in ["failed", "cancelled"]:
            print(f"Batch failed or was cancelled. Status: {retrieved_batch.processing_status}")
            sys.exit(1)
        
        time.sleep(60)  # Wait 60 seconds before polling again

    # --- 5. Retrieve and Save Results ---
    print("Retrieving results...")
    saved_count = 0
    error_count = 0
    
    try:
        for result in anthropic_client.beta.messages.batches.results(batch.id):
            question_number = result.custom_id.replace("question_", "")
            output_file = os.path.join(json_dir, f"question_{question_number}.json")

            if result.result.type == "succeeded":
                # Extract text from all content blocks (handles cases where tools are used)
                response_text = ""
                for block in result.result.message.content:
                    if hasattr(block, 'text'):
                        response_text += block.text
                try:
                    # Parse JSON, add the ID, and save
                    result_json = json.loads(response_text)
                    result_json["id"] = int(question_number)
                    with open(output_file, "w") as f:
                        json.dump(result_json, f, indent=2)
                    saved_count += 1
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for {result.custom_id}: {e}")
                    print(f"Raw response: {response_text}")
                    # Save raw response as MD file
                    md_file = output_file.replace('.json', '.md')
                    with open(md_file, "w") as f:
                        f.write(response_text)
                    print(f"Saved raw response to {md_file}")
                    error_count += 1
                except Exception as e:
                    print(f"An unexpected error occurred while saving {result.custom_id}: {e}")
                    error_count += 1
            else:
                print(f"Request {result.custom_id} failed: {result.result.error}")
                error_count += 1
        
        print(f"Processing finished.")
        print(f"Successfully saved {saved_count} new JSON files.")
        if error_count > 0:
            print(f"Encountered {error_count} errors.")

    except Exception as e:
        print(f"An error occurred while retrieving results: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 batch_process_directory.py <subject>")
        sys.exit(1)

    subject_arg = sys.argv[1]
    main(subject_arg)
