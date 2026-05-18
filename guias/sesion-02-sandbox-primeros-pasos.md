# Sesión 02 — Sandbox y Primeros Pasos Reales

**Duración total:** 3 horas (incluyendo 20 min de descanso)
**Audiencia:** Desarrolladores de Softtek de distintos lenguajes y seniorities
**Formato:** Virtual · Cisco WebEx
**Presentación Gamma:** `https://gamma.app/docs/Devin-AI-zlgv58n04eckzbd`

---

## Objetivos de aprendizaje

Al terminar esta sesión el alumno será capaz de:

1. Configurar su propio fork del repositorio del curso con todas las ramas de escenario.
2. Conectar su fork a Devin y verificar el acceso al repositorio.
3. Explicar qué es el sandbox de Devin, qué permisos controla y qué límites tiene.
4. Escribir un prompt eficaz con contexto, comportamiento actual, comportamiento esperado y restricciones.
5. Delegar una tarea real de corrección de código a Devin y evaluar el PR resultante.

---

## Materiales necesarios antes de empezar

Antes de que lleguen los alumnos, tener abierto y listo:

- **Presentación de Gamma** abierta en el navegador: `https://gamma.app/docs/Devin-AI-zlgv58n04eckzbd`
- **Devin** abierto en `app.devin.ai` con el repo `gestor-tareas-api` conectado y acceso a GitHub autorizado
- **GitHub** con el PR #1 de `gestor-tareas-api` abierto en otra pestaña
- **VS Code** con `aplicacion/rutas/tareas.py` abierto para mostrar el código durante la demo
- **El script de configuración** preparado para compartir por chat del WebEx en cuanto empiece la sesión

*Nota: avisar a los alumnos con 24 horas de antelación que traigan su fork configurado si pudieron hacerlo antes. Si no, la configuración se hace al inicio de la sesión.*

---

## Timing general

| Bloque | Duración | Hora inicio | Hora fin |
|---|---|---|---|
| Apertura + configuración del fork | 25 min | 15:30 | 15:55 |
| B3 — El sandbox de Devin | 20 min | 15:55 | 16:15 |
| B4 — Flujo de trabajo y prompts eficaces | 25 min | 16:15 | 16:40 |
| Demo en vivo | 25 min | 16:40 | 17:05 |
| **DESCANSO** | **20 min** | **17:05** | **17:25** |
| Actividad 1 — Plan sin tocar código | 10 min | 17:25 | 17:35 |
| Actividad 2 — Prompt básico | 15 min | 17:35 | 17:50 |
| Actividad 3 — Prompt detallado | 15 min | 17:50 | 18:05 |
| Actividades 4 y 5 — Review | 10 min | 18:05 | 18:15 |
| Puesta en común y cierre | 15 min | 18:15 | 18:30 |

---

## Apertura y configuración del fork `[25 min — 15:30]`

*Pantalla: diapositiva 1 — portada. Luego pasar a diapositiva 2 — índice.*

Buenas tardes a todos. En la sesión anterior vimos qué es Devin y cómo razona. Hoy dejamos de observar y empezamos a ejecutar — Devin va a trabajar en vuestro propio repositorio.

Antes de la teoría vamos a hacer la configuración. Es lo primero porque si lo dejamos para después perdemos tiempo de práctica.

*Pasar a diapositiva 3 — Configuración previa.*

Tenéis que hacer cuatro cosas. Las hacemos juntos en orden.

### Paso 1 — Fork del repositorio `[5 min — 15:30]`

*Compartir pantalla mostrando GitHub. Navegar a `github.com/jmojpar/gestor-tareas-api`.*

Entrad en esta URL. Arriba a la derecha veis el botón **Fork**. Hacéis clic, dejáis todo por defecto y confirmáis. En 10 segundos tenéis una copia del repositorio en vuestra cuenta de GitHub.

*Esperar a que todos hagan el fork. Resolver dudas.*

### Paso 2 — Script de ramas `[10 min — 15:35]`

*Compartir el script por el chat del WebEx. Mostrar en pantalla la diapositiva 3 con el bloque de código.*

