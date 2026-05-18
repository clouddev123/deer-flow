"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { useThreadStream } from "@/core/threads/hooks";
import { buildCodebaseAnalysisPrompt } from "@/features/codebase/build-codebase-analysis-prompt";

export default function CodebasePage() {
  const router = useRouter();
  const [repoPath, setRepoPath] = useState("/workspace/deer-flow");
  const [focus, setFocus] = useState("");
  const [constraints, setConstraints] = useState("");

  const { sendMessage, thread } = useThreadStream({
    threadId: undefined,
    onStart: (createdThreadId) => {
      history.replaceState(null, "", `/workspace/chats/${createdThreadId}`);
      router.push(`/workspace/chats/${createdThreadId}`);
    },
  });

  const submitting = thread.isLoading;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const prompt = buildCodebaseAnalysisPrompt({ repoPath, focus, constraints });
    await sendMessage("new", { text: prompt, files: [] });
  };

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="mb-2 text-2xl font-semibold">代码库分析</h1>
      <p className="text-muted-foreground mb-6 text-sm">
        填写仓库路径后会复用现有聊天流程发起分析，并跳转到聊天页面查看结果。
      </p>
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium">仓库路径</label>
          <input value={repoPath} onChange={(e) => setRepoPath(e.target.value)} className="w-full rounded border px-3 py-2" required />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">关注重点（可选）</label>
          <textarea value={focus} onChange={(e) => setFocus(e.target.value)} className="w-full rounded border px-3 py-2" rows={3} />
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium">约束条件（可选）</label>
          <textarea value={constraints} onChange={(e) => setConstraints(e.target.value)} className="w-full rounded border px-3 py-2" rows={3} />
        </div>
        <button disabled={submitting} type="submit" className="rounded bg-black px-4 py-2 text-white disabled:opacity-50">
          {submitting ? "分析中..." : "开始分析"}
        </button>
      </form>
    </main>
  );
}
