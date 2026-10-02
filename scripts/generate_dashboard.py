from pathlib import Path
import argparse
import json


parser = argparse.ArgumentParser(
    description="Generate an environment-specific Databricks dashboard."
)

parser.add_argument("--source-file", required=True)
parser.add_argument("--target-file", required=True)
parser.add_argument("--source-catalog", required=True)
parser.add_argument("--target-catalog", required=True)
parser.add_argument("--schema", required=True)

args = parser.parse_args()


source_path = Path(args.source_file)
target_path = Path(args.target_file)

source_prefix = f"{args.source_catalog}.{args.schema}."
target_prefix = f"{args.target_catalog}.{args.schema}."


if not source_path.exists():
    raise FileNotFoundError(
        f"No existe el dashboard origen: {source_path}"
    )

if source_prefix == target_prefix:
    raise ValueError(
        "El catálogo origen y destino no pueden ser iguales."
    )


content = source_path.read_text(encoding="utf-8")

occurrences = content.count(source_prefix)

if occurrences == 0:
    raise RuntimeError(
        f"No se encontraron referencias a: {source_prefix}"
    )


generated_content = content.replace(
    source_prefix,
    target_prefix
)


if source_prefix in generated_content:
    raise RuntimeError(
        f"Quedaron referencias a DEV: {source_prefix}"
    )

if target_prefix not in generated_content:
    raise RuntimeError(
        f"No se generaron referencias a PROD: {target_prefix}"
    )


# Verificar que el resultado siga siendo JSON válido.
json.loads(generated_content)


target_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

target_path.write_text(
    generated_content,
    encoding="utf-8"
)


print("Dashboard generado correctamente.")
print(f"Archivo origen: {source_path}")
print(f"Archivo destino: {target_path}")
print(f"Origen: {source_prefix}")
print(f"Destino: {target_prefix}")
print(f"Referencias reemplazadas: {occurrences}")