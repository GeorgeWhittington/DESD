<script>
    export let userTypes;
    export let title;

    import { getContext, onMount } from "svelte";
    import { DataHandler } from "@vincjo/datatables";
    import { apiGET, apiPOST } from "$lib/apiFetch.js";
    import { USER_TYPES, PATIENT_PAY_TYPES, EMPLOYMENT_TYPES } from "$lib/constants.js";
    import Th from "$lib/components/Th.svelte";
    import TablePagination from "$lib/components/TablePagination.svelte";

    let actions = [
        {id: "none", text: "---"},
        {id: "make_active", text: "Activate selected users"},
        {id: "make_inactive", text: "Deactivate selected users"}
    ];
    let selected_action = "none";

    let payrates = [
        {id: "none", text: "---"}
    ];
    let selected_payrate = "none";

    let patients_included = userTypes.includes(5);
    let staff_included = userTypes.includes(2) || userTypes.includes(3);

    if (staff_included) {
        actions.push({id: "make_full_time", text: "Make selected staff members full time"});
        actions.push({id: "make_part_time", text: "Make selected staff members part time"});
        actions.push({id: "set_pay_rate", text: "Set the selected staff members pay rate"});
    }

    const session = getContext("session");

    let users = []
    const handler = new DataHandler(users, { rowsPerPage: 10 });
    const rows = handler.getRows();
    const rowCount = handler.getRowCount();
    const selected = handler.getSelected();
    const isAllSelected = handler.isAllSelected();

    let error = "";
    let result = "";

    async function loadUsers() {
        error = "";
        let query_args = userTypes.map((userType) => `user_type=${userType}`);
        let response = await apiGET(session, `/auth/user?${query_args.join("&")}`);
        if (response && response.ok) {
            users = await response.json();
            handler.setRows(users);
        } else {
            error = "Server error, please try again later!";
        }
    }

    async function loadPayrates() {
        let response = await apiGET(session, "/payrate/");
        if (response && response.ok) {
            let response_json = await response.json();
            for (const payrate of response_json) {
                payrates.push({id: payrate.id, text: `${payrate.title} ${payrate.rate.toFixed(2)}/h`});
            }
        }
    }

    async function applyAction() {
        result = "";
        error = "";
        if (selected_action === "none")
            return;

        if (selected_action == "make_inactive" && $selected.includes($session.userId)) {
            error = "You cannot deactivate your own account";
            return;
        }

        if (selected_action == "set_pay_rate" && selected_payrate == "none") {
            error = "You must select a pay rate to apply to the staff members selected";
            return;
        }

        let payload = {"users": $selected};
        if (selected_action == "set_pay_rate")
            payload["payrate"] = selected_payrate;

        let request = await apiPOST(session, `/auth/user/${selected_action}/`, JSON.stringify(payload));

        if (!request || !request.ok && request.status != 400 && request.status != 403) {
            error = "Server error, please try again later!";
            return;
        }

        let request_json = await request.json();

        if (request.ok) {
            loadUsers();
            result = request_json.detail;
        } else {
            error = request_json.detail;
        }
    }

    onMount(() => {
        loadUsers();

        if (staff_included) {
            loadPayrates();
        }
    })
</script>

<div class="card mt-3">
    <div class="card-body">
        <h2 class="card-title">{title}</h2>
        {#if error !== ""}
        <div class="alert alert-danger" role="alert">{error}</div>
        {/if}
        {#if result !== ""}
        <div class="alert alert-success" role="alert">{result}</div>
        {/if}
        <form class="d-flex justify-content-between" on:submit|preventDefault={applyAction}>
            <div class="d-flex flex-column justify-content-between w-100">
                <div class="form-floating w-100">
                    <select
                        class="form-select" id={`user-${userTypes.join("")}-action-select`}
                        aria-label="Select an action to apply" bind:value={selected_action}
                    >
                        {#each actions as action}
                            <option value={action.id}>{action.text}</option>
                        {/each}
                    </select>
                    <label for={`user-${userTypes.join("")}-action-select`}>Action</label>
                </div>
                {#if selected_action == "set_pay_rate"}
                <div class="form-floating w-100 mt-2">
                    <select
                        class="form-select" id={`user-${userTypes.join("")}-payrate-select`}
                        aria-label="Select a payrate" bind:value={selected_payrate}
                    >
                        {#each payrates as payrate}
                            <option value={payrate.id}>{payrate.text}</option>
                        {/each}
                    </select>
                    <label for={`user-${userTypes.join("")}-payrate-select`}>Payrate</label>
                </div>
                {/if}
            </div>
            <button type="submit" class="btn btn-primary ms-2">Go</button>
        </form>
        <div class="table-responsive">
            <table class="table table-striped mt-2">
                <thead class="table-light">
                    <tr>
                        <th>
                            <input type="checkbox"
                                on:click={() => handler.selectAll({ selectBy: "id" })}
                                checked={$isAllSelected}
                            >
                        </th>
                        <Th handler={handler} orderBy="id">ID</Th>
                        <Th handler={handler} orderBy="first_name">First Name</Th>
                        <Th handler={handler} orderBy="last_name">Last Name</Th>
                        <Th handler={handler} orderBy="email">Email</Th>
                        <Th handler={handler} orderBy="is_active">Activated</Th>

                        {#if userTypes.length > 1}
                        <Th handler={handler} orderBy="user_type">User Type</Th>
                        {/if}

                        {#if patients_included}
                        <Th handler={handler} orderBy="patient_info.pay_type">Private/NHS</Th>
                        {/if}

                        {#if staff_included}
                        <Th handler={handler} orderBy="staff_info.employment_type">Employment Type</Th>
                        <Th handler={handler} orderBy="staff_info.payrate">Payrate</Th>
                        {/if}
                    </tr>
                </thead>
                <tbody>
                    {#each $rows as row}
                        <tr>
                            <td>
                                <input type="checkbox"
                                    on:click={() => handler.select(row.id)}
                                    checked={$selected.includes(row.id)}
                                />
                            </td>
                            <td>{row.id}</td>
                            <td>{row.first_name}</td>
                            <td>{row.last_name}</td>
                            <td>{row.email}</td>
                            <td>{#if row.is_active} ✅ {:else} ❌ {/if}</td>

                            {#if userTypes.length > 1}
                            <td>{USER_TYPES[row.user_type]}</td>
                            {/if}

                            {#if patients_included}
                            <td>
                                {#if row.patient_info != null}
                                    {PATIENT_PAY_TYPES[row.patient_info.pay_type]}
                                {:else}
                                    -
                                {/if}
                            </td>
                            {/if}

                            {#if staff_included}
                                <td>
                                {#if row.staff_info != null && row.staff_info.employment_type != null}
                                    {EMPLOYMENT_TYPES[row.staff_info.employment_type]}
                                {:else}
                                    -
                                {/if}
                                </td>

                                <td>
                                {#if row.staff_info != null && row.staff_info.payrate != null}
                                    {#each payrates as pr}
                                        {#if pr.id == row.staff_info.payrate}
                                            {pr.text}
                                        {/if}
                                    {/each}
                                {/if}
                                </td>
                            {/if}
                        </tr>
                    {/each}
                </tbody>
            </table>
        </div>
        <footer class="d-flex justify-content-between align-items-center">
            <div>
                {#if $rowCount.total > 0}
                    Showing <b>{$rowCount.start}</b>
                    to <b>{$rowCount.end}</b>
                    of <b>{$rowCount.total}</b>
                {:else}
                    No entries found
                {/if}
            </div>
            <TablePagination handler={handler} />
        </footer>
    </div>
</div>