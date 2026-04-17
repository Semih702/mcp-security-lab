# MCP Security Lab

This repository contains the working materials for a final-year project focused on security weaknesses in MCP-based and LLM-connected systems.

The project direction is:

- reproduce realistic security attack scenarios in a controlled lab
- study why those attacks succeed
- evaluate prevention and mitigation strategies
- document layered threat models and concrete attack patterns

## Main Contents

- `mcp_attack_lab/`
  - Python-based lab scaffold for scenario definitions, MCP profiles, model configs, fixtures, and evaluation logic
- `mcp_security_threat_taxonomy_layered_restored.html`
  - layered MCP threat taxonomy document
- `mcp_attack_catalog.html`
  - attack-pattern catalog with concrete examples and relationships
- `mcp_runtime_defenses.md`
  - notes on runtime defenses and control points
- `policy_gateway.md`
  - notes on policy and enforcement ideas

## Current State

The repository currently provides:

- a reusable scenario schema
- initial attack lab structure
- first baseline scenario definition
- research and documentation artifacts around MCP security

The next implementation phase is to connect the scenario runner to real MCP server execution, model adapters, trace capture, and pass/fail evaluation.
