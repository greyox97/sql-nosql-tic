import { TranslationResponse, ApiError } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

export async function translateSQL(sql: string): Promise<TranslationResponse> {
    const response = await fetch(`${API_BASE_URL}/consulta`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ sql }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error((data as ApiError).error || "Error en la traducción");
    }

    return data as TranslationResponse;
}

export async function executeNoSQL(nosql: Record<string, unknown>): Promise<TranslationResponse> {
    const response = await fetch(`${API_BASE_URL}/consulta`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ nosql }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error((data as ApiError).error || "Error en la ejecución");
    }

    return data as TranslationResponse;
}

export async function checkConnection(): Promise<{ connected: boolean; message: string }> {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (response.ok && data.status === "ok") {
            return { connected: true, message: "Connected" };
        } else {
            return { connected: false, message: "Disconnected" };
        }
    } catch {
        return { connected: false, message: "Disconnected" };
    }
}
