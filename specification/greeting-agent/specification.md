# Specification: greeting-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read the project input (`product-requirements-document.md` and `intent.md`)
- [ ] Bootstrap agent code in `assets/greeting-agent/` using instructions from the sap-agent-bootstrap section (invoke from inside `assets/greeting-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

> This agent has a single, simple responsibility — no complex multi-step workflows, no domain-specific reference data, and no conditional logic trees. Runtime skills are NOT needed.

---

## Project-Specific Tasks

## Time-of-Day Detection

- [ ] Implement a `get_time_of_day()` helper function in `app/` that reads the current server timestamp and returns one of three string values: `"morning"` (00:00–11:59), `"afternoon"` (12:00–17:59), or `"evening"` (18:00–23:59)
- [ ] Ensure the function always returns a valid value — cover all 24 hours with no gaps or edge-case failures
- [ ] Add a fallback that returns `"day"` if time detection raises an unexpected exception

## Greeting Generation

- [ ] Implement a `get_greeting(time_of_day: str) -> str` function that maps each time-of-day value to a polite greeting string:
  - `"morning"` → `"Good morning! Welcome back. Hope you have a great day ahead."`
  - `"afternoon"` → `"Good afternoon! Welcome back. Hope your day is going well."`
  - `"evening"` → `"Good evening! Welcome back. Hope you had a productive day."`
  - fallback → `"Hello! Welcome back."`
- [ ] Ensure the greeting is always non-empty and polite

## Agent System Prompt

- [ ] Update the agent system prompt in `app/agent.py` (`@prompt_section`) to instruct the agent:
  - Its sole purpose is to greet the user politely based on the current time of day
  - It should call the `get_time_of_day` tool, then use the result to select and return the appropriate greeting
  - It must never fabricate data or make up the time — it must always use the tool
  - It should respond concisely with just the greeting message

## Agent Tool — get_time_of_day

- [ ] Register `get_time_of_day` as a LangChain tool in `app/agent.py` so it is available to the agent graph
- [ ] The tool takes no input and returns the current time-of-day classification string (`"morning"`, `"afternoon"`, or `"evening"`)
- [ ] Annotate with a clear docstring so the LLM understands when and how to call it

## Agent Tool — get_greeting

- [ ] Register `get_greeting` as a LangChain tool in `app/agent.py` that accepts `time_of_day: str` and returns the appropriate greeting string
- [ ] Annotate with a clear docstring

## Response Time

- [ ] Verify that the agent responds in under 2 seconds under local conditions — add a comment in the code noting this as the target SLA

---

## Business Instrumentation

- [ ] Instrument M1 (Interaction Received): emit `M1.achieved: interaction received and parsed successfully` on successful request parsing; emit `M1.missed: interaction could not be received or parsed` on failure
- [ ] Instrument M2 (Time Detection): emit `M2.achieved: time of day detected as [morning|afternoon|evening]` after successful `get_time_of_day()` call; emit `M2.missed: time detection failed, falling back to default greeting` on exception
- [ ] Instrument M3 (Greeting Selected): emit `M3.achieved: greeting selected for [morning|afternoon|evening]` after successful `get_greeting()` call; emit `M3.missed: greeting selection failed, using fallback greeting` on failure
- [ ] Instrument M4 (Greeting Delivered): emit `M4.achieved: greeting delivered successfully` when response is returned to caller; emit `M4.missed: greeting delivery failed or exceeded response time threshold` on failure
- [ ] Add OpenTelemetry custom spans for each milestone using the decorator or context manager form (never inside an async generator — extract logic to a plain async helper `_run_agent()` if needed)
- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

> This agent has no SAP API dependencies and no MCP servers. Skip all MCP wiring tasks. No `mcp-mock.json` is required.

---

## Testing

- [ ] Install test dependencies: `pip install -r requirements-test.txt` (from `assets/greeting-agent/`)
- [ ] Write unit test for `get_time_of_day` tool: assert correct classification for a morning time, afternoon time, and evening time (mock `datetime.now()`)
- [ ] Write unit test for `get_greeting` tool: assert correct greeting string is returned for each time-of-day value, including the fallback
- [ ] Write one integration test: invoke the agent end-to-end with a mocked LLM response and verify a non-empty greeting is returned; mock the LLM (ChatLiteLLM) to return a canned response — do NOT make real AI Core calls
- [ ] Run `pytest` from `assets/greeting-agent/` (no args, no extra flags)
- [ ] Verify coverage ≥ 70%; add targeted tests if below threshold
- [ ] Verify `assets/greeting-agent/app/agent.py` has exactly 9 decorated functions — run: `grep -c "^@agent_model\|^@agent_config\|^@prompt_section" assets/greeting-agent/app/agent.py` and confirm it returns 9
- [ ] Run `pytest` again (no args) to produce final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/greeting-agent/`
