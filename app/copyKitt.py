from multiprocessing.sharedctypes import Value
import os
import openai
import argparse
import re
from typing import List

MAX_INPUT_LENGTH = 32


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User Input: {user_input}")

    if validate_length(user_input):
        generateBrandingSnippet(user_input)
        generateKeywords(user_input)
    else:
        raise ValueError(
            f"Input length is too long. Must be under {MAX_INPUT_LENGTH} characters. Input: '{user_input}' is {len(user_input)} characters long")


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generateBrandingSnippet(prompt: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate upbeat branding snippet for {prompt}: "

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)
    print(enriched_prompt)
    branding_text: str = response["choices"][0]["text"]
    branding_text = branding_text.strip()

    last_char = branding_text[-1]

    branding_text = checkIfLastCharIsFullstop(last_char, branding_text)

    print(f"Snippet: {branding_text}")
    return branding_text


def generateKeywords(prompt: str) -> List[str]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    enriched_prompt = f"Generate related branding keyword for {prompt}: "

    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3", prompt=enriched_prompt, max_tokens=32)
    print(enriched_prompt)
    keywords_text: str = response["choices"][0]["text"]
    keywords_text = keywords_text.strip()

    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array]
    keywords_array = [k for k in keywords_array if len(k) > 0]

    print(f"Keywords: {keywords_array}")
    return keywords_array


def checkIfLastCharIsFullstop(last_char: str, branding_text: str):
    if last_char not in {".", "!", "?"}:
        branding_text += "..."

    return branding_text


if __name__ == "__main__":
    main()
