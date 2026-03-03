这份 `git_commit_assistant.py` 脚本是一个非常实用的工具，它通过 AI（基于 ModelScope 的 ZhipuAI/GLM-5 模型）自动分析你的代码变更并生成符合规范的 Git Commit Message。

以下是为您准备的详细 README 文档：

---

# Git Commit Assistant (AI-Powered)

**Git Commit Assistant** 是一个基于 Python 的自动化工具，旨在利用大语言模型（LLM）为你生成的代码变更提供精准、专业且符合规范的提交说明（Commit Message）。

它会自动运行 `git status` 和 `git diff`，分析已暂存（staged）的更改，并调用 **ModelScope** 上的 **ZhipuAI/GLM-5** 模型来撰写提交信息。

## 🌟 核心功能

* **自动差异分析**：自动提取 `git status` 和 `git diff --staged` 的内容作为上下文。
* **遵循行业规范**：生成的提交信息严格遵循 **Conventional Commits** 规范（如 `feat`, `fix`, `docs`, `refactor` 等）。
* **流式推理显示**：支持流式输出，你可以实时看到 AI 的思维链（Reasoning）和生成的最终信息。
* **多渠道配置**：支持通过 `.env` 文件、环境变量或命令行参数直接传入 API Key。

## 🛠️ 环境要求

* **Python**: 3.7+
* **Git**: 系统已安装并配置好 Git。
* **依赖库**:
```bash
pip install openai python-dotenv

```



## 🚀 快速上手

### 1. 获取 API Key

由于脚本默认使用 ModelScope 的接口，你需要从 [ModelScope (魔搭社区)](https://modelscope.cn/) 获取有效的 API Key。

### 2. 配置 API Key

你可以通过以下两种方式之一配置 Key：

* **方式 A（推荐）**：在脚本同级目录下创建 `.env` 文件：
```text
MODELSCOPE_API_KEY=你的_API_Key_在此

```


* **方式 B**：在执行脚本时作为参数传入。

### 3. 使用步骤

在准备提交代码时，先在你的 Git 项目中暂存文件，然后运行此脚本：

```bash
# 1. 暂存更改
git add .

# 2. 运行助手 (假设脚本在当前目录)
python git_commit_assistant.py <你的Git项目路径> [可选API_Key]

```

## 📝 脚本工作流程

1. **检查环境**：确认 Git 命令可用且目录合法。
2. **提取上下文**：
* 执行 `git status` 获取文件状态。
* 执行 `git --no-pager diff --staged` 获取具体的代码增减。


3. **构建 Prompt**：将上述信息封装并要求 AI 输出简洁、清晰、不超过 72 字符摘要的英文提交信息。
4. **AI 生成**：连接至 `https://api-inference.modelscope.cn/v1`，使用 `ZhipuAI/GLM-5` 模型进行推理。
5. **展示结果**：实时显示 AI 的思考过程（如果有）和最终生成的 Commit Message。

## ⚠️ 注意事项

* **暂存区检查**：如果没有任何文件被 `git add`，脚本会提示并退出。
* **编码限制**：摘要行被限制在 72 个字符以内，以保持 Git 历史的最佳可读性。
* **安全性**：请勿将包含 API Key 的 `.env` 文件上传到公共仓库。

---

**想要我为您把这段 README 转换成英文版，或者为您添加一个自动安装依赖的 shell 脚本吗？**