<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import type { Message } from "../types/chat";

const props = defineProps<{
    messages:   Message[]
    loading:    boolean
}>();

const container = ref<HTMLElement | null>(null)

watch(
    () => [props.messages.length, props.loading],
    async () => {
        await nextTick()
        if (container.value) {
            container.value.scrollTop = container.value.scrollHeight
        }
    }
)
</script>

<template>
    <div
        ref="container"
        class="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-4 scroll-smooth"
    >
        <!-- Estado vacío -->
        <div
            v-if="messages.length === 0 && !loading"
            class="flex-1 flex flex-col items-center justiy-center gap-3 text-center"
        >
            <div class="w-12 h-12 rounded-xl bg-[#1A2A24] border border-[#1D9E75]/30 flex items-center justify-center">
                <i class="ti ti-school text-[#1D9E75] text-2xl" aria-hidden="true" />
            </div>

            <p class="text-gray-400 text-sm">Haz una pregunta sobre ÁNIMA</p>

            <div class="flex flex-col mt-1">
                <p class="text-xs text-gray-600">¿Qué programas tiene la institución?</p>
                <p class="text-xs text-gray-600">¿Cuándo tienen Back-end los grupos de FINEST?</p>
                <p class="text-xs text-gray-600">¿Cuántas faltas puedo tener?</p>
            </div>
        </div>

        <!-- Mensajes -->
        <template v-else>
            <div
                v-for="message in messages"
                :key="message.id"
                :class="[
                    'flex gap-3',
                    message.role === 'user' ? 'justify-end' : 'justify-start items-start'
                ]"
            >

                <!-- Avatar del agente -->
                <div
                    v-if="message.role === 'agent'"
                    class="w-6 h-6 rounded-full bg-[#1A2A24] border border-[#1D9E75]/40 flex items-center justify-center shrink-0 mt-1"
                >
                    <i class="ti ti-robot text-[#1D9E75] text-xs" aria-hidden="true" />
                </div>

                <!-- Burbujas del chat -->
                <div
                    :class="[
                        'max-w-[80%] px-3 py-2 rounded-2xl text-sm leading-relaxed',
                        message.role === 'user'
                        ? 'bg-[#1D9E75] text-white rounded-br-sm'
                        : 'bg-[#1A1D26] border border-white/10 text-gray-200 rounded-bl-sm'
                    ]"
                >
                
                    <p class="whitespace-pre-wrap">{{ message.content }}</p>

                    <!-- Fuente -->
                    <div
                        v-if="message.source"
                        class="mt-2 pt-2 border-t border-white/10 flex items-center gap-1.5"
                    >
                        <i class="ti ti-file-text text-gray-500 text-xs" aria-hidden="true" />

                        <span class="text-xs text-gray-500">{{ message.source }}</span>
                    </div>
                </div>
            </div>

            <!-- Indicador de carga -->
            <div v-if="loading" class="flex gap-3 items-start">
                <div class="2-6 h-6 rounded-full bg-[#1A2A24] border border-[#1D9E75]/40 flex items-center justify-center shrink-0 mt-1">
                    <i class="ti ti-robot text-[#1D9E75] text-xs" aria-hidden="true" />
                </div>
                <div class="bg-[#1A1D26] border border-white/10 rounded-2xl rounded-bl-sm px-4 py-3">
                    <div class="flex gap-1 items-center">
                        <span class="w-1.5 h-1.5 rounded-full bg-[#1D9E75] animate-bounce[animation-relay:0ms]" />
                        <span class="w-1.5 h-1.5 rounded-full bg-[#1D9E75] animate-bounce[animation-relay:150ms]" />
                        <span class="w-1.5 h-1.5 rounded-full bg-[#1D9E75] animate-bounce[animation-relay:300ms]" />
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>
