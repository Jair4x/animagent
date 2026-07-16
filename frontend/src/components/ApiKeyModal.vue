<script setup lang="ts">
import { ref } from "vue";

const emit = defineEmits<{
    confirm:    [key: string | null]
    cancel:     []
}>()

const apiKey = ref("");

// Use the user's set Gemini API key
function useOwn() {
    emit("confirm", apiKey.value.trim() || null)
}

// Use the app's Gemini API key
function useApp() {
    emit("confirm", null)
}
</script>

<template>
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4">
        <div class="bg-[#1a1d26] border border-white/10 rounded-xl p-6 w-full max-w-md">

            <h2 class="text-white font-medium text-base mb-1">Usando Google Gemini</h2>
            <p class="text-gray-400 text-sm mb-5 leading-relaxed">
                Puedes usar la API key de la aplicación, pero puede no estar disponible
                o haber llegado a su límite diario. Si tienes una propia, ingrésala aquí.
            </p>

            <label class="block text-xs text-gray-500 mb-1.5">Tu API key de Gemini (opcional)</label>
            <input
                v-model="apiKey"
                type="password"
                placeholder="AIza..."
                class="w-full bg-[#0f1117] border border-white/10 
                       rounded-lg px-3 py-2 text-sm text-white placeholder-gray-600 outline-none 
                     focus:border-[#1D9E75] transition-colors mb-5"
                />
            
            <div class="flex gap-3">
                <button
                    @click="$emit('cancel')"
                    class="flex-1 px-4 py-2 rounded-lg border border-white/10 text-sm text-gray-400
                         hover:text-white hover:border-white/20 transition-colors"
                >
                    Cancelar
                </button>

                <button
                    @click="useApp"
                    class="flex-1 px-4 py-2 rounded-lg border border-white/10 text-sm text-gray-300
                         hover:text-white hover:border-white/20 transition-colors">
                    Usar la API key de la app
                </button>

                <button
                    @click="useOwn"
                    class="flex-1 px-4 py-2 rounded-lg bg-[#1D9E75] text-sm text-white hover:bg-[#0F6E56] transition-colors"
                >
                    Confirmar
                </button>
            </div>
        </div>
    </div>
</template>
