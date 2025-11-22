# 🚀 部署指南

## 快速部署到 Streamlit Cloud

### 第一步：上传代码到 GitHub

在项目目录打开终端，运行：

```bash
git init
git add .
git commit -m "Initial commit: Multi-user annotation system with Google Sheets"
git remote add origin https://github.com/BaoMutian/HumanEval.git
git branch -M main
git push -u origin main
```

### 第二步：部署到 Streamlit Cloud

1. 访问 **https://share.streamlit.io**
2. 使用 GitHub 账号登录
3. 点击 **"New app"**
4. 填写信息：
   - **Repository**: `BaoMutian/HumanEval`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. 点击 **"Deploy"**

### 第三步：配置 Google Sheets（推荐）

> 不配置也能运行，但数据在应用重启后会丢失

1. 按照 [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md) 创建 Service Account
2. 在 Streamlit Cloud 应用设置中添加 Secrets：

```toml
USE_GSHEETS = "true"
GSHEET_NAME = "HumanEval_Results"

[gcp_service_account]
type = "service_account"
project_id = "你的项目ID"
private_key_id = "你的密钥ID"
private_key = "-----BEGIN PRIVATE KEY-----\n你的私钥\n-----END PRIVATE KEY-----\n"
client_email = "你的service-account@你的项目.iam.gserviceaccount.com"
client_id = "你的客户端ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "你的证书URL"
```

3. 保存并重启应用

## 🎉 完成！

部署完成后，您会得到一个公开链接，例如：
```
https://baomutian-humaneval-app-xxxxx.streamlit.app
```

将这个链接分享给标注者，每个人输入自己的姓名即可开始标注！

## 📊 两种存储模式对比

| 特性 | 本地存储 | Google Sheets |
|------|---------|--------------|
| 配置难度 | ⭐ 简单 | ⭐⭐⭐ 需要配置 |
| 数据持久化 | ❌ 重启丢失 | ✅ 永久保存 |
| 实时查看 | ❌ 无法查看 | ✅ 随时查看 |
| 数据导出 | ⚠️ 需要额外操作 | ✅ 一键导出 |
| 多人协作 | ✅ 支持 | ✅ 支持 |
| 推荐场景 | 本地测试 | 线上部署 |

## 💡 使用建议

### 快速测试（不配置 Google Sheets）
适合快速体验功能，但标注数据会在应用重启后丢失。

### 正式标注（配置 Google Sheets）
适合正式的标注任务，数据永久保存在云端，方便查看和分析。

## 🔗 相关链接

- [Streamlit Cloud 文档](https://docs.streamlit.io/streamlit-community-cloud)
- [Google Sheets API 文档](https://developers.google.com/sheets/api)
- [GitHub 仓库](https://github.com/BaoMutian/HumanEval)

