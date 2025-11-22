@echo off
echo ========================================
echo 准备上传代码到 GitHub
echo ========================================
echo.

REM 初始化 Git（如果还没有）
if not exist .git (
    echo [1/4] 初始化 Git 仓库...
    git init
) else (
    echo [1/4] Git 仓库已存在
)

echo.
echo [2/4] 添加所有文件...
git add .

echo.
echo [3/4] 提交更改...
git commit -m "Update: Multi-user annotation system with Google Sheets support"

echo.
echo [4/4] 推送到 GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/BaoMutian/HumanEval.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo 上传完成！
echo.
echo 下一步：
echo 1. 访问 https://share.streamlit.io
echo 2. 使用 GitHub 账号登录
echo 3. 选择 BaoMutian/HumanEval 仓库部署
echo ========================================
pause

