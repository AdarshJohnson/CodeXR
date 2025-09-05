
import * as vscode from "vscode";
import { callGemini, safeParseJSON } from "./gemini";
import { buildPrompt, Mode } from "./prompts";

let lastSnippet: string | null = null; // stores last generated code for insertion

export function activate(context: vscode.ExtensionContext) {
  // Register side panel (webview view)
  const provider = new CodeXRViewProvider(context);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("codexr.panel", provider)
  );

  // Set API Key (stored in SecretStorage)
  context.subscriptions.push(
    vscode.commands.registerCommand("codexr.setApiKey", async () => {
      const val = await vscode.window.showInputBox({
        prompt: "Enter your Gemini API Key",
        ignoreFocusOut: true,
        password: true
      });
      if (val) {
        await context.secrets.store("codexr.geminiApiKey", val.trim());
        vscode.window.showInformationMessage("CodeXR: API key saved.");
      }
    })
  );

  // Insert last snippet at cursor
  context.subscriptions.push(
    vscode.commands.registerCommand("codexr.insertSnippet", async () => {
      if (!lastSnippet) {
        vscode.window.showWarningMessage("No snippet generated yet.");
        return;
      }
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;
      await editor.insertSnippet(new vscode.SnippetString(lastSnippet), editor.selection.active);
    })
  );

  // Explain selected error (command palette)
  context.subscriptions.push(
    vscode.commands.registerCommand("codexr.explainError", async () => {
      const editor = vscode.window.activeTextEditor;
      const selected = editor?.document.getText(editor.selection) || "";
      if (!selected) {
        vscode.window.showWarningMessage("Select an error message in the editor first.");
        return;
      }
      const model = vscode.workspace.getConfiguration().get<string>("codexr.model", "gemini-2.5-flash");
      const apiKey = "AIzaSyCRg1y68H3cwDRImIIO2gDkbnPbv5RUjco";


      const prompt = buildPrompt("debug", selected);
      try {
        const res = await callGemini(prompt, model, apiKey);
        const json = safeParseJSON(res.text);
        if (json) {
          const cause = json.cause ?? "";
          const fix = json.fix ?? "";
          const code = json.fixed_code ?? "";
          lastSnippet = code || null;
          const output = [
            cause && `Cause: ${cause}`,
            fix && `Fix: ${fix}`,
            code && `\nCorrected code:\n${code}`
          ].filter(Boolean).join("\n\n");
          vscode.window.showInformationMessage("CodeXR: Debug result ready (see panel or output).");
          appendToOutput(output);
        } else {
          appendToOutput(res.text);
        }
      } catch (e: any) {
        vscode.window.showErrorMessage(`CodeXR: ${e.message}`);
      }
    })
  );
}

export function deactivate() {}

class CodeXRViewProvider implements vscode.WebviewViewProvider {
  constructor(private readonly ctx: vscode.ExtensionContext) {}

  resolveWebviewView(view: vscode.WebviewView): void | Thenable<void> {
    view.webview.options = { enableScripts: true }; // we don't allow external resources
    view.webview.html = this.getHtml(view.webview);

    view.webview.onDidReceiveMessage(async (msg) => {
      if (msg.type === "generate") {
        const mode: Mode = msg.mode;
        const text: string = msg.text || "";
        const extra: string = msg.context || "";

        const model = vscode.workspace.getConfiguration().get<string>("codexr.model", "gemini-2.5-flash");
        const apiKey = await this.ctx.secrets.get("codexr.geminiApiKey") || "";

        const prompt = buildPrompt(mode, text, extra);
        try {
          const res = await callGemini(prompt, model, apiKey);
          const json = safeParseJSON(res.text);

          if (json) {
            // try to pick a code-bearing field for insert
            const candidate = json.code || json.fixed_code || null;
            lastSnippet = candidate || lastSnippet;
            view.webview.postMessage({ type: "result", ok: true, json });
          } else {
            view.webview.postMessage({ type: "result", ok: true, text: res.text });
          }
        } catch (e: any) {
          view.webview.postMessage({ type: "result", ok: false, error: e.message });
        }
      } else if (msg.type === "insertLast") {
        await vscode.commands.executeCommand("codexr.insertSnippet");
      }
    });
  }

  private getHtml(webview: vscode.Webview): string {
    const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(this.ctx.extensionUri, "media", "panel.js"));
    return /* html */ `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'self';" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>CodeXR Assistant</title>
  <style>
    body { font-family: var(--vscode-font-family); padding: 8px; }
    textarea, select, button { width: 100%; margin-top: 6px; }
    textarea { min-height: 90px; }
    .row { display: flex; gap: 8px; }
    .row > * { flex: 1; }
    pre { background: var(--vscode-editor-background); padding: 8px; overflow: auto; }
    .small { opacity: 0.8; font-size: 12px; }
  </style>
</head>
<body>
  <h3>CodeXR Assistant</h3>
  <div class="row">
    <label>
      Mode
      <select id="mode">
        <option value="plan">📝 Task Planner</option>
        <option value="code" selected>💻 Code Generator</option>
        <option value="debug">🐞 Error Debugger</option>
      </select>
    </label>
  </div>
  <label>
    Input
    <textarea id="text" placeholder="Describe task, code request, or paste an error..."></textarea>
  </label>
  <label>
    Optional Context
    <textarea id="context" placeholder="Paste docs, constraints, or related code..."></textarea>
  </label>
  <div class="row">
    <button id="run">Generate</button>
    <button id="insert">Insert Last Snippet</button>
  </div>

  <div id="out" class="small" style="margin-top:10px">Ready.</div>

  <script src="${scriptUri}"></script>
</body>
</html>`;
  }
}

function appendToOutput(text: string) {
  const chan = getOutputChannel();
  chan.appendLine("\n=== CodeXR ===\n" + text + "\n");
  chan.show(true);
}

let outputChannel: vscode.OutputChannel | null = null;
function getOutputChannel() {
  if (!outputChannel) outputChannel = vscode.window.createOutputChannel("CodeXR");
  return outputChannel;
}