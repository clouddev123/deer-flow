export type CodebaseAnalysisFormValues = {
  repoPath: string;
  focus?: string;
  constraints?: string;
};

export function buildCodebaseAnalysisPrompt(values: CodebaseAnalysisFormValues): string {
  const repoPath = values.repoPath.trim();
  const focus = values.focus?.trim();
  const constraints = values.constraints?.trim();

  return [
    "请使用 codebase-analysis skill 对以下代码库执行分析，并严格输出固定 10 段报告结构。",
    "",
    "【分析目标】",
    "- 产出可执行的仓库分析报告，覆盖架构、链路、风险、改进优先级与30天计划。",
    "",
    "【输入参数】",
    `- 仓库路径: ${repoPath}`,
    `- 关注重点: ${focus ?? "未指定（请先做全局扫描并给出主链路）"}`,
    `- 约束条件: ${constraints ?? "无"}`,
    "",
    "【执行要求】",
    "1) 先确认分析边界，再执行结构扫描与关键链路识别。",
    "2) 仅基于真实文件证据，不确定项请标注“待确认”。",
    "3) 最终必须按以下10段标题输出，顺序不可变：",
    "   1. 分析范围与假设",
    "   2. 项目概览（业务与技术）",
    "   3. 目录结构与模块职责",
    "   4. 关键执行链路（请求/任务/数据流）",
    "   5. 依赖、配置与环境管理",
    "   6. 代码质量与测试现状",
    "   7. 可维护性与扩展性评估",
    "   8. 风险清单（含影响与触发条件）",
    "   9. 优先级改进建议（P0/P1/P2）",
    "   10. 30天落地计划（里程碑）",
  ].join("\n");
}
