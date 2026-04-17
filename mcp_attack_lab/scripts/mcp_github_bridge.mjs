import process from "node:process";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "../../servers/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js";
import { StdioClientTransport } from "../../servers/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DEFAULT_SERVER_BIN = "D:/github-mcp-server-official/github-mcp-server.exe";

async function main() {
  const [toolName, toolArgsJson, optionsJson] = process.argv.slice(2);

  if (!toolName || !toolArgsJson) {
    console.error("Usage: node mcp_github_bridge.mjs <tool-name> <tool-args-json> [options-json]");
    process.exit(2);
  }

  const options = optionsJson ? JSON.parse(optionsJson) : {};
  const serverBin = options.serverBin || process.env.GITHUB_MCP_SERVER_BIN || DEFAULT_SERVER_BIN;
  const toolsets = options.toolsets || "repos,issues,pull_requests";
  const readOnly = options.readOnly !== false;

  const args = ["stdio"];
  if (readOnly) {
    args.push("--read-only");
  }
  if (toolsets) {
    args.push(`--toolsets=${toolsets}`);
  }

  const client = new Client({
    name: "mcp-attack-lab-github-bridge",
    version: "0.1.0",
  });

  const transport = new StdioClientTransport({
    command: serverBin,
    args,
    env: { ...process.env },
    stderr: "pipe",
  });

  const stderrChunks = [];
  if (transport.stderr) {
    transport.stderr.on("data", (chunk) => {
      stderrChunks.push(String(chunk));
    });
  }

  try {
    await client.connect(transport);
    const toolsResult = await client.listTools();
    const toolResult = await client.callTool({
      name: toolName,
      arguments: JSON.parse(toolArgsJson),
    });

    process.stdout.write(
      JSON.stringify(
        {
          ok: true,
          toolName,
          availableTools: toolsResult.tools.map((tool) => tool.name),
          result: toolResult,
          stderr: stderrChunks.join(""),
        },
        null,
        2,
      ),
    );
  } catch (error) {
    process.stdout.write(
      JSON.stringify(
        {
          ok: false,
          toolName,
          error: error instanceof Error ? error.message : String(error),
          stderr: stderrChunks.join(""),
        },
        null,
        2,
      ),
    );
    process.exitCode = 1;
  } finally {
    await transport.close().catch(() => {});
  }
}

await main();
