# Diseño de arquitectura segura y políticas de firewall


---

## Objetivo

Analizar un escenario empresarial y diseñar una política de firewall que proteja una red corporativa. El objetivo es identificar los servicios necesarios, definir zonas de seguridad y proponer reglas de filtrado adecuadas.

---

## 1. Descripción del escenario

La infraestructura de partida presenta un problema crítico: todos los servidores comparten el mismo segmento de red conectado a Internet. Si un atacante compromete el servidor web público, tiene acceso directo a la base de datos interna sin ninguna barrera adicional.

Para corregir esto se propone una arquitectura segmentada en tres zonas separadas por un firewall.

---

## 2. Zonas de seguridad

**Zona WAN (Internet):** representa el exterior de la organización. Nivel de confianza nulo. Cualquier IP de Internet que intente acceder a los servicios públicos corporativos parte de esta zona.

**Zona DMZ (Zona Desmilitarizada):** subred aislada que actúa como escaparate de la empresa. Los servidores aquí ubicados son accesibles desde Internet pero no pueden iniciar conexiones hacia la red interna. Contiene el servidor web (Apache/Nginx) y el servidor de correo (Postfix/Dovecot).

**Zona LAN (Red interna):** contiene los activos más valiosos y no tiene acceso directo desde Internet. Aquí se encuentra la base de datos (MySQL/PostgreSQL) y los equipos de los empleados.

---

## 3. Matriz de reglas de firewall

La política base es *default deny*: todo el tráfico no explícitamente permitido queda bloqueado. Las excepciones necesarias para el funcionamiento de los servicios son las siguientes:

| ID | Origen | Destino | Puerto / Protocolo | Acción | Justificación |
|---|---|---|---|---|---|
| R1 | WAN | Web (DMZ) | 443/TCP (HTTPS) | Permitir | Tráfico web público cifrado hacia la página corporativa |
| R2 | WAN | Correo (DMZ) | 25/TCP (SMTP) | Permitir | Recepción de correos desde otros servidores de Internet |
| R3 | WAN | Correo (DMZ) | 587, 993/TCP | Permitir | Envío autenticado y lectura segura de correo por parte de los clientes |
| R4 | Web (DMZ) | BBDD (LAN) | 3306/TCP (MySQL) | Permitir | El backend de la web necesita consultar la base de datos interna |
| R5 | LAN | WAN | 80, 443/TCP | Permitir | Navegación de los empleados hacia Internet |
| R6 | WAN | BBDD (LAN) | Cualquiera | Bloquear | Previene la exposición directa de la base de datos al exterior |
| R7 | DMZ | LAN | Cualquiera (excepto R4) | Bloquear | Evita el movimiento lateral si un servidor de la DMZ es comprometido |
| R8 | Cualquiera | Cualquiera | Cualquiera | Bloquear | Política default deny |

---

## 4. Conclusión

El diseño transforma una arquitectura plana y vulnerable en un entorno de defensa en profundidad. La DMZ garantiza que, en el peor caso, un atacante que comprometa el servidor web quede aislado en esa subred sin posibilidad de acceder a la base de datos interna. Esta arquitectura es el estándar habitual para cualquier infraestructura que necesite exponer servicios públicos manteniendo protegidos sus datos internos.
