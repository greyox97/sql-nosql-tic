"use client";

import { useState } from "react";
import { ConsoleLog } from "@/types";

interface ConsoleProps {
    logs: ConsoleLog[];
    errorCount: number;
}

export default function Console({ logs, errorCount }: ConsoleProps) {
    const [activeTab, setActiveTab] = useState<"console" | "errors">("console");
    const [isMinimized, setIsMinimized] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);

    const getTypeColor = (type: ConsoleLog["type"]) => {
        switch (type) {
            case "INFO":
                return "text-green-600 dark:text-green-400";
            case "ACTION":
                return "text-[#137fec]";
            case "SUCCESS":
                return "text-[#137fec]";
            case "CONSULT":
                return "text-purple-500";
            case "ERROR":
                return "text-red-500";
            default:
                return "text-slate-400";
        }
    };

    const isHighlighted = (type: ConsoleLog["type"]) => {
        return type === "SUCCESS";
    };

    // Filter logs based on active tab
    const filteredLogs = activeTab === "errors"
        ? logs.filter(log => log.type === "ERROR")
        : logs;

    const getConsoleHeight = () => {
        if (isMinimized) return "h-10";
        if (isExpanded) return "h-96";
        return "h-48";
    };

    const getLogTypeLabel = (type: ConsoleLog["type"]) => {
        switch (type) {
            case "INFO": return "INFO";
            case "ACTION": return "ACCIÓN";
            case "SUCCESS": return "ÉXITO";
            case "CONSULT": return "CONSULTA";
            case "ERROR": return "ERROR";
            default: return type;
        }
    };

    return (
        <div className={`flex-none ${getConsoleHeight()} border-t border-gray-200 dark:border-[#283039] bg-white dark:bg-[#0d1117] flex flex-col transition-all duration-300`}>
            <div className="flex items-center justify-between bg-gray-100 dark:bg-[#151a20] px-4 border-b border-gray-200 dark:border-[#283039]">
                <div className="flex">
                    <button
                        onClick={() => setActiveTab("console")}
                        className={`px-4 py-2 text-xs font-medium transition-colors ${activeTab === "console"
                            ? "text-slate-700 dark:text-white border-b-2 border-[#137fec] bg-white dark:bg-[#0d1117]"
                            : "text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-gray-50 dark:hover:bg-[#1c2127]"
                            }`}
                    >
                        Registros de Consola
                    </button>
                    <button
                        onClick={() => setActiveTab("errors")}
                        className={`px-4 py-2 text-xs font-medium transition-colors flex items-center gap-1 ${activeTab === "errors"
                            ? "text-slate-700 dark:text-white border-b-2 border-[#137fec] bg-white dark:bg-[#0d1117]"
                            : "text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-gray-50 dark:hover:bg-[#1c2127]"
                            }`}
                    >
                        Log de Errores
                        <span className="bg-red-500 text-white rounded-full text-[9px] w-4 h-4 flex items-center justify-center">
                            {errorCount}
                        </span>
                    </button>
                </div>
                <div className="flex items-center gap-2 py-1">
                    <button
                        onClick={() => {
                            setIsMinimized(!isMinimized);
                            if (isExpanded) setIsExpanded(false);
                        }}
                        className="p-1 hover:bg-gray-200 dark:hover:bg-[#1c2127] rounded text-slate-400"
                        title={isMinimized ? "Restaurar consola" : "Minimizar consola"}
                    >
                        <span className="material-symbols-outlined text-sm">
                            {isMinimized ? "expand_less" : "minimize"}
                        </span>
                    </button>
                    <button
                        onClick={() => {
                            setIsExpanded(!isExpanded);
                            if (isMinimized) setIsMinimized(false);
                        }}
                        className="p-1 hover:bg-gray-200 dark:hover:bg-[#1c2127] rounded text-slate-400"
                        title={isExpanded ? "Restaurar consola" : "Expandir consola"}
                    >
                        <span className="material-symbols-outlined text-sm">
                            {isExpanded ? "close_fullscreen" : "open_in_full"}
                        </span>
                    </button>
                </div>
            </div>
            {!isMinimized && (
                <div className="flex-1 overflow-y-auto p-4 font-mono text-xs space-y-2 bg-white dark:bg-[#0d1117]">
                    {filteredLogs.length === 0 ? (
                        <div className="text-slate-400 text-center py-4">
                            {activeTab === "errors" ? "No hay errores para mostrar" : "No hay registros aún"}
                        </div>
                    ) : (
                        filteredLogs.map((log, index) => (
                            <div
                                key={index}
                                className={`flex gap-3 text-slate-600 dark:text-slate-400 border-l-2 p-1 rounded ${isHighlighted(log.type)
                                    ? "border-[#137fec] bg-blue-50/50 dark:bg-[#137fec]/5"
                                    : log.type === "ERROR"
                                        ? "border-red-500 bg-red-50/50 dark:bg-red-500/5"
                                        : "border-transparent hover:bg-gray-50 dark:hover:bg-white/5"
                                    }`}
                            >
                                <span className="text-slate-400 select-none w-20">[{log.timestamp}]</span>
                                <span className={`font-bold w-16 ${getTypeColor(log.type)}`}>{getLogTypeLabel(log.type)}</span>
                                <span>{log.message}</span>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
