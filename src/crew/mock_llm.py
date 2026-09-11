try:
    from crewai.llms.base_llm import BaseLLM
except Exception:
    BaseLLM = object

class MockCrewLLM(BaseLLM):
    def __init__(self, model="mock-llm"):
        try:
            super().__init__(model=model)
        except TypeError:
            try: super().__init__(model)
            except Exception: pass
        self.call_count=0

    def call(self, messages, **kwargs):
        self.call_count += 1
        return "MOCK_LLM: use the available tool result and return only grounded information."
