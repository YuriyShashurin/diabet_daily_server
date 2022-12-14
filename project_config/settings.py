from pydantic import BaseSettings


class ConfigSettings(BaseSettings):
    # Postgresql params
    postgres_db: str
    postgres_name: str
    postgres_host: str
    postgres_password: str
    postgres_port: int

    # Host, Ports params
    prod_host: str
    prod_port: int
    test_host: str
    test_port: int
    dev_host: str
    dev_port: int
    status: str

    # Test params
    is_test: bool
    postgres_db_test: str
    postgres_name_test: str
    postgres_host_test: str
    postgres_password_test: str
    postgres_port_test: int

    # JWT params
    secret_key: str

    class Config:
        env_file = ".env"