"use client";

interface ToolbarProps {
    onTranslate: () => void;
    isLoading: boolean;
}

export default function Toolbar({ onTranslate, isLoading }: ToolbarProps) {
    return (
        <div className="flex-none border-b border-solid border-gray-200 dark:border-[#283039] bg-white dark:bg-[#111418] px-6 py-2 flex justify-between items-center">
            <div className="flex items-center gap-2">
                <button
                    onClick={onTranslate}
                    disabled={isLoading}
                    className="flex items-center justify-center rounded-lg h-9 px-4 bg-[#137fec] hover:bg-[#137fec]/90 text-white gap-2 text-sm font-bold shadow-sm shadow-blue-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <span className="material-symbols-outlined text-[20px]">database</span>
                    <span>{isLoading ? "Procesando..." : "Traducir y Consultar"}</span>
                </button>
            </div>
        </div>
    );
}
