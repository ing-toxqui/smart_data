# Smart Data

Smart Data is a data engineering project built on **Azure Databricks and Azure Data Lake Storage Gen2**.

The project was designed as both a learning project and a professional portfolio project, with an emphasis on reproducible deployments, environment separation, Unity Catalog governance, Medallion Architecture, and production-oriented engineering practices.

---

## Architecture

```text
Source files
    ↓
ADLS Gen2 — Raw
    ↓
Auto Loader
    ↓
Bronze
    ↓
Silver
    ↓
Gold
    ↓
Semantic Views
    ↓
Databricks AI/BI Dashboard
```

The project separates storage, processing, semantic modeling, and visualization responsibilities.

---

## Technology Stack

```text
Microsoft Azure
Azure Data Lake Storage Gen2
Azure Databricks
Unity Catalog
Databricks Volumes
External Delta Tables
Auto Loader
Structured Streaming
PySpark
Spark SQL
Databricks Jobs / Workflows
Databricks Asset Bundles
Databricks AI/BI Dashboards
GitHub
GitHub Flow
```

---

## Medallion Architecture

### Raw

Stores source files before processing.

DEV Volume:

```text
smart_data_dev.storage.raw
```

Physical storage:

```text
abfss://raw@storagetoxdev.dfs.core.windows.net/files/
```

---

### Bronze

Stores ingested source records with ingestion metadata.

Main table:

```text
smart_data_dev.storage.bronze_reportes
```

Auto Loader is used to identify and process new files.

Only files matching the expected naming convention are processed:

```text
report_<number>.txt
```

Example:

```text
report_1.txt
report_6.txt
```

---

### Silver

Contains cleaned and validated records.

Main table:

```text
smart_data_dev.storage.silver_reportes
```

Invalid records are separated into:

```text
smart_data_dev.storage.errores
```

---

### Gold

Contains business-ready datasets.

Main tables:

```text
smart_data_dev.storage.maestro_visitante
smart_data_dev.storage.visitas_mensuales
smart_data_dev.storage.visitante_mensual
```

These tables are the source for the semantic dashboard layer.

---

## Storage Design

The project uses ADLS Gen2 containers:

```text
raw
bronze
silver
gold
backup
```

Raw and backup files are exposed through Unity Catalog Volumes.

```text
smart_data_dev.storage.raw
smart_data_dev.storage.backup
```

Bronze, Silver, and Gold Delta tables are external/unmanaged tables using dedicated storage locations such as:

```text
abfss://bronze@storagetoxdev.dfs.core.windows.net/tables/
abfss://silver@storagetoxdev.dfs.core.windows.net/tables/
abfss://gold@storagetoxdev.dfs.core.windows.net/tables/
```

Volumes are intentionally not used for Bronze, Silver, or Gold table locations to avoid path overlap between Unity Catalog Volumes and external tables.

---

## Auto Loader

Auto Loader reads new source files from Raw.

Checkpoint and schema metadata are stored separately from table data:

```text
abfss://bronze@storagetoxdev.dfs.core.windows.net/metadata/smart_data_ingestion/checkpoints/raw_to_bronze

abfss://bronze@storagetoxdev.dfs.core.windows.net/metadata/smart_data_ingestion/schemas/raw_to_bronze
```

Unity Catalog file metadata is obtained using:

```text
_metadata.file_path
```

instead of `input_file_name()`.

---

## Main Pipeline

The main pipeline is deployed as a Databricks Job through the Asset Bundle.

DEV Job:

```text
smart_data_pipeline_dev
```

Task execution order:

```text
creacion_objetos
    ↓
inicia_proceso
    ↓
procesa_bronze
    ↓
procesa_silver
    ↓
procesa_gold
    ↓
mueve_archivos
```

---

## Process ID

Each pipeline execution generates a unique process identifier:

```python
id_proceso = str(uuid.uuid4())
```

The value is propagated between Job tasks using Databricks Task Values.

This allows records, files, errors, and executions to be associated with the same pipeline run.

---

## Pipeline Tasks

### `00_creacion_objetos.ipynb`

Creates the required external Delta tables.

Main objects:

```text
control_archivos
bronze_reportes
silver_reportes
errores
maestro_visitante
visitas_mensuales
visitante_mensual
```

---

### `00_inicia_proceso.ipynb`

Generates the unique `id_proceso` for the execution.

---

### `01_procesa_bronze.ipynb`

Responsibilities:

```text
Read new Raw files using Auto Loader
Validate file names
Normalize source columns
Write Bronze records
Register processed files
```

---

### `02_procesa_silver.ipynb`

Responsibilities:

```text
Read Bronze records by id_proceso
Clean and validate data
Separate valid and invalid records
Write Silver records
Write validation errors
Update file-control information
```

---

### `03_procesa_gold.ipynb`

Creates the Gold business tables:

```text
maestro_visitante
visitas_mensuales
visitante_mensual
```

---

### `04_mueve_archivos.ipynb`

Moves processed files from Raw to Backup.

Destination structure:

```text
/Volumes/{catalog_name}/{schema_name}/backup/processed/{id_proceso}
```

---

## Semantic Layer

Dashboard-specific semantic views are created by:

```text
notebooks/dashboard/00_creacion_vistas_dashboard.ipynb
```

The notebook is parameterized using:

```text
catalog_name
schema_name
```

All table and view references use fully qualified names:

```text
catalog.schema.object
```

The semantic views are:

