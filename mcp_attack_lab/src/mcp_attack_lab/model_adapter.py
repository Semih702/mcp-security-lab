from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import torch
from openai import OpenAI
from transformers import AutoModelForCausalLM, AutoTokenizer


def _build_prompt_from_messages(tokenizer: Any, messages: list[dict[str, str]]) -> str:
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

    rendered_parts: list[str] = []
    for message in messages:
        role = message["role"].upper()
        rendered_parts.append(f"{role}:\n{message['content']}")
    rendered_parts.append("ASSISTANT:\n")
    return "\n\n".join(rendered_parts)


@lru_cache(maxsize=4)
def _load_huggingface_model(model_name: str) -> tuple[Any, Any]:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model


def _generate_huggingface_text(model_profile: dict[str, Any], messages: list[dict[str, str]]) -> str:
    model_name = model_profile["model"]
    defaults = model_profile.get("defaults", {})
    max_new_tokens = int(defaults.get("max_tokens", 256))
    temperature = float(defaults.get("temperature", 0.1))
    top_p = float(defaults.get("top_p", 0.9))

    tokenizer, model = _load_huggingface_model(model_name)
    prompt = _build_prompt_from_messages(tokenizer, messages)
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        generated = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=max(temperature, 1e-5),
            top_p=top_p,
            pad_token_id=tokenizer.eos_token_id,
        )

    prompt_length = inputs["input_ids"].shape[1]
    output_tokens = generated[0][prompt_length:]
    return tokenizer.decode(output_tokens, skip_special_tokens=True).strip()


def _generate_dashscope_text(model_profile: dict[str, Any], messages: list[dict[str, str]]) -> str:
    api_key_env = model_profile.get("api_key_env", "DASHSCOPE_API_KEY")
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise ValueError(
            f"Environment variable {api_key_env} is not set. "
            "Set your DashScope API key before running a hosted Qwen model."
        )

    base_url = model_profile["base_url"]
    model_name = model_profile["model"]
    defaults = model_profile.get("defaults", {})

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=float(defaults.get("temperature", 0.1)),
        top_p=float(defaults.get("top_p", 0.9)),
        max_tokens=int(defaults.get("max_tokens", 256)),
    )

    content = response.choices[0].message.content
    if content is None:
        return ""
    return content.strip()


def _generate_openai_text(model_profile: dict[str, Any], messages: list[dict[str, str]]) -> str:
    api_key_env = model_profile.get("api_key_env", "OPENAI_API_KEY")
    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise ValueError(
            f"Environment variable {api_key_env} is not set. "
            "Set your OpenAI API key before running an OpenAI-hosted model."
        )

    model_name = model_profile["model"]
    defaults = model_profile.get("defaults", {})

    client = OpenAI(api_key=api_key)
    input_items = [
        {
            "role": message["role"],
            "content": [
                {
                    "type": "input_text",
                    "text": message["content"],
                }
            ],
        }
        for message in messages
    ]

    request_kwargs: dict[str, Any] = {
        "model": model_name,
        "input": input_items,
        "max_output_tokens": int(defaults.get("max_tokens", 256)),
    }

    if model_name.startswith("gpt-5") or model_name.startswith("o"):
        request_kwargs["reasoning"] = {"effort": "minimal"}
        request_kwargs["text"] = {"verbosity": "low"}

    response = client.responses.create(**request_kwargs)

    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()

    # Fallback: extract visible text content if the helper is empty.
    output = getattr(response, "output", None) or []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if text:
                return text.strip()

    return ""


def generate_text(model_profile: dict[str, Any], messages: list[dict[str, str]]) -> str:
    provider = model_profile.get("provider")
    if provider == "huggingface":
        return _generate_huggingface_text(model_profile, messages)
    if provider == "dashscope":
        return _generate_dashscope_text(model_profile, messages)
    if provider == "openai":
        return _generate_openai_text(model_profile, messages)

    raise ValueError(
        "Unsupported provider for experiment execution: "
        f"{provider}. Supported providers are: huggingface, dashscope, openai."
    )
