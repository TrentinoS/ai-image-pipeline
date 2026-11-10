from typing import Protocol


class ImageProvider(Protocol):
    name: str

    def generate(self, prompt: str) -> bytes: ...


class AllProvidersFailed(Exception):
    pass


class Router:
    def __init__(self, providers: list):
        self.providers = providers

    def generate(self, prompt: str):
        errors = []
        for provider in self.providers:
            try:
                return provider.name, provider.generate(prompt)
            except Exception as exc:
                errors.append(f"{provider.name}: {exc}")
        raise AllProvidersFailed("; ".join(errors))
