#!/usr/bin/env python3
"""校验一个技能目录是否符合规范。零错误才可交付。

用法: python validate_skill.py <skill-dir> [--strict]
      --strict  把警告也当错误（CI 门禁用）
退出码: 0=通过  1=有错误  2=参数错误
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_rules import check  # noqa: E402


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print(__doc__)
        return 2

    errs, warns, infos = check(args[0], strict)
    print(f"校验：{os.path.abspath(args[0])}")
    for i in infos:
        print(f"  · {i}")
    for w in warns:
        print(f"  [警告] {w}")
    for e in errs:
        print(f"  [错误] {e}")
    if errs:
        print(f"\n结果：{len(errs)} 个错误，{len(warns)} 个警告 —— 不可交付")
        return 1
    print(f"\n结果：通过（{len(warns)} 个警告）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
