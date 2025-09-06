import asyncio
import os
import re
import streamlit as st

from config.open_ai_model_client import get_Model_Client
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from teams.automation_Team import get_MCP_team

st.title("AutoGen Project for UI Automation using Playwright MCP")

uploaded_file = st.file_uploader("Upload your test cases file", type="txt")
show_verbose = st.toggle("Show verbose MCP logs", value=False)

task = None
if uploaded_file is not None:
    test_cases = uploaded_file.read().decode("utf-8")
    st.write("📂 File uploaded successfully!")
    st.text_area("File Content", test_cases, height=300)
    task = test_cases  # use file content as task


# ---------- helpers ----------
CODE_FENCE_RE = re.compile(r"```([\w+\-]*)\n(.*?)```", re.DOTALL)

def extract_code_blocks(text: str):
    """Return list of (lang, code) blocks from text. Fallback to heuristics for Playwright code."""
    if not text:
        return []

    blocks = []
    # 1) Fenced blocks
    for m in CODE_FENCE_RE.finditer(text):
        lang = (m.group(1) or "").strip()
        code = m.group(2).strip()
        if code:
            blocks.append((lang, code))
    if blocks:
        return blocks

    # 2) Heuristic: detect Playwright-like code even if not fenced
    if re.search(r"\bpage\.(goto|fill|type|click|locator|get_by|wait_for_)", text) or \
       "async_playwright" in text or \
       "@playwright/test" in text or \
       "using Microsoft.Playwright" in text:
        blocks.append(("", text.strip()))
    return blocks

def detect_lang(code: str) -> str:
    c = code.lower()
    if "from playwright" in c or "async def" in c or "await page" in c:
        return "python"
    if "@playwright/test" in c or "import { test" in c:
        return "typescript"
    if "using microsoft.playwright" in c:
        return "csharp"
    return "python"

def is_accessibility_tree(text: str) -> bool:
    """Detects raw accessibility tree dumps like '- generic [ref=…]'"""
    if not text:
        return False
    stripped = text.strip()
    return stripped.startswith("- generic") or stripped.startswith("generic [ref=") or "ref=" in stripped


# ---------- main stream ----------
async def run_analuser_gpt(task, openai_model_client):
    try:
        team = await get_MCP_team(openai_model_client)

        async for message in team.run_stream(task=task):
            src = getattr(message, "source", "Unknown")
            content = getattr(message, "content", None)

            # 1) Final result status
            if isinstance(message, TaskResult):
                st.success(f"✅ Stop reason: {message.stop_reason}")
                continue

            # 2) Plain agent text
            if isinstance(message, TextMessage):
                if is_accessibility_tree(str(content)):
                    continue  # 🚫 skip accessibility tree dumps

                blocks = extract_code_blocks(str(content))
                if blocks:
                    st.markdown(f"🧠 **{src} (code)**")
                    for lang, code in blocks:
                        st.code(code, language=lang or detect_lang(code))
                elif content:
                    st.markdown(f"🗒️ **{src}:** {content}")
                continue

            # 3) Tool/other events
            if isinstance(content, list):
                showed_any_code = False
                for item in content:
                    txt = getattr(item, "content", None)
                    name = getattr(item, "name", "")

                    if not isinstance(txt, str) or is_accessibility_tree(txt):
                        continue  # 🚫 skip tree noise

                    # snapshots only if verbose
                    if name in {"browser_snapshot", "console", "page_snapshot"}:
                        if show_verbose:
                            st.markdown(f"🔎 **{src} · {name}**")
                            st.text(txt)
                        continue

                    blocks = extract_code_blocks(txt)
                    if blocks:
                        if not showed_any_code:
                            st.markdown(f"🤖 **{src} (generated code)**")
                            showed_any_code = True
                        for lang, code in blocks:
                            st.code(code, language=lang or detect_lang(code))
                    else:
                        st.markdown(f"🗒️ **{src}:** {txt}")
                continue

            # 4) Fallback: only if verbose
            if show_verbose and content and not is_accessibility_tree(str(content)):
                st.write(f"🔎 {src}: {content}")

    except Exception as e:
        st.error(f"Error during team execution: {e}")
        return e


if st.button("Run Analysis"):
    if uploaded_file is not None:
        os.makedirs("temp", exist_ok=True)
        with open("temp/data.txt", "wb") as f:
            f.write(uploaded_file.getbuffer())
        openai_model_client = get_Model_Client()
        asyncio.run(run_analuser_gpt(task, openai_model_client))
    else:
        st.warning("Please upload a TXT file.")