<script>
    export let userTypesPermitted;
    export let userType;

    import { goto } from "$app/navigation";
    import { page } from '$app/stores';
    import { browser } from '$app/environment';

    $: pathname = $page.url.pathname;
    $: pathUp = pathname.substring(0, pathname.lastIndexOf('/')) || "/";

    $: {
        if (browser && userType !== undefined) {
            if (!userTypesPermitted.includes(userType)) {
                goto(pathUp);
            }
        }
    }
</script>