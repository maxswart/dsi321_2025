from prefect import flow
from pathlib import Path

source=str(Path.cwd())
entrypoint = f"firmsapiflow.py:firmsapi_flow" #python file: function
print(f'entrypoint:{entrypoint}, source:{source}')

if __name__ == "__main__":
    flow.from_source(
        source=source,
        entrypoint=entrypoint,
    ).deploy(
        name="firms_deployment",
        parameters={},
        work_pool_name="default-agent-pool",
        cron="0 */8 * * *",  # Run every 8 hours
    )