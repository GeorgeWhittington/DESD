<script>
    import { onMount } from "svelte";
    import { bootstrapThemes } from "$lib/constants.js";
    let themes = Object.keys(bootstrapThemes);
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="/">Smartcare</a>

    
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
            
            <li class="nav-item active">
                <a class="nav-link" href="/">Home</a>
            </li>

            

            <li class="nav-item dropdown">

                <a class="nav-link dropdown-toggle" href="/" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <img src="http://cdn.onlinewebfonts.com/svg/img_311846.png" alt="logo" style="width: 20px;height:20px;">
                </a>
                
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <!-- {% if user.is_authenticated %} -->

                            <a class="dropdown-item" href="/dashboard">Profile</a>
                            
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" href="/logout">Logout</a>
                        <!-- {% endif%}
                    {% else%} -->
                        <a class="dropdown-item" href="/login">Login</a>
                        <a class="dropdown-item" href="/register">Register</a>
                    <!-- {% endif %} -->
                </div>

            </li>
            
        </ul>
    
    
    </div>
    
</nav>

<div class="vh-100 d-flex align-items-center">
    <div class="d-grid gap-2 col-6 mx-auto justify-content-center">
        <h1>Welcome to Smartcare!</h1>
        <a href="/login" class="btn btn-outline-primary btn-lg">Login</a>
        <a href="/register" class="btn btn-outline-primary btn-lg">Register</a>
        <div class="dropdown">
            <button class="btn btn-outline-primary btn-lg dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
              Select Theme
            </button>
            <ul class="dropdown-menu">
            {#each themes as theme}
            <li>
                <form method="POST" action="?/theme">
                    <input type="hidden" name="id" value="{theme}"/>
                    <button class="dropdown-item">{theme}</button>
                </form>
            </li>
            {/each}
            </ul>
        </div>
    </div>
</div>