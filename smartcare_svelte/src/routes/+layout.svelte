<script>
    import { browser } from '$app/environment';
    import { writable } from "svelte/store";
    import { bootstrapThemes } from "$lib/constants.js";
    import { getContext, setContext, onDestroy } from "svelte";
    import { BLANK_SESSION } from "$lib/constants.js";
    import { page } from '$app/stores';
    import { apiPOST } from "$lib/apiFetch.js";
    import { goto } from "$app/navigation";

    // Try to fetch existing session from localstorage.
    const storedSession = browser ? JSON.parse(window.localStorage.getItem("session")) : BLANK_SESSION;
    // Add a writeable store containing session data to context,
    // a blank object is used if session couldn't be fetched
    setContext("session", writable(storedSession || BLANK_SESSION))

    // Fetch the store that was just stored from context and ensure
    // that any changes made to it are written to localstorage
    const session = getContext("session");
    const unsubscribe = session.subscribe((value) => {
        if (value && browser)
            window.localStorage.setItem("session", JSON.stringify(value));
    });

    let themes = Object.keys(bootstrapThemes);

    async function logout() {
        let response = await apiPOST(session, "/auth/logout/", "");
        if (response && response.status < 500) {
            session.set(BLANK_SESSION);
            goto("/");
        } else {
            alert("Server error, please try again later!");
        }
    }

    onDestroy(unsubscribe);
</script>

{#if !$page.url.pathname.includes("dashboard")}
<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand mb-0 h1" href="/">Smartcare Surgery</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        {#if $session.userId != null}
        <li class="nav-item">
          <a class="nav-link" href="/dashboard">Dashboard</a>
        </li>
        {/if}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownTheme" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Select Theme
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdownTheme">
          {#each themes as theme}
            <li class="dropdown-item">
              <form method="POST" action="?/theme">
                <input type="hidden" name="id" value="{theme}"/>
                <button class="dropdown-item">{theme}</button>
              </form>
            </li>
          {/each}
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownAccount" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-person-circle"></i>
          </a>
          <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownAccount">
          {#if $session.userId == null}
            <li><a class="dropdown-item" href="/login">Login</a></li>
            <li><a class="dropdown-item" href="/register">Register</a></li>
          {:else}
            <li><a class="dropdown-item" href="#" on:click={logout}>Logout</a></li>
          {/if}
          </ul>
        </li>
        </ul>
     </div>
  </div>
</nav>
{/if}

<slot/>