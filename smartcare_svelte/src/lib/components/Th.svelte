<script>
    export let handler;
    export let orderBy = null;

    const identifier = orderBy?.toString()
    const sorted = handler.getSort()
</script>

<th on:click={() => handler.sort(orderBy)} class:active={$sorted.identifier === identifier}>
    <slot />
    {#if $sorted.direction === "asc"}
    <i class="bi bi-caret-up-fill"></i>
    {:else if $sorted.direction === "desc"}
    <i class="bi bi-caret-down-fill"></i>
    {:else}
    <i class="bi bi-dash"></i>
    {/if}
</th>

<style>
    th i {
        visibility: hidden;
    }
    th.active i {
        visibility: initial;
    }
    th {
        white-space: nowrap;
    }
</style>