# GeoQA Human Evaluation System

一个用于 GeoQA 数据集人工评估的 Streamlit 应用，支持多人同时在线标注。

## ✨ 功能特点

- 👥 **多人标注**：支持多个标注者同时使用，每人的结果独立保存
- ☁️ **云端存储**：支持 Google Sheets 云端存储，数据永久保存
- 📊 **实时统计**：显示标注进度和评分相关性分析
- 🎯 **智能评分**：根据任务类型自动调整评分标准
- 🔄 **自动导航**：保存后自动跳转到下一条未标注记录
- 💾 **双模式**：支持本地文件存储和云端 Google Sheets 存储

## 任务类型与评分标准

| 任务类型                         | 推理得分 | 答案得分 | 总分 |
| -------------------------------- | -------- | -------- | ---- |
| distance, direction, relation-\* | 0-15     | 0-10     | 25   |
| planning 及其他                  | 0-20     | 0-10     | 30   |

## 🚀 快速开始

### 📱 在线使用（推荐）

直接访问部署的链接，输入姓名即可开始标注。

### 💻 本地运行

1. 克隆仓库：
```bash
git clone https://github.com/BaoMutian/HumanEval.git
cd HumanEval
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
streamlit run app.py
```

4. 在侧边栏输入您的姓名开始标注

### ☁️ 部署到 Streamlit Cloud

详细部署步骤请参考 [DEPLOYMENT.md](./DEPLOYMENT.md)

配置 Google Sheets 云端存储请参考 [GOOGLE_SHEETS_SETUP.md](./GOOGLE_SHEETS_SETUP.md)

## 📁 文件说明

- `app.py` - 主应用程序（支持本地和云端存储）
- `judge_prompt.py` - 评分标准定义
- `requirements.txt` - Python 依赖包
- `100_llama3.1-70b-instruct_human_eval_gpt-4o.jsonl` - 待标注数据
- `geoqa_reason/full_dataset.jsonl` - 完整数据集（包含问题）
- `human_eval_results/` - 标注结果保存目录（本地模式）
- `DEPLOYMENT.md` - 部署指南
- `GOOGLE_SHEETS_SETUP.md` - Google Sheets 配置指南

## 📊 数据存储

### 本地模式
标注结果保存在 `human_eval_results/` 目录下，格式为 `human_eval_results_姓名.jsonl`

### Google Sheets 模式
每个标注者有独立的工作表，数据实时同步到云端，支持：
- 实时查看所有标注者的进度
- 一键导出为 Excel/CSV
- 在线数据分析和统计

### 记录格式

每条标注记录包含：
- `id` - 记录 ID
- `annotator_name` - 标注者姓名
- `human_reason_score` - 推理得分
- `human_answer_score` - 答案得分
- `human_total_score` - 总分
- `task_type` - 任务类型
- `timestamp` - 标注时间（仅 Google Sheets）
- `original_record` - 原始数据（仅本地模式）

## 作者

BaoMutian

## 许可证

MIT License
