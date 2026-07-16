import type { ChatRequest, ChatResponse } from "../types/chat";

const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000"

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const headers: Record<string, string> = {
        "Content-Type": "application/json",
    }

    if (request.geminiKey) {
        headers["X-Gemini-Key"] = request.geminiKey;
    }

    const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers,
        body: JSON.stringify({
            query:      request.query,
            provider:   request.provider,
        }),
    })

    if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    return response.json();
}