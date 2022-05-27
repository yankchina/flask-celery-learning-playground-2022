document.addEventListener("DOMContentLoaded",function(){socket.on('ping_find_match',(data)=>{if(!checkingTaskStatus){checkingTaskStatus=setInterval(()=>{checkFindMatchTaskStatus(data.location);},1000);}})});function checkFindMatchTaskStatus(url){return fetch(url,{mode:"no-cors",}).then(res=>res.json()).then(json=>{if(json.task_status=='SUCCESS'){clearInterval(checkingTaskStatus);checkingTaskStatus=undefined;}}).catch(error=>console.warn(error));}
document.addEventListener("DOMContentLoaded",function(){let key;socket.on('match_found',handleMatchFoundEmit);socket.on('clear_match_found',clearMatchFound);function handleMatchFoundEmit(data){key=data['key'];document.querySelector('#match-found-notification').style.background='rgb(125, 125, 199)';document.querySelector('#match-found-notification').style.display="flex";}
function acceptMatch(){socket.emit('match_found_choice',{'key':key,'choice':'accept'});document.querySelector('#match-found-notification').style.background='green';}
function declineMatch(){socket.emit('match_found_choice',{'choice':'decline'});document.querySelector('#match-found-notification').style.background='red';}
document.querySelector('#accept-match-found-btn').addEventListener('click',acceptMatch);document.querySelector('#decline-match-found-btn').addEventListener('click',declineMatch);});function clearMatchFound(){key=null;hideMatchFound();}
function hideMatchFound(){document.querySelector('#match-found-notification').style.display="none";}
let checkingTaskStatus;function joinMatchmaking(){$.ajax({url:`/join_matchmaking`,success:function(result){showNotification(result);if(result.success){startQueueTimer(1);if(!checkingTaskStatus){checkingTaskStatus=setInterval(()=>{checkFindMatchTaskStatus(result.location);},1000);}}},error:function(request,status,error){console.log(request.responseText);},});}
let queueTimerInterval;function startQueueTimer(timeInQueue){if(queueTimerInterval)return;let outerDiv=document.getElementById('queue-timer');outerDiv.style.display='block';let div=document.getElementById('queue-timer-count');div.innerText=timeInQueue;queueTimerInterval=setInterval(()=>{div.innerText=parseInt(div.innerText)+1;},1000);}
function endQueueTimer(){let outerDiv=document.getElementById('queue-timer');outerDiv.style.display='none';clearInterval(queueTimerInterval);queueTimerInterval=undefined;}
function hideQueueTimer(){endQueueTimer();}
function clearQueueTimer(){console.log("clearing");endQueueTimer();}
function testCelery(){$.ajax({url:`/test_task`,success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function testRedis(){$.ajax({url:`/test_redis`,success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function checkRedisQueue(){$.ajax({url:`/check_redis_queue`,success:function(result){console.log(result.queue);},error:function(request,status,error){console.log(request.responseText);},});}
function testResponse(){$.ajax({url:"/test_response",success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function testGameServerResponse(){$.ajax({url:"http://127.0.0.1:5001/test_response",success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function testCreateGame(){$.ajax({url:"http://127.0.0.1:5001/create_game",success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function testRequestWebsiteToGameServer(){$.ajax({url:"/test_request_to_game_server",success:function(result){console.log(result);},error:function(request,status,error){console.log(request.responseText);},});}
function testPlaySound(){playAtVolume(queuePoppedSound);}
function resetAllMatchmaking(data){console.log("resetting all")
clearQueueTimer();clearMatchFound();}
document.addEventListener("DOMContentLoaded",function(){socket.on('reset_all_matchmaking',resetAllMatchmaking);});let queuePoppedSound=new Audio("/static/matchmaking/audio/music_pipe_chord_nice.mp3");