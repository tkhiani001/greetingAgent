# Greeting Agent

An AI agent that greets internal employees politely based on the time of day.

## Business challenge

Build an AI greeting agent that politely greets internal employees based on the time of day (morning, afternoon, evening) when they log into an internal system.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Greeting accuracy by time of day | — | 100% correct (morning/afternoon/evening) | — | Employee Engagement | user |
| User feel welcomed | — | Positive user experience | — | Employee Engagement | user |
| Response time | — | < 2 seconds | — | Agent Performance | user |

## Key Milestones

1. **Interaction received** — Agent receives a user interaction/request.
2. **Time detection** — Agent detects the current time of day.
3. **Greeting selected** — Agent selects the appropriate greeting (Good Morning / Good Afternoon / Good Evening).
4. **Greeting delivered** — Agent delivers a polite, time-aware greeting to the employee.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash (E2E)

### Process Hierarchy

```
Lead to Cash (E2E)
└── Manage Customers and Channels (generic)
    └── Manage and operate sales channels (generic) (BPS-371)
        └── Operate omnichannel customer platforms
```

### Summary

The greeting agent maps to the "Lead to Cash" E2E process under "Manage Customers and Channels", enabling personalised, context-aware employee engagement at the point of system access.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Data Product ORD ID | Gap? | Notes / assumptions |
|---|---|---|---|---|---|---|---|
| Time-aware greeting for internal employees | None | — | — | — | — | Yes | No standard SAP product covers this; custom AI Agent required |
| Polite, context-sensitive response | None | — | — | — | — | Yes | Must be custom-built using an LLM-backed agent |
| Response time < 2 seconds | None | — | — | — | — | Maybe | Depends on agent runtime and model latency |

### Key findings

- No standard SAP product covers this use case directly; a custom build is required.
- The solution is intentionally lightweight — a focused AI Agent with no external API dependencies.
- Time-of-day detection is a simple server-side operation (no external data source needed).
- The agent will be implemented as a Python A2A protocol agent.
- No MCP server or data product integration is needed for this use case.

## Recommendations

### Time-Aware Greeting AI Agent

#### Executive Summary

Lightweight Python AI agent greeting employees by time of day.

#### Recommended Solution

A custom Python AI agent (A2A protocol) that detects the current server time, maps it to a time-of-day bucket (morning, afternoon, evening), and returns a polite greeting message. No external SAP API or data product integration is required.

#### Problem Statement

Employees logging into an internal system currently receive no personalised welcome experience. A simple, time-aware greeting improves engagement and sets a positive tone for the workday.

#### Affected User Roles

- Internal employees (all roles) logging into an internal system.

#### Important factors

##### Simplicity
The agent has a single, well-defined responsibility — greet based on time. This keeps it fast, maintainable, and easy to extend.

##### No External Dependencies
No SAP API or data product is required, reducing integration complexity and deployment risk.

#### Potential risks

##### LLM Latency
Using an LLM for greeting generation may introduce latency. Mitigation: use deterministic logic for time mapping; LLM used only if dynamic phrasing is needed.

#### Recommended solution category

AI Agent

#### Intent fit
85%
