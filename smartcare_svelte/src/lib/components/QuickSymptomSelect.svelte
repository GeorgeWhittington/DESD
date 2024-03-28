<script>
    import { QUICK_SYMPTOMS } from "$lib/constants";
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    function onSymptomClicked(event) {
        let symptomString = event.target.innerText
        console.log(symptomString);
        dispatch('symptomClicked', {
            text: symptomString,
        });
    };

</script>

<div class="card mb-2">
    <div class="card-body">
        <label class="card-title">Quick-Add Symptoms</label>

        <ul class="nav nav-tabs" id="myTab" role="tablist">
            {#each Object.entries(QUICK_SYMPTOMS) as [qs], i}
                <li class="nav-item" role="presentation">
                    {#if i == 0}
                        <button
                            class="nav-link active"
                            id={qs + "-tab"}
                            data-bs-toggle="tab"
                            data-bs-target={"#" + qs}
                            type="button"
                            role="tab"
                            aria-controls={qs}
                            aria-selected="false">{qs}</button
                        >
                    {:else}
                        <button
                            class="nav-link"
                            id={qs + "-tab"}
                            data-bs-toggle="tab"
                            data-bs-target={"#" + qs}
                            type="button"
                            role="tab"
                            aria-controls={qs}
                            aria-selected="false">{qs}</button
                        >
                    {/if}
                </li>
            {/each}
        </ul>
        <div class="tab-content" id="myTabContent">
            {#each Object.entries(QUICK_SYMPTOMS) as [qs], i}
                {#if i == 0}
                    <div
                        class="tab-pane p-1 fade show active"
                        id={qs}
                        role="tabpanel"
                        aria-labelledby={qs + "-tab"}
                    >
                    {#each QUICK_SYMPTOMS[qs] as symptom}
                    <a href="#" class="badge rounded-pill bg-secondary link-underline-light m-1" on:click|preventDefault={onSymptomClicked}
                            >{symptom}</a
                        >
                    {/each}
                        
                    </div>
                {:else}
                    <div
                        class="tab-pane p-1 fade"
                        id={qs}
                        role="tabpanel"
                        aria-labelledby={qs + "-tab"}
                    >
                    {#each QUICK_SYMPTOMS[qs] as symptom, i}
                    <a href="#" class="badge rounded-pill bg-secondary link-underline-light  m-1" on:click|preventDefault={onSymptomClicked}
                            >{symptom}</a
                        >
                        {/each}
                    </div>
                {/if}
            {/each}
        </div>
    </div>
</div>
