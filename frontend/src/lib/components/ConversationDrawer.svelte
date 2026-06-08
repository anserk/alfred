<script lang="ts">
  import { X, Sun, Moon } from "@lucide/svelte";
  import { appState } from "../../routes/state.svelte";
  import { getTopicsAsync, type TopicDtoList } from "$lib/api/chat";
  import { onMount } from "svelte";

  function toggleTheme() {
    appState.isDark = !appState.isDark;
    document.documentElement.classList.toggle("dark", appState.isDark);
    localStorage.setItem("theme", appState.isDark ? "dark" : "light");
  }

  let topics = $state<TopicDtoList>([]);

  onMount(async () => {
    topics = await getTopicsAsync();
  });
</script>

<aside
  class={[
    "grid grid-rows-[1fr_11fr] bg-background text-foreground",
    "fixed inset-y-0 left-0 z-50 w-80 shadow-xl",
    "transition-transform duration-300 ease-out",
    "border-r-2 border-border ",
    appState.sidebarOpen ? "translate-x-0" : "-translate-x-full",
  ]}
>
  <div class="flex flex-row p-2 items-center justify-end gap-1 bg-surface">
    <button
      onclick={toggleTheme}
      class="p-3 bg-surface rounded-full text-foreground transition-colors duration-200 hover:bg-surface-muted"
      aria-label="Toggle theme"
    >
      {#if appState.isDark}
        <Sun />
      {:else}
        <Moon />{/if}
    </button>
    <button
      class="p-3 bg-surface rounded-full text-foreground transition-colors duration-200 hover:bg-surface-muted"
      onclick={() => (appState.sidebarOpen = false)}
      aria-label="Close menu"
    >
      <X />
    </button>
  </div>
  <div class="p-4 bg-background flex">
    <ul>
      {#each topics as topic}<li>{topic.title}</li>{/each}
    </ul>
  </div>
</aside>
