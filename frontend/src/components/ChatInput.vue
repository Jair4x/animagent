<script setup lang="ts">
import { ref } from 'vue';
import ApiKeyModal from './ApiKeyModal.vue';
import type { Provider } from '../types/chat';

const emit = defineEmits<{
    send: [query: string, provider: Provider, geminiKey: string | null]
}>();

const query             = ref("")
const provider          = ref<Provider>("groq")
const geminiKey         = ref<string | null>(null)
const geminiConfigured  = ref(false)
const showModal         = ref(false)
const isLoading         = defineModel<boolean>("loading")

const providers = [
    { value: "groq",    label: "Groq" },
    { value: "gemini",  label: "Gemini" }
];

// When the user changes LLM provider
function onProviderChange(value: Provider) {
    if (value === "gemini" && !geminiConfigured.value) {
        showModal.value = true
    } else {
        provider.value = value
    }
}

// APIKeyModal functions
function onModalConfirm(key: string | null) {
    provider.value = "gemini"
    geminiKey.value = key
    showModal = false
}

function onModalCancel() {
    provider.value = "groq"
    showModal.value = false
}

// When sending message
function onSend() {
    const q = query.value.trim()
    if (!q || isLoading.value) return
    emit("send", q, provider.value, geminiKey.value)
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
                        'px-3 py-1 rounded-md text-xs transition-colors',
                        provider === p.value
                            ? 'bg-[#1D9E75] text-white'
                            : 'text-gray-400 hover:text-white border border-white/10 hover:border-white/20'
                    ]"
                >
                    {{ p.label }}
                </button>
            </div>

            <template v-if="provider === 'gemini'">
                <span class="text-xs text-gray-500">
                    · {{ geminiKey ? "key propia" : "key de la app" }}
                </span>
                <button
                    @click="showModal = true"
                    class="text-xs text-gray-500 hover:text-[#1D9E75] transition-colors underline underline-offset-2"
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
                class="flex-1 bg-transparent outline-none text-sm text-white placeholder-gray-600 resize-none leading-relaxed disabled:opacity-50"
            />

            <button
                @click="onSend"
                :disabled="!query.trim() || isLoading"
                class="w-8 h-8 flex items-center justify-center rounded-lg bg-[#1D9E75] hover:bg-[#0F6E56] disabled:opacity-40 disabled:cursor-not-allowed transition-colors shrink-0"
            >
                <i class="ti ti-send text-white text-sm" aria-hidden="true" />
            </button>
        </div>

        <p class="text-xs text-gray-600 text-center mt-2">
            Enter para enviar · Shift+Enter para nueva línea
        </p>
    </div>

    <ApiKeyModal
        v-if="showModal"
        @confirm="onModalConfirm"
        @cancel="onModalCancel"
    />

</template>