import argparse
from fund.services.config_service import ConfigService
from fund.services.database_service import DatabaseService
from fund.services.fundamental_data_service import FundamentalDataService

# ANSI 顏色碼
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

def colored_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def format_number(value, format_type='general'):
    """格式化數字顯示"""
    if value is None:
        return 'N/A'
    
    if format_type == 'currency':
        if value >= 1e12:
            return f"${value/1e12:.2f}兆"
        elif value >= 1e9:
            return f"${value/1e9:.2f}十億"
        elif value >= 1e6:
            return f"${value/1e6:.2f}百萬"
        else:
            return f"${value:,.0f}"
    elif format_type == 'percentage':
        return f"{value*100:.2f}%" if value else 'N/A'
    elif format_type == 'ratio':
        return f"{value:.2f}" if value else 'N/A'
    else:
        return str(value) if value else 'N/A'

def display_fundamental_data(symbol, data):
    """顯示基本面資料"""
    print(f"\n{'='*60}")
    print(f"  {symbol} - {data.get('shortName', 'N/A')} 基本面分析")
    print(f"{'='*60}")
    
    # 基本資訊
    print("\n📊 基本資訊:")
    print(f"  產業: {data.get('industry', 'N/A')}")
    print(f"  板塊: {data.get('sector', 'N/A')}")
    print(f"  國家: {data.get('country', 'N/A')}")
    print(f"  交易所: {data.get('exchange', 'N/A')}")
    print(f"  貨幣: {data.get('currency', 'N/A')}")
    
    # 估值指標
    print("\n💰 估值指標:")
    print(f"  市值: {format_number(data.get('marketCap'), 'currency')}")
    print(f"  本益比 (P/E): {format_number(data.get('trailingPE'), 'ratio')}")
    print(f"  預估本益比: {format_number(data.get('forwardPE'), 'ratio')}")
    print(f"  股價淨值比 (P/B): {format_number(data.get('priceToBook'), 'ratio')}")
    print(f"  股價營收比 (P/S): {format_number(data.get('priceToSales'), 'ratio')}")
    print(f"  PEG比率: {format_number(data.get('pegRatio'), 'ratio')}")
    
    # 財務健康度
    print("\n🏥 財務健康度:")
    print(f"  負債權益比: {format_number(data.get('debtToEquity'), 'ratio')}")
    print(f"  流動比率: {format_number(data.get('currentRatio'), 'ratio')}")
    print(f"  速動比率: {format_number(data.get('quickRatio'), 'ratio')}")
    print(f"  總現金: {format_number(data.get('totalCash'), 'currency')}")
    print(f"  總負債: {format_number(data.get('totalDebt'), 'currency')}")
    
    # 獲利能力
    print("\n📈 獲利能力:")
    print(f"  股東權益報酬率 (ROE): {format_number(data.get('returnOnEquity'), 'percentage')}")
    print(f"  資產報酬率 (ROA): {format_number(data.get('returnOnAssets'), 'percentage')}")
    print(f"  淨利率: {format_number(data.get('profitMargins'), 'percentage')}")
    print(f"  營業利益率: {format_number(data.get('operatingMargins'), 'percentage')}")
    print(f"  毛利率: {format_number(data.get('grossMargins'), 'percentage')}")
    
    # 成長性
    print("\n🚀 成長性:")
    print(f"  營收成長率: {format_number(data.get('revenueGrowth'), 'percentage')}")
    print(f"  盈餘成長率: {format_number(data.get('earningsGrowth'), 'percentage')}")
    print(f"  總營收: {format_number(data.get('totalRevenue'), 'currency')}")
    
    # 股利資訊
    print("\n💵 股利資訊:")
    print(f"  股利率: {format_number(data.get('dividendYield'), 'percentage')}")
    print(f"  股利金額: {format_number(data.get('dividendRate'), 'ratio')}")
    print(f"  配息率: {format_number(data.get('payoutRatio'), 'percentage')}")
    print(f"  除息日: {data.get('exDividendDate', 'N/A')}")
    
    # 股票資訊
    print("\n📊 股票資訊:")
    print(f"  Beta值: {format_number(data.get('beta'), 'ratio')}")
    print(f"  每股淨值: {format_number(data.get('bookValue'), 'ratio')}")
    print(f"  52週最高: {format_number(data.get('fiftyTwoWeekHigh'), 'ratio')}")
    print(f"  52週最低: {format_number(data.get('fiftyTwoWeekLow'), 'ratio')}")
    print(f"  平均成交量: {format_number(data.get('averageVolume'))}")

