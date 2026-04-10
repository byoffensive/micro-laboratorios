<div align="center">
  <h1>🛡️ Securización Perimetral: Firewall para Servidor de Correo</h1>
  <p><i>Implementación de políticas UFW, auditoría de puertos y validación de túneles TLS</i></p>
</div>

<br>

## Objetivo
Configurar un firewall en un servidor Ubuntu que ya dispone de servicios de correo (Postfix
y Dovecot), permitiendo únicamente los puertos necesarios y verificando su
funcionamiento.

## Escenario
Dispones de un servidor Linux con servicios de correo activos. Debes protegerlo mediante
firewall permitiendo solo los puertos esenciales. Actualmente, el servidor funciona en un
entorno de pruebas y no tiene activo ningún cortafuegos.

## 🛠️ Stack Tecnológico
<p>
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu" />
  <img src="https://img.shields.io/badge/UFW_Firewall-005571?style=for-the-badge&logo=linux&logoColor=white" alt="UFW" />
  <img src="https://img.shields.io/badge/Postfix-D22128?style=for-the-badge&logo=postfix&logoColor=white" alt="Postfix" />
  <img src="https://img.shields.io/badge/Dovecot-2B445A?style=for-the-badge&logo=dovecot&logoColor=white" alt="Dovecot" />
</p>

---

## 🔒 Ejecución Técnica y Fases

### 1. Configuración de Políticas Base (UFW)
El primer paso para aplicar una arquitectura de confianza cero a nivel de red es denegar todo el tráfico entrante por defecto. A continuación, se procedió a abrir exclusivamente los tres puertos requeridos para la infraestructura de correo:

* **Puerto 25/TCP (SMTP):** Necesario para el enrutamiento y recepción de correos entre distintos servidores (Server-to-Server).
* **Puerto 587/TCP (SMTP Submission):** Utilizado por los clientes de correo para enviar correos hacia nuestro servidor de forma autenticada.
* **Puerto 993/TCP (IMAPS):** Protocolo IMAP encapsulado sobre TLS/SSL para garantizar la lectura segura de los buzones.

**Comandos de despliegue:**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 25/tcp
sudo ufw allow 587/tcp
sudo ufw allow 993/tcp
sudo ufw enable
```

<details>
  <summary><b>📸</b></summary>
  
  <br>
  <p align="center">
    <!-- INSTRUCCIÓN: ARRASTRA AQUÍ LA IMAGEN DEL 'ufw status verbose' (Asegúrate de dejar una línea en blanco arriba y abajo) -->
    <img src="https://github.com/user-attachments/assets/20f2b5c6-f355-47e7-be9a-fee9ec6e5478" width="800">
  </p>
</details>

<br>

### 2. Auditoría de Servicios en Escucha
Una vez levantado el cortafuegos, es vital comprobar que los demonios de Postfix y Dovecot siguen ejecutándose y están correctamente vinculados (bind) a los puertos autorizados. Para ello, se utilizó el comando `ss` (Socket Statistics) filtrando la salida para los puertos críticos.

**Comando de validación:**
```bash
sudo ss -lntp | egrep ':(25|587|993)'
```

<details>
  <summary><b>📸</b></summary>
  
  <br>
  <p align="center">
    <!-- INSTRUCCIÓN: ARRASTRA AQUÍ LA IMAGEN DEL COMANDO 'ss -lntp' -->
    <img src="https://github.com/user-attachments/assets/10aa5e2b-d7f4-487a-8898-b1e15ebf6edd" width="800">
  </p>
</details>

<br>

### 3. Validación del Handshake Criptográfico (TLS)
Para confirmar que el puerto 993 está operando correctamente bajo un túnel seguro y no en texto plano, se utilizó la herramienta `openssl` simulando la conexión de un cliente de correo. Esto permite verificar el intercambio de claves (Handshake TLS) y la correcta entrega del certificado digital del servidor.

**Comando de simulación de cliente:**
```bash
openssl s_client -connect localhost:993
```

<details>
  <summary><b>📸 </b></summary>
  
  <br>
  <p align="center">
    <!-- INSTRUCCIÓN: ARRASTRA AQUÍ LA IMAGEN DEL COMANDO 'openssl s_client' -->
    <img src="https://github.com/user-attachments/assets/c96da253-f709-4dc5-b0b6-e9e2699684e5" width="800">
  </p>
</details>

---

## 🧠 Análisis de Riesgos y Conclusión

**Incidente Simulado:** *¿Qué riesgo de seguridad implica abrir el puerto 143 (IMAP estándar) en lugar del 993?*

Abrir el puerto 143 permitiría a los clientes conectarse al servidor utilizando el protocolo IMAP tradicional en **texto plano** (sin una capa de cifrado TLS/SSL obligatoria). Esto expone a la organización a un riesgo crítico de interceptación mediante ataques de **Man-in-the-Middle (MitM)** o *Packet Sniffing*. 

Si un empleado de la organización sincroniza su bandeja de entrada desde una red Wi-Fi pública no confiable utilizando el puerto 143, un atacante posicionado en la misma red podría utilizar herramientas como Wireshark para capturar el tráfico y **leer en claro tanto las credenciales de acceso (usuario y contraseña) como el contenido íntegro de todos los correos electrónicos confidenciales**. Forzar el uso exclusivo del puerto 993 (IMAPS) garantiza que toda la comunicación viaje dentro de un túnel criptográfico ilegible para terceros.

<br>

*Este proyecto forma parte de mi portfolio técnico. Puedes ver más casos de estudio en mi [perfil principal de GitHub](https://github.com/byoffensive).*




