# ZooKeeper Primitives 

ZooKeeper proporciona una vista unificada y coherente de los datos a través de una estructura jerárquica de nodos llamada **ZNodes**. Estos funcionan de forma similar a un sistema de archivos: puedes crear, leer, modificar o eliminar nodos para compartir información o bloquear recursos distribuidos.

Un clúster de ZooKeeper está formado por varios **servidores** llamados **instancias o nodos quorum** (generalmente 3 o 5). Cada clúster sigue el siguiente modelo:
- **Líder**: coordina las escrituras y propaga los cambios al resto del clúster.
- **Seguidores**: replican los cambios del líder y responden solicitudes de lectura.
- **Observers (opcionales)**: ayudan con la carga de lectura sin participar en el consenso.
  
El consenso se logra usando el protocolo **Zab (ZooKeeper Atomic Broadcast)**, que asegura que todas las actualizaciones se apliquen de manera **atómica, ordenada y consistente**. 

## Modelo de datos: ZNodes
ZooKeeper organiza la información como un árbol jerárquico de datos llamado **DataTree**, donde cada nodo (ZNode) puede contener datos y subnodos.

Cada ZNode tiene:
- **Datos binarios** (configuraciones, metadatos, señales de estado).
- **Metadatos** (versión, timestamps, ACLs — listas de seguridad).

Los tipos de ZNodes:
- **Persistentes**: permanecen tras cerrar la sesión del cliente.
- **Ephemerales (efímeros)**: desaparecen cuando el cliente se desconecta.
- **Secuenciales**: incluyen un número incremental automático al crearse.

## Persistencia y durabilidad
Los datos se escriben en:
- **Transaction logs** (registros de operaciones secuenciales).
- **Snapshots** periódicos del árbol completo (DataTree), almacenados en disco.
- 

## Usage

### 1. Start ZooKeeper Cluster

```bash
docker-compose up -d
```

This starts a 3-node ZooKeeper cluster:
- ZooKeeper 1: `localhost:2181`
- ZooKeeper 2: `localhost:2182` 
- ZooKeeper 3: `localhost:2183`

### 2. Run python scripts...


```bash+
uv sync
uv add basics.py
```

## 3. Activity 
- https://zookeeper.apache.org/doc/current/recipes.html
- Create and test a class: zooMutex.py
- Create and test a class: leaderElection.py

## References
- https://www.oreilly.com/library/view/zookeeper/9781449361297/
- https://zookeeper.apache.org/doc/current/index.html