import { ref } from "vue";

export type ToastType = "error" | "warning" | "info"

export interface Toast {
    id:         string
    type:       ToastType
    message:    string
}

const toasts = ref<Toast[]>([]);

export function useToast() {
    function add(message: string, type: ToastType = "error") {
        toasts.value.push({
            id: crypto.randomUUID(),
            type,
            message,
        });
    }

    function remove(id: string) {
        toasts.value = toasts.value.filter(t => t.id !== id)
    }

    function error(message: string)     { add(message, "error") }
    function warning(message: string)   { add(message, "warning") }
    function info(message: string)      { add(message, "info") }
    
    return { toasts, add, remove, error, warning, info}
}
