<script>
    let innerWidth;
    $: alwaysShowNav = innerWidth >= 992 ? "show" : "";
</script>

<svelte:window bind:innerWidth={innerWidth} />

<div class="row">
    <div class="col-lg-3 sticky-top dashboard-nav-wrapper py-2">
        <nav class="navbar dashboard-nav-controls">
            <div class="container-fluid">
                <button
                    class="navbar-toggler" type="button"
                    data-bs-toggle="collapse" data-bs-target="#dashboard-nav"
                    aria-controls="dashboard-nav" aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
        </nav>
        <div class=" dashboard-nav collapse {alwaysShowNav}" id="dashboard-nav">
            <div class="h-100">
                <nav class="nav nav-pills flex-column align-items-stretch">
                    <a class="nav-link" href="#item-1">
                        <i class="bi bi-calendar"></i>
                        My Appointments
                    </a>
                    <a class="nav-link" href="#item-2">
                        <i class="bi bi-capsule"></i>
                        My Prescriptions
                    </a>
                    <a class="nav-link" href="#item-3">
                        <i class="bi bi-box-arrow-right"></i>
                        Log Out
                    </a>
                    <a class="nav-link" href="#item-4">Item 4</a>
                </nav>
            </div>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="dashboard-body">
            <div id="item-1">
                <h4>My Appointments</h4>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
            </div>

            <div id="item-2">
                <h4>My Prescriptions</h4>
                <p>Duis hendrerit pharetra ligula eget interdum. Fusce porttitor lacinia tristique. Curabitur nec nibh a ex cursus consectetur eget id turpis. Nulla nec pretium dolor. Pellentesque ex urna, commodo nec accumsan id, ultrices non sapien. Mauris fringilla pulvinar purus. Integer eu dapibus justo. Morbi eu vehicula lacus. Nam tristique enim est, cursus facilisis nisi finibus ac. Ut vestibulum tincidunt tellus, eu sagittis nisl vulputate et. Sed sagittis lectus eu eros suscipit sodales. Duis imperdiet eget ipsum vitae luctus. Suspendisse potenti. Suspendisse imperdiet diam at ex efficitur, sed eleifend velit viverra.</p>
                <p>In varius dignissim risus. Mauris vitae egestas diam. Maecenas vitae risus vel diam egestas lacinia eu in metus. Vivamus eleifend aliquam sem, ut mollis quam dignissim quis. Curabitur viverra turpis non eleifend sagittis. Mauris sed urna vehicula, sodales quam vel, rhoncus augue. Duis in sem sed nunc vestibulum tempor vel non orci. Curabitur sem purus, pellentesque iaculis nisi et, posuere accumsan mauris. Quisque libero turpis, ullamcorper vitae sem sed, porta blandit lectus. Integer aliquet id nisl ut interdum.</p>
            </div>

            <div id="item-3">
                <h4>Log Out</h4>
                <p>Pellentesque eleifend ipsum metus, sit amet rhoncus est porttitor sit amet. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas consectetur lorem at leo hendrerit, et tempus libero vestibulum. Vestibulum non diam in tortor pharetra condimentum. Aliquam aliquet sit amet tortor a aliquam. Donec fringilla justo a metus condimentum vestibulum. Donec maximus faucibus neque, vitae fringilla massa maximus ut. Morbi at nunc quis urna tincidunt tempus at fermentum orci. Nulla pulvinar volutpat augue non feugiat. Nulla eleifend porta arcu sed scelerisque. Aliquam ut faucibus augue. Aliquam consequat a magna vel sodales. Nulla a enim nec eros consectetur sodales mattis ut nisl. Nulla tincidunt posuere bibendum. Donec a dapibus nisi. Duis placerat dui turpis, vitae condimentum purus maximus at.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
            </div>

            <div id="item-4">
                <h4>Item 4</h4>
                <p>Pellentesque eleifend ipsum metus, sit amet rhoncus est porttitor sit amet. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Maecenas consectetur lorem at leo hendrerit, et tempus libero vestibulum. Vestibulum non diam in tortor pharetra condimentum. Aliquam aliquet sit amet tortor a aliquam. Donec fringilla justo a metus condimentum vestibulum. Donec maximus faucibus neque, vitae fringilla massa maximus ut. Morbi at nunc quis urna tincidunt tempus at fermentum orci. Nulla pulvinar volutpat augue non feugiat. Nulla eleifend porta arcu sed scelerisque. Aliquam ut faucibus augue. Aliquam consequat a magna vel sodales. Nulla a enim nec eros consectetur sodales mattis ut nisl. Nulla tincidunt posuere bibendum. Donec a dapibus nisi. Duis placerat dui turpis, vitae condimentum purus maximus at.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc velit nibh, eleifend ac ligula eget, efficitur auctor magna. Sed maximus semper suscipit. Aenean ultrices turpis eget diam sagittis, vel interdum elit dignissim. Cras in dolor in arcu placerat commodo. Duis sed laoreet elit, et euismod nisl. Mauris varius ligula vitae porttitor porta. Phasellus aliquam, urna in convallis gravida, mauris est rutrum arcu, a mattis nibh orci sed sapien. Phasellus luctus facilisis dui eu rutrum. Integer velit quam, maximus quis semper quis, commodo pulvinar leo.</p>
                <p>Suspendisse pharetra elit in dui faucibus faucibus. Vivamus placerat rhoncus nisl, non scelerisque enim pulvinar vitae. Donec fringilla sapien sit amet leo scelerisque ullamcorper. Sed interdum nibh sed ultricies dapibus. Quisque quis tincidunt diam, id faucibus arcu. Duis volutpat in massa at interdum. Sed quam lacus, dictum tristique ex quis, feugiat ornare turpis. Quisque malesuada diam ut sapien tempor tempor.</p>
            </div>
        </div>
    </div>
</div>

<style>
    .dashboard-body {
        height: 100vh;
        overflow-y: scroll;
    }

    .dashboard-nav-controls {
        display: none;
    }

    @media only screen and (max-width: 992px) {
        .dashboard-body {
            height: initial;
            overflow-y: initial;
        }

        .dashboard-nav-wrapper {
            background-color: white;
        }

        .dashboard-nav-controls {
            display: initial;
        }
    }
</style>