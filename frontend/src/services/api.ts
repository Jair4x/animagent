import type { ChatRequest, ChatResponse } from "../types/chat";
import { ApiError } from "./errors";

const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000"

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const headers: Record<string, string> = {
        "Content-Type": "application/json",
    }

    if (request.apiKey) {
        headers["X-API-Key"] = request.apiKey;
    }

    const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers,
        body: JSON.stringify({
            query: request.query,
            provider: request.provider,
            history: request.history,
        }),
    });

    if (!response.ok) {
        let detail: string | undefined;

        try {
            const data = await response.json();
            detail = data.detail;
        } catch { }

        throw new ApiError(
            response.status,
            detail ?? `Error ${response.status}`
        );
    }

    return response.json();
}