Abrid una terminal en vuestra máquina, id a la carpeta donde queráis trabajar y ejecutad este script. Solo tenéis que sustituir `USUARIO` por vuestro nombre de GitHub en la primera línea — el resto funciona igual para todos.

```
git clone https://github.com/jmojpar/gestor-tareas-api.git
cd gestor-tareas-api
git remote set-url origin https://github.com/USUARIO/gestor-tareas-api.git
git remote add upstream https://github.com/jmojpar/gestor-tareas-api.git
git fetch upstream
git push origin main
git push origin refs/remotes/upstream/escenario-1-bug-logico:refs/heads/escenario-1-bug-logico
git push origin refs/remotes/upstream/escenario-2-sin-tests:refs/heads/escenario-2-sin-tests
git push origin refs/remotes/upstream/escenario-3-codigo-duplicado:refs/heads/escenario-3-codigo-duplicado
git push origin refs/remotes/upstream/escenario-4-sin-documentacion:refs/heads/escenario-4-sin-documentacion
git push origin refs/remotes/upstream/escenario-5-endpoint-roto:refs/heads/escenario-5-endpoint-roto
```

*Mientras los alumnos ejecutan el script, explicar qué hace cada línea:*

La primera clona el repositorio del curso. La segunda entra en la carpeta. La tercera redirige el destino de los push a vuestro fork en lugar del repo original. La cuarta añade el repo del curso como fuente secundaria. El `git fetch upstream` descarga todas las ramas del curso. Y los push finales copian cada rama de escenario a vuestro fork.

*Esperar a que todos terminen. Si alguien tiene error, pedir que lo comparta por chat para no detener al grupo.*

### Paso 3 — Abrir los 5 PRs `[5 min — 15:45]`

*Mostrar en GitHub cómo abrir un PR desde el banner amarillo.*

Ahora entrad en vuestro fork en GitHub — `github.com/USUARIO/gestor-tareas-api`. Veréis banners amarillos para algunas ramas. Para las que no aparezcan, usad la URL directa:

`github.com/USUARIO/gestor-tareas-api/compare/main...nombre-de-la-rama`

Abrid un PR por cada una de las 5 ramas contra `main`. Los títulos y descripciones pueden ser breves — lo importante es que estén abiertos.

*Dar 3 minutos. No hace falta que sean perfectos, solo que existan.*

### Paso 4 — Conectar el fork en Devin `[5 min — 15:50]`

*Mostrar en Devin el proceso de conectar un repo.*

Abrid Devin. En el panel de nueva sesión, en el selector de repositorios, buscad vuestro fork `USUARIO/gestor-tareas-api`. Si es la primera vez que conectáis GitHub, os pedirá que autoricéis el acceso — aceptáis. Una vez conectado ya podéis seleccionar el repo.

*Verificar que todos tienen su fork visible en Devin antes de continuar.*

Una aclaración importante: Devin no tiene un interruptor de "solo lectura" o "escritura". Lo que controla si Devin modifica código o no sois vosotros a través del prompt. Si le decís que analice y no toque nada, no toca nada. Si le decís que corrija y abra un PR, lo hace. Hoy vais a pedirle las dos cosas en distintas actividades.

Perfecto. Tenéis el entorno listo. Ahora entramos en la teoría.

---

## B3 — El sandbox de Devin `[20 min — 15:55]`

*Pasar a diapositiva 4 — El entorno de trabajo de Devin.*

### Qué es el sandbox

Cuando Devin ejecuta una tarea no lo hace en vuestra máquina. Trabaja en un entorno virtual propio que se llama sandbox. Cada vez que abrís una sesión, Devin arranca en un contenedor limpio, con acceso solo a lo que vosotros le hayáis dado acceso, y sin memoria de sesiones anteriores.

Eso tiene tres consecuencias prácticas.

La primera es que lo que hace Devin no afecta a vuestra máquina local bajo ninguna circunstancia. Si comete un error gordo en el repositorio, lo veis en el PR antes de que llegue a ningún sitio. No hay daño directo.

