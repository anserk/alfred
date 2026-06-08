<script lang="ts">
  import clsx from "clsx";
  import { Menu } from "@lucide/svelte";
  import { appState } from "../../routes/state.svelte";
  import { onMount } from "svelte";

  let {
    cls,
  }: {
    cls?: string;
  } = $props();
  let title = $state("");

  onMount(() => {
    const source = new EventSource("/api/chat/getTitle");

    source.addEventListener("title.updated", (event) => {
      const data = JSON.parse(event.data);
      title = data.title;
    });

    return () => source.close();
  });
</script>

<div class={clsx("flex flex-row p-2 items-center bg-surface ", cls && cls)}>
  <button
    class="p-4 bg-surface rounded-full text-foreground transition-colors duration-200 hover:bg-surface-muted"
    onclick={() => (appState.sidebarOpen = true)}
    aria-label="Open menu"
  >
    <Menu />
  </button>
  <h1 class="p-4">{title}</h1>
</div>
