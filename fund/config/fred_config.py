from fund.config.config_manage import ConfigManager

class FredConfig:
    """FRED 配置類 - 提供 FRED API 配置介面"""

    def __init__(self):
        self._manager = ConfigManager()
    
    @property
    def api_key(self):
        """取得 FRED API Key"""
        return self._manager.get("fred_api_key")
    
    def update_api_key(self, api_key):
        """更新 FRED API Key"""
        if api_key:
            self._manager.set("fred_api_key", api_key)
    
    def clear_api_key(self):
        """清除 FRED API Key"""
        self._manager.delete("fred_api_key")
    
    def is_configured(self):
        """檢查是否已配置 API Key"""
        return self.api_key is not None