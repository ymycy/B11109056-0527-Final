# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11109056 
**系級：** 資管系大四  
**姓名：** 洪敏瀞

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) | 用 f.readlines() 讀取"lib_data.txt"整個檔案的每一行 | file_lines |
| Q2 d2 (in main) | 程式的核心資料結構，在記憶體中保存所有書籍紀錄 | library_data |
| Q3 c_res (in check) | 檢查一個 ISBN 是否已經存在於資料(d2)中 | contains_isbn |

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：全域可變狀態 - d2 在 load_proc(), main() 和 c_res() 之間共享，增加了程式的耦合度，讓函式依賴隱性狀態，難以測試、維護與重構。

- **Q2：變數命名非常不清楚 - 例如 l1, d2, c_res 以及書籍字典鍵 t, i, s 可讀性極差，別人或未來自己都很難快速了解資料代表什麼，增加錯誤風險。

- **Q3：檔案讀寫沒有使用 with / 沒有例外處理 - 在函式中都直接用 close()，如果程式在讀寫中間發生錯誤，檔案可能無法正確關閉；也缺少 I/O 失敗時的錯誤處理，容易崩潰。

- **Q4：自訂文字格式解析脆弱 - 使用 @@ 和 ## 分隔檔案欄位，沒有檢查格式是否正確，如果檔案行格式不符合預期就會拋例外；也無法處理書名或狀態中本身包含這些符號的情況。

- **Q5：資料寫回只在 exit 執行 - 程式如果意外關閉、當機或被強制終止，新增資料會遺失，資料持久性不足，實務上不可靠。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好

Prompt B： 請幫我將程式進行模組化： 將功能拆解為類別 (Class) 或多個函式 (Function)，並直接給我程式碼就好

Prompt C：執行的時候，同一本書在出借狀態下如果重複輸入borrow他一樣會顯示updated，可以加入一個檢查 改成顯示已出借嗎
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？（例如：漏寫了某個功能、語法錯誤）你是如何發現並請它修正的？
- 沒有出什麼錯誤，但是一開始沒有明確說要將修正的放在新檔案，他會想直接幫我改在原始檔案中，只要告訴他我要放在哪個具體的檔案中就成功了

2. 發現的問題： (範例：AI 漏掉了 exit 時要印出分類統計的功能)
- 在出借狀態中重複出借這個問題他沒有發現到，其餘的沒有大問題

3. 修正的對話： (範例：我告訴它「請在結束前迴圈遍歷 JSON 資料並計算分類總額」)
- 告訴它 請幫我在出借時檢查狀態，並正確顯示已出借，不要重複出借。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
PS C:\Users\pclab\Desktop\NTUST-0527-Final-master> & C:/Users/pclab/AppData/Local/Programs/Python/Python313/python.exe c:/Users/pclab/Desktop/NTUST-0527-Final-master/modern_library.py
=== 圖書管理系統 v0.1 (Legacy) ===
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
# 請在此處貼上 git log 內容
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
# 請貼上你的 Repo 網址
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
