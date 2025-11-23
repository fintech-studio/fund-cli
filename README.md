# 基本面資料分析系統

一個功能完整的金融資料擷取與分析工具,支援股票基本面分析、經濟指標查詢及大宗商品價格追蹤。

## ✨ 主要功能

### 📊 股票基本面分析
- **多市場支援**:台股、美股、台灣興櫃市場
- **完整財務指標**:
  - 估值指標 (P/E、P/B、P/S、PEG等)
  - 財務健康度 (負債比、流動比率、速動比率)
  - 獲利能力 (ROE、ROA、各項利潤率)
  - 成長性指標 (營收成長、盈餘成長)
  - 股利資訊 (股利率、配息率)
  - 股價技術指標 (Beta、52週高低點)

### 📈 經濟指標查詢
- **CPI (消費者物價指數)**
  - 支援單筆最新資料與期間範圍查詢
  - 包含年增率 (YoY%) 與月增率 (MoM%)
  
- **NFP (非農就業人數)**
  - 支援單筆最新資料與期間範圍查詢
  - 包含月變化量與年變化量

### 💰 大宗商品價格
- **WTI原油**: 西德州中級原油即時價格
- **黃金期貨**: 黃金期貨價格追蹤

## 🚀 快速開始

### 環境需求
- Python 3.12+
- SQL Server (用於資料儲存)
- FRED API Key (用於經濟指標查詢)

### 安裝

1. **克隆專案**
```powershell
git clone <repository-url>
cd fundamental
```

2. **安裝相依套件**
```powershell
pip install -e .
或
pip install -r requirements.txt
```

3. **環境設定**

建立 `.env.local` 檔案:
```env
# 資料庫連線設定
DB_SERVER=your_server_name
DB_NAME=fundamental_data
DB_USER=your_username
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 17 for SQL Server

# FRED API Key (從 https://fred.stlouisfed.org/docs/api/api_key.html 申請)
FRED_API_KEY=your_fred_api_key
```
## 管理工具 uv

安裝uv
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
初始化專案
```powershell
uv init
```
安裝套件
```poershell
uv add [package-name]
```

## 📖 使用說明

### 基本語法
```powershell
python main.py [選項] [股票代號...]
```

### 股票查詢範例

**台股查詢**
```powershell
# 查詢單一台股
python main.py 2330 --tw

# 查詢多支台股
python main.py 2330 2317 --tw
python main.py --tw 2330 2317
```

**美股查詢**
```powershell
# 查詢單一美股
python main.py AAPL --us

# 查詢多支美股
python main.py AAPL TSLA MSFT --us
python main.py --us AAPL TSLA
```

**興櫃市場**
```powershell
python main.py 6547 --two
```

### 經濟指標查詢

**CPI查詢**
```powershell
# 最新資料
python main.py --cpi

# 期間資料
python main.py --cpi --start_date 2020/01/01 --end_date 2024/12/31
```

**NFP查詢**
```powershell
# 最新資料
python main.py --nfp

# 期間資料
python main.py --nfp --start_date 2020/01/01 --end_date 2024/12/31
```

### 大宗商品價格查詢

**WTI原油**
```powershell
# 最新價格
python main.py --oil

# 期間資料
python main.py --oil --start_date 2023/01/01 --end_date 2023/12/31
```

**黃金期貨**
```powershell
# 最新價格
python main.py --gold

# 期間資料
python main.py --gold --start_date 2023/01/01 --end_date 2023/12/31
```

### 顯示說明
```powershell
python main.py --help
```

## 🏗️ 專案結構

```
fundamental/
├── main.py                          # 主程式進入點
├── uv.lock                          # 套件詳細訊息
├── .python-version                  # python版本
├── pyproject.toml                   # 專案配置
├── requirements.txt                 # 相依套件清單
├── README.md                        # 專案說明文件
├── config/
│   └── database_config.py          # 資料庫連線配置
├── providers/
│   └── fundamental_data_provider.py # 資料提供者 (API整合)
├── repositories/
│   └── fundamental_data_repository.py # 資料儲存庫 (資料庫操作)
└── services/
    └── fundamental_data_service.py  # 業務邏輯服務層
```

### 架構說明

**分層架構 (Layered Architecture)**
```
main.py
   ↓
services (業務邏輯層)
   ↓
providers (資料提供層) ←→ repositories (資料持久層)
   ↓                           ↓
External APIs              SQL Server
```

- **Provider**: 負責從外部API (yfinance, FRED) 擷取資料
- **Repository**: 處理資料庫的CRUD操作
- **Service**: 協調Provider與Repository,實現業務邏輯
- **Config**: 統一管理配置資訊

## 📊 輸出範例

```
============================================================
  AAPL - Apple Inc. 基本面分析
============================================================

📊 基本資訊:
  產業: Consumer Electronics
  板塊: Technology
  國家: United States
  交易所: NMS
  貨幣: USD

💰 估值指標:
  市值: $3.45兆
  本益比 (P/E): 33.82
  預估本益比: 31.25
  股價淨值比 (P/B): 48.67
  股價營收比 (P/S): 9.15
  PEG比率: 3.12

🏥 財務健康度:
  負債權益比: 181.23
  流動比率: 0.98
  速動比率: 0.85
  總現金: $61.56十億
  總負債: $111.09十億

📈 獲利能力:
  股東權益報酬率 (ROE): 147.35%
  資產報酬率 (ROA): 22.07%
  淨利率: 26.44%
  營業利益率: 31.14%
  毛利率: 46.25%
...
```

## 🔧 技術堆疊

| 類別 | 技術 |
|------|------|
| 程式語言 | Python 3.12+ |
| 資料來源 | yfinance, FRED API |
| 資料庫 | SQL Server |
| 主要套件 | pandas, pyodbc, python-dotenv |

## 📝 資料庫結構

系統會自動建立以下資料表:

- `fundamental_data_tw`: 台股基本面資料
- `fundamental_data_us`: 美股基本面資料
- `fundamental_data_two`: 興櫃市場資料
- `fundamental_data_cpi_us`: 美國CPI資料
- `fundamental_data_nfp_us`: 美國NFP資料
- `fundamental_data_oil`: WTI原油價格資料
- `fundamental_data_gold`: 黃金期貨價格資料

所有資料表皆包含 `lastUpdate` 欄位,記錄最後更新時間。

## ⚠️ 注意事項

1. **API限制**: FRED API有每日請求次數限制,請合理使用
2. **資料更新**: 股票資料依賴yfinance,可能有延遲
3. **市場休市**: 休市期間無法取得即時資料
4. **資料庫權限**: 確保資料庫使用者有建表及讀寫權限

## 🤝 貢獻

歡迎提交 Issue 或 Pull Request!

## 📄 授權

本專案採用 MIT 授權條款

## 📮 聯絡方式

如有問題或建議,歡迎開啟 Issue 討論。
