<script lang="ts">
  import clsx from "clsx";

  let message = $state("");
  let {
    sendMessage,
    cls,
  }: {
    sendMessage: (userMessage: string) => void | Promise<void>;
    cls?: string;
  } = $props();
</script>

<div class={clsx("border-t border-border bg-surface p-2", cls && cls)}>
  <div class="max-w-3xl mx-auto flex gap-2">
    <input
      class="flex-1 border border-border rounded-lg bg-background px-4 py-2 text-foreground placeholder:text-muted focus:outline-none focus:ring focus:ring-primary"
      placeholder="Send a message..."
      bind:value={message}
      onkeydown={(e) => {
        if (e.key === "Enter") {
          sendMessage(message);
          message = "";
        }
      }}
    />

    <button
      class="bg-primary text-primary-foreground px-4 rounded-lg hover:opacity-90 disabled:opacity-50"
      onclick={() => {
        sendMessage(message);
        message = "";
      }}
      disabled={!message.trim()}
      aria-label="Send message"
    >
      ➤
    </button>
  </div>
</div>
