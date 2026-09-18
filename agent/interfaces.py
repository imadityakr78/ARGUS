"""
Agent Module Interfaces

Clean interfaces for Member 3 to implement.
These define the LLM client, tool, and orchestration contracts.

Owner: Member 3
"""
from typing import Protocol, List, Optional
from argus_contracts import InvestigationRequest, InvestigationResponse


class LLMClient(Protocol):
    """Abstract LLM interface. Implementations: FakeLLMClient, BedrockLLMClient."""

    def invoke(self, prompt: str, tools: Optional[List[dict]] = None) -> str:
        """Send a prompt, optionally with tool definitions, and get a response string."""
        ...


class FakeLLMClient:
    """Returns canned responses for testing without AWS credentials."""

    def invoke(self, prompt: str, tools: Optional[List[dict]] = None) -> str:
        return "This is a mock LLM response. TODO(member3): implement Bedrock client."


class InvestigatorInterface(Protocol):
    """Drives the investigation loop: question → tool calls → hypotheses → response."""

    def investigate(self, request: InvestigationRequest) -> InvestigationResponse: ...


class VerifierInterface(Protocol):
    """Post-processes LLM output to enforce PACE constraints and strip hallucinations."""

    def verify(self, response: InvestigationResponse) -> InvestigationResponse: ...
