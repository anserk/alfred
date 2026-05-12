<script lang="ts">
  import "./layout.css";
  import favicon from "$lib/assets/favicon.svg";
  import { Sun, Moon } from "@lucide/svelte";

  let { children } = $props();
  let isDark = $state(false);

  function toggleTheme() {
    isDark = !isDark;
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }

  $effect(() => {
    const saved = localStorage.getItem("theme");
    isDark = saved
      ? saved === "dark"
      : window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.classList.toggle("dark", isDark);
  });
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div id="theme-toggle" class="fixed top-4 right-4 z-50">
  <button
    onclick={toggleTheme}
    class="p-2 rounded-full bg-gray-200 dark:bg-gray-700 dark:text-white transition-colors duration-200 hover:bg-gray-300 dark:hover:bg-gray-600"
  >
    {#if isDark}
      <Sun />
    {:else}
      <Moon />{/if}
  </button>
</div>

{@render children()}
