import subprocess
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


def run_git_command(directory: str, args: list[str]) -> tuple[str, str, int]:
    """在指定目录下执行 git 命令，返回 (stdout, stderr, returncode)。"""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=directory,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", "git 命令未找到，请确认已安装 git", 1


def generate_commit_message(directory: str, api_key: str) -> None:
    # 1. 运行 git status
    print(">>> 正在运行 git status ...")
    status_out, status_err, status_code = run_git_command(directory, ["status"])
    if status_code != 0:
        print(f"git status 执行失败：{status_err}", file=sys.stderr)
        sys.exit(1)
    print(status_out)

    # 2. 运行 git --no-pager diff --staged
    print(">>> 正在运行 git --no-pager diff --staged ...")
    diff_out, diff_err, diff_code = run_git_command(
        directory, ["--no-pager", "diff", "--staged"]
    )
    if diff_code != 0:
        print(f"git diff --staged 执行失败：{diff_err}", file=sys.stderr)
        sys.exit(1)

    if not diff_out.strip():
        print("没有检测到已暂存（staged）的变更，请先使用 git add 暂存文件后再运行。")
        sys.exit(0)

    # 3. 构建 prompt
    prompt = f"""请根据以下 git 信息，生成一个简洁、清晰的 git commit message。

要求：
- 使用英文
- 首行为简短摘要，不超过 72 个字符
- 遵循 Conventional Commits 规范（如 feat、fix、refactor、docs、chore 等前缀）
- 如有必要，可在空行后附上简短的正文描述
- 直接输出 commit message，不需要任何额外解释

--- git status ---
{status_out}

--- git diff --staged ---
{diff_out}
"""

    # 4. 调用 ZhipuAI/GLM-5
    client = OpenAI(
        base_url="https://api-inference.modelscope.cn/v1",
        api_key=api_key,
    )

    print(">>> 正在生成 commit message ...\n")

    response = client.chat.completions.create(
        model="ZhipuAI/GLM-5",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    done_reasoning = False
    for chunk in response:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        reasoning_chunk = getattr(delta, "reasoning_content", None) or ""
        answer_chunk = delta.content or ""

        if reasoning_chunk:
            print(reasoning_chunk, end="", flush=True)
        elif answer_chunk:
            if not done_reasoning:
                print("\n\n=== Generated Commit Message ===\n")
                done_reasoning = True
            print(answer_chunk, end="", flush=True)

    print()  # 末尾换行


def main() -> None:
    if len(sys.argv) < 2:
        print("用法：python solution.py <git仓库目录> [ModelScope API Key]")
        print("      API Key 默认从 .env 文件读取，或通过环境变量 MODELSCOPE_API_KEY 获取")
        sys.exit(1)

    directory = sys.argv[1]

    if not os.path.isdir(directory):
        print(f"错误：'{directory}' 不是有效目录", file=sys.stderr)
        sys.exit(1)

    # API Key 优先级：命令行参数 > 环境变量（从 .env 文件）
    if len(sys.argv) >= 3:
        api_key = sys.argv[2]
    else:
        api_key = os.environ.get("MODELSCOPE_API_KEY", "")

    if not api_key:
        print("错误：未提供 API Key，请在 .env 文件中设置 MODELSCOPE_API_KEY，或通过命令行参数传入。",
              file=sys.stderr)
        sys.exit(1)

    generate_commit_message(directory, api_key)


if __name__ == "__main__":
    main()
