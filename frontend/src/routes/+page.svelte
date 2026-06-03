<script lang="ts">
  import { tick, onMount } from "svelte";

  let message = $state("");
  let chatHistory = $state<{ role: "user" | "assistant"; content: string }[]>(
    [],
  );
  let isLoading = $state(false);
  let isThinking = $state(false);
  let chatContainer: HTMLDivElement | null = $state(null);
  let userScrolledUp = $state(false);

  async function scrollToBottom(behavior: ScrollBehavior = "smooth") {
    if (userScrolledUp) return;
    await tick();
    chatContainer?.scrollTo({ top: chatContainer.scrollHeight, behavior });
  }

  function onScroll() {
    if (!chatContainer) return;
    const distanceFromBottom =
      chatContainer.scrollHeight -
      chatContainer.scrollTop -
      chatContainer.clientHeight;
    userScrolledUp = distanceFromBottom > 100;
  }

  async function sendMessage() {
    if (!message.trim()) return;

    const userMessage = message;
    message = "";

    chatHistory = [...chatHistory, { role: "user", content: userMessage }];

    isLoading = true;
    isThinking = true;

    // placeholder assistant message for streaming
    let assistantIndex = chatHistory.length;
    chatHistory = [...chatHistory, { role: "assistant", content: "" }];
    await scrollToBottom("smooth");

    try {
      const res = await fetch("/api/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!res.ok || !res.body) throw new Error("Stream unavailable");
      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { value, done } = await reader?.read();
        if (done) break;

        const chunk = decoder.decode(value);

        if (isThinking) {
          isThinking = false;
        }

        chatHistory = chatHistory.map((msg, i) =>
          i === assistantIndex ? { ...msg, content: msg.content + chunk } : msg,
        );

        await scrollToBottom("instant");
      }
    } catch (err) {
      console.error(err);
    } finally {
      isLoading = false;
      isThinking = false;
    }
  }

  onMount(() => scrollToBottom());
</script>

<div class="h-screen flex flex-col bg-gray-100 dark:bg-gray-900">
  <!-- Chat -->
  <div class="flex-1 overflow-y-auto p-6 space-y-4 max-w-3xl w-full mx-auto">
    {#each chatHistory as msg}
      <div
        class={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
      >
        <div
          class={`px-4 py-2 rounded-lg max-w-md whitespace-pre-wrap
					${msg.role === "user" ? "bg-blue-500 text-white" : "bg-white dark:bg-gray-800 border dark:border-gray-700"}`}
        >
          {@html msg.content}
        </div>
      </div>
    {/each}

    {#if isThinking}
      <div class="text-sm text-gray-400 dark:text-gray-500">thinking...</div>
    {/if}
  </div>

  <!-- Input -->
  <div
    class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4"
  >
    <div class="max-w-3xl mx-auto flex gap-2">
      <input
        class="flex-1 border border-gray-300 dark:border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        placeholder="Send a message..."
        bind:value={message}
        onkeydown={(e) => e.key === "Enter" && sendMessage()}
      />

      <button
        class="bg-blue-500 text-white px-4 rounded-lg hover:bg-blue-600 disabled:opacity-50"
        onclick={sendMessage}
        disabled={!message.trim()}
        aria-label="Send message"
      >
        ➤
      </button>
    </div>
  </div>
</div>
