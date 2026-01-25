# Historias de usuario – Middleware SQL → NoSQL (Clave-Valor)
**Proyecto:** Middleware unificado SQL para bases de datos NoSQL   

---

## HU01
| Campo | Detalle |
|---|---|
| **Código** | HU01 |
| **Usuario** | Usuario |
| **Nombre historia** | Ingresar una consulta SQL |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Bajo |
| **Puntos estimados** | 3 |
| **Iteración asignada** | 1 |
| **Descripción** | Como usuario, quiero ingresar una sentencia SQL en un área de texto para realizar consultas sobre la base de datos NoSQL. |
| **Criterios de aceptación** | • El sistema acepta sentencias SQL básicas.<br>• Se valida la sintaxis antes de ejecutar.<br>• El usuario puede editar y limpiar el área de consulta. |
| **Observaciones** | El área debe tener resaltado de sintaxis para mejorar la legibilidad. |

---

## HU02
| Campo | Detalle |
|---|---|
| **Código** | HU02 |
| **Usuario** | Usuario |
| **Nombre historia** | Ejecutar la consulta SQL |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Medio |
| **Puntos estimados** | 5 |
| **Iteración asignada** | 1 |
| **Descripción** | Como usuario, quiero ejecutar mi consulta SQL y recibir una respuesta clara sobre el resultado de la operación. |
| **Criterios de aceptación** | • Botón visible para ejecutar la consulta.<br>• El sistema muestra un mensaje si la consulta es inválida.<br>• Se registra el tiempo de ejecución. |
| **Observaciones** | Mostrar indicadores visuales de progreso mientras se ejecuta. |

---

## HU03
| Campo | Detalle |
|---|---|
| **Código** | HU03 |
| **Usuario** | Usuario |
| **Nombre historia** | Ver la traducción generada de la consulta |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Medio |
| **Puntos estimados** | 8 |
| **Iteración asignada** | 2 |
| **Descripción** | Como usuario, quiero visualizar cómo mi consulta SQL fue traducida a una operación NoSQL para entender el proceso de transformación. |
| **Criterios de aceptación** | • Se muestra la traducción generada al lenguaje NoSQL.<br>• La correspondencia entre SQL y NoSQL es comprensible.<br>• Se puede copiar o expandir la traducción. |
| **Observaciones** | Mostrar la traducción en un panel separado junto a la consulta original. |

---

## HU04
| Campo | Detalle |
|---|---|
| **Código** | HU04 |
| **Usuario** | Usuario |
| **Nombre historia** | Identificar errores en la traducción |
| **Prioridad en negocio** | Media |
| **Riesgo en desarrollo** | Medio |
| **Puntos estimados** | 3 |
| **Iteración asignada** | 2 |
| **Descripción** | Como usuario, quiero recibir un mensaje claro si la traducción de mi consulta SQL no puede realizarse para corregirla fácilmente. |
| **Criterios de aceptación** | • Se muestra un mensaje descriptivo cuando no se puede traducir la sentencia.<br>• El mensaje indica la parte problemática de la consulta.<br>• No se pierde la consulta ingresada. |
| **Observaciones** | Debe mantener la consulta original visible al mostrar el error. |

---

## HU05
| Campo | Detalle |
|---|---|
| **Código** | HU05 |
| **Usuario** | Usuario |
| **Nombre historia** | Visualizar resultados de la ejecución |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Bajo |
| **Puntos estimados** | 5 |
| **Iteración asignada** | 3 |
| **Descripción** | Como usuario, quiero ver los resultados devueltos por la base de datos NoSQL en una tabla para interpretar fácilmente la información. |
| **Criterios de aceptación** | • Los resultados se muestran en formato de tabla legible.<br>• Se indica cantidad de registros devueltos.<br>• El área de resultados se limpia entre ejecuciones. |
| **Observaciones** | Permitir desplazamiento horizontal y vertical en resultados extensos. |

---

## HU06
| Campo | Detalle |
|---|---|
| **Código** | HU06 |
| **Usuario** | Usuario |
| **Nombre historia** | Ver la consulta original y la traducción simultáneamente |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Medio |
| **Puntos estimados** | 8 |
| **Iteración asignada** | 3 |
| **Descripción** | Como usuario, quiero ver al mismo tiempo mi consulta original y su traducción NoSQL para comparar ambas fácilmente. |
| **Criterios de aceptación** | • Ambas sentencias se muestran lado a lado o en paneles apilados.<br>• Se mantiene sincronía al desplazarse entre paneles.<br>• El usuario puede ocultar o mostrar la traducción. |
| **Observaciones** | Ideal para entornos educativos o de validación visual. |

---

## HU07
| Campo | Detalle |
|---|---|
| **Código** | HU07 |
| **Usuario** | Usuario |
| **Nombre historia** | Interfaz intuitiva y ordenada |
| **Prioridad en negocio** | Alta |
| **Riesgo en desarrollo** | Bajo |
| **Puntos estimados** | 5 |
| **Iteración asignada** | 4 |
| **Descripción** | Como usuario, quiero que la interfaz del sistema sea clara y organizada para poder comprender rápidamente cada sección del proceso. |
| **Criterios de aceptación** | • La interfaz incluye secciones diferenciadas (entrada, traducción, resultados).<br>• Los controles son visibles y consistentes.<br>• El diseño responde correctamente a distintos tamaños de pantalla. |
| **Observaciones** | Usar colores y jerarquías visuales para guiar al usuario. |

---

## HU08
| Campo | Detalle |
|---|---|
| **Código** | HU08 |
| **Usuario** | Usuario |
| **Nombre historia** | Recibir retroalimentación visual durante la ejecución |
| **Prioridad en negocio** | Media |
| **Riesgo en desarrollo** | Bajo |
| **Puntos estimados** | 3 |
| **Iteración asignada** | 4 |
| **Descripción** | Como usuario, quiero que el sistema muestre indicadores de progreso o estado durante la ejecución de una consulta para saber que el proceso está en curso. |
| **Criterios de aceptación** | • Se muestra un indicador de carga o progreso durante la ejecución.<br>• El indicador desaparece al mostrar los resultados.<br>• En caso de error, el indicador cambia de color o forma. |
| **Observaciones** | Facilita la percepción de respuesta y mejora la experiencia de uso. |
