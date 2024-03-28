export const API_ENDPOINT = "http://localhost:8000/api"

export const BLANK_SESSION = {
    token: "",
    userType: null,
    firstName: "",
    lastName: ""
}

export const USER_TYPES = {
    0: "Superuser",
    1: "Admin",
    2: "Doctor",
    3: "Nurse",
    4: "External",
    5: "Patient"
}

export const QUICK_SYMPTOMS = {

    "Physical": ["Bite or sting",
        "Bleeding",
        "Bruise(s)",
        "Injury or burn",
        "Itching",
        "Lump(s)",
        "Paralysis",
        "Weight Loss",
        "Weight gain",
        "Blue lips",
        "Croaky voice or hoarseness",
        "Difficulty hearing",
        "Difficulty seeing",
        "Difficulty speaking",
        "Difficulty swallowing",
        "Dizziness",
        "Loss or change to sense of smell or taste "],

    "Mental": ["Changed Behaviour",
        "Concentration Difficulty",
        "Depression or anxiety",
        "Memory problem",
        "Nausea",
        "Difficulty sleeping",
        "Irritable or restless",
        "Loss of appetite"],    
}

export const bootstrapThemes = {
    "default": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
    "vapor": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/vapor/bootstrap.min.css",
    "united": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/united/bootstrap.min.css",
    "superhero": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/superhero/bootstrap.min.css",
    "spacelab": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/spacelab/bootstrap.min.css",
    "solar": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/solar/bootstrap.min.css",
    "sketchy": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/sketchy/bootstrap.min.css",
    "sandstone": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/sandstone/bootstrap.min.css",
    "pulse": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/pulse/bootstrap.min.css",
    "morph": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/morph/bootstrap.min.css",
    "minty": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/minty/bootstrap.min.css",
    "litera": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/litera/bootstrap.min.css",
    "journal": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/journal/bootstrap.min.css",
    "flatly": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/flatly/bootstrap.min.css",
    "darkly": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/darkly/bootstrap.min.css",
    "cyborg": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cyborg/bootstrap.min.css",
    "cosmo": "https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cosmo/bootstrap.min.css"
}