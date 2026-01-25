export interface ConsoleLog {
    timestamp: string;
    type: "INFO" | "ACTION" | "SUCCESS" | "CONSULT" | "ERROR";
    message: string;
}

export interface TranslationResponse {
    original: string;
    consulta_parseada: Record<string, unknown>;
    firebase_queries?: {
        javascript: string;
        python: string;
    };
    resultado: Record<string, unknown> | string;
}

export interface ApiError {
    error: string;
}
