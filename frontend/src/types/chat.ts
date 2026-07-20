export type Provider = "groq" | "gemini"

export interface Message {
    id:         string
    role:       "user" | "agent"
    content:    string
    source?:    string
    timestamp:  Date
}

export interface HistoryMessage {
    role:       "user" | "assistant"
    content:    string
}

export interface ChatRequest {
    query:      string
    provider:   Provider
    apiKey?:    string
    history:    HistoryMessage[]
}

export interface ChatResponse {
    response:   string
    source:     string | null
}