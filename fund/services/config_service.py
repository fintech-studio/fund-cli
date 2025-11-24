from fund.config.database_config import DatabaseConfig
from fund.config.fred_config import FredConfig

class ConfigService:
    """配置管理服務 - 提供配置的業務邏輯"""
    
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.fred_config = FredConfig()
    
    def show_db_config(self):
        """顯示資料庫配置"""
        return {
            'server': self.db_config.server or 'Not configured',
            'database': self.db_config.database or 'Not configured',
            'username': self.db_config.username or 'Not configured',
            'password': '***' if self.db_config.password else 'Not configured',
            'driver': self.db_config.driver or 'Not configured'
        }
    
    def show_fred_config(self):
        """顯示 FRED API 配置"""
        key = self.fred_config.api_key
        # 只顯示前4位和後4位
        if self.fred_config.is_configured():
            masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
            return {
                'api_key': masked_key,
                'status': 'Configured'
            }
        else:
            return {
                'api_key': "Not configured",
                'status': 'Not configured'
            }
    
    def update_db_config(self, server=None, database=None, username=None, password=None, driver=None):
        """更新資料庫配置"""
        self.db_config.update_database(server, database, username, password, driver)
        return "database configuration updated"
    
    def clear_db_config(self):
        """清除資料庫配置"""
        self.db_config.clear_db_config()
        return "Database configuration cleared"
    
    def update_fred_config(self, api_key):
        """更新 FRED API Key"""
        self.fred_config.update_api_key(api_key)
        return "FRED API Key updated"
    
    def clear_fred_config(self):
        """清除 FRED API Key"""
        self.fred_config.clear_api_key()
        return "FRED API Key cleared"
