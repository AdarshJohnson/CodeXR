"use strict";
// src/gemini.ts
Object.defineProperty(exports, "__esModule", { value: true });
exports.callGemini = callGemini;
exports.safeParseJSON = safeParseJSON;
async function callGemini(prompt, model, apiKey) {
    if (!apiKey) {
        throw new Error("❌ Missing Gemini API key. Run: CodeXR: Set Gemini API Key");
    }
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(apiKey)}`;
    const body = {
        contents: [
            {
                parts: [{ text: prompt }]
            }
        ]
    };
    const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    // ✅ Better error handling
    if (!res.ok) {
        let errorText = await res.text();
        let errorJson = null;
        try {
            errorJson = JSON.parse(errorText);
        }
        catch {
            // ignore if not valid JSON
        }
        console.error("❌ Gemini API Error Details:", {
            status: res.status,
            statusText: res.statusText,
            body: body,
            error: errorJson || errorText
        });
        throw new Error(`Gemini API Error ${res.status} ${res.statusText}\nDetails: ${errorJson ? JSON.stringify(errorJson, null, 2) : errorText}`);
    }
    const data = await res.json();
    const text = data?.candidates?.[0]?.content?.parts?.map((p) => p.text).join("") ?? "";
    return { text };
}
function safeParseJSON(raw) {
    try {
        return JSON.parse(raw);
    }
    catch {
        return null;
    }
}
