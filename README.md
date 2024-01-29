<img src='static/red-envelopes.png' height=86 align='right' />

# New Year Lotter 新年紅包抽獎
做給家裡人玩的紅包抽獎的網頁小程式，~~把我沒太多錢這件事給合理化~~，使用Python & Flask 開發<br>

## 現有功能
- 紅包抽獎
  - 紀錄抽獎人數
  - 防止重複IP抽獎
- 後臺設定
  - 紅包數量
  - 最小 & 最大點擊次數
  - 讀/寫至設定檔 (`config.ini`)

## 未來功能 
- 過去IP連入紀錄
- Log文字檔
- *想到再說...*


# Build
- To Run This Project, You Will Need To Check That All The Packages Below Have Been Installed：
  - Python 3.10
  - Flask
  - Flask-admin
- Or, You Can Run This Command In Bash / Terminal To Install The Project：
```bash
pip install -r requirement.txt
```

# Run
```bash
python appmain.py
```

## License
本專案程式碼採用[啤酒軟體授權條款](https://en.wikipedia.org/wiki/Beerware)釋出