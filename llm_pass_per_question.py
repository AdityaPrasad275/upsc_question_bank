#!/usr/bin/env python3
"""
from <subject>/questions/<question number.md>

like economy_1/questions/question_39.md

we take this, give it to claude,enable web search, with system prompt as prompts/question-builder.md and get a output of json

save it in <subject>/json/<questions number.json>
"""

import os
import sys
import json
from anthropic import Anthropic
from dotenv import load_dotenv

def main(subject, question_number):
    load_dotenv()  # Load environment variables from .env file

    # Read question file
    question_file = os.path.join(subject, "questions", f"question_{question_number}.md")
    if not os.path.exists(question_file):
        print(f"Question file {question_file} not found")
        sys.exit(1)

    with open(question_file, "r") as f:
        question_content = f.read()

    # Read system prompt
    system_prompt_file = "prompts/question-builder.md"
    if not os.path.exists(system_prompt_file):
        print(f"System prompt file {system_prompt_file} not found")
        sys.exit(1)

    with open(system_prompt_file, "r") as f:
        system_prompt = f.read()

    # Set up client
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Define tools
    tools = [
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
    ]

    # Call Claude with structured JSON output schema
    model_name = os.getenv("ANTHROPIC_MODEL", "claude-3.5-sonnet")
    response = anthropic_client.messages.create(
        model=model_name,
        max_tokens=8000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": question_content
            }
        ],
        tools=tools,
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
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
            }
        }
    )

    # Get the final response
    final_content = ""
    for content in response.content:
        if content.type == "text":
            final_content += content.text

    # Parse JSON
    try:
        result_json = json.loads(final_content.strip())
        # Add id
        result_json["id"] = question_number
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Response:", final_content)
        sys.exit(1)

    # Create output directory
    output_dir = os.path.join(subject, "json")
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    output_file = os.path.join(output_dir, f"question_{question_number}.json")
    with open(output_file, "w") as f:
        json.dump(result_json, f, indent=2)

    print(f"Saved JSON to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 llm_pass_per_question.py <subject> <question_number>")
        sys.exit(1)

    subject_arg = sys.argv[1]
    question_number_arg = int(sys.argv[2])
    main(subject_arg, question_number_arg)

