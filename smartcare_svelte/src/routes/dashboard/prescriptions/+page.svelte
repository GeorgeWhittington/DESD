<script>
    import { DataHandler } from '@vincjo/datatables'
    let someData = [{first_name: "Alasdair", last_name: "Freeman"}, {first_name: "George", last_name: "Whittington"}]

    const handler = new DataHandler(someData, { rowsPerPage: 50 })
    const rows = handler.getRows()
</script>

<table class="table">
    <thead class="table-light">
        <tr>
            <th>First name</th>
            <th>Last name</th>
        </tr>
    </thead>
    <tbody>
        {#each $rows as row}
            <tr>
                <td>{row.first_name}</td>
                <td>{row.last_name}</td>
            </tr>
        {/each}
    </tbody>
</table>