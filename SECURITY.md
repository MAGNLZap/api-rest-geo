# Seguridad y publicación

## Configuración privada

- No versionar `.env`, contraseñas, tokens, certificados privados, dumps,
  bases locales, datos operativos, logs o respaldos.
- Los `.env*.example` son plantillas públicas: solo valores ficticios.
- `VITE_*` es público por diseño; nunca colocar secretos ahí.
- Mantener los `.env` con permisos restringidos y fuera del contexto Docker.
- Las imágenes API/web ejecutan procesos no root. Solo la web se publica,
  por defecto en loopback; HTTPS y certificados pertenecen al proxy público.
- Conceder al usuario de BD únicamente los permisos necesarios para ejecutar
  consultas. Usar cuentas distintas para cargas/migraciones.

## Antes de publicar

1. Revisar el diff y los archivos que se van a subir, no solo `.gitignore`.
2. Revisar **todo el historial**, ramas y tags con un escáner de secretos,
   por ejemplo Gitleaks, y revisar manualmente datos y recursos binarios.
3. Confirmar derechos de distribución sobre límites geográficos, catálogo,
   imágenes, marcas, tipografías y dependencias.
4. Confirmar que se tiene autoridad para licenciar el código bajo Apache-2.0
   y respetar los derechos independientes de recursos y datos de terceros.
5. Confirmar que no se publican datos operativos ni detalles internos de
   infraestructura, y revisar avisos de dependencias de la versión elegida.

**El historial previo contiene datasets operativos**. Quitarlos del índice
actual no los elimina de commits anteriores. Esta limpieza no reescribe
historial ni autoriza publicar el repositorio existente sin esa revisión.
Si el contenido no está autorizado para publicación, preparar un historial
limpio o sanearlo con aprobación explícita antes de subirlo; coordinarlo con
los colaboradores y no hacer `push --force` por defecto.

Si un secreto ya estuvo publicado, revocarlo/rotarlo; borrar el archivo o
reescribir Git no lo vuelve seguro por sí solo. No adjuntar secretos en
issues, capturas, logs o solicitudes de soporte.

## Vulnerabilidades

Reportar detalles sensibles por un canal privado acordado con el mantenedor.
Si la plataforma ofrece avisos privados de seguridad, utilizarlos en vez
de abrir un issue público con información explotable.
