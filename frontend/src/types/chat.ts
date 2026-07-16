export type Provider = "groq" | "gemini"

export interface Message {
    id:         string
    role:       "user" | "agent"
    content:    string
    source?:    string
    category?:  string
    timestamp:  Date
}

export interface ChatRequest {
    query:      string
    provider:   Provider
    geminiKey?: string
}

export interface ChatResponse {
    response:   string
    category:   string | null
    source:     string | null
}