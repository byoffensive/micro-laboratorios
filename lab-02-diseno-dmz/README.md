<div align="center">
  <h1>🏢 Diseño de Arquitectura Segura y Políticas de Firewall</h1>
  <p><i>Segmentación de red corporativa mediante DMZ y reglas de filtrado perimetral</i></p>
</div>
<br>

## Objetivo de la actividad
Analizar un escenario empresarial y diseñar una política de firewall que proteja una red
corporativa. El alumnado deberá identificar los servicios necesarios, definir zonas de
seguridad y proponer reglas de filtrado adecuadas.


## 1. Descripción del Escenario
El presente documento define la arquitectura de red y las políticas de seguridad perimetral para una infraestructura corporativa que requiere exponer servicios al público (Web y Correo) manteniendo la confidencialidad e integridad de sus datos internos (Base de Datos). 

La infraestructura inicial presenta un riesgo crítico: todos los servidores comparten el mismo segmento de red conectados a Internet. Esto implica que, si un atacante compromete el servidor web público, tendría acceso directo a la base de datos interna.

## 2. Clasificación de Zonas de Seguridad (Segmentación)
Para mitigar el riesgo de movimiento lateral, se propone una arquitectura de tres zonas segregadas lógicamente mediante un Firewall de Próxima Generación (NGFW):

### 🔴 Zona WAN (Internet - Red Pública)
* **Nivel de confianza:** Nulo (0%).
* **Descripción:** Representa el exterior de la organización. Cualquier IP de Internet que intente acceder a los servicios públicos corporativos.
* **Servicios ubicados:** Ninguno propio. Solo clientes externos y atacantes potenciales.

### 🟡 Zona DMZ (Zona Desmilitarizada)
* **Nivel de confianza:** Medio (50%).
* **Descripción:** Subred aislada que actúa como "escaparate" de la empresa. Los servidores aquí ubicados son accesibles desde Internet, pero no tienen permiso para iniciar conexiones hacia la Red Interna corporativa.
* **Servicios ubicados:**
  * **Servidor Web:** (Apache/Nginx) Expone la página corporativa.
  * **Servidor de Correo (Frontend):** (Postfix/Dovecot) Recibe conexiones SMTP/IMAP del exterior.

### 🟢 Zona LAN (Red Interna Corporativa)
* **Nivel de confianza:** Alto (100%).
* **Descripción:** El "corazón" de la empresa. Contiene los activos más valiosos y no tiene acceso directo desde Internet bajo ningún concepto.
* **Servicios ubicados:**
  * **Base de Datos (BBDD):** (MySQL/PostgreSQL) Almacena información sensible. Solo el servidor Web de la DMZ puede consultarla.
  * **Equipos de empleados (End-points):** Workstations del personal.

<br>

## 3. Matriz de Reglas de Firewall (Políticas de Filtrado)

La política de seguridad se basa en el principio de **"Denegación por Defecto"** (Default Deny). A continuación, se detallan las excepciones estrictamente necesarias para el flujo de negocio:

| ID | Origen | Destino | Puerto / Protocolo | Acción | Justificación Técnica |
|:---|:---:|:---:|:---:|:---:|:---|
| **R1** | Internet (WAN) | Web (DMZ) | **443 / TCP** (HTTPS) | ✅ PERMITIR | Tráfico web público cifrado hacia la página corporativa. *(Se asume que el puerto 80 redirige al 443).* |
| **R2** | Internet (WAN) | Correo (DMZ) | **25 / TCP** (SMTP) | ✅ PERMITIR | Recepción de correos electrónicos desde otros servidores de Internet. |
| **R3** | Internet (WAN) | Correo (DMZ) | **587, 993 / TCP** | ✅ PERMITIR | Envío (Submission) y lectura (IMAPS) de correos por parte de los clientes. |
| **R4** | Web (DMZ) | BBDD (LAN) | **3306 / TCP** (MySQL) | ✅ PERMITIR | El backend de la web necesita hacer consultas a la base de datos interna. |
| **R5** | LAN | Internet (WAN) | **80, 443 / TCP** | ✅ PERMITIR | Navegación de los empleados hacia Internet. |
| **R6** | Internet (WAN) | BBDD (LAN) | **Cualquiera** | ❌ BLOQUEAR | **Regla Crítica:** Prevención de exposición directa de la base de datos al exterior. |
| **R7** | DMZ | LAN | **Cualquiera** (Excepto R4) | ❌ BLOQUEAR | Previene el movimiento lateral si un servidor de la DMZ es vulnerado. |
| **R8** | Cualquiera | Cualquiera | **Cualquiera** | ❌ BLOQUEAR | Política "Default Deny" (Cierra todo lo no explícitamente permitido). |

<br>

## 4. Conclusión Final
El diseño propuesto transforma una arquitectura plana y vulnerable en un entorno estructurado de Defensa en Profundidad. La creación de la Zona DMZ garantiza que, en el peor de los escenarios (un *defacement* o compromiso total del servidor Web), el atacante se encuentre "encerrado" en una subred sin privilegios, incapaz de saltar a la Red Interna para exfiltrar la base de datos corporativa. Esta arquitectura cumple con los estándares actuales de seguridad perimetral para servicios expuestos.
    
