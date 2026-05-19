---
name: codebase-analysis
description: Analyze software repositories and produce a structured onboarding-focused report with concrete file-path evidence.
---

# Codebase Analysis Skill

## Goal
Turn a repository exploration request into a structured, evidence-based analysis report for onboarding and secondary development planning.

## Workflow
Follow this order unless the user explicitly requests a different sequence:

1. Check metadata first:
   - `README.md`, `README_*.md`
   - key config/build files (e.g. `package.json`, `pyproject.toml`, `Makefile`, `Dockerfile`, `docker-compose*.yaml`, `config.yaml`)
2. Scan top-level structure:
   - summarize top-level directories and key files only
3. Find startup entrypoints:
   - backend, frontend, worker, CLI, and infra entrypoints
4. Analyze core modules:
   - identify domain modules and responsibilities
5. Analyze key call chains:
   - at least 1-3 high-value flows with concrete path references
6. Extract development commands:
   - install, dev, test, build, lint, format, docker commands
7. Identify risks:
   - architecture risks, coupling, config drift, test gaps, operational risks
8. Output onboarding route:
   - provide a practical 30-60 minute newcomer reading/verification path

## Fixed Output Format
Always use this exact section structure for a full repository analysis:

# 代码库分析报告

## 1. 项目概览
## 2. 技术栈
## 3. 目录结构
## 4. 启动流程
## 5. 核心模块
## 6. 关键调用链
## 7. 开发与测试命令
## 8. 风险点
## 9. 二次开发建议
## 10. 新人上手路线

## Rules
- Must cite concrete file paths for every major conclusion.
- Do NOT output a complete file tree.
- Do NOT invent files that have not been checked.
- If user asks in Chinese, answer in Chinese.
- Keep code identifiers, file paths, and commands in English.
- If repository path is missing or inaccessible, state it clearly and provide next-step guidance.

## Execution Notes
- Prefer quick reconnaissance first, then drill down on user-specified focus areas.
- If tool support exists, prioritize repository overview, entrypoint detection, and dependency/command extraction tools.
