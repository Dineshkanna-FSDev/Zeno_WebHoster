"""
AI Code Generator for website deployment.

Supports multiple LLM providers: OpenAI, Anthropic Claude, and local Ollama models.
"""

import os
import json
from django.conf import settings


SYSTEM_PROMPT = """You are an expert web developer. Generate a complete, modern website in response to the user's description. Return ONLY a JSON object with three keys: 'html', 'css', 'js'.

- html: Complete HTML5 structure (include <html>, <head>, <body> tags)
- css: All CSS styles (no <style> tags, just the CSS)
- js: All JavaScript code (no <script> tags, just the code)

Make it beautiful, responsive, and production-ready. Use modern design patterns.
Return ONLY valid JSON, no markdown, no explanation."""


class LLMProvider:
    """Base class for LLM providers."""
    
    def generate_code(self, prompt: str) -> dict:
        """
        Generate HTML/CSS/JS from a text description.
        
        Args:
            prompt: User description of the website
            
        Returns:
            {
                "html": "<html>...",
                "css": "body { ... }",
                "js": "...",
                "error": None or error message
            }
        """
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI GPT integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Set OPENAI_API_KEY in environment or provide llm_api_key in the request.")
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("pip install openai")
    
    def generate_code(self, prompt: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return {
                "html": result.get("html", ""),
                "css": result.get("css", ""),
                "js": result.get("js", ""),
                "error": None
            }
        except json.JSONDecodeError as e:
            return {"html": "", "css": "", "js": "", "error": f"Invalid JSON from LLM: {str(e)}"}
        except Exception as e:
            return {"html": "", "css": "", "js": "", "error": str(e)}


class AnthropicProvider(LLMProvider):
    """Anthropic Claude integration."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("pip install anthropic")
    
    def generate_code(self, prompt: str) -> dict:
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            result = json.loads(content)
            
            return {
                "html": result.get("html", ""),
                "css": result.get("css", ""),
                "js": result.get("js", ""),
                "error": None
            }
        except json.JSONDecodeError as e:
            return {"html": "", "css": "", "js": "", "error": f"Invalid JSON from LLM: {str(e)}"}
        except Exception as e:
            return {"html": "", "css": "", "js": "", "error": str(e)}


class OllamaProvider(LLMProvider):
    """Local Ollama model integration."""
    
    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        try:
            import ollama
            self.client = ollama
        except ImportError:
            raise ImportError("pip install ollama")
    
    def generate_code(self, prompt: str) -> dict:
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\nUser request: {prompt}"
            
            response = self.client.generate(
                model=self.model,
                prompt=full_prompt,
                stream=False
            )
            
            content = response.get("response", "")
            result = json.loads(content)
            
            return {
                "html": result.get("html", ""),
                "css": result.get("css", ""),
                "js": result.get("js", ""),
                "error": None
            }
        except json.JSONDecodeError as e:
            return {"html": "", "css": "", "js": "", "error": f"Invalid JSON from LLM: {str(e)}"}
        except Exception as e:
            return {"html": "", "css": "", "js": "", "error": str(e)}


def get_llm_provider(provider_name: str = None, api_key: str = None) -> LLMProvider:
    """Get LLM provider instance based on settings.

    Args:
        provider_name: Optional override for which provider to use (openai/anthropic/ollama)
        api_key: Optional API key to pass through to the provider (OpenAI/Anthropic)
    """
    provider = provider_name or getattr(settings, 'LLM_PROVIDER', 'openai')
    
    if provider == 'openai':
        return OpenAIProvider(api_key=api_key)
    elif provider == 'anthropic':
        return AnthropicProvider(api_key=api_key)
    elif provider == 'ollama':
        return OllamaProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")