```text
vw_dashboard_resumen_mensual
vw_dashboard_actividad_mensual
vw_dashboard_visitantes
vw_dashboard_procesamiento
vw_dashboard_errores
```

---

## Dashboard Setup Job

Semantic views are not recreated during every pipeline execution.

Instead, they are managed through an independent on-demand Job:

```text
smart_data_dashboard_setup_dev
```

Bundle configuration:

```text
resources/dashboard_setup.yml
```

This preserves the separation:

```text
Main pipeline
→ data processing

Dashboard setup
→ semantic-layer deployment

Dashboard
→ presentation
```

---

## AI/BI Dashboard

The project includes a Databricks AI/BI Dashboard.

DEV dashboard artifact:

```text
dashboards/smart_data_dashboard_dev.lvdash.json
```

The dashboard contains two pages.

### Resumen de visitantes

Includes:

```text
Visitantes totales
Visitantes activos
Visitantes nuevos
Visitantes con actividad
Visitas del mes
Evolución de visitantes
Actividad mensual
Promedio de visitas por visitante
Top visitantes del periodo
```

### Procesamiento y calidad

Includes:

```text
Archivos procesados
Registros Bronze
Registros Silver
Registros inválidos
Registros con error
Registros procesados por ejecución
Errores por tipo
Errores por archivo
Detalle de errores
```

More information is available in:

```text
dashboards/README.md
```

---

## Databricks Asset Bundle

Infrastructure and deployable Databricks resources are defined using a Databricks Asset Bundle.

Main file:

```text
databricks.yml
```

Resources:

```text
resources/
├── jobs.yml
├── dashboard.yml
└── dashboard_setup.yml
```

The Bundle currently defines two targets:

```text
dev
prod
```

Environment-dependent values are passed as Bundle variables.

Examples:

```text
environment
catalog_name
schema_name
storage_account
warehouse_id
```

---

## Environment Strategy

### DEV

```text
catalog       smart_data_dev
schema        storage
storage       storagetoxdev
```

DEV is the environment where all functionality is validated first.

### PROD

Planned catalog:

```text
smart_data_prod
```

PROD uses independent Azure and Databricks resources.

Environment-specific values are never expected to be hardcoded inside reusable notebooks.

All SQL object references remain fully qualified:

```text
catalog.schema.object
```

Dashboard artifacts are also environment-specific because their serialized dataset definitions contain explicit Unity Catalog references.

Example:

```text
smart_data_dashboard_dev.lvdash.json
smart_data_dashboard_prod.lvdash.json
```

---

## Repository Structure

```text
smart_data/
│
├── databricks.yml
│
├── README.md
│
├── resources/
│   ├── jobs.yml
│   ├── dashboard.yml
│   └── dashboard_setup.yml
│
├── dashboards/
│   ├── README.md
│   └── smart_data_dashboard_dev.lvdash.json
│
└── notebooks/
    │
    ├── setup/
    │   ├── 00_setup_storage.ipynb
    │   └── 00_creacion_objetos.ipynb
    │
    ├── pipeline/
    │   ├── 00_inicia_proceso.ipynb
    │   ├── 01_procesa_bronze.ipynb
    │   ├── 02_procesa_silver.ipynb
    │   ├── 03_procesa_gold.ipynb
    │   └── 04_mueve_archivos.ipynb
    │
    └── dashboard/
        └── 00_creacion_vistas_dashboard.ipynb
```

---

## Git Workflow

The project follows GitHub Flow:

```text
feature/*
    ↓
dev
    ↓
main
```

Development work is performed in feature branches.

Changes are validated in DEV before they are promoted toward production.

Direct development on `main` is avoided.

---

## Development Practices

The project follows several engineering principles:

```text
Environment-specific configuration is parameterized
No credentials or personal access tokens are hardcoded
Unity Catalog objects use fully qualified names
DEV is validated before PROD
Infrastructure and Jobs are defined as code when practical
Semantic-layer setup is separated from recurring processing
Source, table, checkpoint, and backup paths have separate responsibilities
Git feature branches are used for changes
```

Serverless-specific limitations are also respected. For example, `cache()` and `persist()` are not used inside the streaming `foreachBatch` implementation.

---

## Current Project Status

### Completed in DEV

```text
ADLS Gen2 storage architecture
Unity Catalog integration
Storage Credential / External Locations
Raw and Backup Volumes
External Delta tables
Auto Loader ingestion
Bronze processing
Silver validation
Gold processing
File backup process
Databricks Asset Bundle
Main pipeline Job
Dashboard semantic views
Dashboard setup Job
AI/BI Dashboard
DEV Bundle deployment
```

### Pending

```text
Complete PROD storage/access configuration
Deploy and validate PROD
Generate PROD dashboard artifact
GitHub Actions / CI-CD
Final DEV → main promotion
```

---

## Production Preparation

Before PROD deployment, the production environment must have its required infrastructure and permissions configured, including:

```text
Azure Storage Account
Access Connector
Azure RBAC permissions
Databricks Storage Credential
External Locations
Unity Catalog catalog/schema
Required Volumes
External table storage locations
SQL Warehouse
```

The PROD target must only be deployed after these prerequisites are validated.

---

## Project Goal

The goal of Smart Data is not only to demonstrate a working ETL pipeline, but also to demonstrate how a data engineering solution can be structured for:

```text
environment separation
governance
repeatability
observability
deployment automation
maintainability
analytics consumption
```

The project is designed to be understandable both as a technical implementation and as a portfolio example of an end-to-end Azure Databricks data platform.
