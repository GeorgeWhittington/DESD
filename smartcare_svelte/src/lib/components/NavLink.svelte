<script>
    export let link;
    export let iconClass;
    export let title;
</script>

<a class="nav-link text-white" href="{link}">
    <i class="bi {iconClass}"></i>
    {title}
</a>