"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import Header from "@/components/Header";
import Toolbar from "@/components/Toolbar";
import SQLInputPanel from "@/components/SQLInputPanel";
import NoSQLOutputPanel from "@/components/NoSQLOutputPanel";
import QueryResultPanel from "@/components/QueryResultPanel";
import Console from "@/components/Console";
import { translateSQL, checkConnection } from "@/services/api";
import { ConsoleLog } from "@/types";

const INITIAL_SQL = `SELECT displayName, firstName FROM northwind WHERE lastName = 'Gaines';`;

export default function Home() {
  const [sqlInput, setSqlInput] = useState(INITIAL_SQL);
  const [nosqlOutput, setNosqlOutput] = useState("");
  const [firebaseQueries, setFirebaseQueries] = useState<{ javascript: string; python: string } | undefined>(undefined);
  const [queryResult, setQueryResult] = useState<Record<string, unknown> | null>(null);
  const [documentCount, setDocumentCount] = useState(0);
  const [execTime, setExecTime] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const [isConnected, setIsConnected] = useState(false);
  const [consoleLogs, setConsoleLogs] = useState<ConsoleLog[]>([]);
  const [errorCount, setErrorCount] = useState(0);

  function getTimestamp(): string {
    const now = new Date();
    return now.toLocaleTimeString("en-US", { hour12: false }).slice(0, 8);
  }

  const addLog = useCallback((type: ConsoleLog["type"], message: string) => {
    setConsoleLogs((prev) => [...prev, { timestamp: getTimestamp(), type, message }]);
    if (type === "ERROR") {
      setErrorCount((prev) => prev + 1);
    }
  }, []);

  // Check connection on mount and periodically
  const hasInitialized = useRef(false);
  useEffect(() => {
    const checkBackendConnection = async () => {
      const result = await checkConnection();

      setIsConnected(result.connected);
    };

    // Initial check
    checkBackendConnection();

    // Only log once (prevents duplicate in React Strict Mode)
    if (!hasInitialized.current) {
      hasInitialized.current = true;
      addLog("INFO", "Sistema inicializado. Listo para la traducción.");
    }

    // Check every 30 seconds
    const interval = setInterval(checkBackendConnection, 30000);

    return () => clearInterval(interval);
  }, [addLog]);



  const handleTranslate = async () => {
    if (!sqlInput.trim()) {
      addLog("ERROR", "La consulta SQL no puede estar vacía.");
      return;
    }

    if (!isConnected) {
      addLog("ERROR", "No se puede traducir: El backend no está conectado.");
      return;
    }

    setIsLoading(true);
    addLog("ACTION", "Conectando a la colección... Éxito.");
    const startTime = Date.now();

    try {
      const response = await translateSQL(sqlInput);
      const endTime = Date.now();
      setExecTime(endTime - startTime);

      // Format the NoSQL output
      const nosqlFormatted = JSON.stringify(response.consulta_parseada, null, 2);
      setNosqlOutput(nosqlFormatted);
      setFirebaseQueries(response.firebase_queries);

      // Get operation type from parsed query
      const operacion = (response.consulta_parseada?.operacion as string) || "QUERY";

      // Set the result and generate appropriate log message
      if (response.resultado) {
        setQueryResult(response.resultado as Record<string, unknown>);

        // Generate dynamic message based on operation type
        let countMessage = "";
        if (typeof response.resultado === "string") {
          // For INSERT/UPDATE/DELETE operations that return a string message
          countMessage = response.resultado;
          setDocumentCount(0);
        } else {
          const resultKeys = Object.keys(response.resultado);
          setDocumentCount(resultKeys.length);
          countMessage = `${resultKeys.length} documento(s) retornado(s)`;
        }

        addLog("SUCCESS", "SQL traducido a objeto de consulta Firebase. Proyección aplicada.");
        addLog("CONSULT", `Ejecutado ${operacion}. ${countMessage}.`);
      } else {
        setQueryResult(null);
        setDocumentCount(0);
        addLog("SUCCESS", "SQL traducido exitosamente.");
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Error desconocido";
      addLog("ERROR", `Error en traducción: ${errorMessage}`);
      setNosqlOutput("");
      setQueryResult(null);
      // Re-check connection on error
      const result = await checkConnection();

      setIsConnected(result.connected);
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <div className="bg-[#f6f7f8] dark:bg-[#101922] text-slate-900 dark:text-white overflow-hidden h-screen flex flex-col font-sans">
      <Header
        isConnected={isConnected}
      />
      <Toolbar
        onTranslate={handleTranslate}
        isLoading={isLoading}
      />
      <main className="flex-1 flex min-h-0 overflow-hidden bg-gray-50 dark:bg-[#101922]">
        <SQLInputPanel value={sqlInput} onChange={setSqlInput} />
        <NoSQLOutputPanel consultaParseada={nosqlOutput} firebaseQueries={firebaseQueries} />
        <QueryResultPanel result={queryResult} documentCount={documentCount} execTime={execTime} />
      </main>
      <Console logs={consoleLogs} errorCount={errorCount} />
    </div>
  );
}
