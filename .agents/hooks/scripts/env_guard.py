#!/usr/bin/env python3
"""
PreToolUse Hook: 가상환경 및 패키지 규정 준수 검사기
"""
import sys
import json
import re

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(raw_input)
        tool_call = payload.get("toolCall", {})
        args = tool_call.get("args", {})
        cmd = args.get("CommandLine", "")

        # 비인가 가상환경 생성 명령어 탐지
        forbidden_patterns = [
            r'conda\s+create',
            r'python[3]?\s+-m\s+venv',
            r'virtualenv\s+',
            r'pipenv\s+'
        ]

        for pattern in forbidden_patterns:
            if re.search(pattern, cmd):
                response = {
                    "decision": "deny",
                    "reason": "규정 위반 차단: 워크스페이스 루트의 단일 .venv 및 uv(uv add/uv sync)만 사용해야 합니다. (file-folders.md 및 data-pipeline-rules.md 준수)"
                }
                print(json.dumps(response, ensure_ascii=False))
                return

        print(json.dumps({"decision": "allow"}))
    except Exception:
        # 훅 예외 발생 시 안전하게 allow
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
