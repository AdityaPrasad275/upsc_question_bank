#!/usr/bin/env python3
"""
Calculate the total cost of the batch processing based on token usage in JSON files.
"""

import json
import os
import glob

def main():
    # Model: claude-haiku-4-5-20251001
    # Batch pricing: 50% of standard
    # Standard: $0.80/MTok input, $4/MTok output
    # Batch: $0.40/MTok input, $2/MTok output

    INPUT_PRICE_PER_MTOK = 0.40  # $ per million tokens
    OUTPUT_PRICE_PER_MTOK = 2.00

    json_dir = "economy_1/json"
    json_files = glob.glob(os.path.join(json_dir, "question_*.json"))

    total_input_tokens = 0
    total_output_tokens = 0
    processed_files = 0

    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                usage = data.get('usage', {})
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
                
                total_input_tokens += input_tokens
                total_output_tokens += output_tokens
                processed_files += 1
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

    # Calculate costs
    input_cost = (total_input_tokens / 1_000_000) * INPUT_PRICE_PER_MTOK
    output_cost = (total_output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MTOK
    total_cost = input_cost + output_cost

    print("Batch Processing Cost Analysis")
    print("=" * 40)
    print(f"Model: claude-haiku-4-5-20251001 (Batch pricing - 50% discount)")
    print(f"Files processed: {processed_files}")
    print(f"Total input tokens: {total_input_tokens:,}")
    print(f"Total output tokens: {total_output_tokens:,}")
    print(f"Total tokens: {total_input_tokens + total_output_tokens:,}")
    print(".6f")
    print(".6f")
    print(".6f")
    print("\nPricing details:")
    print(".2f")
    print(".2f")

if __name__ == "__main__":
    main()