import pytest

from pipeline.providers import AllProvidersFailed, Router
from pipeline.queues import next_job


class Fake:
    def __init__(self, name, fail=False):
        self.name = name
        self.fail = fail

    def generate(self, prompt):
        if self.fail:
            raise RuntimeError("down")
        return f"{self.name}:{prompt}".encode()


class Q:
    def __init__(self, jobs):
        self.jobs = list(jobs)

    def receive(self):
        return self.jobs.pop(0) if self.jobs else None


def test_router_uses_first_provider():
    name, data = Router([Fake("bedrock"), Fake("openai")]).generate("p")
    assert name == "bedrock"
    assert data == b"bedrock:p"


def test_router_falls_back_when_first_fails():
    name, _ = Router([Fake("bedrock", fail=True), Fake("openai")]).generate("p")
    assert name == "openai"


def test_router_raises_when_all_fail():
    with pytest.raises(AllProvidersFailed):
        Router([Fake("a", fail=True), Fake("b", fail=True)]).generate("p")


def test_express_is_drained_before_bulk():
    queues = {"express": Q(["e1"]), "standard": Q([]), "bulk": Q(["b1"])}
    assert next_job(queues) == ("express", "e1")
    assert next_job(queues) == ("bulk", "b1")
    assert next_job(queues) is None
