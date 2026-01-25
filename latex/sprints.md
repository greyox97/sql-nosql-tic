# Planificación de sprints – Middleware SQL → NoSQL (Clave-Valor)
**Proyecto:** Middleware unificado SQL para bases de datos NoSQL  
**Componente:** Sebastián Alejandro Sánchez Maldonado  
**Periodo:** Noviembre - Diciembre 2025
**Duración por Sprint:** 2 semanas  
**Metodología:** Scrum  

---

## Sprint 1 – Entrada y ejecución básica de consultas
| Campo | Detalle |
|---|---|
| **Duración** | 3 – 16 noviembre 2025 |
| **Objetivo del Sprint** | Diseñar la interfaz inicial, permitir ingresar consultas SQL y ejecutar sentencias básicas sobre el middleware. |
| **Historias incluidas** | HU01 – Ingresar una consulta SQL<br>HU02 – Ejecutar la consulta SQL |
| **Tareas principales** | - Diseñar el área de entrada de consultas SQL.<br>- Validar la sintaxis básica antes de ejecutar.<br>- Implementar el endpoint Flask de recepción.<br>- Comunicar Frontend ↔ Backend.<br>- Mostrar resultados o errores iniciales. |
| **Entregables** | Prototipo funcional que permite escribir y ejecutar consultas SQL simples con mensajes de validación. |
| **Horas estimadas** | 60 h |
| **Reuniones Scrum** | Daily Scrum (15 min), Sprint Review, Sprint Retrospective. |

---

## Sprint 2 – Traducción SQL → NoSQL y manejo de errores
| Campo | Detalle |
|---|---|
| **Duración** | 17 – 30 noviembre 2025 |
| **Objetivo del Sprint** | Implementar el módulo de traducción SQL → NoSQL y mostrar errores claros de conversión o sintaxis. |
| **Historias incluidas** | HU03 – Ver la traducción generada de la consulta<br>HU04 – Identificar errores en la traducción |
| **Tareas principales** | - Crear motor de traducción SQL → NoSQL (clave-valor).<br>- Diseñar panel de visualización de traducción.<br>- Mostrar mensajes de error asociados a consultas inválidas.<br>- Validar precisión de traducción y coherencia visual. |
| **Entregables** | Middleware capaz de traducir sentencias SQL a formato NoSQL con retroalimentación de errores. |
| **Horas estimadas** | 60 h |
| **Reuniones Scrum** | Daily Scrum, Sprint Review, Sprint Retrospective. |

---

## Sprint 3 – Visualización y comparación de resultados
| Campo | Detalle |
|---|---|
| **Duración** | 1 – 14 diciembre 2025 |
| **Objetivo del Sprint** | Mostrar los resultados devueltos por la base NoSQL y permitir comparar la consulta original con su traducción. |
| **Historias incluidas** | HU05 – Visualizar resultados de la ejecución<br>HU06 – Ver consulta original y traducción simultáneamente |
| **Tareas principales** | - Renderizar resultados en tabla legible.<br>- Mostrar panel doble (SQL/NoSQL).<br>- Mantener sincronía entre ejecución y visualización.<br>- Probar distintos tipos de resultados y tamaños de datos. |
| **Entregables** | Interfaz integrada que muestra consulta original, traducción y resultados ejecutados correctamente. |
| **Horas estimadas** | 60 h |
| **Reuniones Scrum** | Daily Scrum, Sprint Review, Sprint Retrospective. |

---

## Sprint 4 – Interfaz intuitiva, retroalimentación visual y refinamiento final
| Campo | Detalle |
|---|---|
| **Duración** | 15 – 28 diciembre 2025 |
| **Objetivo del Sprint** | Mejorar la experiencia de uso del sistema, agregar indicadores de ejecución y preparar la documentación técnica final. |
| **Historias incluidas** | HU07 – Interfaz intuitiva y ordenada<br>HU08 – Retroalimentación visual durante la ejecución |
| **Tareas principales** | - Ajustar esquema visual (colores, tipografía, jerarquías).<br>- Agregar animaciones e indicadores de carga.<br>- Validar fluidez y accesibilidad.<br>- Documentar lineamientos visuales y flujo general del sistema. |
| **Entregables** | Versión final del middleware con interfaz refinada, retroalimentación visual y documentación técnica de uso. |
| **Horas estimadas** | 60 h |
| **Reuniones Scrum** | Daily Scrum, Sprint Review, Sprint Retrospective. |

