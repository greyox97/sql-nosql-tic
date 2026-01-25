"use client";

interface QueryResultPanelProps {
    result: Record<string, unknown> | string | null;
    documentCount: number;
    execTime: number | null;
}

export default function QueryResultPanel({ result, documentCount, execTime }: QueryResultPanelProps) {
    const formatJSON = (data: unknown): string => {
        if (!data) return "";
        if (typeof data === "string") return data;
        return JSON.stringify(data, null, 2);
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(formatJSON(result));
    };

    const renderJSONWithSyntaxHighlight = (jsonString: string) => {
        if (!jsonString) return "";
        // Basic syntax highlighting for JSON
        const highlighted = jsonString
            .replace(/"([^"]+)":/g, '<span class="text-purple-600 dark:text-purple-400">"$1"</span>:')
            .replace(/: "([^"]+)"/g, ': <span class="text-green-600 dark:text-green-400">"$1"</span>')
            .replace(/: (\d+)/g, ': <span class="text-amber-600 dark:text-amber-400">$1</span>')
            .replace(/[\[\]{}]/g, '<span class="text-slate-500 dark:text-slate-500">$&</span>');

        return highlighted;
    };

    return (
        <section className="flex-1 flex flex-col min-w-[300px] bg-white dark:bg-[#111418]">
            <div className="flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-[#151a20] border-b border-gray-200 dark:border-[#283039]">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-[#137fec] text-sm">data_object</span>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        RESULTADO DE CONSULTA
                    </h3>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-400 px-2 py-0.5 rounded bg-gray-200 dark:bg-[#1c2127]">
                        JSON
                    </span>
                </div>
            </div>
            <div className="flex-1 overflow-auto bg-[#f8fafc] dark:bg-[#0d1117] relative group">
                <button
                    onClick={copyToClipboard}
                    className="absolute top-4 right-4 p-2 bg-white dark:bg-[#1c2127] border border-gray-200 dark:border-[#283039] rounded shadow-sm opacity-50 hover:opacity-100 transition-opacity z-10"
                    title="Copiar Resultado"
                >
                    <span className="material-symbols-outlined text-sm">content_copy</span>
                </button>
                <pre
                    className="p-4 text-sm font-mono leading-relaxed text-slate-800 dark:text-slate-300"
                    dangerouslySetInnerHTML={{
                        __html: renderJSONWithSyntaxHighlight(formatJSON(result)),
                    }}
                />
            </div>
            <div className="flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-[#151a20] border-t border-gray-200 dark:border-[#283039] text-xs text-slate-500">
                <span>{documentCount} Documento{documentCount !== 1 ? "s" : ""} retornado{documentCount !== 1 ? "s" : ""}</span>
                <div className="flex gap-2">
                    {execTime !== null && <span className="text-slate-400">Tiempo de ejecución: {execTime}ms</span>}
                </div>
            </div>
        </section>
    );
}
