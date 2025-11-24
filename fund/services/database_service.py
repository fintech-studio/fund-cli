import pyodbc
from fund.config.database_config import DatabaseConfig

class DatabaseService:
    """資料庫配置與管理服務"""
    
    def __init__(self):
        self.config = DatabaseConfig()
        self.conn_str = self.config.get_connection_string()
    
    def test_connection(self):
        """測試資料庫連線"""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                return True, f"connection successful!\nSQL Server version: {version}"
        except Exception as e:
            return False, f"connection failed: {str(e)}"
    
    def list_tables(self):
        """列出所有基本面資料表"""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT TABLE_NAME 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME LIKE 'fundamental_data_%'
                    ORDER BY TABLE_NAME
                """)
                tables = [row[0] for row in cursor.fetchall()]
                return True, tables
        except Exception as e:
            return False, str(e)
    
    def get_table_info(self, table_name):
        """取得資料表詳細資訊"""
        try:
            with pyodbc.connect(self.conn_str) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                
                cursor.execute(f"""
                    SELECT MAX(lastUpdate) FROM {table_name}
                    WHERE lastUpdate IS NOT NULL
                """)
                last_update = cursor.fetchone()[0]
                
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = '{table_name}'
                    ORDER BY ORDINAL_POSITION
                """)
                columns = cursor.fetchall()
                
                return True, {
                    'count': count,
                    'last_update': last_update,
                    'columns': columns
                }
        except Exception as e:
            return False, str(e)