La segunda es que vosotros controlais el acceso. Devin solo puede ver y tocar los repositorios que le habéis conectado explícitamente. No puede explorar vuestra cuenta de GitHub ni acceder a repos que no le hayáis dado.

La tercera es que cada sesión parte de cero. Devin no recuerda lo que le dijisteis en la sesión anterior. Si empezáis una sesión nueva, tenéis que darle el contexto desde el principio.

*Pasar a diapositiva 5 — Lectura vs Escritura.*

### El control es vuestro — a través del prompt

En la sesión 1 conectasteis el repositorio del curso y solo le pedisteis a Devin análisis — que identificara bugs, que propusiera correcciones, pero sin implementar nada. Hoy vais a pedirle que corrija código y abra PRs. La diferencia no está en ningún permiso de la interfaz, está en lo que le pedís.

Devin no tiene un selector de "solo lectura" o "escritura". Lo que controla su comportamiento es el prompt. Si le decís "analiza pero no toques nada", no toca nada. Si le decís "corrígelo y abre un PR", lo hace.

La regla práctica es simple: sed explícitos en el prompt sobre qué puede y qué no puede hacer. Si no queréis que modifique nada, decidlo. Si queréis que abra el PR, decidlo. No asumáis que Devin infiere vuestras intenciones.

*Pasar a diapositiva 6 — Lo que Devin no puede hacer.*

### Límites que protegen vuestro código

Hay cuatro cosas que Devin nunca hace, independientemente de los permisos que le deis.

**No hace merge directo.** Siempre abre un PR. Nunca fusiona código sin vuestra aprobación explícita. Eso significa que tenéis siempre la última palabra antes de que cualquier cambio llegue a `main`.

**No accede a secretos.** Variables de entorno, credenciales, tokens de API — Devin no tiene acceso a nada de eso. No los busca, no los lee, no los usa.

**Solo accede a repos autorizados.** No puede explorar vuestra cuenta ni entrar en repositorios que no hayáis conectado.

**Cada sesión es independiente.** No hay memoria entre sesiones. Cada vez que abrís una sesión nueva, Devin empieza sin ningún contexto previo.

*Pausa. Preguntar al grupo si hay preguntas sobre el sandbox antes de continuar.*

---

## B4 — Flujo de trabajo y prompts eficaces `[25 min — 16:15]`

*Pasar a diapositiva 7 — Flujo completo de una sesión.*

### Los cuatro pasos de una sesión

Trabajar con Devin siempre sigue el mismo ciclo: conectar, instruir, supervisar y revisar. En ese orden. Saltarse cualquiera de los cuatro crea problemas.

**Conectar.** Seleccionáis el repositorio y la rama de trabajo antes de escribir nada. Devin necesita saber sobre qué código está trabajando desde el principio.

**Instruir.** Escribís el prompt. Esta es la parte más importante — y también la que más subestima la gente. El prompt no es un comentario informal, es una especificación. Cuanto más preciso, mejor el resultado.

**Supervisar.** Una vez enviado el prompt, Devin genera un plan de subtareas visible en tiempo real. Podéis ver cómo razona, qué archivos lee, qué comandos ejecuta. Si el plan no va en la dirección correcta podéis intervenir antes de que termine.

**Revisar.** Cuando Devin termina, abre un PR. Vosotros lo revisáis antes de aprobarlo. Siempre. No es opcional. Devin comete errores — ya lo vimos en la sesión 1 — y la revisión del PR es el último filtro antes de que ese código llegue a producción.

*Hacer pausa. Señalar la advertencia de la diapositiva:*

El error más común que comete la gente que empieza a usar Devin es aprobar el PR sin leerlo. Especialmente cuando la tarea parece sencilla. Eso es exactamente cuando más te sorprende.

*Pasar a diapositiva 8 — El prompt determina el resultado.*

### Cómo escribir un prompt eficaz

Un prompt eficaz para Devin tiene cuatro elementos. Si falta alguno, la calidad del resultado baja.

