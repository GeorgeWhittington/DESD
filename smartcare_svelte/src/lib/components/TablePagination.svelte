<script>
  export let handler;

  const pageNumber = handler.getPageNumber()
  const pageCount = handler.getPageCount()
  const pages = handler.getPages({ ellipsis: true })
</script>

{#if $pageCount > 1}
  <div aria-label="table pagination">
    <ul class="pagination m-0">
      <li class="page-item" class:disabled={$pageNumber === 1}>
        <a class="page-link" href="#" aria-label="Previous" on:click={() => handler.setPage("previous")}>
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>
      {#each $pages as page}
      <li class="page-item" class:active={$pageNumber === page} class:disabled={page === null}>
        <a class="page-link" href="#" on:click={() => handler.setPage(page)}>
          {page ?? "..."}
        </a>
      </li>
      {/each}
      <li class="page-item" class:disabled={$pageNumber === $pageCount}>
        <a class="page-link" href="#" aria-label="Next" on:click={() => handler.setPage("next")}>
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </div>
{/if}