# Product backlog – Middleware SQL → NoSQL (Clave-Valor)
**Proyecto:** Middleware unificado SQL para bases de datos NoSQL   
**Metodología:** Scrum  

---

## HU01 – Ingresar una consulta SQL
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T1.1 | Diseñar la sección de entrada de texto para consultas SQL. | Diseño UI | 4 |
| T1.2 | Implementar campo de texto con resaltado de sintaxis. | Desarrollo frontend | 6 |
| T1.3 | Validar la estructura básica de sentencias SQL (SELECT, FROM, WHERE). | Desarrollo backend | 6 |
| T1.4 | Probar la entrada y validación con ejemplos de consultas simples. | Pruebas funcionales | 4 |
| T1.5 | Revisar la legibilidad y facilidad de uso en distintos tamaños de pantalla. | Validación UX | 2 |

---

## HU02 – Ejecutar la consulta SQL
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T2.1 | Crear botón de ejecución y su evento asociado. | Desarrollo frontend | 4 |
| T2.2 | Configurar endpoint Flask para recibir la consulta. | Desarrollo backend | 6 |
| T2.3 | Integrar comunicación HTTP Frontend → Backend. | Integración | 6 |
| T2.4 | Manejar errores de ejecución (sintaxis, conexión, timeout). | Backend | 4 |
| T2.5 | Implementar mensajes de resultado y notificaciones visuales. | Frontend | 4 |
| T2.6 | Probar flujo completo con consultas válidas e inválidas. | Pruebas | 4 |

---

## HU03 – Ver la traducción generada de la consulta
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T3.1 | Diseñar panel para mostrar traducción NoSQL. | Diseño UI | 4 |
| T3.2 | Implementar módulo de traducción SQL → NoSQL (clave-valor). | Desarrollo backend | 10 |
| T3.3 | Mostrar la traducción generada en tiempo real en el panel. | Frontend | 6 |
| T3.4 | Agregar opción para copiar la traducción al portapapeles. | Frontend | 2 |
| T3.5 | Validar precisión de la traducción con ejemplos. | Pruebas | 4 |

---

## HU04 – Identificar errores en la traducción
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T4.1 | Definir estructura de mensajes de error de traducción. | Backend | 4 |
| T4.2 | Implementar manejo de errores detallado en módulo traductor. | Backend | 6 |
| T4.3 | Mostrar mensajes en interfaz junto a la consulta. | Frontend | 4 |
| T4.4 | Validar distintos escenarios de error (palabras clave, sintaxis). | Pruebas | 4 |
| T4.5 | Revisar usabilidad y comprensión de los mensajes. | UX | 2 |

---

## HU05 – Visualizar resultados de la ejecución
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T5.1 | Diseñar componente de tabla para mostrar resultados. | Diseño UI | 4 |
| T5.2 | Implementar renderizado dinámico de datos en tabla. | Frontend | 6 |
| T5.3 | Recibir respuesta desde el backend (JSON). | Integración | 4 |
| T5.4 | Mostrar cantidad de registros y tiempo de ejecución. | Frontend | 4 |
| T5.5 | Probar visualización con distintos tamaños de resultados. | Pruebas | 4 |

---

## HU06 – Ver consulta original y traducción simultáneamente
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T6.1 | Diseñar disposición doble de paneles (SQL / NoSQL). | Diseño UI | 4 |
| T6.2 | Implementar vista con sincronización de desplazamiento. | Frontend | 6 |
| T6.3 | Agregar control para ocultar/mostrar panel de traducción. | Frontend | 4 |
| T6.4 | Validar que ambas vistas se actualicen tras ejecutar consulta. | Pruebas | 4 |
| T6.5 | Revisar la alineación visual y consistencia de formato. | UX | 2 |

---

## HU07 – Interfaz intuitiva y ordenada
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T7.1 | Unificar esquema visual (tipografía, colores, espaciado). | Diseño UI | 4 |
| T7.2 | Revisar jerarquía visual y consistencia entre secciones. | UX | 4 |
| T7.3 | Implementar mejoras visuales (íconos, bordes, layout). | Frontend | 6 |
| T7.4 | Validar la experiencia de usuario con feedback de compañeros. | Validación | 2 |
| T7.5 | Documentar lineamientos visuales básicos. | Documentación | 2 |

---

## HU08 – Retroalimentación visual durante la ejecución
| ID Tarea | Descripción de la tarea | Tipo | Estimación (h) |
|-----------|-------------------------|------|----------------|
| T8.1 | Diseñar animación o indicador de progreso. | Diseño UI | 3 |
| T8.2 | Implementar indicador de carga en frontend. | Frontend | 4 |
| T8.3 | Integrar estados de “procesando”, “éxito”, “error”. | Frontend | 4 |
| T8.4 | Validar que el indicador desaparezca correctamente al finalizar. | Pruebas | 3 |
| T8.5 | Probar con ejecuciones largas o con error simulado. | QA | 2 |

---

## Totales aproximados
| Categoría | Horas estimadas |
|------------|----------------|
| Diseño UI/UX | 39 |
| Desarrollo frontend | 48 |
| Desarrollo backend | 32 |
| Integración | 10 |
| Pruebas / QA | 23 |
| Documentación / Validación | 8 |
| **Total general** | **≈160 horas técnicas**  |