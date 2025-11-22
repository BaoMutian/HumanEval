# ⚡ 快速开始指南

## 🎯 目标
将标注系统部署到 Streamlit Cloud，实现多人在线标注，数据保存到 Google Sheets 云端。

## 📋 准备工作清单

- [ ] GitHub 账号
- [ ] Google 账号（用于 Google Sheets）
- [ ] 项目代码已准备好

## 🚀 三步部署

### 第一步：上传代码到 GitHub

#### 方法 A：使用批处理脚本（Windows，推荐）
双击运行 `push_to_github.bat`，按提示操作即可。

#### 方法 B：手动执行命令
在项目目录打开命令行，运行：
```bash
git init
git add .
git commit -m "Initial commit: Multi-user annotation system"
git remote add origin https://github.com/BaoMutian/HumanEval.git
git branch -M main
git push -u origin main
```

### 第二步：部署到 Streamlit Cloud

1. 访问 **https://share.streamlit.io**
2. 使用 GitHub 账号登录
3. 点击 **"New app"**
4. 填写信息：
   - Repository: `BaoMutian/HumanEval`
   - Branch: `main`
   - Main file path: `app.py`
5. 点击 **"Deploy"**
6. 等待 2-3 分钟，部署完成！

此时应用已经可以使用了，但是**数据会在重启后丢失**。

### 第三步：配置 Google Sheets（推荐）

#### 3.1 创建 Google Cloud Service Account

1. 访问 https://console.cloud.google.com/
2. 创建新项目（或选择现有项目）
3. 启用 API：
   - 搜索 "Google Sheets API" 并启用
   - 搜索 "Google Drive API" 并启用
4. 创建 Service Account：
   - 左侧菜单 → APIs & Services → Credentials
   - Create Credentials → Service Account
   - 名称填写：`humaneval-annotator`
   - 创建完成后，点击进入
   - Keys 标签 → Add Key → Create new key
   - 选择 JSON 格式下载

#### 3.2 配置 Streamlit Secrets

1. 在 Streamlit Cloud 中打开您的应用
2. 点击右下角 **"Settings"** → **"Secrets"**
3. 复制以下内容，替换为您的 JSON 文件内容：

