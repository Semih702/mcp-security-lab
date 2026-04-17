# Research Map

This folder contains the paper-facing side of the project.

The easiest way to understand it is to read it in order.

## Recommended Reading Order

### 1. Case Definition

- [case-studies/github-mcp-toxic-flow.md](/d:/ens491/mcp_attack_lab/research/case-studies/github-mcp-toxic-flow.md)

What it explains:

- why the GitHub MCP toxic-flow case was selected
- how it maps to the custom layer taxonomy
- what attack family it represents

### 2. Experiment Sequence

- [roadmaps/github-mcp-toxic-flow-roadmap.md](/d:/ens491/mcp_attack_lab/research/roadmaps/github-mcp-toxic-flow-roadmap.md)
- [roadmaps/github-mcp-production-proof-plan.md](/d:/ens491/mcp_attack_lab/research/roadmaps/github-mcp-production-proof-plan.md)

What they explain:

- the progression from local analogue to official MCP reproduction
- what counts as stronger evidence

### 3. Official Testbed Design

- [testbeds/github-mcp-official-testbed-spec.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-testbed-spec.md)
- [testbeds/github-controlled-repo-seed-plan.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-controlled-repo-seed-plan.md)
- [testbeds/github-repo-setup-instructions.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-repo-setup-instructions.md)

What they explain:

- how the controlled GitHub environment is structured
- what public/private assets exist

### 4. Official Results

- [testbeds/github-mcp-official-read-path-result.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-read-path-result.md)
- [testbeds/github-mcp-official-write-path-result.md](/d:/ens491/mcp_attack_lab/research/testbeds/github-mcp-official-write-path-result.md)

What they explain:

- what was actually reproduced on the official GitHub MCP server

### 5. Popular Client Follow-Up

- [testbeds/vscode-black-box-client-eval-plan.md](/d:/ens491/mcp_attack_lab/research/testbeds/vscode-black-box-client-eval-plan.md)
- [checklists/vscode-black-box-run-checklist.md](/d:/ens491/mcp_attack_lab/research/checklists/vscode-black-box-run-checklist.md)

What they explain:

- how the architectural issue should be tested in a popular black-box client

## Folder Roles

- `case-studies/`
  - threat and public-report interpretation
- `roadmaps/`
  - sequencing and decision logic
- `testbeds/`
  - concrete reproduction environment design and observed results
- `checklists/`
  - operational run sheets
