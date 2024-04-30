<script>
    export let type = "text";
    /** @type {any} */
    export let value;
    /** @type {String} */
    export let id;
    /** @type {String} */
    export let label;
    /** @type {Array} */
    export let errors;
    export let custom_classes = "";

    $: isInvalid = errors !== undefined && errors.length > 0 ? "is-invalid" : "";
</script>

{#if type === "password"}
    <div class="form-floating {custom_classes}">
        <input type="password" class="form-control {isInvalid}" id="{id}" placeholder="{label}" bind:value/>
        <label for="{id}">{label}</label>
        <div class="invalid-feedback">
            {errors.join(", ")}
        </div>
    </div>
{:else if type === "email"}
    <div class="form-floating {custom_classes}">
        <input type="email" class="form-control {isInvalid}" id="{id}" placeholder="{label}" bind:value/>
        <label for="{id}">{label}</label>
        <div class="invalid-feedback">
            {errors.join(", ")}
        </div>
    </div>
{:else}
    <div class="form-floating {custom_classes}">
        <input type="text" class="form-control {isInvalid}" id="{id}" placeholder="{label}" bind:value/>
        <label for="{id}">{label}</label>
        <div class="invalid-feedback">
            {errors.join(", ")}
        </div>
    </div>
{/if}