```toml
USE_GSHEETS = "true"
GSHEET_NAME = "HumanEval_Results"

[gcp_service_account]
type = "service_account"
project_id = "geoeval-reason-humaneval"
private_key_id = "27b6ffa5e70ace06a975577903c53b0f70e53db0"
private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDO/7aWWEG8uW+8\nQGwPMCE8qSszd/RccLYsqAEQeF0G9HfWMUproeYM7Zc0MT81Mx0x57kRoOd+8YWP\nc6X/zfBTa2lPJ39YjKMNxOf8NUvgkIIdtgyl7U/d/Bxa3FBTupJBe/qWK1Us4R4E\nI4HwW+VPqPBYgalrm8TNS3FOuraLY/WJFr6UHHgVabgEdeoPnHqDFDOBZeDevZUj\n60hUGLdmxPG54j4GdgfkrbxpfQq9PeVd1a1hKmg09kax5adGPr56l5TJDKoRR/pR\nIwPIMIFy7CaIUhgydVKW7UDVNg5heB0RnYyPitY6uKz05iRyyJUDXZ91GcAGcTHy\nI6zIKU6DAgMBAAECgf9o8gqb5FzKh3tk4TP4XkD/td2H7CPaqXvDgwa0iKQMvXmA\nCflJ2mwOGaCsE1P0TiM448rC75LyeqG8NdExNnWVH8svrPvfJuoIBK+YvxoHehMB\n3C186fkLv9puywn/JyBBhpWZxrk6yb32UvFw9za6pBln/6+vwfLPXELwzIczlwf9\nGjw38xOcrXBkTjzovjmXC0YtOtF7WJBf1xllGl60MhhsCzwA34f0rGDNLWQNRWZb\njnkpckIjkKUq7ajchigxeZ/eCBZvuH8rLaz1jCK767j8QcAJp4oYDB/Mi8yRnr7w\nVXaxO/xZqMCP9AA3MgcRPnWHxMDH6J5sZ1o+ivUCgYEA9Uu9Hz7TIHrtUtRRD3kM\nAPM6RFB6FL5/HcXS4FWitvo59KldSyqCPVQF8sUClsRa18SNTmse8j/lRbUn/4QW\ntReGvZzPAW5R5Q8WJTlFU3CLKazwLnit7yB256q3CHxaapUhyGhS14CFec/5y2ou\nEMmR+ajxusB476VY8KWKIO0CgYEA2AgmP3u77GYxaBLWuDAp5j8esibcSFIOuE8T\n4JQ4TXl09MiZ/JidUaGG1rxK3PLnolNZHraTvw4Bnlphe8MRECXqOpz/K9VRU9ya\nTKWC7pdoQ1Ex85RVBwBL3HGMglgGdRkZ6SHNQsSST06rrKfSod3D7bHgAmh0Th2Z\ntRlQ7y8CgYB7Vqb0pAlSxpy4TkuoBQx1GdfNa83GynZuSP8cj9KuQKmNjO99ERXF\nso7/H/KKTpcC8TDAInrAAkLNRyaigw9L5VV51/P6WzdQfsJ62w4xw2AmB3AJXeLP\nXzqKiDtaR/TKrMv80f/9ngD/XATVNEGPbVs59qn9ZjQpA7Hx5rrKjQKBgQCw6uOf\n484/yGU3zQ3JY7A8nn6d+VM3avQhHqmxptEBKbGNcechxT45BuZtX2CT1924wzdd\n/rm6olbS/0OMXnDP360V+VLD6/uhiS1YDcfPa3F4h7s3tsd3Z1e5HcirSjlnlnnw\nwbzerCsCBfRz/jByXTJCrAQ/FJoDCxzBAg2VAwKBgQCNitbQikOGpZkCU9TmYJ3s\nySqQ4MD1ozdc+84pYqXSIJNNMWpQbXHdqOHtd7o1Cqg9v5ytB7dRTTmNzUl0Q/gA\n7f+/br3TEkIIHWJbMe7T2tGjY31JT9j2i2kpnx1+zrxxfHGregYjM4f6H9FNpXxw\n9R6iutad3FajN5yMp/2Y5A==\n-----END PRIVATE KEY-----\n"
client_email = "humaneval-annotator@geoeval-reason-humaneval.iam.gserviceaccount.com"
client_id = "108544180731681786650"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/humaneval-annotator%40geoeval-reason-humaneval.iam.gserviceaccount.com"
```

4. 点击 **"Save"**
5. 应用会自动重启

#### 3.3 验证配置

打开应用，在侧边栏输入姓名后，应该看到 **"☁️ 云端存储: Google Sheets"**

## ✅ 完成！

现在您可以：
1. 分享应用链接给标注者
2. 每个人输入自己的姓名开始标注
3. 在 Google Sheets 中实时查看标注结果

## 📱 访问 Google Sheets

1. 访问 https://sheets.google.com
2. 找到名为 `HumanEval_Results` 的表格
3. 每个标注者有独立的工作表

## ⚠️ 注意事项

1. **不要将 Service Account JSON 文件提交到 GitHub**
2. 如果看不到 Google Sheet，检查：
   - Service Account 邮箱是否有权限
   - Secrets 配置是否正确
   - 应用是否已重启

## 🆘 遇到问题？

- 部署问题：查看 [DEPLOYMENT.md](./DEPLOYMENT.md)
- Google Sheets 配置：查看 [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md)
- 其他问题：检查 Streamlit Cloud 的日志

## 🎉 开始标注

一切就绪后，标注者只需要：
1. 打开应用链接
2. 输入姓名
3. 开始标注
4. 数据自动保存到云端

就这么简单！