def main():
    parser = argparse.ArgumentParser(description='基本面資料查詢工具',add_help=False)
    
    # 建立子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 幫助訊息
    help_parser = subparsers.add_parser('help', help='顯示幫助訊息')

    # add 子命令 - 基本面資料查詢
    add_parser = subparsers.add_parser('add', help='查詢並儲存基本面資料')

    # 市場選項
    add_parser.add_argument('symbols', nargs='*', help='股票代號列表 (例: 2330 AAPL)')
    add_parser.add_argument('--tw', action='store_true', help='台股市場')
    add_parser.add_argument('--us', action='store_true', help='美股市場')
    add_parser.add_argument('--two', action='store_true', help='台灣興櫃市場')
    add_parser.add_argument('--etf', action='store_true', help='ETF')
    add_parser.add_argument('--index', action='store_true', help='指數')
    add_parser.add_argument('--crypto', action='store_true', help='加密貨幣')
    add_parser.add_argument('--forex', action='store_true', help='外匯')
    add_parser.add_argument('--futures', action='store_true', help='期貨')

    # 經濟指標選項
    add_parser.add_argument('--cpi', action='store_true', help='查詢美國CPI')
    add_parser.add_argument('--nfp', action='store_true', help='查詢美國NFP')
    add_parser.add_argument('--oil', action='store_true', help='查詢WTI原油價格')
    add_parser.add_argument('--gold', action='store_true', help='查詢黃金期貨價格')

    # 日期範圍選項
    add_parser.add_argument('--start_date', type=str, help='查詢起始日期 (yyyy/mm/dd)')
    add_parser.add_argument('--end_date', type=str, help='查詢結束日期 (yyyy/mm/dd)')

    # db 子命令 - 資料庫管理
    db_parser = subparsers.add_parser('db', help='資料庫配置與管理')

    # 資料庫配置
    db_parser.add_argument('--host', type=str, help='設定資料庫位址')
    db_parser.add_argument('--database', type=str, help='設定資料庫名稱')
    db_parser.add_argument('--user', type=str, help='設定資料庫使用者名稱')
    db_parser.add_argument('--password', type=str, help='設定資料庫使用者密碼')
    db_parser.add_argument('--driver', type=str, help='設定資料庫驅動程式名稱')
    db_parser.add_argument('--clear', action='store_true', help='清除資料庫設置')
    
    # fred 子命令 - FRED API 管理
    fred_parser = subparsers.add_parser('fred', help='FRED API 配置')
    fred_parser.add_argument('--fred', type=str, help='設定 FRED API Key')
    fred_parser.add_argument('--clear', action='store_true', help='清除 FRED API Key')

    args = parser.parse_args()
    
    # 顯示幫助訊息
    if args.command=='help' or args.command is None:
         show_help()
         return
    
    # 處理 add 子命令 - 基本面資料查詢
    if args.command == 'add':
        service = FundamentalDataService()
        
        # CPI/NFP/OIL/GOLD 查詢
        if args.cpi:
            try:
                if args.start_date and args.end_date:
                    print(f"正在獲取美國CPI期間資料: {args.start_date} ~ {args.end_date}")
                    cpi_list = service.fetch_and_store_cpi_us_range(args.start_date, args.end_date)
                    print("✓ 美國CPI期間資料:")
                    for cpi_data in cpi_list:
                        print(f"  日期={cpi_data['date']} 數值={cpi_data['value']}（指數）")
                    print("CPI期間資料已成功儲存")
                else:
                    print("正在獲取美國CPI...")
                    cpi_data = service.fetch_and_store_cpi_us()
                    print(f"✓ 美國CPI最新資料: 日期={cpi_data['date']} 數值={cpi_data['value']}（指數）")
                    print("CPI已成功儲存")
            except Exception as e:
                print(f"✗ 美國CPI獲取失敗: {str(e)}")
            return

        if args.nfp:
            try:
                if args.start_date and args.end_date:
                    print(f"正在獲取美國NFP期間資料: {args.start_date} ~ {args.end_date}")
                    nfp_list = service.fetch_and_store_nfp_us_range(args.start_date, args.end_date)
                    print("✓ 美國NFP期間資料:")
                    for nfp_data in nfp_list:
                        print(f"  日期={nfp_data['date']} 數值={nfp_data['value']}（千人）")
                    print("NFP期間資料已成功儲存")
                else:
                    print("正在獲取美國NFP...")
                    nfp_data = service.fetch_and_store_nfp_us()
                    print(f"✓ 美國NFP最新資料: 日期={nfp_data['date']} 數值={nfp_data['value']}（千人）")
                    print("NFP已成功儲存")
            except Exception as e:
                print(f"✗ 美國NFP獲取失敗: {str(e)}")
            return

        if args.oil:
            try:
                if args.start_date and args.end_date:
                    print(f"正在獲取WTI原油價格期間資料: {args.start_date} ~ {args.end_date}")
                    oil_list = service.fetch_and_store_oil_price_range(args.start_date, args.end_date)
                    print("✓ WTI原油價格期間資料:")
                    for oil_data in oil_list:
                        print(f"  日期={oil_data['date']} 價格={oil_data['value']} (USD)")
                    print("WTI原油價格期間資料已成功儲存")
                else:
                    print("正在獲取WTI原油最新價格...")
                    oil_data = service.fetch_and_store_oil_price()
                    print(f"✓ WTI原油最新價格: 日期={oil_data['date']} 價格={oil_data['value']} (USD)")
                    print("WTI原油價格已成功儲存")
            except Exception as e:
                print(f"✗ WTI原油價格獲取失敗: {str(e)}")
            return

        if args.gold:
            try:
                if args.start_date and args.end_date:
                    print(f"正在獲取黃金期貨價格期間資料: {args.start_date} ~ {args.end_date}")
                    gold_list = service.fetch_and_store_gold_price_range(args.start_date, args.end_date)
                    print("✓ 黃金期貨價格期間資料:")
                    for gold_data in gold_list:
                        print(f"  日期={gold_data['date']} 價格={gold_data['value']} (USD)")
                    print("黃金期貨價格期間資料已成功儲存")
                else:
                    print("正在獲取黃金期貨最新價格...")
                    gold_data = service.fetch_and_store_gold_price()
                    print(f"✓ 黃金期貨最新價格: 日期={gold_data['date']} 價格={gold_data['value']} (USD)")
                    print("黃金期貨價格已成功儲存")
            except Exception as e:
                print(f"✗ 黃金期貨價格獲取失敗: {str(e)}")
            return

        # 股票基本面查詢
        if not args.symbols:
            print("請提供至少一個股票代號或指定查詢類型")
            print("範例: fund add 2330 --tw")
            print("      fund add AAPL --us")
            print("      fund add --cpi")
            return
        
        # 確定市場類型
        market = None
        if args.tw:
            market = 'tw'
        elif args.us:
            market = 'us'
        elif args.two:
            market = 'two'
        elif args.etf:
            market = 'etf'
        elif args.index:
            market = 'index'
        elif args.crypto:
            market = 'crypto'
        elif args.forex:
            market = 'forex'
        elif args.futures:
            market = 'futures'
        else:
            print("請指定市場類型 (例: --tw, --us, --crypto)")
            return
        
        for symbol in args.symbols:
            try:
                print(f"正在處理 {symbol} ({market})...")
                result = service.fetch_and_store(symbol, market)
                print(f"✓ {symbol} 基本面資料已成功儲存")
                
                # 使用新的顯示函數
                display_fundamental_data(symbol, result)
                
            except Exception as e:
                print(f"✗ {symbol} 處理失敗: {str(e)}")
    
    # 處理 db 子命令 - 資料庫配置與管理
    elif args.command == 'db':
        config_service = ConfigService()
        db_service = DatabaseService()
        
        if args.clear:
            confirm = input("Confirm to clear all database settings? (yes/no): ")
            if confirm.lower() == 'yes':
                message = config_service.clear_db_config()
                print(f"✓ {message}")
            else:
                print("Operation cancelled")
            return
        
        if args.host or args.database or args.user or args.password or args.driver:
            message = config_service.update_db_config(
                server=args.host,
                database=args.database,
                username=args.user,
                password=args.password,
                driver=args.driver
            )
            print(f"✓ {message}")
        
        # 顯示配置資訊
        #print("\n")
        config = config_service.show_db_config()
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        # 測試連線
        print("\n")
        success, message = db_service.test_connection()
        print(f"  {message}")
        
        # 列出資料表
        print("\n")
        success, tables = db_service.list_tables()
        if success and tables:
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
        else:
            print("not available tables.")
    
    # 處理 fred 子命令 - FRED API 配置
    elif args.command == 'fred':
        config_service = ConfigService()
        
        if args.clear:
            confirm = input("Confirm to clear FRED API Key? (yes/no): ")
            if confirm.lower() == 'yes':
                message = config_service.clear_fred_config()
                print(f"✓ {message}")
            else:
                print("Operation cancelled")
            return
        
        if args.fred:
            message = config_service.update_fred_config(args.fred)
            print(f"✓ {message}")
        
        # 顯示 FRED API 配置
        #print("\n")
        config = config_service.show_fred_config()
        for key, value in config.items():
            print(f"  {key}: {value}")

