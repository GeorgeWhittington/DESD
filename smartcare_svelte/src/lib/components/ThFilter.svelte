<script>
    export let handler
    export let filterBy = null
    let value = ''
</script>

<th>
    <input
        type="text"
        placeholder="Filter"
        bind:value
        on:input={() => handler.filter(value, filterBy)}
    />
</th>

<style>
    input {
        width: 100%;
        border: none;
        background: inherit;
    }
    input::placeholder {
        color: grey;
        font-style: italic;
    }
</style>