**Contexto.** Dónde está el problema. Qué archivo, qué función, qué parte de la codebase afecta. Devin puede encontrarlo solo, pero si se lo dais directamente ahorrái iteraciones.

**Comportamiento actual.** Qué hace el código ahora mismo. El síntoma concreto, no la causa. "El endpoint devuelve 200 aunque el título tenga un carácter" es mejor que "falta una validación".

**Comportamiento esperado.** Qué debería hacer. El criterio de aceptación. Cuanto más específico, más fácil para Devin validar que su solución es correcta.

**Restricciones.** Qué no debe tocar. Qué convenciones debe respetar. Si no queréis que Devin modifique otros endpoints, decidlo. Si tiene que seguir el patrón de tests existente, decidlo.

*Señalar los dos ejemplos de la diapositiva. Leer el débil primero.*

"Arregla el bug del endpoint de tareas." Esto le llega a Devin sin contexto, sin síntoma, sin criterio de aceptación. Puede hacer cualquier cosa y técnicamente habrá respondido al prompt.

*Leer el fuerte.*

"En `update_task`, la condición comprueba `payload.status` en lugar de `task.status`. Corrígelo para que bloquee modificaciones sobre tareas con status `done`. Añade un test pytest que verifique que un PATCH sobre una tarea `done` devuelve 400. No modifiques otros endpoints."

Este prompt le dice exactamente qué está mal, por qué es incorrecto, qué debe producir y qué no debe tocar. El margen de error se reduce drásticamente.

---

## Demo en vivo `[25 min — 16:40]`

*Pantalla: abrir Devin en Sessions con el repo `gestor-tareas-api` seleccionado.*

Ahora vamos a ver esto en funcionamiento. Voy a pedirle a Devin que corrija el bug #1 — la validación de longitud del título en `create_task` — y que incluya el test pytest correspondiente. No le voy a decir qué línea cambiar. Solo le voy a dar el contexto, el síntoma y el criterio.

### Paso 1 — Revisar el código antes de llamar a Devin `[3 min]`

*Cambiar a VS Code. Mostrar `aplicacion/rutas/tareas.py`, función `create_task`.*

Primero revisamos el código. Aquí está `create_task`. Recibimos el payload, creamos la tarea directamente y la persistimos. No hay ninguna validación del título antes de guardarlo. Si alguien envía un título de un carácter, se guarda sin error.

Eso es exactamente lo que vamos a pedirle a Devin que corrija.

### Paso 2 — Escribir el prompt `[3 min]`

*Cambiar a Devin. Escribir el prompt despacio en el campo de Sessions.*

```
En el archivo aplicacion/rutas/tareas.py, la función
create_task no valida la longitud del título antes de
persistir la tarea. Actualmente acepta títulos de cualquier
longitud, incluyendo strings vacíos o de un solo carácter.

Corrígelo para que devuelva un error 422 si el título tiene
menos de 3 caracteres. Añade un test pytest en
tests/test_tasks.py que verifique que POST /tasks/ con un
título de 2 caracteres devuelve 422.

No modifiques ningún otro endpoint ni ningún otro archivo
fuera de los dos mencionados.
```

*Enviar. Mientras Devin empieza a procesar, comentar:*

Fijaos en la estructura. Contexto — qué archivo y qué función. Comportamiento actual — acepta títulos de cualquier longitud. Comportamiento esperado — 422 si menos de 3 caracteres. Restricciones — no tocar nada más.

### Paso 3 — Supervisar la ejecución `[8 min]`

*Observar el panel de Devin en tiempo real. Comentar lo que va pasando.*

Veréis que Devin empieza generando un plan. Lee el archivo, identifica la función, decide dónde insertar la validación. A continuación modifica el código, ejecuta los tests existentes para verificar que no ha roto nada, escribe el test nuevo y lo ejecuta también.

*Señalar cada paso mientras ocurre. No hace falta leer todo — comentar lo más relevante.*

Fijaos que está ejecutando los tests después de cada cambio. No asume que su modificación es correcta. Verifica. Ese ciclo — modificar, ejecutar, leer resultado, corregir si hace falta — es lo que hace Devin autónomamente.

