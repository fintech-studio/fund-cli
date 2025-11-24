from fund.config.database_config import DatabaseConfig

class ConfigService:
    """配置管理服務"""
    
    def __init__(self):
        self.config = DatabaseConfig()
    
    def show_db_config(self):
        """顯示資料庫配置"""
        return {
            'server': self.config.server or 'Not configured',
            'database': self.config.database or 'Not configured',
            'username': self.config.username or 'Not configured',
            'password': '***' if self.config.password else 'Not configured',
            'driver': self.config.driver or 'Not configured'
        }
    
    def show_fred_config(self):
        """顯示 FRED API 配置"""
        key = self.config.get_fred_key()
            # 只顯示前4位和後4位
        if key:
            masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
            return {'api_key': masked_key,
                    'status': 'Configured' 
                    }
        else:
            return {'api_key': "Not configured",
                    'status': 'Not configured' 
            }
    
    def update_db_config(self, server=None, database=None, username=None, password=None, driver=None):
        """更新資料庫配置"""
        self.config.update_database(server, database, username, password, driver)
        return "database configuration updated"
    
    def clear_db_config(self):
        """清除資料庫配置"""
        self.config.clear_db_config()
        return "Database configuration cleared"
    
    def clear_fred_config(self):
        """清除 FRED API Key"""
        self.config.clear_fred_key()
        return "FRED API Key cleared"

    def update_fred_config(self, api_key):
        """更新 FRED API Key"""
        self.config.update_fred_key(api_key)
        return "FRED API Key updated"
