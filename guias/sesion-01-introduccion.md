# Sesión 01 — Introducción a Devin AI

**Duración total:** 3 horas (incluyendo 20 min de descanso)
**Audiencia:** Desarrolladores de Softtek de distintos lenguajes y seniorities
**Formato:** Virtual · Cisco WebEx

---

## Objetivos de aprendizaje

Al terminar esta sesión el alumno será capaz de:

1. Explicar qué diferencia a Devin de un asistente de código convencional como GitHub Copilot.
2. Identificar qué tipos de tareas son adecuadas para delegar en Devin y cuáles no.
3. Describir cómo Devin planifica y ejecuta una tarea internamente.
4. Orientarse en la interfaz de Devin e identificar para qué sirve cada sección.
5. Conectar Devin a un repositorio real y pedirle que analice un PR con bugs.

---

## Materiales necesarios antes de empezar

Antes de que lleguen los alumnos, tener abierto y listo:

- **Repositorio `gestor-tareas-api`** clonado localmente, rama `main`. La rama `escenario-1-bug-logico` ya pusheada y con un PR abierto contra `main` (PR #1: *bug: validaciones de negocio ausentes en tareas*).
- **Cuenta en [devin.ai](https://devin.ai)** con sesión iniciada. Tener listo el panel de nueva sesión para no perder tiempo.
- **Presentación de Gamma** abierta en el navegador: `https://gamma.app/docs/Devin-AI-drzx5jgsctwn5hs`
- **Navegador con estas pestañas preparadas:**
  - PR #1 del repo en GitHub
  - Devin: `app.devin.ai`
  - Documentación de Devin: `docs.devin.ai`
  - Artículo de Gumroad / Sahil Lavingia sobre los 1500 PRs (o captura de pantalla)
- **VS Code** con el repo abierto en `aplicacion/rutas/tareas.py`.
- Tener probado previamente que Devin puede acceder al repo (permisos de GitHub configurados).

*Nota: los accesos a devin.ai deben verificarse el día anterior. Contactar con los participantes con 24 horas de antelación para confirmar que todos tienen cuenta activa. No dedicar tiempo de sesión a resolver accesos.*

---

## Timing general

| Bloque | Duración | Hora inicio | Hora fin |
|---|---|---|---|
| Apertura + conectar Devin al repo | 20 min | 15:30 | 15:50 |
| B1 — Qué es Devin | 30 min | 15:50 | 16:20 |
| Caso real: Gumroad | 5 min | 16:20 | 16:25 |
| B2 — Arquitectura interna | 20 min | 16:25 | 16:45 |
| Tour de la interfaz de Devin | 10 min | 16:45 | 16:55 |
| Demo en vivo | 25 min | 16:55 | 17:20 |
| **DESCANSO** | **20 min** | **17:20** | **17:40** |
| Actividad 1 — identificar bugs | 15 min | 17:40 | 17:55 |
| Actividad 2 — pedir la corrección | 15 min | 17:55 | 18:10 |
| Puesta en común | 10 min | 18:10 | 18:20 |
| Cierre y preview sesión 2 | 10 min | 18:20 | 18:30 |

---

## Apertura y conexión del repo `[20 min — 15:30]`

*Pantalla: diapositiva 1 de la presentación Gamma — portada.*

Buenas tardes a todos. Voy a empezar puntual porque tenemos mucho contenido.

Esta sesión es la primera de un curso sobre Devin AI, y el objetivo no es que salgáis convencidos de que Devin es la herramienta definitiva, sino que salgáis con una imagen realista: qué hace bien, qué hace mal, cómo encaja en un equipo de desarrollo real, y qué tenéis que cambiar en vuestra forma de trabajar para sacarle partido.

Vamos a trabajar sobre un repositorio concreto que vais a conocer hoy: una API de gestión de tareas en Python. No importa si no sois desarrolladores Python, porque lo que importa es la interacción con Devin, no el lenguaje.

La sesión tiene dos mitades separadas por un descanso. En la primera mitad: teoría y demo en vivo. En la segunda: vosotros mismos con Devin.

*Pasar a diapositiva 2 — Qué vamos a ver hoy.*

Esto es lo que vamos a cubrir en estas tres horas. Lo primero que haremos antes de entrar en materia es conectar Devin al repositorio todos juntos — así cuando llegue la actividad no perdemos tiempo con configuración.

### Conectar Devin al repositorio `[10 min — 15:40]`

*Pantalla: abrir devin.ai con sesión iniciada. Compartir pantalla y pedir a los alumnos que hagan lo mismo en paralelo.*

Antes de empezar con la teoría vamos a hacer algo práctico: conectar Devin al repositorio del curso. Lo hacemos juntos ahora para que cuando llegue la actividad no tengáis que preocuparos por la configuración.

Abrid devin.ai e iniciad sesión con vuestra cuenta.

*Esperar 1 minuto a que todos estén dentro.*

Una vez dentro, lo que necesitamos hacer es dar a Devin acceso al repositorio. En el panel central veréis abajo del campo de texto que dice el número de repositorios conectados. Hacéis clic ahí.

*Mostrar en pantalla el proceso paso a paso:*

1. Clic en el selector de repositorios
2. Si no tenéis ninguno conectado, os pedirá que autoricéis el acceso a GitHub — aceptáis
3. Buscáis `gestor-tareas-api` — es el repositorio del usuario `jmojpar`
4. Lo seleccionáis

*Dar 2-3 minutos para que todos lo completen. Resolver dudas rápidas.*

Perfecto. Con esto Devin ya tiene acceso al repositorio y podemos trabajar sobre él durante toda la sesión de hoy. En esta sesión solo le pediremos análisis — no le daremos instrucciones de modificar nada.

*Nota para el formador: los accesos a devin.ai deben verificarse el día anterior. Contactar con los participantes con 24 horas de antelación para confirmar que todos tienen cuenta activa. No dedicar más de 3 minutos adicionales a resolver problemas de acceso en clase.*

Perfecto. Empezamos con la teoría.

---

## B1 — Qué es Devin, capacidades y limitaciones `[35 min — 15:40]`

*Pasar a diapositiva 3 — Copilot vs. Agente Autónomo.*

### Copilot vs agente autónomo

Llevamos años usando herramientas de asistencia al código. GitHub Copilot, ChatGPT, Cursor. Todas tienen algo en común: necesitan a un humano en el bucle para cada paso. Yo escribo, la herramienta sugiere, yo acepto o rechazo, yo ejecuto, yo leo el error, yo vuelvo a preguntar. El control sigue siendo mío en cada momento.

Devin es distinto en un aspecto fundamental: **puede ejecutar un ciclo completo de desarrollo sin que yo intervenga en cada paso**. Le doy una tarea, y él abre una terminal, lee el código, escribe cambios, ejecuta los tests, lee los errores, corrige, vuelve a ejecutar, y cuando considera que ha terminado, me entrega un resultado. Yo no tengo que estar mirando.

Eso tiene un nombre técnico: **agente autónomo**. Un agente es un sistema que percibe su entorno, toma decisiones y ejecuta acciones para alcanzar un objetivo, sin requerir instrucción humana en cada decisión intermedia.

La diferencia práctica es enorme. Con Copilot, si quiero que alguien arregle un bug, tengo que sentarme con él, describir el problema, copiar y pegar código, leer sugerencias, probar, volver a preguntar. El proceso sigue siendo mío. Con Devin, puedo escribirle "hay un bug en el endpoint de actualización de tareas, lee el código y corrígelo", y puedo irme a una reunión. Cuando vuelvo, tiene un PR preparado.

*Pausa de un segundo. Dejar que esto aterrice.*

Eso no significa que Devin sea mejor que vosotros. Significa que es un colaborador diferente, con un perfil diferente. Ahora vamos a ver cuál es ese perfil con honestidad.

### Capacidades reales

*Pasar a diapositiva 4 — Capacidades reales de Devin.*

Devin tiene cuatro capacidades que lo hacen útil en un contexto empresarial:

**Primera: leer y entender una codebase completa.** Cuando le das acceso a un repositorio, Devin no lee solo el archivo que le señalas. Navega el árbol de ficheros, lee la configuración, entiende las dependencias, traza las llamadas entre módulos. Es capaz de situarse en un proyecto desconocido con una velocidad que ningún desarrollador humano puede igualar, simplemente porque puede leer miles de líneas en segundos sin cansarse.

**Segunda: ejecutar y depurar.** Devin tiene acceso a una terminal real. Puede instalar paquetes, ejecutar tests, leer la salida de error, modificar el código, volver a ejecutar. Este ciclo lo hace solo, sin que yo tenga que copiar y pegar errores en un chat.

**Tercera: trabajar con contexto prolongado.** Mantiene el estado de la tarea a lo largo de docenas de pasos. Si en el paso 12 falla algo relacionado con una decisión tomada en el paso 3, puede retroceder y reconsiderar. Esto es muy distinto a un chat donde cada mensaje empieza casi desde cero.

**Cuarta: generar entregables completos.** No solo escribe código. Puede escribir los tests, actualizar la documentación, crear el PR con una descripción coherente y ejecutar la suite completa antes de entregarla.

### Limitaciones reales

*Pasar a diapositiva 5 — Limitaciones reales.*

*Esta parte es igual de importante. No pasarla rápido.*

Las limitaciones de Devin son reales y hay que conocerlas para no llevarse sorpresas en producción.

**Primera limitación: no tiene criterio de negocio.** Devin hace lo que le dices, no lo que necesitas. Si le pides que "mejore el rendimiento del endpoint de listado", puede añadir un índice en la base de datos, añadir caché, o simplemente añadir un parámetro de limit que no aplica. Las tres son "mejoras de rendimiento". Sin contexto de negocio preciso, Devin optimiza en la dirección que encuentra más obvia, que puede no ser la correcta.

**Segunda: se equivoca con lógica compleja.** En tareas de algorítmica no trivial, reglas de negocio entrelazadas o sistemas con muchos efectos laterales, la tasa de error de Devin sube. No es que no intente hacerlo bien; es que los errores de razonamiento sobre lógica compleja son el talón de Aquiles actual de los LLMs.

**Tercera: no puede reemplazar la revisión humana.** Todo lo que produce Devin tiene que pasar por code review. No como formalidad, sino porque comete errores sutiles: una condición invertida, un caso borde ignorado, una validación ausente. Veremos ejemplos de esto hoy.

**Cuarta: las instrucciones vagas producen resultados vagos.** Si el prompt es impreciso, Devin producirá algo que técnicamente responde al prompt pero que no es lo que querías. La calidad del output está directamente correlacionada con la calidad del input. Esto es una habilidad que hay que desarrollar.

*Hacer pausa aquí. Preguntar al grupo:* "¿Alguien ha usado ya Devin o algún agente similar en su trabajo? ¿Qué experiencia tuvo?" Escuchar una o dos respuestas, 1 minuto máximo.

### Casos de uso empresariales

*Pantalla: mantener diapositiva 5 o pasar a una pizarra en blanco. No hay slide específica para esto — hablar directamente.*

Los casos de uso donde Devin aporta más valor se agrupan en tres categorías.

**Deuda técnica y refactoring.** Cambiar nombres de variables en todo el repositorio, migrar una librería deprecated a su sucesor, convertir código síncrono a asíncrono en varios ficheros. Tareas que un desarrollador sénior haría bien pero que son lentas, mecánicas y aburridas. Devin las ejecuta rápido y con consistencia.

**Bugs bien definidos.** Si el bug está localizado y el comportamiento esperado está claro, Devin puede encontrarlo, corregirlo y añadir el test de regresión. El requisito es que alguien haya descrito bien el problema.

**Features pequeñas y repetitivas.** Añadir un nuevo endpoint que sigue el mismo patrón que los existentes, crear un nuevo campo en un modelo con su migración, añadir validaciones simples. Tareas donde el patrón ya existe en el repo y hay que replicarlo.

**Lo que no funciona bien:** arquitectura nueva desde cero, decisiones que requieren negociación con stakeholders, integraciones con APIs sin documentación clara, o cualquier tarea donde "el criterio" es más importante que "la ejecución".

---

## Caso real intercalado — Gumroad `[5 min — 16:15]`

*Pasar a diapositiva 6 — Caso real: Gumroad. Mostrar el post de Sahil Lavingia o la captura preparada.*

Voy a pausar un momento para hablar de un caso real que probablemente es el más citado cuando se habla de Devin en producción.

Gumroad es una plataforma de comercio electrónico para creadores de contenido. No es una startup de cinco personas, tiene millones de usuarios y una codebase activa. Su CEO, Sahil Lavingia, publicó en 2024 que Devin se había convertido en el mayor contribuidor al repositorio de Gumroad, con más de **1.500 pull requests fusionados**.

Para poner eso en perspectiva: 1.500 PRs es una cantidad que un equipo de cuatro desarrolladores tardaría años en producir. Devin los produjo en meses, trabajando en paralelo con el equipo humano.

¿Qué hacía Devin exactamente? Principalmente tres cosas: implementar features pequeñas que seguían patrones ya establecidos, corregir bugs reportados con descripción clara del comportamiento incorrecto, y escribir tests para código existente sin cobertura.

*Pasar a diapositiva 7 — Goldman Sachs y Visma.*

Goldman Sachs ha reportado reducciones de tiempo significativas en procesos de mesas de operaciones usando agentes de IA para tareas repetitivas de análisis y generación de código de soporte. Y Visma, empresa europea de software de gestión empresarial, reportó que había duplicado la productividad de algunos equipos de desarrollo tras integrar Devin en su flujo de trabajo.

Estos tres casos tienen algo en común: **ninguno eliminó desarrolladores, todos cambiaron qué hacen esos desarrolladores**. Eso es lo que tenéis que esperar si Devin entra en vuestros proyectos.

---

## B2 — Arquitectura interna de Devin `[25 min — 16:20]`

*Pasar a diapositiva 8 — Arquitectura interna: cómo planifica Devin.*

### Cómo planifica una tarea

Cuando le enviáis una tarea a Devin, lo primero que hace no es escribir código. Lo primero es **leer**. Devin explora el repositorio: estructura de carpetas, archivos de configuración, dependencias declaradas, tests existentes. Construye un modelo mental del proyecto antes de tocar nada.

A continuación **planifica en pasos**. Genera una lista de subtareas ordenadas: "primero necesito entender cómo funciona el endpoint X, luego identificar dónde se valida Y, luego modificar Z, luego ejecutar los tests para verificar". Esta planificación es visible en la interfaz de Devin, en tiempo real. Podéis ver cómo piensa.

*Pasar a diapositiva 9 — Las tres herramientas de Devin.*

### Las herramientas que usa Devin

Devin tiene acceso a tres herramientas principales que usa de forma coordinada.

**Terminal.** Puede ejecutar cualquier comando de shell. `git`, `pytest`, `pip install`, `curl`. Cuando un test falla, lee la salida de error y la usa para decidir el siguiente paso. Esto es lo que lo diferencia de un chatbot: no simula la ejecución, la hace de verdad.

**Editor de código.** Lee archivos completos, no fragmentos. Puede abrir varios archivos a la vez y cruzar información entre ellos. Cuando modifica código, lo hace directamente sobre el árbol de ficheros, no sobre un snippet aislado.

**Navegador.** Puede acceder a documentación online, leer páginas de referencia de librerías, consultar Stack Overflow si lo necesita. También puede interactuar con GitHub directamente: abrir el PR, leer los comentarios, añadir respuestas.

### Cómo itera cuando algo falla

*Mantener diapositiva 9.*

Cuando un test falla, Devin no para y te pregunta qué hacer. Lee el stack trace completo, identifica la línea exacta donde falla, vuelve al código, analiza la causa, modifica, vuelve a ejecutar. Este ciclo puede repetirse 10, 15, 20 veces en una tarea compleja. Cada iteración es una decisión autónoma.

Hay un límite. Si después de muchas iteraciones no encuentra la solución, puede bloquearse o producir una solución incorrecta. Cuando eso pasa, necesita un humano que le dé más contexto o que reencamine el prompt. El rol del desarrollador en ese momento es de supervisor, no de ejecutor.

*Hacer pausa y preguntar si hay preguntas sobre la arquitectura antes de pasar al tour de la interfaz.*

---

## Tour de la interfaz de Devin `[10 min — 16:45]`

*Pasar a diapositiva 10 — La interfaz de Devin: orientación rápida. Luego abrir devin.ai en el navegador para mostrar en vivo.*

Antes de ver la demo, vamos a hacer un recorrido rápido por la interfaz para que sepáis dónde está cada cosa. Cuando empiece la demo y la actividad no quiero que estéis pendientes de encontrar botones.

*Mostrar la diapositiva con los 5 bloques y luego abrir la app en vivo para señalar cada sección.*

El panel lateral izquierdo tiene cinco secciones y siempre está visible:

**Sessions** — es el punto de entrada principal. Aquí es donde lanzáis las tareas a Devin. El campo central es donde escribís el prompt. Abajo veis los repositorios que tenéis conectados.

**Ask** — modo consulta rápida. No ejecuta tareas ni modifica código. Solo responde preguntas sobre vuestra codebase. Muy útil para entender un proyecto desconocido antes de delegar trabajo.

**Wiki (DeepWiki)** — genera documentación automática de vuestros repositorios. Lo veremos en más detalle en sesiones posteriores.

**Review** — pegáis la URL de cualquier PR de GitHub y Devin lo analiza y revisa. Esto es exactamente lo que vamos a hacer en la demo ahora mismo.

**Automations (Beta)** — triggers automáticos: arreglar CIs fallidos, responder a issues de GitHub con `/devin`, triaje de bugs en Slack. No lo vamos a tocar en este curso pero vale la pena saber que existe.

*Señalar en la app en vivo mientras se explica cada sección.*

El panel central cambia según la sección en la que estéis. Cuando abráis una sesión veréis el plan de ejecución de Devin en tiempo real, la terminal, el editor y el navegador según lo que esté haciendo en cada momento.

Perfecto. Con esto ubicados, vamos a la demo.

---

## Demo en vivo `[25 min — 16:55]`

*Pantalla: cambiar a la sección Review de Devin o abrir una nueva sesión en Sessions.*

Ahora vamos a ver esto en funcionamiento real. Voy a conectar Devin al repositorio y pedirle que analice el PR #1, que contiene bugs de validación que introdujimos deliberadamente para este ejercicio.

### Paso 1 — Revisar el PR antes de llamar a Devin `[3 min]`

*Mostrar el PR en GitHub. Navegar a la pestaña "Files changed".*

Primero voy a mostrarles el PR tal como lo vería cualquier revisor humano. El título es "bug: validaciones de negocio ausentes en tareas" y el cambio está en `aplicacion/rutas/tareas.py`.

*Mostrar el diff. Señalar específicamente:*
- El endpoint `create_task` no tiene ninguna validación de longitud de título.
- El endpoint `update_task` tiene una comprobación de estado, pero está mirando `payload.status` en lugar de `task.status`. La condición bloquea el caso equivocado.

Un revisor humano puede tardar varios minutos en detectar esto, especialmente la segunda parte, que es sutil. Vamos a ver qué hace Devin.

### Paso 2 — Abrir Devin y conectar el repo `[3 min]`

*Cambiar a Devin. Usar la sección Review o Sessions según lo que sea más claro en vivo.*

Abro Devin. Lo primero que hago es asegurarme de que el repositorio `gestor-tareas-api` está conectado. Podéis ver aquí abajo que aparece entre los repos disponibles.

*Mostrar el proceso de conectar el repo si no está ya conectado.*

### Paso 3 — Escribir el prompt inicial `[2 min]`

*Escribir el siguiente prompt despacio para que los alumnos puedan leerlo:*

```
Analiza el PR #1 del repositorio gestor-tareas-api. Este PR
introduce dos bugs de validación en el archivo
aplicacion/rutas/tareas.py.

Tu tarea es:
1. Identificar exactamente qué validaciones faltan o están
   mal implementadas.
2. Explicar en qué escenario concreto falla cada bug (qué
   petición HTTP produce el comportamiento incorrecto).
3. Proponer el código corregido para cada caso.

No hagas cambios en el repositorio todavía. Solo análisis
y propuesta.
```

*Enviar. Mientras Devin empieza a trabajar, comentar al grupo:*

Fijaos en el prompt. He sido muy específico en tres cosas: qué tiene que hacer (identificar, explicar, proponer), qué no tiene que hacer (no modificar nada), y en qué fichero buscar. Cuanto más acotado es el prompt, más útil es la respuesta.

### Paso 4 — Leer y comentar la respuesta de Devin `[10 min]`

*Esperar a que Devin complete el análisis. Leer la respuesta resumiendo, no literalmente.*

Devin ha encontrado los dos problemas. Vamos a ver qué dice sobre cada uno.

*Mostrar la parte de la respuesta sobre el primer bug:*

Sobre el primero, Devin identifica que `create_task` acepta un título de cualquier longitud, incluyendo un string vacío o de un carácter. Propone añadir una validación antes de persistir, devolviendo un 422 si `len(payload.title) < 3`.

*Mostrar la parte sobre el segundo bug:*

El segundo es más interesante. Devin detecta que la condición `if payload.status == TaskStatus.done` comprueba lo que el cliente quiere *poner*, no lo que la tarea *es* actualmente. Lo que queremos bloquear es modificar una tarea que ya está en `done`. La condición correcta sería `if task.status == TaskStatus.done`.

Este segundo bug es exactamente el tipo de error sutil que cuesta detectar en code review porque la lógica *parece* correcta a primera vista. Hay un `if`, hay una comparación, hay un `raise`. Pero la variable equivocada. Devin lo detectó leyendo el código completo, no solo la línea modificada.

### Paso 5 — Pedir el código corregido `[5 min]`

*Enviar un segundo mensaje a Devin:*

```
Perfecto. Ahora escribe el código corregido para la función
update_task con la validación de estado correcta. Incluye
también el test pytest que verifica que una tarea con estado
"done" no puede modificarse.
```

*Mostrar la respuesta con el código propuesto. Señalar los cambios clave sin leerlos todos.*

Aquí está la corrección. Podéis ver que ha corregido la variable en `update_task` y ha añadido el test correspondiente. En un flujo real, ahora haría code review de esta propuesta y si es correcta, dejaría que Devin abra el PR.

---

## DESCANSO `[20 min — 17:20]`

*Anunciar el descanso claramente. Decir la hora exacta de regreso.*

Hacemos 20 minutos de descanso. Volvemos a las 17:40. Cuando regresemos vosotros vais a hacer lo que acabo de hacer yo.

---

## Actividad 1 — Identificar los bugs con Devin `[15 min — 17:40]`

*Pasar a diapositiva 12 — Actividad: tú con Devin.*

**Objetivo:** Usar Devin para identificar los dos bugs del PR #1 con vuestro propio prompt, sin copiar el del formador.

**Pasos:**
1. Abrid Devin y cread una nueva sesión.
2. Conectad el repositorio `gestor-tareas-api` y aseguraos de que el PR #1 está visible.
3. Escribid vuestro propio prompt para pedirle a Devin que analice el PR y encuentre los problemas.
4. Anotad si Devin encontró los dos bugs y si describió correctamente el escenario de fallo de cada uno.
5. Si no los encontró en el primer intento, refinad el prompt y volved a intentarlo.

**Criterio de éxito:** Devin identifica que `create_task` no valida la longitud del título y que `update_task` comprueba `payload.status` en lugar de `task.status`.

*Mientras los alumnos trabajan, observar qué prompts usan. No dar pistas a menos que alguien lleve más de 5 minutos completamente bloqueado.*

---

## Actividad 2 — Pedir la corrección a Devin `[15 min — 17:55]`

**Objetivo:** Pedirle a Devin el código corregido para uno de los dos bugs y evaluar si la propuesta es correcta.

**Pasos:**
1. En la misma sesión de Devin, escribid un segundo prompt pidiendo el código corregido para el bug que prefiráis.
2. Evaluad la propuesta: ¿es técnicamente correcta? ¿Incluye el test de regresión?
3. Si la propuesta no es correcta o está incompleta, ajustad el prompt y pedid una revisión.

**Solución esperada para el formador al validar:**

*Bug 1 — Validación de longitud ausente en `create_task`:*
```python
if len(payload.title) < 3:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="El título debe tener al menos 3 caracteres",
    )
```
El test verifica que `POST /tasks/` con `{"title": "AB"}` devuelve 422.

*Bug 2 — Condición invertida en `update_task`:*
```python
# Incorrecto (bug):
if payload.status == TaskStatus.done:
# Correcto:
if task.status == TaskStatus.done:
```
El test verifica que un `PATCH` sobre una tarea con `status: done` devuelve 400.

---

## Puesta en común `[10 min — 18:10]`

*Volver a pantalla compartida. Lanzar las preguntas una a una.*

Vamos a poner en común lo que habéis encontrado. Quiero respuestas concretas.

**Pregunta 1:** ¿Cuántos encontrasteis los dos bugs en el primer intento? ¿Quién necesitó refinar el prompt? ¿Qué cambiasteis?

*Recoger respuestas. Pedir a alguien que refinó que explique qué cambió en su segundo prompt.*

**Pregunta 2:** Comparad vuestro prompt con el mío. ¿Cuál fue más específico? ¿Eso hizo que Devin fuera más preciso?

*Buscar diferencias concretas: si alguien fue más vago, si alguien fue más específico, si alguien añadió contexto que yo no añadí.*

**Pregunta 3:** Para los que encontrasteis el bug número 2 (la condición invertida), ¿la descripción de Devin fue suficientemente clara para que alguien que no conoce el repo la entienda?

**Pregunta 4:** ¿Alguien probó un prompt muy general, tipo "encuentra los bugs en este PR"? ¿Qué pasó?

*Si nadie lo probó, comentar qué suele pasar: Devin tiende a dar un análisis superficial o a enumerar posibles mejoras de estilo en lugar de localizar bugs de lógica específicos.*

---

## Cierre y preview de la sesión 2 `[10 min — 18:20]`

*Pasar a diapositiva 13 — Qué aprendimos hoy.*

Vamos a cerrar. Lo que hemos visto hoy se resume en tres ideas.

**Primera:** Devin no es Copilot con esteroides. Es una categoría diferente de herramienta. Copilot os ayuda a escribir. Devin puede ejecutar. Esa diferencia cambia cómo lo usáis y qué tipo de tareas le dais.

**Segunda:** la calidad de vuestro prompt determina la calidad del resultado. No adivina intenciones. Lo que le dais es lo que aprovecha. Hoy habéis visto la diferencia entre un prompt específico y uno vago.

**Tercera:** Devin comete errores. La revisión humana no es opcional. Lo que cambia es dónde enfocáis esa revisión: en el criterio, la arquitectura, las decisiones de negocio, no en la mecánica de escritura.

En la **sesión 2** trabajaremos los bloques B3 y B4: configurar el entorno sandbox de Devin con los permisos adecuados, conectar vuestro propio repositorio y ejecutar las primeras tareas reales de principio a fin — desde el prompt hasta el PR generado por Devin. Traed el repo clonado y la cuenta de Devin activa.

Hasta la próxima.