### Paso 4 — Revisar el PR `[8 min]`

*Cuando Devin termine, ir al PR en GitHub.*

Devin ha abierto el PR. Vamos a revisarlo juntos como haríais en un code review real.

*Mostrar la pestaña "Files changed". Señalar los cambios.*

Aquí está la validación añadida en `create_task`. Comprobad que la condición es correcta — `len(payload.title) < 3` — y que el error es 422 y no otro código.

*Mostrar el test añadido.*

Y aquí el test. Verificad que llama al endpoint con un título de 2 caracteres y que el assert comprueba el código 422. Si el test es correcto, la validación está cubierta.

*Señalar si hay algo que mejorar o si está listo para aprobar.*

Este PR yo lo aprobaría. La corrección es correcta, el test cubre el caso, y no ha tocado nada fuera de lo que le pedí.

*Nota para el formador: si Devin comete algún error durante la demo, no es un problema — es una oportunidad. Mostrar el error, explicar por qué está mal y refinar el prompt en vivo. Es más didáctico que una demo perfecta.*

---

## DESCANSO `[20 min — 17:05]`

*Anunciar el descanso claramente.*

Hacemos 20 minutos. Volvemos a las 17:25. En la segunda parte sois vosotros con Devin.

---

## Actividad 1 — Pide el plan, no la solución `[10 min — 17:25]`

*Pasar a diapositiva 10 — Actividad 1.*

**Objetivo:** Pedirle a Devin que describa cómo corregiría el bug #2 de vuestro fork — la condición invertida en `update_task` — sin implementar ningún cambio todavía.

**Pasos:**
1. Abrid una nueva sesión en Devin con vuestro fork conectado.
2. Escribid un prompt pidiendo el **plan de corrección** para el PR `escenario-1-bug-logico` de vuestro fork. Pedid solo el análisis y la propuesta, no la implementación.
3. Evaluad si Devin identifica correctamente la condición invertida y propone el cambio correcto.

**Criterio de éxito:** Devin explica que la condición debe comparar `task.status` en lugar de `payload.status` y propone el código corregido sin haberlo implementado.

*No dar pistas mientras trabajan. Si alguien no avanza en 3 minutos, sugerir que incluya el nombre del archivo en el prompt.*

---

## Actividad 2 — Corrección con prompt básico `[15 min — 17:35]`

*Pasar a diapositiva 11 — Actividades 2 y 3.*

**Objetivo:** Pedirle a Devin que corrija el bug de la condición invertida con un prompt de una sola línea. Observar qué PR genera.

**Pasos:**
1. En una nueva sesión de Devin, escribid un prompt de una sola línea pidiendo que corrija el bug en `update_task`.
2. Dejad que Devin trabaje y revisad el PR resultante.
3. Anotad: ¿encontró el bug correcto? ¿El PR es aprobable? ¿Qué le falta?

**Solución esperada para el formador al validar:**

El PR correcto debe cambiar esta línea en `update_task`:
```python
# Incorrecto (bug):
if payload.status == TaskStatus.done:

# Correcto:
if task.status == TaskStatus.done:
```

Si el PR no incluye el test de regresión, el prompt básico ha fallado en ese aspecto. Eso es exactamente el punto de comparación con la actividad 3.

---

## Actividad 3 — Corrección con prompt detallado `[15 min — 17:50]`

**Objetivo:** Repetir la corrección con un prompt que incluya los cuatro elementos — contexto, comportamiento actual, comportamiento esperado y restricciones. Comparar el PR con el de la actividad 2.

**Pasos:**
1. Abrid una nueva sesión de Devin (no continuéis la anterior).
2. Escribid un prompt detallado con los cuatro elementos para corregir el mismo bug.
3. Revisad el PR y comparadlo con el anterior.

**Guía para construir el prompt detallado:**

