"use client";

import { useState, useRef, useCallback } from "react";

interface FirebaseQueries {
    javascript: string;
    python: string;
}

interface NoSQLOutputPanelProps {
    consultaParseada: string;
    firebaseQueries?: FirebaseQueries;
}

export default function NoSQLOutputPanel({ consultaParseada, firebaseQueries }: NoSQLOutputPanelProps) {
    const [activeTab, setActiveTab] = useState<"javascript" | "python">("javascript");
    const [firebaseHeight, setFirebaseHeight] = useState(65); // percentage
    const containerRef = useRef<HTMLDivElement>(null);
    const isDragging = useRef(false);

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
    };

    const currentQuery = firebaseQueries?.[activeTab] || "";

    const handleMouseDown = useCallback(() => {
        isDragging.current = true;
        document.body.style.cursor = "row-resize";
        document.body.style.userSelect = "none";
    }, []);

    const handleMouseUp = useCallback(() => {
        isDragging.current = false;
        document.body.style.cursor = "";
        document.body.style.userSelect = "";
    }, []);

    const handleMouseMove = useCallback((e: React.MouseEvent) => {
        if (!isDragging.current || !containerRef.current) return;

        const container = containerRef.current;
        const rect = container.getBoundingClientRect();
        const headerHeight = 41; // Header height in pixels
        const availableHeight = rect.height - headerHeight;
        const relativeY = e.clientY - rect.top - headerHeight;
        const percentage = Math.min(85, Math.max(25, (relativeY / availableHeight) * 100));

        setFirebaseHeight(percentage);
    }, []);

    return (
        <section
            ref={containerRef}
            className="flex-1 flex flex-col min-w-[300px] border-r border-gray-200 dark:border-[#283039] bg-white dark:bg-[#111418]"
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
        >
            {/* Header */}
            <div className="flex-none flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-[#151a20] border-b border-gray-200 dark:border-[#283039]">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-green-500 text-sm">code</span>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        SALIDA NOSQL
                    </h3>
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-400 px-2 py-0.5 rounded bg-gray-200 dark:bg-[#1c2127]">
                        Firebase RTDB
                    </span>
                </div>
            </div>

            {/* Content area */}
            <div className="flex-1 flex flex-col min-h-0 overflow-hidden">
                {/* Firebase Queries Section */}
                {firebaseQueries && (
                    <div
                        className="flex flex-col overflow-hidden"
                        style={{ height: `${firebaseHeight}%` }}
                    >
                        <div className="flex-none flex items-center bg-gray-100 dark:bg-[#1c2127] px-2 border-b border-gray-200 dark:border-[#283039]">
                            <button
                                onClick={() => setActiveTab("javascript")}
                                className={`px-3 py-1.5 text-xs font-medium transition-colors ${activeTab === "javascript"
                                        ? "text-amber-600 dark:text-amber-400 border-b-2 border-amber-500 bg-white dark:bg-[#0d1117]"
                                        : "text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                                    }`}
                            >
                                JavaScript
                            </button>
                            <button
                                onClick={() => setActiveTab("python")}
                                className={`px-3 py-1.5 text-xs font-medium transition-colors ${activeTab === "python"
                                        ? "text-blue-600 dark:text-blue-400 border-b-2 border-blue-500 bg-white dark:bg-[#0d1117]"
                                        : "text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                                    }`}
                            >
                                Python
                            </button>
                            <button
                                onClick={() => copyToClipboard(currentQuery)}
                                className="ml-auto p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                                title="Copiar código"
                            >
                                <span className="material-symbols-outlined text-sm">content_copy</span>
                            </button>
                        </div>
                        <div className="flex-1 overflow-auto bg-[#1e1e1e] dark:bg-[#0d1117] p-3">
                            <pre className={`text-sm font-mono whitespace-pre-wrap leading-relaxed ${activeTab === "javascript" ? "text-amber-300" : "text-blue-300"
                                }`}>
                                {currentQuery || "Sin código disponible"}
                            </pre>
                        </div>
                    </div>
                )}

                {/* Resizable Divider */}
                {firebaseQueries && (
                    <div
                        className="flex-none h-2 bg-gray-200 dark:bg-[#283039] cursor-row-resize hover:bg-blue-400 dark:hover:bg-blue-600 transition-colors flex items-center justify-center group"
                        onMouseDown={handleMouseDown}
                    >
                        <div className="w-8 h-1 rounded-full bg-gray-400 dark:bg-gray-600 group-hover:bg-white transition-colors" />
                    </div>
                )}

                {/* Consulta Parseada Section */}
                <div
                    className="flex flex-col overflow-hidden"
                    style={{ height: firebaseQueries ? `${100 - firebaseHeight}%` : "100%" }}
                >
                    <div className="flex-none flex items-center justify-between px-3 py-1.5 bg-gray-50 dark:bg-[#151a20] border-b border-gray-200 dark:border-[#283039]">
                        <span className="text-[10px] font-medium uppercase tracking-wider text-slate-400">Consulta Parseada</span>
                        <button
                            onClick={() => copyToClipboard(consultaParseada)}
                            className="p-1 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                            title="Copiar JSON"
                        >
                            <span className="material-symbols-outlined text-sm">content_copy</span>
                        </button>
                    </div>
                    <div className="flex-1 overflow-auto bg-[#f8fafc] dark:bg-[#0d1117]">
                        <pre className="p-3 text-xs font-mono leading-relaxed text-blue-700 dark:text-[#a5d6ff] whitespace-pre-wrap">
                            {consultaParseada || "Ejecuta una consulta para ver el resultado"}
                        </pre>
                    </div>
                </div>
            </div>
        </section>
    );
}


