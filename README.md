# 基金保管市場看板

使用投信投顧公會公開資料查詢境內基金保管市場。預設顯示全市場；可選擇任一保管行查看市占、排名、新基金趨勢，並比較不同保管行。

GitHub Actions 每天約台北時間 10:17 檢查來源更新時間，資料未變時不下載完整 CSV。新月份資料一致且通過品質檢查後才保存。前端 Site 讀取最新月份與資料檔，舊月份保留。資料每月更新，非即時。

原始檔：`data/raw/<年月>/`；計算結果：`public/data/<年月>.json`。

驗證與重算：

```bash
python3 tests/market_integrity.py
python3 pipeline/build_data.py --month 202608 --offline
python3 pipeline/build_data.py --mode auto
```

同基金不同級別算一檔，新基金依基金層級成立日計算，只含仍存續基金與國內保管行。
