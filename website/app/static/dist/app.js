function addToScore(){console.log(gameSocket);gameSocket.emit('add_to_score',{'he':'test','there':'t2'})}
let hideNotification;function showNotification(resultObject){if(hideNotification){clearTimeout(hideNotification);}
let div=document.getElementById('notification_div');div.style.display='block';div.style.background=resultObject.success?"green":"red";div.innerText=resultObject.message;hideNotification=setTimeout(()=>{div.style.display='none';},5000);}
const SOUNDS_ON=true;const VOL_HALF=[]
const VOL_DOUBLE=[]
function playAtVolume(sound,vol){if(!vol){vol=0.2;}
let volume;if(SOUNDS_ON){if(VOL_HALF.includes(sound)){volume=vol*0.5;}else if(VOL_DOUBLE.includes(sound)){volume=(vol<0.5)?vol*2:1;}else{volume=vol;}
playPause(sound,volume);}}
function playPause(sound,vol){sound.volume=vol;sound.currentTime=0;console.log(sound);sound.play();}