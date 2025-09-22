from pydantic import BaseModel, ConfigDict


class DatabaseSettings(BaseModel):
    model_config = ConfigDict(extra="allow")

    driver: str
    host: str | None = None
    port: int | None = None
    database: str
    username: str | None = None
    password: str | None = None

    # pool_size: int = 5
    # max_overflow: int = 15
    # pool_pre_ping: bool = True
    # connection_timeout: int = 300
    # command_timeout: int = 300
    # connect_args: dict = Field(default_factory=dict)
    # server_settings: dict = Field(default_factory=dict)
    # app_name: str = "default"
    # timezone: str = "UTC"
    debug: bool = True
    # transaction_timeout_ms: int = 60
    # use_bouncer: bool = False

    @property
    def dsn(self) -> str:
        if self.username and self.password:
            return f"{self.driver}://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        if self.host and self.port:
            return f"{self.driver}://{self.host}:{self.port}/{self.database}"
        return f"{self.driver}:///{self.database}"
