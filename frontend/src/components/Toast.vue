<script setup lang="ts">
import { useToast } from '../services/useToast';
import type { Toast } from '../services/useToast';

const { toasts, remove } = useToast();

const icons: Record<string, string> = {
    error:      "ti-circle-x",
    warning:    "ti-alert-triangle",
    info:       "ti-info-circle",
}

const colors: Record<string, string> = {
    error:      "border-red-500/30 bg-red-500/10 text-red-400",
    warning:    "border-yellow-500/30 bg-yellow-500/10 text-yellow-400",
    info:       "border-blue-500/30 bg-blue-500/10 text-blue-400",
}

const iconColors: Record<string, string> = {
    error:      "text-red-400",
    warning:    "text-yellow-400",
    info:       "text-blue-400",
}
</script>

<template>
    <div class="fixed top-4 right-4 z-50 flex flex-col gap-2 w-fill max-w-sm">
        <div
            v-for="toast in toasts"
            :key="toast.id"
            :class="[
                'flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-sm',
                colors[toast.type]
            ]"
        >
            <i :class="['ti text-base shrink-0', icons[toast.type], iconColors[toast.type]]" />

            <p class="text-sm flex-1 leading-relaxed">{{ toast.message }}</p>

            <button
                @click="remove(toast.id)"
                class="shrink-0 opacity-50 hover:opacity-100 hover:cursor-pointer bg-transparent border-none transition-opacity mt-0.5"
                aria-label="Cerrar"
            >
                <i class="ti ti-x text-sm text-white" aria-hidden="true" />
            </button>
        </div>
    </div>
</template>