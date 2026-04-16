import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

import { Client } from "../../servers/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js";
import { StdioClientTransport } from "../../servers/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, "../..");
const FILESYSTEM_SERVER_ENTRY = path.resolve(REPO_ROOT, "servers/src/filesystem/dist/index.js");

async function main() {
  const [allowedRoot, toolName, toolArgsJson] = process.argv.slice(2);

  if (!allowedRoot || !toolName || !toolArgsJson) {
    console.error("Usage: node mcp_filesystem_bridge.mjs <allowed-root> <tool-name> <tool-args-json>");
    process.exit(2);
  }

  const client = new Client({
    name: "mcp-attack-lab-tool-bridge",
    version: "0.1.0",
  });

  const transport = new StdioClientTransport({
    command: "node",
    args: [FILESYSTEM_SERVER_ENTRY, allowedRoot],
    cwd: REPO_ROOT,
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
    await transport.close();
  }
}

await main();
