import os
from pathlib import Path
from typing import Any, Literal
from dotenv import find_dotenv, load_dotenv

_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv(find_dotenv())


def validator(variable: str, expected_type: Literal["number", "string"], value: Any) -> Any:
    if value is None or str(value).strip() == "":
        raise ValueError(f"Variable {variable} is required!")

    if expected_type == "number":
        try:
            return int(value)
        except ValueError as err:
            raise ValueError(f"Variable {variable} must be a number!") from err

    if expected_type == "string":
        if not isinstance(value, str):
            raise ValueError(f"Variable {variable} must be a string!")
        return value

    return value


class EnvConfig:
    @property
    def HTTP_PORT(self) -> int:
        return validator("HTTP_PORT", "number", os.getenv("HTTP_PORT"))

    @property
    def GRPC_PORT(self) -> int:
        return validator("GRPC_PORT", "number", os.getenv("GRPC_PORT"))

    @property
    def DB_HOST(self) -> str:
        return validator("DB_HOST", "string", os.getenv("DB_HOST"))

    @property
    def DB_PORT(self) -> int:
        return validator("DB_PORT", "number", os.getenv("DB_PORT"))

    @property
    def DB_USER(self) -> str:
        return validator("DB_USER", "string", os.getenv("DB_USER"))

    @property
    def DB_PASSWORD(self) -> str:
        return validator("DB_PASSWORD", "string", os.getenv("DB_PASSWORD"))

    @property
    def DB_NAME(self) -> str:
        return validator("DB_NAME", "string", os.getenv("DB_NAME"))

    @property
    def DB_POOL_MAX(self) -> int:
        return validator("DB_POOL_MAX", "number", os.getenv("DB_POOL_MAX"))


env = EnvConfig()

__all__ = ["env", "EnvConfig", "validator"]
