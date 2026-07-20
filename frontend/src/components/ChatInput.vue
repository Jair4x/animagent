<script setup lang="ts">
import { ref } from 'vue';
import ProviderApiKeyModal from './ProviderApiKeyModal.vue';
import type { Provider } from '../types/chat';

const emit = defineEmits<{
    send: [query: string, provider: Provider, apiKey: string | null]
}>();

let query               = ref("");
let provider            = ref<Provider>("groq");
let showModal           = ref(false);
let isLoading           = defineModel<boolean>("loading");
let apiKeys             = ref<Record<Provider, string | null>>({
    groq:   null,
    gemini: null,
    openai: null,
});
let configuredProvider  = ref<Record<Provider, boolean>>({
    groq:   false,
    gemini: false,
    openai: false,
});
const pendingProvider   = ref<Provider>("groq");

const providers = [
    { value: "groq",    label: "Groq" },
    { value: "gemini",  label: "Gemini" },
    { value: "openai",  label: "OpenAI" },
];

// When the user changes LLM provider
function onProviderChange(value: Provider) {
    if (!configuredProvider.value[value]) {
        pendingProvider.value = value;
        showModal.value = true;
        return;
    }

    provider.value = value;
}

// APIKeyModal functions
function onModalConfirm(key: string | null) {
    apiKeys.value[pendingProvider.value] = key;
    configuredProvider.value[pendingProvider.value] = true;

    provider.value = pendingProvider.value;
    showModal.value = false;
}

// When sending message
function onSend() {
    const q = query.value.trim()
    if (!q || isLoading.value) return
    emit("send", q, provider.value, apiKeys.value[provider.value])
    query.value = ""
}

// Pressing the "Enter" key also sends the message in chat
function onKeydown(e: KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault()
        onSend()
    }
}
</script>

<template>
    <div class="p-4 border-t border-white/10">
        
        <!-- Selector de provider -->
        <div class="flex items-center gap-2 mb-2">
            <span class="text-xs text-gray-500">Modelo:</span>
            <div class="flex gap-1">
                <button
                    v-for="p in providers"
                    :key="p.value"
                    @click="onProviderChange(p.value as Provider)"
                    :class="[
                        'px-3 py-1 rounded-md text-xs transition-colors hover:cursor-pointer',
                        provider === p.value
                            ? 'bg-[#1D9E75] text-white border-none hover:bg-[#0F6E56]'
                            : 'text-gray-600 border border-white/10 hover:border-white/20'
                    ]"
                >
                    {{ p.label }}
                </button>
            </div>

            <template v-if="provider">
                <span class="text-xs text-gray-500">
                    · {{ apiKeys[provider] ? "key propia" : "key de la app" }}
                </span>
                <button
                    @click="showModal = true"
                    class="text-xs text-gray-600 hover:text-[#1D9E75] transition-colors hover:cursor-pointer"
                >
                    Cambiar API key
                </button>
            </template>
        </div>

        <!-- Input -->
        <div class="flex gap-2 items-end bg-[#1A1D26] border border-white/10 rounded-xl px-3 py-2">
            <textarea
                v-model="query"
                @keydown="onKeydown"
                placeholder="Haz una pregunta..."
                rows="1"
                :disabled="isLoading"
                class="flex-1 bg-transparent outline-none border-none py-1.5 text-sm text-white placeholder-gray-600 resize-none leading-relaxed disabled:opacity-50"
            />

            <button
                @click="onSend"
                :disabled="!query.trim() || isLoading"
                class="w-8 h-8 flex items-center justify-center rounded-lg bg-[#1D9E75] hover:bg-[#0F6E56] hover:cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed transition-colors shrink-0"
            >
                <i class="ti ti-send text-white text-sm" aria-hidden="true" />
            </button>
        </div>

        <p class="text-xs text-gray-600 text-center mt-2">
            Enter para enviar · Shift+Enter para nueva línea
        </p>
    </div>

    <ProviderApiKeyModal
        v-if="showModal"
        :provider="pendingProvider"
        @confirm="onModalConfirm"
        @cancel="showModal = false"
    />

</template>