<script setup lang="ts">
import { ref } from "vue";
import ChatWindow from "./ChatWindow.vue";
import ChatInput from "./ChatInput.vue";
import { sendMessage } from "../services/api.ts";
import type { Message, Provider } from "../types/chat";

const messages  = ref<Message[]>([])
const loading = ref(false)

async function onSend(query: string, provider: Provider, geminiKey: string | null) {
    messages.value.push({
        id:         crypto.randomUUID(),
        role:       "user",
        content:    query,
        timestamp:  new Date()
    });

    loading.value = true;

    try {
        const response = await sendMessage({ query, provider, geminiKey: geminiKey ?? undefined });

        messages.value.push({
            id:         crypto.randomUUID(),
            role:       "agent",
            content:    response.response,
            source:     response.source     ?? undefined,
            category:   response.category   ?? undefined,
            timestamp:  new Date(),
        });
    } catch (error) {
        messages.value.push({
            id:         crypto.randomUUID(),
            role:       "agent",
            content:    "Ocurrió un error al contactar con el agente. Intenta de nuevo.",
            timestamp:  new Date(),
        });

        console.log(error)

    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <ChatWindow :messages="messages" :loading="loading" />
    <ChatInput v-model:loading="loading" @send="onSend" />
</template>