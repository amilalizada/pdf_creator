from fastapi_utils.tasks import repeat_every
import shutil


@repeat_every(seconds=21600, raise_exceptions=True)
def remove_files() -> None:
    ...