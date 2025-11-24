import os
import json


class DatabaseConfig:
    """資料庫配置類"""

    def __init__(self):
        self.config_path = os.path.join(os.getcwd(), "config.json")
        self._load_config()

    def _load_config(self):
        """載入配置檔案"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                config_data = {}
        else:
            config_data = {}

        self.server = config_data.get("db_server")
        self.database = config_data.get("db_name")
        self.username = config_data.get("db_user")
        self.password = config_data.get("db_password")
        self.driver = config_data.get("db_driver", "ODBC Driver 17 for SQL Server")
        self.fred_api_key = config_data.get("fred_api_key")

    def _save_config(self):
        """保存配置到 JSON 檔案"""
        config_data = {
            "db_server": self.server,
            "db_name": self.database,
            "db_user": self.username,
            "db_password": self.password,
            "db_driver": self.driver,
            "fred_api_key": self.fred_api_key,
        }

        # 移除空值
        config_data = {k: v for k, v in config_data.items() if v is not None}

        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

    def get_connection_string(self):
        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password}"
        )

    def get_master_connection_string(self):
        """取得連接到 master 資料庫的連線字串"""
        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE=master;"
            f"UID={self.username};"
            f"PWD={self.password}"
        )

    def update_database(
        self, server=None, database=None, username=None, password=None, driver=None
    ):
        """更新配置並保存到 JSON"""
        if server:
            self.server = server
        if database:
            self.database = database
        if username:
            self.username = username
        if password:
            self.password = password
        if driver:
            self.driver = driver

        self._save_config()

    def clear_db_config(self):
        """清除資料庫配置"""
        self.server = None
        self.database = None
        self.username = None
        self.password = None
        self.driver = "ODBC Driver 17 for SQL Server"
        self._save_config()

    def update_fred_key(self, api_key):
        """更新 FRED API Key"""
        self.fred_api_key = api_key
        self._save_config()

    def clear_fred_key(self):
        """清除 FRED API Key"""
        self.fred_api_key = None
        self._save_config()

    def get_fred_key(self):
        """取得 FRED API Key"""
        return self.fred_api_key