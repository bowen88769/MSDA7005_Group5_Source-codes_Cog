import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class APIConfig:
    model: str
    api_url: str
    api_key: str
    temperature: float
    max_tokens: int
    pre_input: str

class APIClient:
    def __init__(self):
        self.config: Optional[APIConfig] = None
        self.load_config()

    def load_config(self) -> bool:
        """Load API configuration from settings file"""
        settings_file = Path("settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    if not settings.get('api_url') or not settings.get('api_keys'):
                        return False
                    
                    self.config = APIConfig(
                        model=settings.get('model', 'gpt-3.5-turbo-1106'),
                        api_url=settings.get('api_url', ''),
                        api_key=settings.get('api_keys', [''])[0],
                        temperature=float(settings.get('temperature', 0.7)),
                        max_tokens=int(settings.get('max_tokens', 4096)),
                        pre_input=settings.get('pre_input', '')
                    )
                    return True
            except Exception as e:
                print(f"Error loading API config: {e}")
        return False

    def format_message(self, user_input: str) -> Dict[str, Any]:
        """Format the message using GPT format for all models"""
        if not self.config:
            raise ValueError("API configuration not loaded")

        # Add pre-input if configured
        full_input = f"{self.config.pre_input}\n{user_input}" if self.config.pre_input else user_input

        return {
            "model": self.config.model,
            "messages": [{"role": "user", "content": full_input}],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

    def send_request(self, user_input: str) -> str:
        """Send a request to the configured API endpoint"""
        if not self.config or not self.load_config():
            raise ValueError("API configuration not loaded or invalid")

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }

        try:
            payload = self.format_message(user_input)
            response = requests.post(
                self.config.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            # Parse response
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.RequestException as e:
            return f"Error: Failed to get response from API - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"

    def send_batch_requests(self, prompt: str, count: int, interval: float, 
                          progress_callback=None) -> list[str]:
        """Send multiple requests with the same prompt"""
        responses = []
        for i in range(count):
            response = self.send_request(prompt)
            responses.append(response)
            
            if progress_callback:
                progress_callback(i + 1, count)
                
        return responses
