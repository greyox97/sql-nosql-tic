"use client";

interface SQLInputPanelProps {
    value: string;
    onChange: (value: string) => void;
}

export default function SQLInputPanel({ value, onChange }: SQLInputPanelProps) {
    const lines = value.split("\n").length;

    const copyToClipboard = () => {
        navigator.clipboard.writeText(value);
    };

    return (
        <section className="flex-1 flex flex-col min-w-[300px] border-r border-gray-200 dark:border-[#283039] bg-white dark:bg-[#111418]">
            <div className="flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-[#151a20] border-b border-gray-200 dark:border-[#283039]">
                <div className="flex items-center gap-2">
                    <span className="material-symbols-outlined text-slate-400 text-sm">database</span>
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        ENTRADA SQL
                    </h3>
                </div>
                <div className="text-xs text-slate-400">SQL Estándar</div>
            </div>
            <div className="flex-1 relative">
                <textarea
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="absolute inset-0 w-full h-full p-4 pl-10 resize-none bg-transparent text-sm font-mono leading-relaxed text-slate-800 dark:text-slate-200 border-none focus:ring-0 focus:outline-none placeholder:text-slate-400"
                    placeholder="SELECT * FROM users WHERE status = 'active';"
                    spellCheck={false}
                />
                <div className="absolute left-0 top-0 bottom-0 w-8 bg-gray-50 dark:bg-[#151a20] border-r border-gray-200 dark:border-[#283039] flex flex-col items-center pt-4 text-[10px] text-slate-400 font-mono select-none pointer-events-none">
                    {Array.from({ length: Math.max(lines, 15) }, (_, i) => (
                        <span key={i} className="leading-relaxed text-sm">
                            {i + 1}
                        </span>
                    ))}
                </div>
                <button
                    onClick={copyToClipboard}
                    className="absolute top-4 right-4 p-2 bg-white dark:bg-[#1c2127] border border-gray-200 dark:border-[#283039] rounded shadow-sm opacity-50 hover:opacity-100 transition-opacity"
                    title="Copiar SQL"
                >
                    <span className="material-symbols-outlined text-sm">content_copy</span>
                </button>
            </div>
        </section>
    );
}
