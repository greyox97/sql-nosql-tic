"use client";

import { useTheme } from "@/context/ThemeContext";

interface HeaderProps {
    isConnected: boolean;
}

export default function Header({ isConnected }: HeaderProps) {
    const { theme, toggleTheme } = useTheme();

    return (
        <header className="flex-none flex items-center justify-between whitespace-nowrap border-b border-solid border-gray-200 dark:border-[#283039] bg-white dark:bg-[#111418] px-6 py-3">
            <div className="flex items-center gap-4">
                <div className="size-8 text-[#137fec]">
                    <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                        <g clipPath="url(#clip0_6_319)">
                            <path
                                d="M8.57829 8.57829C5.52816 11.6284 3.451 15.5145 2.60947 19.7452C1.76794 23.9758 2.19984 28.361 3.85056 32.3462C5.50128 36.3314 8.29667 39.7376 11.8832 42.134C15.4698 44.5305 19.6865 45.8096 24 45.8096C28.3135 45.8096 32.5302 44.5305 36.1168 42.134C39.7033 39.7375 42.4987 36.3314 44.1494 32.3462C45.8002 28.361 46.2321 23.9758 45.3905 19.7452C44.549 15.5145 42.4718 11.6284 39.4217 8.57829L24 24L8.57829 8.57829Z"
                                fill="currentColor"
                            />
                        </g>
                        <defs>
                            <clipPath id="clip0_6_319">
                                <rect fill="white" height="48" width="48" />
                            </clipPath>
                        </defs>
                    </svg>
                </div>
                <h1 className="text-lg font-bold leading-tight tracking-[-0.015em]">
                    Traductor SQL a NoSQL
                </h1>
                <span className="px-2 py-1 rounded bg-green-500/10 text-green-500 text-xs font-medium border border-green-500/20">
                    v1.0.0
                </span>
            </div>
            <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400 px-3 py-1.5 rounded-lg border border-transparent hover:border-gray-200 dark:hover:border-[#283039] transition-colors cursor-default">
                    <span className={`material-symbols-outlined text-[18px] ${isConnected ? "text-green-500" : "text-red-500"}`}>
                        dns
                    </span>
                    <span>{isConnected ? "Conectado" : "Desconectado"}</span>
                </div>
                <button
                    onClick={toggleTheme}
                    className="p-2 rounded-lg text-slate-500 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-[#1c2127] hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
                    title={theme === "dark" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"}
                >
                    <span className="material-symbols-outlined text-[20px]">
                        {theme === "dark" ? "light_mode" : "dark_mode"}
                    </span>
                </button>
            </div>
        </header>
    );
}

