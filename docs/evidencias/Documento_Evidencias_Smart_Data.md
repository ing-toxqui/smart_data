# Documento de Evidencias – Proyecto Smart Data

Ambiente evaluado: **PROD**  
Repositorio: **ing-toxqui/smart_data**  
Fecha: **03/10/2026**

## Resumen ejecutivo

Este documento reúne evidencias de la entrega del proyecto Smart Data en Azure Databricks con ADLS Gen2, Unity Catalog, Databricks Asset Bundles, GitHub Actions y AI/BI Dashboard.

## Ubicación recomendada en Git

```text
docs/evidencias/
├── Documento_Evidencias_Smart_Data.docx
├── Documento_Evidencias_Smart_Data.md
└── imagenes/
```

## Evidencias

### GitHub - estructura del repositorio

Evidencia de repositorio smart_data con carpetas principales y archivo databricks.yml.

![GitHub - estructura del repositorio](imagenes/01_github_repo_estructura.png)

### GitHub - ramas

Evidencia del flujo con ramas main, dev y feature/*.

![GitHub - ramas](imagenes/02_github_branches.png)

### GitHub - pull requests cerrados

Evidencia de integración mediante pull requests hacia ramas superiores.

![GitHub - pull requests cerrados](imagenes/03_github_pull_requests.png)

### GitHub Actions - ejecución exitosa

Evidencia de workflow Deploy PROD ejecutado correctamente.

![GitHub Actions - ejecución exitosa](imagenes/04_github_actions_success.png)

### GitHub Actions - pasos del despliegue

Evidencia de generación del dashboard PROD, validación y despliegue del bundle.

![GitHub Actions - pasos del despliegue](imagenes/05_github_actions_steps.png)

### GitHub Environment production

Evidencia de variables de environment para producción sin uso de secretos visibles.

![GitHub Environment production](imagenes/06_github_environment_production.png)

### GitHub workflow deploy-prod.yml

Evidencia de uso de environment production, OIDC y comandos Databricks Bundle.

![GitHub workflow deploy-prod.yml](imagenes/07_github_workflow_environment_production.png)

### Databricks - Git folder en PROD

Evidencia de repositorio smart_data sincronizado en workspace_prod.

![Databricks - Git folder en PROD](imagenes/08_databricks_git_folder_main.png)

### Databricks - job principal PROD

Evidencia del job smart_data_pipeline_prod conectado al bundle y ejecutado por el service principal.

![Databricks - job principal PROD](imagenes/09_databricks_job_pipeline_prod.png)

### Databricks - tasks del pipeline

Evidencia del flujo creacion_objetos → inicia_proceso → bronze → silver → gold → mueve_archivos.

![Databricks - tasks del pipeline](imagenes/10_databricks_job_pipeline_tasks.png)

### Databricks - pipeline finalizado

Evidencia de ejecución Succeeded del pipeline productivo.

![Databricks - pipeline finalizado](imagenes/11_databricks_job_pipeline_succeeded.png)

### Databricks - job dashboard setup PROD

Evidencia del job independiente para creación/actualización de vistas semánticas.

![Databricks - job dashboard setup PROD](imagenes/12_databricks_job_dashboard_setup_prod.png)

### Databricks - dashboard setup finalizado

Evidencia de ejecución correcta del setup del dashboard.

![Databricks - dashboard setup finalizado](imagenes/13_databricks_job_dashboard_setup_succeeded.png)

### Unity Catalog - catálogo, schema, tablas, vistas y volumes

Evidencia de smart_data_prod.storage con tablas, vistas del dashboard y volumes raw/backup.

![Unity Catalog - catálogo, schema, tablas, vistas y volumes](imagenes/14_uc_catalog_smart_data_prod.png)

### Unity Catalog - external locations PROD

Evidencia de external locations ext_prod_* apuntando a containers ADLS Gen2.

![Unity Catalog - external locations PROD](imagenes/19_uc_external_locations_prod.png)

### Unity Catalog - storage credential PROD

Evidencia de storage_credential_prod con Managed Identity.

![Unity Catalog - storage credential PROD](imagenes/20_uc_storage_credential_prod.png)

### Azure - recursos principales

Evidencia de recursos DEV/PROD: workspace, storage accounts y access connectors.

![Azure - recursos principales](imagenes/21_azure_resources_prod.png)

### Azure - containers de ADLS PROD

Evidencia de containers raw, bronze, silver, gold y backup en storagetoxprod.

![Azure - containers de ADLS PROD](imagenes/23_azure_storage_containers.png)

### Azure - Access Connector PROD

Evidencia del recurso connector_prod para integración con Databricks.

![Azure - Access Connector PROD](imagenes/24_azure_access_connector_prod.png)

### Azure - role assignment

Evidencia de Storage Blob Data Contributor para connector_prod sobre storagetoxprod.

![Azure - role assignment](imagenes/25_azure_connector_role_assignment.png)

### SQL - conteos de tablas PROD

Evidencia de datos cargados en las tablas productivas.

![SQL - conteos de tablas PROD](imagenes/26_sql_counts_prod_tables.png)

### SQL - vista semántica del dashboard

Evidencia de consulta exitosa sobre vw_dashboard_resumen_mensual.

![SQL - vista semántica del dashboard](imagenes/27_sql_vw_dashboard_resumen_mensual.png)

### AI/BI Dashboard - listado

Evidencia de dashboard smart_data_dashboard desplegado.

![AI/BI Dashboard - listado](imagenes/32_dashboard_home.png)

### AI/BI Dashboard - Resumen de visitantes

Evidencia de página funcional con gráficas de visitantes.

![AI/BI Dashboard - Resumen de visitantes](imagenes/33_dashboard_resumen_visitantes.png)

### AI/BI Dashboard - Procesamiento y calidad

Evidencia de KPIs y visualizaciones de procesamiento/calidad.

![AI/BI Dashboard - Procesamiento y calidad](imagenes/34_dashboard_procesamiento_calidad.png)

### Databricks Volume - backup procesado

Evidencia de archivos procesados movidos a backup/processed/<id_proceso>.

![Databricks Volume - backup procesado](imagenes/35_backup_processed_files.png)
