# backend/core/utils.py
import openai
import re
import json
from django.conf import settings

client = openai.OpenAI(api_key="place-your-api-key-here")

filter_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "response",
        "schema": {
            "type": "object",
            "required": ["product_type", "color", "size", "gender", "brands"],
            "properties": {
                "product_type": {
                    "type": ["string", "null"],
                    "description": "Type of clothing product",
                },
                "color": {
                    "type": ["string", "null"],
                    "description": "Color of the product with the first letter in Capital",
                },
                "size": {
                    "type": ["string", "null"],
                    "description": "Size of the product in Capital letters",
                },
                "gender": {
                    "type": ["string", "null"],
                    "enum":["Men","Women","Boys","Girls"],
                    "description": "Target gender for the product",
                },
                "brands": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "string"
                    },
                    "description": "List of clothing brands",
                }
            },
            "additionalProperties": False,
        },
    },
}


def ensure_json(response_content):
    if isinstance(response_content, str):  # If it's a string, try to parse it
        try:
            return json.loads(response_content)  # Convert to JSON (dict)
        except json.JSONDecodeError:
            return response_content  # Return original string if not valid JSON
    return response_content  # If already a dict, return as is



def parse_query_with_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                        Extract clothing details from the user query. 
                        Convert any mentioned sizes (e.g., small, medium, large, extra large, extra extra large) 
                        to their uppercase abbreviations: S, M, L, XL, XXL. Return the response in the specified schema.
                        """,
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            response_format=filter_schema,
        )

        response_content = response.choices[0].message.content
        parsed_response =ensure_json(response_content)
        return parsed_response
    except Exception as e:
        return {"error": str(e)}
