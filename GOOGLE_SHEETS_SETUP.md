# Google Sheets 配置指南

本应用支持使用 Google Sheets 作为云端存储，适合多人在线协作标注。

## 📋 配置步骤

### 1. 创建 Google Cloud Service Account

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Google Sheets API** 和 **Google Drive API**：
   - 导航到 "APIs & Services" > "Library"
   - 搜索并启用这两个 API

4. 创建 Service Account：
   - 导航到 "APIs & Services" > "Credentials"
   - 点击 "Create Credentials" > "Service Account"
   - 填写名称（如 "humaneval-annotator"）
   - 点击 "Create and Continue"
   - 跳过权限设置，点击 "Done"

5. 创建密钥：
   - 点击刚创建的 Service Account
   - 切换到 "Keys" 标签
   - 点击 "Add Key" > "Create new key"
   - 选择 **JSON** 格式
   - 下载 JSON 文件（妥善保管！）

### 2. 配置 Streamlit Cloud

1. 在 Streamlit Cloud 中打开您的应用设置
2. 找到 "Secrets" 部分
3. 添加以下内容（替换为您的 JSON 文件内容）：

```toml
# Google Sheets Configuration
USE_GSHEETS = "true"
GSHEET_NAME = "HumanEval_Results"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

4. 点击 "Save"

### 3. 创建并共享 Google Sheet（可选）

应用会自动创建名为 `HumanEval_Results` 的 Google Sheet，但您也可以手动创建：

1. 创建新的 Google Sheet，命名为 `HumanEval_Results`
2. 将 Sheet 共享给 Service Account 的邮箱：
   - 点击 "共享" 按钮
   - 输入 Service Account 的邮箱地址（在 JSON 文件的 `client_email` 字段）
   - 设置权限为 "编辑者"
   - 点击 "发送"

## 🎯 数据结构

每个标注者会有独立的工作表（worksheet），包含以下列：

| 列名 | 说明 |
|------|------|
| id | 记录ID |
| annotator_name | 标注者姓名 |
| reason_score | 推理得分 |
| answer_score | 答案得分 |
| total_score | 总分 |
| task_type | 任务类型 |
| timestamp | 标注时间 |
| response | 模型回答（截断） |
| ground_truth | 标准答案（截断） |
| question | 问题（截断） |

## 🔄 本地开发模式

如果想在本地使用 Google Sheets：

1. 下载 Service Account 的 JSON 文件
2. 创建 `.streamlit/secrets.toml` 文件
3. 添加配置（格式同上）
4. 运行应用

## 💾 切换回本地存储

如果不想使用 Google Sheets，可以：

1. 在 Streamlit Cloud Secrets 中删除或注释掉 `USE_GSHEETS = "true"`
2. 或设置为 `USE_GSHEETS = "false"`
3. 应用会自动切换回本地文件存储模式

## ⚠️ 注意事项

1. **Service Account JSON 文件包含敏感信息**，不要提交到 GitHub！
2. `.gitignore` 已配置忽略 `.streamlit/secrets.toml`
3. Google Sheets 免费版有以下限制：
   - 每个表格最多 1000 万个单元格
   - 每分钟 300 次读写请求
   - 通常足够标注使用

## 📊 查看结果

标注结果会实时保存到 Google Sheets，您可以：

1. 直接在 Google Sheets 中查看和编辑
2. 导出为 Excel、CSV 等格式
3. 使用 Google Sheets 的数据分析功能
4. 多人同时查看和分析结果

## 🆘 故障排除

### 错误：SpreadsheetNotFound
- 确保 Service Account 邮箱已被添加到 Sheet 的共享列表
- 或让应用自动创建（首次运行时）

### 错误：Permission denied
- 检查 Service Account 的权限是否为"编辑者"
- 确保已启用 Google Sheets API 和 Google Drive API

### 连接超时
- 检查网络连接
- Google API 可能暂时不可用，稍后重试

