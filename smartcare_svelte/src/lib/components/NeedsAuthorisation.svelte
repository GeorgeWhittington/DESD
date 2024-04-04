<script>
    export let userTypesPermitted;
    export let userType;

    import { goto } from "$app/navigation";
    import { page } from '$app/stores';

    $: pathname = $page.url.pathname;
    $: pathUp = pathname.substring(0, pathname.lastIndexOf('/'));

    $: {
        if (userType !== null && userType !== undefined) {
            $page.url.pathname
            if (!userTypesPermitted.includes(userType)) {
                goto(pathUp);
            }
        }
    }
</script>