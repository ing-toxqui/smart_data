# Smart Data Dashboard

This directory contains the Databricks AI/BI Dashboard used as the presentation layer of the **Smart Data** project.

The dashboard consumes semantic views created on top of the Gold layer and provides both business-oriented visitor analytics and operational pipeline monitoring.

## Architecture

The dashboard follows this separation of responsibilities:

```text
Gold tables
    ↓
Semantic views
    ↓
Dashboard datasets
    ↓
AI/BI Dashboard
```

Business logic is kept outside the visualization layer whenever possible.

The dashboard is responsible for presenting already prepared information instead of duplicating transformation logic inside individual visualizations.

---

## Dashboard Setup

The semantic views used by the dashboard are created by:

```text
notebooks/dashboard/00_creacion_vistas_dashboard.ipynb
```

The notebook receives environment-specific parameters:

```text
catalog_name
schema_name
```

All Unity Catalog references use fully qualified names:

```text
catalog.schema.object
```

For example:

```text
smart_data_dev.storage.vw_dashboard_resumen_mensual
```

The notebook is executed through an independent Databricks Job defined in:

```text
resources/dashboard_setup.yml
```

The deployed DEV Job is:

```text
smart_data_dashboard_setup_dev
```

This Job is intentionally independent from the main data pipeline.

The main pipeline processes data, while the dashboard setup Job creates or updates the semantic layer only when required.

---

## Semantic Views

The dashboard uses the following Unity Catalog views.

### `vw_dashboard_resumen_mensual`

Provides monthly visitor snapshot metrics.

Main metrics include:

```text
total_visitantes
visitantes_activos
visitantes_baja
visitantes_nuevos
visitantes_con_actividad
visitas_mes
visitas_anio_acumuladas
visitas_totales_acumuladas
```

---

### `vw_dashboard_actividad_mensual`

Provides historical monthly activity.

Main fields include:

```text
periodo
periodo_fecha
visitantes_con_actividad
total_visitas
promedio_visitas_por_visitante
primera_visita_mes
ultima_visita_mes
```

---

### `vw_dashboard_visitantes`

Provides visitor-level information by period.

Main fields include:

```text
periodo
email
fecha_primera_visita
fecha_ultima_visita
visitas_totales
visitas_anio_actual
visitas_mes_actual
periodo_baja
estado_visitante
```

---

### `vw_dashboard_procesamiento`

Provides operational information about pipeline executions.

Main fields include:

```text
id_proceso
fecha_ejecucion
fecha_ejecucion_dia
archivos_procesados
registros_bronze
registros_invalidos_bronze
registros_silver
registros_error
```

---

### `vw_dashboard_errores`

Provides aggregated data-quality errors.

Main fields include:

```text
id_proceso
fecha_ejecucion
fecha_ejecucion_dia
nombre_archivo
razon_error
total_errores
```

---

## Dashboard Pages

The dashboard contains two pages.

### Resumen de visitantes

Provides a business-oriented view of visitor activity.

Main KPIs:

```text
Visitantes totales
Visitantes activos
Visitantes nuevos
Visitantes con actividad
Visitas del mes
```

Visualizations include:

```text
Evolución de visitantes
Actividad mensual
Promedio de visitas por visitante
Top visitantes del periodo
```

A single-period filter controls the monthly KPIs and visitor table.

Historical trend charts remain independent from the selected month so that the complete time series remains visible.

---

### Procesamiento y calidad

Provides operational monitoring of the ingestion and transformation process.

Main KPIs:

```text
Archivos procesados
Registros Bronze
Registros Silver
Registros inválidos
Registros con error
```

Visualizations include:

```text
Registros procesados por ejecución
Errores por tipo
Errores por archivo
Detalle de errores
```

Available operational filters include:

```text
ID Proceso
Fecha de ejecución
```

`fecha_ejecucion` remains a timestamp for execution-level analysis, while `fecha_ejecucion_dia` is used for day-level dashboard filtering.

---

## Databricks Asset Bundle

The dashboard is deployed through a Databricks Asset Bundle resource defined in:

```text
resources/dashboard.yml
```

The dashboard resource uses an environment-specific dashboard artifact:

```text
dashboards/smart_data_dashboard_${environment}.lvdash.json
```

Current DEV artifact:

```text
dashboards/smart_data_dashboard_dev.lvdash.json
```

The SQL Warehouse is also configured per environment through:

```text
warehouse_id
```

---

## Environment Strategy

Dashboard datasets always use fully qualified Unity Catalog object names:

```text
catalog.schema.object
```

DEV references therefore use:

```text
smart_data_dev.storage.<object>
```

PROD references will use:

```text
smart_data_prod.storage.<object>
```

Environment-specific `.lvdash.json` artifacts are used so that explicit three-part Unity Catalog references are preserved.

---

## Deployment

For DEV, the Bundle currently manages:

```text
smart_data_pipeline_dev
smart_data_dashboard_setup_dev
smart_data_dashboard
```

The recommended execution order when semantic definitions change is:

```text
Deploy Bundle
    ↓
Run smart_data_dashboard_setup_dev
    ↓
Validate semantic views
    ↓
Validate deployed dashboard
```

The dashboard setup Job does not have a recurring schedule.

---

## Files

```text
dashboards/
├── README.md
└── smart_data_dashboard_dev.lvdash.json
```

Related files:

```text
notebooks/dashboard/
└── 00_creacion_vistas_dashboard.ipynb

resources/
├── dashboard.yml
└── dashboard_setup.yml
```

---

## Current Status

DEV:

```text
Semantic views          Completed
Dashboard               Completed
Bundle resource         Completed
Dashboard setup Job     Completed
DEV deployment          Validated
```

PROD preparation and automated CI/CD deployment are handled separately from this dashboard implementation.
