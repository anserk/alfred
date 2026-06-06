<script lang="ts">
  import toast, { Toaster } from "svelte-french-toast";
  import ConversationHeader from "$lib/components/ConversationHeader.svelte";
  import ConversationMessageList from "$lib/components/ConversationMessageList.svelte";
  import ConversationInput from "$lib/components/ConversationInput.svelte";
  import ConversationDrawer from "$lib/components/ConversationDrawer.svelte";

  let chatHistory = $state<{ role: "user" | "assistant"; content: string }[]>(
    [],
  );
  let isThinking = $state(false);

  async function sendMessage(userMessage: string) {
    if (!userMessage.trim()) return;

    chatHistory = [...chatHistory, { role: "user", content: userMessage }];

    isThinking = true;

    // placeholder assistant message for streaming
    let assistantIndex = chatHistory.length;
    chatHistory = [...chatHistory, { role: "assistant", content: "" }];

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
      }
    } catch (err) {
      chatHistory = chatHistory.filter((msg) => msg.content.length > 0);
      toast.error("Unable to parse response from the server.");
    } finally {
      isThinking = false;
    }
  }
</script>

<div
  class="h-screen grid grid-rows-[1fr_10fr_1fr] bg-background text-foreground"
>
  <ConversationHeader />
  <ConversationMessageList {chatHistory} {isThinking} />
  <ConversationInput {sendMessage} />
  <ConversationDrawer />
</div>
<Toaster />
