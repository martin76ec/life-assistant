import os
import re
import subprocess
from dotenv import load_dotenv

load_dotenv()

OUTPUT_PATH: str = "src/providers/sqlalchemy/models/models.py"
DB_URL: str = os.getenv("DB_URL") or ""
MIGRATIONS_DIR: str = "migrations"


def generate_models() -> None:
  """Generates SQLAlchemy models using sqlacodegen."""
  cmd = ["sqlacodegen", DB_URL, "--generator", "sqlmodels"]
  result = subprocess.run(cmd, check=True, capture_output=True, text=True)
  with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(result.stdout)
  print(f"✅ Models generated successfully at {OUTPUT_PATH}")


def remove_pg_tables(file_path: str) -> None:
  """Removes pg_stat_statements tables from the generated models."""
  undesired_starts = ("t_pg_stat_statements = Table(", "t_pg_stat_statements_info = Table(")

  with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

  new_lines = []
  skip_mode = False
  paren_count = 0

  for line in lines:
    stripped = line.lstrip()
    if not skip_mode and any(stripped.startswith(prefix) for prefix in undesired_starts):
      skip_mode = True
      paren_count = line.count("(") - line.count(")")
      continue

    if skip_mode:
      paren_count += line.count("(") - line.count(")")
      if paren_count <= 0:
        skip_mode = False
      continue

    new_lines.append(line)

  with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

  print(f"✅ Removed pg tables from {file_path}")


def run_alembic() -> None:
  """Runs Alembic migrations."""
  if not os.path.exists(MIGRATIONS_DIR):
    print("Initializing Alembic...")
    subprocess.run(["alembic", "init", MIGRATIONS_DIR], check=True)

  print("Generating Alembic migration...")
  subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Initial migration"], check=True)
  print("✅ Alembic migration complete.")


def main() -> None:
  """Main function to run model generation and Alembic migrations."""
  try:
    generate_models()
    remove_pg_tables(OUTPUT_PATH)
    run_alembic()
    print("✅ Model generation and Alembic migration complete.")
  except subprocess.CalledProcessError as e:
    print(f"❌ Error running a subprocess: {e}")
    print(f"Output: {e.output}")
    exit(1)
  except FileNotFoundError as e:
    print(f"❌ Error: File not found: {e.filename if hasattr(e, 'filename') else e}")
    exit(1)
  except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    exit(1)


if __name__ == "__main__":
  main()
