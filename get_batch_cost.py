#!/usr/bin/env python3
"""
Fetch batch results and calculate total cost.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

def main():
    load_dotenv()

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    batch_id = "msgbatch_01EbMrNLj2LvxHYqutHoz747"

    # Model: claude-haiku-4-5-20251001
    INPUT_PRICE_PER_MTOK = 0.50  # Batch pricing
    OUTPUT_PRICE_PER_MTOK = 2.00

    total_input_tokens = 0
    total_output_tokens = 0
    count = 0

    print(f"Fetching results for batch {batch_id}...")

    try:
        for result in client.beta.messages.batches.results(batch_id):
            if result.result.type == "succeeded":
                usage = result.result.message.usage
                total_input_tokens += usage.input_tokens
                total_output_tokens += usage.output_tokens
                count += 1
    except Exception as e:
        print(f"Error: {e}")
        return

    input_cost = (total_input_tokens / 1_000_000) * INPUT_PRICE_PER_MTOK
    output_cost = (total_output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MTOK
    total_cost = input_cost + output_cost

    print("Batch Processing Cost Analysis")
    print("=" * 40)
    print(f"Model: claude-haiku-4-5-20251001 (Batch pricing - 50% discount)")
    print(f"Requests processed: {count}")
    print(f"Total input tokens: {total_input_tokens:,}")
    print(f"Total output tokens: {total_output_tokens:,}")
    print(f"Total tokens: {total_input_tokens + total_output_tokens:,}")
    print(f"Input cost: ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost: ${total_cost:.6f}")

if __name__ == "__main__":
    main()