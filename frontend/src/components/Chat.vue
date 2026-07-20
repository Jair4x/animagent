<script setup lang="ts">
import { ref } from "vue";
import ChatWindow from "./ChatWindow.vue";
import ChatInput from "./ChatInput.vue";
import Toast from "./Toast.vue";
import { sendMessage } from "../services/api.ts";
import type { Message, Provider } from "../types/chat";
import { useToast } from "../services/useToast.ts";

const messages  = ref<Message[]>([])
const loading = ref(false)
const { error: showError } = useToast();

async function onSend(query: string, provider: Provider, geminiKey: string | null) {
    messages.value.push({
        id:         crypto.randomUUID(),
        role:       "user",
        content:    query,
        timestamp:  new Date()
    });

    loading.value = true;

    const history = messages.value
        .slice(-10)
        .filter(m => m.role === "user" || m.role === "agent")
        .map(m => ({
            role:       m.role === "agent" ? "assistant" : "user" as "user" | "assistant",
            content:    m.content,
        }));

    try {
        const response = await sendMessage({ query, provider, geminiKey: geminiKey ?? undefined, history });

        messages.value.push({
            id:         crypto.randomUUID(),
            role:       "agent",
            content:    response.response,
            source:     response.source     ?? undefined,
            category:   response.category   ?? undefined,
            timestamp:  new Date(),
        });
    } catch (error: any) {
        const status = error?.status || error?.response?.status;

        messages.value.push({
            id:         crypto.randomUUID(),
            role:       "agent",
            content:    "Ocurrió un error al intentar generar tu respuesta. Intenta de nuevo.",
            timestamp:  new Date(),
        });

        if (!navigator.onLine) {
            showError("Sin conexión a internet. Verifica tu red e intenta de nuevo.");
        } else if (status === 401) {
            showError("API key inválida. Revisa tu clave de Gemini/Groq.");
        } else if (status === 413 || status === 429) {
            showError("Límite de tokens alcanzado. Espera unos minutos o cambia de proveedor.");
        } else if (error?.message?.includes("NetworkError") || error?.message?.includes("Failed to fetch")) {
            showError("Error interno del servidor. El agente no pudo procesar la consulta.");
        } else if (error?.name === "AbortError" || error?.message?.includes("timeout")) {
            showError("El agente tardó demasiado en responder. Intenta de nuevo.");
        } else {
            showError("No se pudo conectar con el agente. Verifica que el servidor esté activo.")
        }

    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <ChatWindow :messages="messages" :loading="loading" />
    <ChatInput v-model:loading="loading" @send="onSend" />
    <Toast />
</template>