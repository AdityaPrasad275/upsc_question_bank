#!/usr/bin/env python3
"""
Script to retrieve and save results from a completed Anthropic Message Batch.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

def main():
    load_dotenv()

    # Set up client
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Batch ID from the completed batch
    batch_id = "msgbatch_01UcVnq3CsjDSQVPYCaZ1XFx"

    # Directory to save JSON files
    json_dir = "economy_1/json"
    os.makedirs(json_dir, exist_ok=True)

    saved_count = 0
    error_count = 0

    print(f"Retrieving results for batch {batch_id}...")

    try:
        for result in anthropic_client.beta.messages.batches.results(batch_id):
            question_number = result.custom_id.replace("question_", "")
            output_file = os.path.join(json_dir, f"question_{question_number}.json")

            if result.result.type == "succeeded":
                # Extract text from all content blocks
                response_text = ""
                for block in result.result.message.content:
                    try:
                        response_text += block.text
                    except AttributeError:
                        # Skip blocks that don't have text (e.g., tool use blocks)
                        pass

                try:
                    # Parse JSON, add the ID and usage, and save
                    result_json = json.loads(response_text)
                    result_json["id"] = int(question_number)
                    result_json["usage"] = result.result.message.usage.model_dump() if hasattr(result.result.message.usage, 'model_dump') else result.result.message.usage
                    with open(output_file, "w") as f:
                        json.dump(result_json, f, indent=2)
                    saved_count += 1
                    print(f"Saved {output_file}")
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON for {result.custom_id}: {e}")
                    print(f"Raw response: {response_text}")
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

if __name__ == "__main__":
    main()