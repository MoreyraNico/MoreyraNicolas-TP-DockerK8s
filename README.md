# Proyecto Docker y Kubernetes

**Alumno:** Nicolás Moreyra

## Descripción del proyecto

Este proyecto consiste en una aplicación web CRUD desarrollada con una arquitectura de tres capas:

- **Frontend:** interfaz web desarrollada con Flask.
- **Backend:** API desarrollada con FastAPI y SQLAlchemy.
- **Base de datos:** PostgreSQL.

La aplicación permite gestionar usuarios mediante operaciones CRUD (crear, consultar, actualizar y eliminar).

El proyecto utiliza Docker y Docker Compose para la ejecución de los servicios en contenedores, y Kubernetes para su despliegue y administración.

## Tecnologías utilizadas

- Python
- Flask
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker
- Docker Compose
- Kubernetes
- Nginx

## Estructura del proyecto

```text
MoreyraNicolas-TP-DockerK8s/
│
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── k8s/
│   ├── 01-config-secret.yaml
│   ├── 02-postgres.yaml
│   ├── 03-backend.yaml
│   ├── 04-frontend.yaml
│   ├── 05-ingress.yaml
│   └── sealed-secret.yaml
│
├── docker-compose.yml
├── nginx.conf
└── .gitignore
```

## Requisitos previos

Para ejecutar el proyecto se necesita tener instalado:

- Docker
- Docker Compose

Para el despliegue en Kubernetes también se necesita:
- kubectl
- Un clúster de Kubernetes funcionando.
- El controlador de Bitnami Sealed Secrets, para utilizar los secretos sellados.

## Ejecución con Docker Compose

### 1. Clonar el repositorio

```bash
git clone https://github.com/MoreyraNico/MoreyraNicolas-TP-DockerK8s.git
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd MoreyraNicolas-TP-DockerK8s
```

### 3. Construir las imágenes y levantar los contenedores

```bash
docker compose up --build -d
```

Este comando construye las imágenes necesarias y ejecuta los servicios definidos en `docker-compose.yml`.

### 4. Verificar los contenedores

```bash
docker compose ps
```

### 5. Consultar los registros de ejecución

```bash
docker compose logs -f
```

### 6. Detener la aplicación

```bash
docker compose down
```

Para detener los servicios y eliminar también los volúmenes:

```bash
docker compose down -v
```

**Importante:** este último comando elimina los datos persistidos de los volúmenes, incluida la información almacenada en PostgreSQL.

## Despliegue en Kubernetes

El proyecto incluye manifiestos YAML para desplegar los componentes en un clúster de Kubernetes.

Con el clúster iniciado y `kubectl` configurado, se pueden aplicar los manifiestos en el siguiente orden:

```bash
kubectl apply -f k8s/01-config-secret.yaml
kubectl apply -f k8s/sealed-secret.yaml
kubectl apply -f k8s/02-postgres.yaml
kubectl apply -f k8s/03-backend.yaml
kubectl apply -f k8s/04-frontend.yaml
kubectl apply -f k8s/05-ingress.yaml
```

El controlador de Sealed Secrets debe estar instalado y el secreto sellado debe ser compatible con el clúster utilizado.

### Verificar los recursos

```bash
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get ingress
```

### Consultar los registros de un pod

```bash
kubectl logs nombre-del-pod
```

### Eliminar los recursos desplegados

```bash
kubectl delete -f k8s/05-ingress.yaml
kubectl delete -f k8s/04-frontend.yaml
kubectl delete -f k8s/03-backend.yaml
kubectl delete -f k8s/02-postgres.yaml
kubectl delete -f k8s/sealed-secret.yaml
kubectl delete -f k8s/01-config-secret.yaml
```

## Pruebas de funcionamiento

La API permite realizar operaciones sobre los usuarios.

Algunos ejemplos de operaciones HTTP:

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/users` | Crear un usuario |
| GET | `/users` | Consultar usuarios |

También se puede acceder a la interfaz web desde el navegador utilizando el puerto publicado por Nginx en `docker-compose.yml`.

## Autor

**Nicolás Moreyra**

Trabajo práctico: Docker y Kubernetes.