def show_help():
    """幫助訊息"""
    help_text = f"""
{colored_text('Fundamental Analysis System', Colors.BOLD + Colors.CYAN)}

{colored_text('Basic Usage:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('fund', Colors.GREEN)} {colored_text('[command]', Colors.BLUE)} {colored_text('[options]', Colors.MAGENTA)}

{colored_text('Subcommands:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('fund add', Colors.GREEN)}                             Query and store fundamental data
  {colored_text('fund db', Colors.GREEN)}                              Database configuration and management
  {colored_text('fund fred', Colors.GREEN)}                            FRED API configuration

{colored_text('Fundamental Data Query:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('fund add', Colors.GREEN)} {colored_text('<stock_symbol>', Colors.BLUE)} {colored_text('--<market>', Colors.MAGENTA)}   Query stock fundamental data
  {colored_text('fund add --cpi', Colors.GREEN)}                       Query US CPI
  {colored_text('fund add --nfp', Colors.GREEN)}                       Query US NFP
  {colored_text('fund add --oil', Colors.GREEN)}                       Query WTI Oil Price
  {colored_text('fund add --gold', Colors.GREEN)}                      Query Gold Futures Price

{colored_text('Market Options:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('--tw', Colors.MAGENTA)}        Taiwan Stock Exchange
  {colored_text('--two', Colors.MAGENTA)}       Taiwan OTC Exchange
  {colored_text('--us', Colors.MAGENTA)}        US Stock Market
  {colored_text('--forex', Colors.MAGENTA)}     Foreign Exchange
  {colored_text('--crypto', Colors.MAGENTA)}    Cryptocurrency

{colored_text('Database Configuration:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('fund db --host', Colors.GREEN)} {colored_text('<address>', Colors.BLUE)}             Set database host
  {colored_text('fund db --database', Colors.GREEN)} {colored_text('<name>', Colors.BLUE)}            Set database name
  {colored_text('fund db --user', Colors.GREEN)} {colored_text('<username>', Colors.BLUE)}            Set database username
  {colored_text('fund db --password', Colors.GREEN)} {colored_text('<password>', Colors.BLUE)}        Set database password
  {colored_text('fund db --driver', Colors.GREEN)} {colored_text('<driver>', Colors.BLUE)}            Set database driver
  {colored_text('fund db --clear', Colors.GREEN)}                      Clear all database settings

{colored_text('FRED API Configuration:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('fund fred --fred', Colors.GREEN)} {colored_text('<API_Key>', Colors.BLUE)}           Set FRED API Key
  {colored_text('fund fred --clear', Colors.GREEN)}                    Clear FRED API Key

{colored_text('Usage Examples:', Colors.BOLD + Colors.YELLOW)}
  {colored_text('# Configure database', Colors.GRAY)}
  {colored_text('fund db --host localhost --database FundDB --user sa --password YourPassword', Colors.GREEN)}
  
  {colored_text('# Configure FRED API', Colors.GRAY)}
  {colored_text('fund fred --fred your_fred_api_key_here', Colors.GREEN)}
  
  {colored_text('# View configuration', Colors.GRAY)}
  {colored_text('fund db', Colors.GREEN)}
  {colored_text('fund fred', Colors.GREEN)}
  
  {colored_text('# Query stocks', Colors.GRAY)}
  {colored_text('fund add AAPL --us', Colors.GREEN)}
  {colored_text('fund add 2330 --tw', Colors.GREEN)}
  
  {colored_text('# Query economic indicators', Colors.GRAY)}
  {colored_text('fund add --cpi --start_date 2008/08/01 --end_date 2025/10/01', Colors.GREEN)}
  {colored_text('fund add --nfp', Colors.GREEN)}
  {colored_text('fund add --oil', Colors.GREEN)}
  {colored_text('fund add --gold', Colors.GREEN)}
"""
    print(help_text)