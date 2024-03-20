<script>
    import { onMount } from "svelte";
    import { bootstrapThemes } from "$lib/constants.js";
    let themes = Object.keys(bootstrapThemes);
</script>

<div class="vh-100 d-flex align-items-center">
    <div class="d-grid gap-2 col-6 mx-auto justify-content-center">
        <h1>Welcome to Smartcare!</h1>
        <a href="/login" class="btn btn-outline-primary btn-lg">Login</a>
        <a href="/register" class="btn btn-outline-primary btn-lg">Register</a>
        <div class="dropdown">
            <button class="btn btn-outline-primary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              Select Theme
            </button>
            <ul class="dropdown-menu">
            {#each themes as theme}
            <li>
                <form method="POST" action="?/theme">
                    <input type="hidden" name="id" value="{theme}"/>
                    <button class="dropdown-item">{theme}</button>
                </form>
            </li>
            {/each}
            </ul>
        </div>
    </div>
</div>