<script lang="ts">
  import clsx from "clsx";
  import { Menu } from "@lucide/svelte";
  import { appState } from "../../routes/state.svelte";

  let {
    cls,
  }: {
    cls?: string;
  } = $props();
</script>

<div
  class={clsx("flex flex-row p-2 justify-items-center bg-surface ", cls && cls)}
>
  <button
    class="p-4 bg-surface rounded-full text-foreground transition-colors duration-200 hover:bg-surface-muted"
    onclick={() => (appState.sidebarOpen = true)}
    aria-label="Open menu"
  >
    <Menu />
  </button>
</div>
