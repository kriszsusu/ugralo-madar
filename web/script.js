const languageToggleButton = document.getElementById("lang-toggle");
const descriptionText = document.querySelector('.description-section p');
const warningText = document.querySelector('.warning p');

const texts = {
    english: {
        description: "Ugráló Madár is a Python game influenced by the well-known Flappy Bird, developed using the Pygame library. Players must control a bird and navigate it through various obstacles while steering clear of collisions. As your score increases, the game gradually becomes more difficult.",
        warning: "USE AT YOUR OWN RISK",
        nav: {
            home: "Home",
            features: "Features",
            levels: "Description",
            play: "Play"
        },
        features: [
            "Classic Flappy Bird-inspired gameplay. (it's low quality on purpose)",
            "Randomly generated pipe obstacles.",
            "Simple, responsive controls.",
            "Scoring system that tracks how far you progress.",
            "Game-over screen with final score display."
        ]
    },
    hungarian: {
        description: "Ugráló Madár egy Python játék, amelyet a híres Flappy Bird ihletett, és a Pygame könyvtár segítségével fejlesztették ki. A játékosoknak irányítaniuk kell egy madarat, és navigálniuk kell különféle akadályok között, miközben elkerülik az ütközéseket. Ahogy a pontszámod növekszik, a játék fokozatosan nehezebbé válik.",
        warning: "HASZNÁLD A SAJÁT FELELŐSSÉGEDRE",
        nav: {
            home: "Kezdőlap",
            features: "Jellemzők",
            levels: "Leírás",
            play: "Játssz"
        },
        features: [
            "Klasszikus Flappy Bird ihletésű játékmenet. (szándékosan alacsony minőség)",
            "Véletlenszerűen generált csőakadályok.",
            "Egyszerű, reszponzív vezérlés.",
            "Pontozási rendszer, amely nyomon követi a haladásodat.",
            "Játék vége képernyő a végső pontszám megjelenítésével."
        ]
    }
};

const updateText = (language) => {
    descriptionText.innerHTML = texts[language].description;
    warningText.innerHTML = texts[language].warning;

    const navLinks = document.querySelectorAll('.pixel-nav li a');
    navLinks[0].textContent = texts[language].nav.home;
    navLinks[1].textContent = texts[language].nav.features;
    navLinks[2].textContent = texts[language].nav.levels;
    navLinks[3].textContent = texts[language].nav.play;

    const featuresList = document.querySelector('#features ul');
    featuresList.innerHTML = ''; 
    texts[language].features.forEach(feature => {
        const li = document.createElement('li');
        li.textContent = feature;
        featuresList.appendChild(li);
    });
};

let currentLanguage = 'english';
updateText(currentLanguage);

languageToggleButton.addEventListener("click", () => {
    currentLanguage = currentLanguage === 'english' ? 'hungarian' : 'english';

    updateText(currentLanguage);
    languageToggleButton.textContent = currentLanguage === 'english' ? "HU" : "EN";
});

const playButton = document.querySelector('.play-button');
const popupOverlay = document.getElementById('popup-overlay');

playButton.addEventListener("click", () => {

    popupOverlay.style.display = 'flex'; 


    setTimeout(() => {
        popupOverlay.style.display = 'none';
        window.location.href = "https://github.com/kriszsusu/ugralo-madar/tree/main"; 
    }, 1000);
});

const hamburgerToggle = document.getElementById('hamburger-toggle');
const pixelNav = document.querySelector('.pixel-nav');

hamburgerToggle.addEventListener("click", () => {
    pixelNav.classList.toggle('show'); // Toggle visibility
});

