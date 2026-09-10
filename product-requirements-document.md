# Product Requirements Document (PRD)

**Title:** Greeting Agent  
**Date:** 2026-09-10  
**Owner:** Product Owner  
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**
Employees logging into an internal system currently receive no personalised welcome. This AI agent greets each employee politely based on the time of day, creating a warm and engaging first interaction every time they access the system.

**Business Need:**
A simple, consistent, time-aware greeting improves the employee experience at the point of system access. It sets a positive tone for the workday without requiring any manual effort or configuration per user.

**Expected Value:**
- 100% greeting accuracy across all times of day (morning, afternoon, evening)
- Positive user experience — employees feel welcomed upon login
- Response time under 2 seconds, ensuring no friction at login

**Product Objectives (Prioritized):**
1. Deliver accurate, time-appropriate greetings 100% of the time
2. Ensure response time is consistently under 2 seconds
3. Provide a foundation for future extensibility (e.g., personalisation, multi-language)

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Greeting accuracy by time of day | — | 100% correct (morning/afternoon/evening) | — | Employee Engagement | user |
| User feel welcomed | — | Positive user experience | — | Employee Engagement | user |
| Response time | — | < 2 seconds | — | Agent Performance | user |

---

## User Profiles & Personas

### Primary Persona: Alex — Internal Employee

Alex is a 34-year-old office worker who logs into the internal company system at the start of each working day. Alex works across a range of business functions and accesses the system multiple times a day. Alex is comfortable with technology and expects tools to work quickly and reliably. Alex's primary frustration is with impersonal, generic system interfaces that feel transactional rather than human. A simple, polite greeting at login would immediately improve Alex's perception of the system and set a positive tone for the day.

---

## Requirements

### Must-Have Requirements

**REQ-01: Time-of-Day Detection**

- **Problem to Solve:** The agent must know what time of day it is in order to deliver an appropriate greeting.
- **User Story:** As an internal employee, I need the system to detect the current time of day so that I receive a greeting that matches the moment I am logging in.
- **Acceptance Criteria:**
  - Given a login event at any time, when the agent processes the request, then it correctly classifies the time as morning (00:00–11:59), afternoon (12:00–17:59), or evening (18:00–23:59).
- **Maps to Objective:** Objective 1 — greeting accuracy
- **Priority Rank:** 1

**REQ-02: Polite Time-Aware Greeting Response**

- **Problem to Solve:** Employees receive no personalised welcome when logging in, making the experience feel impersonal.
- **User Story:** As an internal employee, I need to receive a polite greeting appropriate to the time of day so that I feel welcomed when I access the system.
- **Acceptance Criteria:**
  - Given a detected time of day, when the agent generates a response, then the greeting includes the correct salutation (e.g., "Good morning", "Good afternoon", "Good evening") and is phrased politely.
- **Maps to Objective:** Objective 1 — greeting accuracy
- **Priority Rank:** 2

**REQ-03: Response Time Under 2 Seconds**

- **Problem to Solve:** A slow greeting response would create friction at login and negatively impact the user experience.
- **User Story:** As an internal employee, I need the greeting to appear quickly so that my login experience is not delayed.
- **Acceptance Criteria:**
  - Given any login event, when the agent is invoked, then the greeting response is returned within 2 seconds under normal operating conditions.
- **Maps to Objective:** Objective 2 — response time
- **Priority Rank:** 3

**REQ-04: Graceful Handling of All Times of Day**

- **Problem to Solve:** The agent must handle every possible time of day without failure or unexpected output.
- **User Story:** As an internal employee, I need the agent to always return a valid greeting regardless of when I log in, so that I never encounter an error or blank response.
- **Acceptance Criteria:**
  - Given any time between 00:00 and 23:59, when the agent is invoked, then a valid and appropriate greeting is always returned.
- **Maps to Objective:** Objective 1 — greeting accuracy
- **Priority Rank:** 4

---

## Solution Architecture

**Architecture Overview:**
A standalone Python AI agent built on the A2A (Agent-to-Agent) protocol. The agent receives a login interaction, detects the current server time, maps it to a time-of-day bucket, and returns a polite greeting. No external APIs, data products, or MCP servers are required.

**Key Components:**

- **Greeting Agent (Python / A2A):** Core agent that handles time detection and greeting generation.
- **Time Detection Module:** Server-side logic that maps the current timestamp to morning, afternoon, or evening.
- **Response Generator:** Constructs a polite, time-appropriate greeting string.

**Integration Points:**

- None required for the initial implementation. The agent is self-contained.

---

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
The agent is designed with extension points to support future capabilities:
- **Personalisation hook:** A placeholder for incorporating the employee's name or role in future versions.
- **Language hook:** A placeholder for multi-language greeting support.
- **Custom greeting hook:** Allows future injection of occasion-based greetings (e.g., holidays, company events).

**Business Step Instrumentation:**
All key business logic steps emit structured log statements for observability. Log statements follow the pattern: `[MILESTONE_ID].[achieved|missed]: [description]`

---

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent

**Actions the system performs without human approval:**
- Detect current time of day
- Select and deliver the appropriate greeting

**Actions that require human review or approval:**
- None — the agent operates fully autonomously for this use case

**Model or engine used:** Deterministic server-side time logic; LLM may be used optionally for dynamic greeting phrasing via SAP Generative AI Hub.

**Knowledge & data sources accessed:**
- System clock (server-side timestamp) — no external data source required

**Tools or connectors invoked:**
- None — the agent is self-contained

**Guardrails & fail-safes:**
- If time detection fails, default to a neutral greeting (e.g., "Hello, welcome back!")
- Agent never writes to any system; it is strictly read and respond

---

## Milestones

### M1: Interaction Received

- **Description:** The agent receives a login interaction or greeting request from a user.
- **Achieved when:** The agent successfully receives and parses the incoming request.
- **Log on achievement:** `M1.achieved: interaction received and parsed successfully`
- **Log on miss:** `M1.missed: interaction could not be received or parsed`

### M2: Time Detection

- **Description:** The agent detects the current time of day and classifies it as morning, afternoon, or evening.
- **Achieved when:** A valid time-of-day classification is produced from the server timestamp.
- **Log on achievement:** `M2.achieved: time of day detected as [morning|afternoon|evening]`
- **Log on miss:** `M2.missed: time detection failed, falling back to default greeting`

### M3: Greeting Selected

- **Description:** The agent selects the appropriate greeting based on the detected time of day.
- **Achieved when:** A greeting string matching the time-of-day classification is prepared.
- **Log on achievement:** `M3.achieved: greeting selected for [morning|afternoon|evening]`
- **Log on miss:** `M3.missed: greeting selection failed, using fallback greeting`

### M4: Greeting Delivered

- **Description:** The agent delivers the polite, time-aware greeting to the employee.
- **Achieved when:** The greeting response is successfully returned to the caller within the target response time.
- **Log on achievement:** `M4.achieved: greeting delivered successfully in [Xms]`
- **Log on miss:** `M4.missed: greeting delivery failed or exceeded response time threshold`