```
En aplicacion/rutas/tareas.py, la función update_task
comprueba payload.status == TaskStatus.done en lugar de
task.status == TaskStatus.done. Esto permite modificar
tareas que ya tienen estado done porque la condición
comprueba lo que el cliente intenta poner, no el estado
actual de la tarea.

Corrígelo para que devuelva 400 si task.status es done
antes de aplicar cualquier cambio. Añade un test pytest
que verifique que un PATCH sobre una tarea con status done
devuelve 400. No modifiques otros endpoints ni otros
archivos.
```

*No compartir este prompt con los alumnos — es la solución de referencia para el formador. Los alumnos deben construir el suyo.*

---

## Actividades 4 y 5 — Devin como revisor `[10 min — 18:05]`

*Pasar a diapositiva 12 — Actividades 4 y 5.*

**Objetivo:** Usar la sección Review de Devin para analizar PRs sin ejecutar ningún cambio.

**Actividad 4 — PR de código duplicado `[5 min]`**

1. Abrid la sección **Review** en Devin (panel lateral izquierdo).
2. Pegad la URL del PR `escenario-3-codigo-duplicado` de vuestro fork.
3. Preguntad a Devin: *"¿Cuál es el problema principal de este PR y cómo lo refactorizarías?"*
4. Verificad que Devin identifica el bloque duplicado y propone la función `get_task_or_404`.

**Actividad 5 — PR de endpoint roto `[5 min]`**

1. En la misma sección Review, pegad la URL del PR `escenario-5-endpoint-roto`.
2. Preguntad a Devin: *"¿En qué escenario concreto falla este endpoint y por qué?"*
3. Verificad que Devin identifica que el filtro usa `!=` en lugar de `==` y que el parámetro `limit` nunca se aplica.

*Señalar la diferencia entre Sessions y Review: en Sessions Devin ejecuta y modifica, en Review solo analiza y opina. Para análisis rápidos sin riesgo, Review es más eficiente.*

---

## Puesta en común y cierre `[15 min — 18:15]`

*Volver a pantalla compartida. Lanzar las preguntas una a una.*

### Puesta en común

**Pregunta 1:** Comparad los dos PRs de las actividades 2 y 3. ¿Cuál aprobarías sin modificaciones? ¿Qué tiene el segundo que no tiene el primero?

*Buscar respuestas concretas: test de regresión, descripción del PR, calidad de la corrección.*

**Pregunta 2:** En la actividad 1, ¿Devin describió el plan correctamente antes de implementar? ¿Fue útil pedir el plan primero o perdisteis tiempo?

**Pregunta 3:** En Review, ¿la descripción de Devin del problema del código duplicado fue suficientemente clara para entenderla sin mirar el código?

**Pregunta 4:** ¿Cuántas iteraciones necesitó Devin para llegar al PR final en las actividades 2 y 3? ¿El prompt más detallado redujo las iteraciones?

### Cierre

*Pasar a diapositiva 13 — Qué aprendimos hoy.*

Lo de hoy se resume en tres ideas.

**Primera:** el sandbox os protege — Devin trabaja en un entorno aislado y nunca hace merge sin vuestra aprobación. Pero lo que controla si escribe código o no sois vosotros a través del prompt. Sed explícitos en cada instrucción sobre qué puede y qué no puede hacer.

**Segunda:** el prompt es el trabajo. Escribir una instrucción con contexto, comportamiento actual, comportamiento esperado y restricciones no es burocracia — es la diferencia entre un PR que aprobáis directamente y uno que reescribís entero. Lo habéis comprobado hoy comparando los dos.

**Tercera:** Sessions y Review son herramientas distintas con propósitos distintos. Sessions para ejecutar, Review para analizar. Saber cuándo usar cada una define cómo integrais Devin en vuestro flujo sin fricción.

En la **sesión 3** trabajaremos el bloque B5: flujo de trabajo con PRs — cómo delegar code review a Devin, cómo pedirle que proponga refactors sobre código existente, y cómo validar su output antes de aprobar. Usaremos el PR de código duplicado que hoy solo analizasteis — en la sesión 3 Devin lo corrige de verdad.

Hasta la próxima.
