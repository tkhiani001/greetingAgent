"""Integration test for greeting agent end-to-end flow."""

from unittest.mock import AsyncMock, MagicMock, patch
import pytest


@pytest.mark.asyncio
async def test_agent_end_to_end_greeting():
    """End-to-end test: agent receives greeting request and returns a non-empty greeting."""
    from agent import SampleAgent

    agent = SampleAgent()

    # Mock the LLM to return a canned response (AI Core not available in tests)
    mock_response = MagicMock()
    mock_response.content = "Good morning! Welcome back. Hope you have a great day ahead."

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {"messages": [mock_response]}

        result = await agent.invoke("Hello", context_id="test-context-001")

    assert result.status == "completed"
    assert len(result.message) > 0
    assert any(
        word in result.message.lower()
        for word in ["morning", "afternoon", "evening", "hello", "welcome"]
    )


@pytest.mark.asyncio
async def test_agent_stream_yields_final_response():
    """Test that stream() yields a completed response."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_response = MagicMock()
    mock_response.content = "Good afternoon! Welcome back."

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {"messages": [mock_response]}

        chunks = []
        async for chunk in agent.stream("Hi", context_id="test-context-002"):
            chunks.append(chunk)

    assert len(chunks) >= 1
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "afternoon" in final["content"].lower() or "welcome" in final["content"].lower()


@pytest.mark.asyncio
async def test_agent_handles_error_gracefully():
    """Test that agent returns an error response when invocation fails."""
    from agent import SampleAgent

    agent = SampleAgent()

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.side_effect = Exception("Simulated failure")

        result = await agent.invoke("Hello", context_id="test-context-003")

    assert result.status in ("completed", "error")
    assert len(result.message) > 0
