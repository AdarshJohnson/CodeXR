"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildPrompt = buildPrompt;
function buildPrompt(mode, text, extraContext) {
    if (mode === "plan") {
        return `You are CodeXR, an AI assistant for AR/VR developers.\n\nBreak the following task into subtasks. Add difficulty (easy/medium/hard) and time (minutes) for each.\nReturn STRICT JSON with fields: steps (string[]), difficulty (string[]), time (number[]). Do NOT include markdown fences.\n\nTask:\n${text}\n\nIf helpful context is provided, use it:\n${extraContext ?? ""}`;
    }
    if (mode === "code") {
        return `You are CodeXR. Generate a concise code snippet with a short explanation.\nReturn STRICT JSON with fields: code (string), explanation (string). Do NOT include markdown fences.\n\nRequest:\n${text}\n\nContext (optional):\n${extraContext ?? ""}`;
    }
    // debug mode
    return `You are CodeXR. Explain the error and provide a fix with corrected code if possible.\nReturn STRICT JSON: {"cause": string, "fix": string, "fixed_code": string}. Do NOT include markdown fences.\n\nError:\n${text}\n\nRelated code (optional):\n${extraContext ?? ""}`;
}
