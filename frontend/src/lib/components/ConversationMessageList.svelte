<script lang="ts">
  import clsx from "clsx";
  import SvelteMarkdown from "@humanspeak/svelte-markdown";

  let {
    chatHistory,
    isThinking,
    cls,
  }: {
    chatHistory: { role: "user" | "assistant"; content: string }[];
    isThinking: boolean;
    cls?: string;
  } = $props();
</script>

<div
  class={clsx(
    "flex-1 overflow-y-auto p-6 space-y-4 max-w-3xl w-full mx-auto",
    cls && cls,
  )}
>
  {#each chatHistory as msg}
    <div
      class={clsx(
        "flex",
        msg.role == "user" && "justify-end",
        msg.role != "user" && "justify-start",
      )}
    >
      <div
        class={clsx(
          "px-4 py-2 rounded-lg max-w-md whitespace-pre-wrap",
          msg.role == "user" && "bg-primary text-primary-foreground",
          msg.role != "user" &&
            "bg-surface border border-border text-foreground",
        )}
      >
        <SvelteMarkdown source={msg.content} />
      </div>
    </div>
  {/each}

  {#if isThinking}
    <div class="text-sm text-muted">thinking...</div>
  {/if}
</div>
