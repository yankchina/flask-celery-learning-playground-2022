
const SOUNDS_ON = true;

// xylo sounds
// let timerTickSound = new Audio("/static/sounds/xylo/music_xylo_hit.mp3");
// let timerEndSound = new Audio("/static/sounds/xylo/music_xylo_hi_prompt.mp3");
// let helperSound = new Audio("/static/sounds/xylo/music_xylo_alert.mp3");
// let saveSound = new Audio("/static/sounds/xylo/music_xylo_hi_chord.mp3");

// let chatSound = new Audio("/static/sounds/click_snip.mp3");

// let turnStartSound = new Audio("/static/sounds/xylo/music_xylo_up.mp3");
// let turnEndSound = new Audio("/static/sounds/xylo/music_xylo_drop.mp3");

// let gameStartSound = new Audio("/static/sounds/xylo/music_xylo_end.mp3");
// let gameOverSound = new Audio("/static/sounds/xylo/music_xylo_end.mp3");

// let userJoinedSound = new Audio("/static/sounds/chime_short_hi_on.wav");
// let userLeftSound = new Audio("/static/sounds/chime_short_hi_off.wav");
// let incorrectGuessSound = new Audio("/static/sounds/incorrect5.mp3");
// let correctGuessSound = new Audio("/static/sounds/scale-d6.mp3");
// // let inputNotAcceptedSound = new Audio("/static/sounds/button1.mp3");
// let mouseSnipSound = new Audio("/static/sounds/click_snip.mp3");
// let mouseClickSound = new Audio("/static/sounds/click_mouse.mp3");
// let eraseSound = new Audio("/static/sounds/draw_erase.mp3");


// let sound1 = new Audio("/static/sounds/xylo/music_xylo_hi_no.mp3");
// let sound2 = new Audio("/static/sounds/xylo/music_xylo_hit.mp3");
// let sound3 = new Audio("/static/sounds/xylo/music_xylo_note.mp3");



const VOL_HALF = [
]
const VOL_DOUBLE = [
]




function playAtVolume(sound, vol) {
    //plays sound at certain volume
    if (!vol) {
        vol = 0.2;
    }
    let volume;
    if (SOUNDS_ON) {
        if (VOL_HALF.includes(sound)) {
            volume = vol * 0.5;
        } else if (VOL_DOUBLE.includes(sound)) {
            volume = (vol < 0.5) ? vol * 2 : 1;
        } else {
            volume = vol;
        }
        playPause(sound, volume);
    }
}

function playPause(sound, vol) {
    sound.volume = vol;
    sound.currentTime = 0;
    console.log(sound);
    sound.play();
}