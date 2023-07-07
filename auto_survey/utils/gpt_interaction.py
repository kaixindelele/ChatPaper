import os
import time

import openai
import logging
import requests
import json

log = logging.getLogger(__name__)

def get_gpt_responses(systems, prompts, model="gpt-4", temperature=0.4):
    conversation_history = [
        {"role": "system", "content": systems},
        {"role": "user", "content": prompts}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation_history,
        n=1,  # Number of responses you want to generate
        temperature=temperature,  # Controls the creativity of the generated response
    )
    assistant_message = response['choices'][0]["message"]["content"]
    usage = response['usage']
    log.info(assistant_message)
    return assistant_message, usage


class GPTModel_API2D_SUPPORT:
    def __init__(self, model="gpt-4", temperature=0, presence_penalty=0,
                 frequency_penalty=0, url=None, key=None, max_attempts=1, delay=20):
        if url is None:
            url = "https://api.openai.com/v1/chat/completions"
        if key is None:
            key = os.getenv("OPENAI_API_KEY")

        self.model = model
        self.temperature = temperature
        self.url = url
        self.key = key
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_attempts = max_attempts
        self.delay = delay

    def __call__(self, systems, prompts, return_json=False):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}",
            'Content-type': 'text/plain; charset=utf-8'
        }

        data = {
                "model": f"{self.model}",
                "messages": [
                {"role": "system", "content": systems},
                {"role": "user", "content": prompts}],
                "temperature": self.temperature,
                "n": 1,
                "stream": False,
                "presence_penalty": self.presence_penalty,
                "frequency_penalty": self.frequency_penalty
                }
        for _ in range(self.max_attempts):
            try:
                # todo: in some cases, UnicodeEncodeError is raised:
                #   'gbk' codec can't encode character '\xdf' in position 1898: illegal multibyte sequence
                response = requests.post(self.url, headers=headers, data=json.dumps(data))
                response = response.json()
                assistant_message = response['choices'][0]["message"]["content"]
                usage = response['usage']
                log.info(assistant_message)
                if return_json:
                    assistant_message = json.loads(assistant_message)
                return assistant_message, usage
            except Exception as e:
                print(f"Failed to get response. Error: {e}")
                time.sleep(self.delay)
        raise RuntimeError("Failed to get response from OpenAI.")


class GPTModel:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.9, presence_penalty=0,
                 frequency_penalty=0, max_attempts=1, delay=20):
        self.model = model
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_attempts = max_attempts
        self.delay = delay

    def __call__(self, systems, prompts, return_json=False):
        conversation_history = [
            {"role": "system", "content": systems},
            {"role": "user", "content": prompts}
        ]
        for _ in range(self.max_attempts):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=conversation_history,
                    n=1,
                    temperature=self.temperature,
                    presence_penalty=self.presence_penalty,
                    frequency_penalty=self.frequency_penalty,
                    stream=False
                )
                assistant_message = response['choices'][0]["message"]["content"]
                usage = response['usage']
                log.info(assistant_message)
                if return_json:
                    assistant_message = json.loads(assistant_message)
                return assistant_message, usage
            except openai.error.APIConnectionError as e:
                print(f"Failed to get response. Error: {e}")
                time.sleep(self.delay)
        raise RuntimeError("Failed to get response from OpenAI.")



if __name__ == "__main__":
    bot = GPTModel(model="gpt-3.5-turbo-16k")
    r = bot("You are an assistant.", "Hello.")
    print(r)