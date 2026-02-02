# MCP Setup Challenge Report

## 1. What I did
I configured VS Code with the Tenx MCP server using `.vscode/mcp.json`. 
For Task 2, I created a `.github/copilot-instructions.md` file. Based on my research into Boris Cherny's workflow, I implemented rules that force the agent to be concise and plan before coding.

## 2. What worked
The "Be Concise" rule worked immediately; Copilot stopped giving me long introductions. The connection to the Tenx MCP server was successful after authenticating via browser.

## 3. What didn't work & Troubleshooting
 The setup was smooth, but I had to ensure the folder structure (.github) was exactly correct.

## 4. Insights gained
I learned that `copilot-instructions.md` acts as a persistent context for the AI, allowing me to program its behavior without repeating myself in every chat message.