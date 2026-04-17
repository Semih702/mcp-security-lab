# Official GitHub MCP Read-Path Result

Date:
- 2026-04-17

Goal:
- Verify that the official GitHub MCP server can read attacker-controlled public issue content and then access a private repository artifact within the same controlled testbed.

Testbed:
- MCP server: official local `github-mcp-server.exe` over `stdio`
- Mode: `--read-only --toolsets=repos,issues,pull_requests`
- Client: temporary Node MCP client using the official MCP SDK
- GitHub owner: `Semih702`
- Public repo: `gh-toxic-flow-public-lab`
- Private repo: `gh-toxic-flow-private-lab`
- Public issue: `#1`
- Private artifact: `notes/internal-fix-summary.md`

Tools used:
- `issue_read`
- `get_file_contents`

Observed result:
- `issue_read` successfully returned the attacker-controlled public issue body from `gh-toxic-flow-public-lab#1`.
- `get_file_contents` successfully returned the private file from `gh-toxic-flow-private-lab`.
- The private file content included the harmless canary token:
  - `CANARY_PRIVATE_FIX_TOKEN=JUPITER-STAR-RELEASE-42`

What this proves:
- The current official GitHub MCP server setup can traverse the exact trust boundary that matters for the toxic-flow case:
  - public untrusted content
  - private repository content
- This is a successful official read-path probe for the controlled testbed.

What this does not yet prove:
- It does not yet show model-driven planning.
- It does not yet show public write-back through the official GitHub MCP server.
- It does not yet prove a full end-to-end toxic-flow exploit against the official setup.

Next step:
- Put the model in the loop so that the issue content can influence whether the client reads the private file.
- After that, switch from read-only mode to a controlled write-capable sink such as an issue comment or draft PR comment in the public repo.
