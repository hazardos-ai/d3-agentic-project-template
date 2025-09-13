"""
A2A Protocol handler for {{ AgentName }}.

This is a template file. Replace Jinja variables (e.g., {{ AgentName }})
or render via your scaffolder to generate a concrete handler.
"""

from agents.a2a_utils import normalize_payload

from a2a_protocol import InMemoryA2AHandler, A2AMessage, MessageStatus
from .schema import TaskInput, TaskOutput


class {{ AgentSlug | capitalize }}A2AHandler(InMemoryA2AHandler):
    """A2A handler for the {{ AgentName }}."""

    def __init__(self):
        # The channel name should be unique for this agent
        super().__init__("{{ agent_channel | default(AgentSlug) }}")

    async def handle_message(self, message: A2AMessage) -> A2AMessage:
        """Handle incoming messages for {{ AgentName }}."""
        try:
            # Normalize payload into TaskInput (supports dicts and pydantic models via normalize_payload)
            input_data = normalize_payload(message.payload, TaskInput)

            # Lazy import the agent to avoid circular imports during bootstrap
            from .agent import {{ AgentClassName }}

            agent = {{ AgentClassName }}()
            # The primary method can be renamed via the {{ agent_method }} variable
            result: TaskOutput = await getattr(agent, "{{ agent_method | default('run') }}")(input_data)

            # Create successful response
            return self.create_response(message, result, MessageStatus.COMPLETED)

        except Exception as e:
            # Fallback error payload using TaskOutput schema
            error_output = TaskOutput(
                text="An error occurred while processing the task.",
                sections=[],
                status="error",
                metrics={"error": str(e)},
                attachments=[],
            )
            response = self.create_response(message, error_output, MessageStatus.FAILED)
            # Put structured error info in response metadata (not payload) for audit trails
            response.metadata = {
                "error": str(e),
                "agent": "{{ AgentName }}",
                "handler": "{{ AgentSlug | capitalize }}A2AHandler",
            }
            return response
