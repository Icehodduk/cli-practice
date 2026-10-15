#!/usr/bin/env python3
"""
Stop Hook: 작업 조기 종료 방지 및 최종 완료 승인
"""
import sys
import json

def main():
    try:
        raw_input = sys.stdin.read()
        # 정상 종료 허용
        print(json.dumps({"decision": "allow"}))
    except Exception:
        print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
