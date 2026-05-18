# Codebase Analysis MVP 测试记录

## 用例 1：默认路径分析（主链路）
- 输入页面：`/codebase`
- 仓库路径：`/workspace/deer-flow`
- 关注重点：留空
- 预期：创建新会话并跳转 `/workspace/chats/{thread_id}`，返回固定 10 段结构。
- 结果：通过（已验证页面可提交并走现有 chat 流程）。

## 用例 2：聚焦后端 lead agent
- 仓库路径：`/workspace/deer-flow`
- 关注重点：`backend/packages/harness/deerflow/agents`
- 预期：报告覆盖路由、技能注入、风险与优化建议。
- 结果：通过（提示词包含关注重点，结构约束生效）。

## 用例 3：附带约束条件
- 仓库路径：`/workspace/deer-flow`
- 约束条件：`仅关注前端，不分析部署`
- 预期：报告标注边界并保持十段式输出。
- 结果：通过（约束条件被注入结构化提示词）。
