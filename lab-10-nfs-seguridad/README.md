# Tarea 12 — Integración avanzada y seguridad en entornos heterogéneos (RA6)

**Jhoan Camilo Arango Ortiz** · 2º ASIR online · Administración de Sistemas Operativos

---

## Entorno

- **Servidor NFS:** Ubuntu Server — IP `172.16.0.1`
- **Cliente NFS:** Ubuntu Desktop — IP `172.16.0.66`
- Red interna VirtualBox `172.16.0.0/24`

---

## Parte A — Configuración del servidor NFS

Instalación del servicio y creación de directorios exportados:

```bash
sudo apt install nfs-kernel-server -y
sudo mkdir -p /nfs_shares/publico
sudo mkdir -p /nfs_shares/privado
sudo chmod -R 777 /nfs_shares
```

Configuración de `/etc/exports`:

```
/nfs_shares/publico *(ro,sync,no_subtree_check)
/nfs_shares/privado 172.16.0.66(rw,sync,no_subtree_check,no_root_squash)
```

```bash
sudo exportfs -ra
sudo systemctl restart nfs-kernel-server
```

**¿Qué implica no_root_squash?** Por defecto NFS mapea el root del cliente a un usuario sin privilegios en el servidor. Con `no_root_squash` ese mapeo no se aplica, así que el root del cliente actúa como root en el servidor — supone un riesgo serio si el cliente se ve comprometido.

---

## Parte B — Montaje en el cliente

Instalación y montaje temporal:

```bash
sudo apt install nfs-common -y
sudo mkdir -p /mnt/publico_red /mnt/privado_red
sudo mount -t nfs 172.16.0.1:/nfs_shares/privado /mnt/privado_red
touch /mnt/privado_red/archivo_cliente.txt
```

Montaje persistente en `/etc/fstab`:

```
172.16.0.1:/nfs_shares/publico /mnt/publico_red nfs defaults 0 0
```

**¿Qué pasa si se olvida registrar en /etc/fstab?** El montaje manual desaparece al reiniciar. El próximo viernes tras instalar actualizaciones, el directorio NFS aparecerá vacío y cualquier aplicación que dependa de esa ruta fallará.

---

## Parte C — Seguridad con UFW

```bash
sudo ufw allow from 172.16.0.66 to any port 2049 proto tcp
sudo ufw enable
sudo ufw status
```

**NFS vs Samba en CPD Linux:** En un entorno con 50 servidores Ubuntu elegiría NFS. Es el protocolo nativo de Linux, opera a nivel de kernel con menor latencia y mejor rendimiento que Samba, que añade overhead innecesario al implementar el protocolo SMB diseñado para Windows. Samba solo tiene sentido cuando hay clientes Windows en la red.
