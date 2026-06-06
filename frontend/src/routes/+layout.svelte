<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";
  import { appState } from "./state.svelte";

  let { children } = $props();

  $effect(() => {
    const saved = localStorage.getItem("theme");
    appState.isDark = saved
      ? saved === "dark"
      : window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.classList.toggle("dark", appState.isDark);
  });
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

{@render children()}
