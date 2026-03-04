# Documentación Técnica de TE-API

**TE-API** es una herramienta de línea de comandos (CLI) desarrollada en Python que encapsula la API de Transparent Edge. Permite interactuar con todos los servicios de la plataforma de manera estructurada, segura y eficiente desde la terminal.

## 1. Introducción

El objetivo de este proyecto es proporcionar una interfaz unificada para gestionar recursos de Transparent Edge (CDNs, WAF, Almacenamiento, Usuarios, etc.) sin necesidad de construir peticiones HTTP manualmente.

La herramienta se genera **automáticamente** a partir de la especificación OpenAPI (`transparent-api.yaml`), lo que garantiza que siempre cubra el 100% de los endpoints disponibles.

## 2. Instalación y Requisitos

Este proyecto utiliza **`uv`** para la gestión de dependencias y entornos virtuales, lo que asegura una instalación rápida y aislada.

### Prerrequisitos

- Python 3.12 o superior.
- [uv](https://github.com/astral-sh/uv) instalado.

### Instalación para Usuarios (Consumo)

Si solo quieres usar la herramienta, puedes instalarla directamente desde el repositorio git:

```bash
# Instalar como herramienta global
uv tool install git+https://github.com/TransparentEdge/te-api.git
```

Una vez instalada, el comando `te-api` estará disponible en tu terminal.

## 3. Uso Básico

### Autenticación

La herramienta maneja la autenticación OAuth2 automáticamente.

1.  Configura tus credenciales en un archivo `.env` o variables de entorno:

    ```bash
    export TRANSPARENT_CLIENT_ID="tu_client_id"
    export TRANSPARENT_CLIENT_SECRET="tu_client_secret"
    ```

    Si no quieres usar las variables de entorno, puedes poner un archivo .env en el directorio donde lo ejecutes o en tu $HOME

    ```bash
    cat <<EOF >> ~/.env
    TRANSPARENT_CLIENT_ID="tu_client_id"
    TRANSPARENT_CLIENT_SECRET="tu_client_secret"
    EOF
    ```

2.  Inicia sesión (opcional, se hace auto en la primera petición):
    ```bash
    te-api login
    ```
    El token se guarda de forma segura en `~/.te-api/token.json` y se refresca automáticamente cuando expira.

### Gestión de Contexto (Company ID)

Para no tener que escribir `--company-id <ID>` en cada comando, puedes establecer una compañía por defecto:

```bash
# Establecer ID por defecto
te-api set-company 12345

# Usar comandos sin especificar ID
te-api companies get alerts

# Sobreescribir puntualmente
te-api companies get alerts --company-id 67890

# Ver configuración actual
te-api show-context

# Borrar contexto
te-api clear-company
```

### Autocompletado (Completions)

Para habilitar el autocompletado en tu terminal (Bash, Fish, Zsh), ejecuta:

```bash
# Bash
te-api completion bash > ~/.te-api-completion.bash
echo "source ~/.te-api-completion.bash" >> ~/.bashrc

# Fish
te-api completion fish > ~/.config/fish/completions/te-api.fish

# Zsh
te-api completion zsh > ~/.te-api-completion.zsh
echo "source ~/.te-api-completion.zsh" >> ~/.zshrc
```

### Estructura de Comandos

La CLI sigue una estructura jerárquica intuitiva:

```bash
te-api [MODULO] [VERBO] [RECURSO] [OPCIONES]
```

- **MÓDULO**: La sección de la API (ej: `companies`, `security`, `cdn`).
- **VERBO**: La acción a realizar (`get`, `create`, `update`, `delete`).
- **RECURSO**: El objeto específico (ej: `current-user`, `rules`, `cache`).

#### Ejemplos

```bash
# Ver información del usuario actual
te-api companies get current-user

# Listar alertas de una compañía
te-api companies get alerts <COMPANY_ID>

# Purgar caché
te-api companies create invalidate <COMPANY_ID> --json-body '{"urls": ["..."]}'
```
