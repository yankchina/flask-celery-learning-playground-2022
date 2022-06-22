document.querySelector('#friends-general-btn').addEventListener('click',(e)=>{toggleFriendsList();resetFriendsNotification('general');});document.querySelector('#friends-messages-btn').addEventListener('click',(e)=>{toggleMessagesList();resetFriendsNotification('messages');});for(let type of['list','requests','blocked','recent']){document.getElementById(`friends-${type}-btn`).addEventListener('click',()=>{showFriendsListVariation(type);resetFriendsNotification(type);});}
document.querySelectorAll('.friends-list-friend').forEach((el)=>el.addEventListener('click',clickUserTagInFriendsList));document.querySelectorAll('#friends-messages-friends-friends div').forEach((el)=>el.addEventListener('click',clickUserTagInMessages));function clickUserTagInFriendsList(e){openMessagesList();closeFriendsList();let userTag=(e.target.firstChild.innerText===undefined)?e.target.innerText:e.target.firstChild.innerText;focusUserTag(userTag);resetUserTagNotification(userTagElem);}
function clickUserTagInMessages(e){let userTagElem=e.target;let userTag=userTagElem.dataset.userTag;focusUserTag(userTag);resetUserTagNotification(userTagElem);}
document.addEventListener("DOMContentLoaded",function(){document.getElementById('send-friend-message-input').addEventListener('keypress',(e)=>{if(e.key==='Enter'||e.key==='NumpadEnter'){reqSendMessageToFriend(e.target.value,friendUserTagSelected);}});});document.addEventListener("DOMContentLoaded",function(){socket.on('friend_request',(data)=>{document.getElementById('friends-list-requests').appendChild(htmlToElement(`<li>${data.user_tag}<span style="float:right"><button onclick="reqAddFriend(${data.user_tag})"></span></li>`))
showFriendsNotification('general');showFriendsNotification('requests');});});document.addEventListener("DOMContentLoaded",function(){socket.on('friend_message',(data)=>{console.log(data);let userTag=data.user_tag
let msg=data.message;if(!document.querySelector(`[data-user-tag="${userTag}"]`)){addUserTagToMessages(data.user_tag);}
if(messagesListOpen){let focusedFriendTag=getFocusedFriendTagMessages();if(focusedFriendTag!=userTag){showUserTagNotification(userTag);}else{addMessageToFriendMessages(msg,"friend");}}else{showFriendsNotification('messages');showUserTagNotification(userTag);}});});function setMessagesUserTagActive(userTag){userTagElem=document.querySelector(`[data-user-tag="${userTag}"]`).classList.add('active');}
function addActiveToMessageUserTag(elem){elem.classList.add('active');}
function removeActiveFromMessageUserTags(){document.querySelectorAll('#friends-messages-friends-friends div').forEach((el)=>el.classList.remove('active'));}
function moveChildToFirstChild(child,parent){parent.removeChild(child);parent.insertBefore(child,parent.firstChild);}
function setMessagesInFriendMessagesDiv(messages,self_id){document.getElementById('friends-messages-user-messages').innerHTML=htmlToElement(getMessagesHtml(messages,self_id));}
function addMessageToFriendMessages(message,type="self"){document.querySelector('#friends-messages-user-messages > div').appendChild((type=="self")?getSelfMessageHtml(message):getFriendMessageHtml(message))}
function addUserTagToMessages(userTag){let list=document.getElementById('friends-messages-friends-friends');let userTagElem=htmlToElement(`<div data-user-tag="${userTag}">${userTag}<span class="friends-user-tag-notification-div">0</span></div>`);list.insertBefore(userTagElem,list.firstChild);userTagElem.addEventListener('click',clickUserTagInMessages);return userTagElem;}
function focusUserTag(userTag){let userTagElem=document.querySelector(`[data-user-tag="${userTag}"]`);if(!userTagElem){userTagElem=addUserTagToMessages(userTag)
initializeUserTagElem(userTagElem);}
let list=document.getElementById('friends-messages-friends-friends');let messages=reqGetFriendMessages(userTag);moveChildToFirstChild(userTagElem,list);removeActiveFromMessageUserTags();addActiveToMessageUserTag(userTagElem);friendUserTagSelected=userTag;}
function getFocusedFriendTagMessages(){return document.querySelector(`[data-user-tag].active`);}
let friendUserTagSelected;function initializeUserTagElem(userTagElem){userTagElem.addEventListener('click',(e)=>{clickUserTagInMessages(e)});}
function getFriendMessageHtml(message){return`<div class="friends-messages-friend-message">${message}</div>`}
function getSelfMessageHtml(message){return`<div class="friends-messages-self-message">${message}</div>`}
function getMessagesHtml(messages,self_id){let html='<div>';for(let msg of messages){html+=(msg.user_id==self_id)?getSelfMessageHtml(msg.message):getFriendMessageHtml(msg.message);}
html+='</div>'
return html;}
function showFriendsNotification(type="",increment=true){let notifDiv=document.getElementById(`friends-${type}-notification-div`);if(increment){notifDiv.innerText=parseInt(notifDiv.innerText)+1;}
notifDiv.style.display="flex";}
function resetFriendsNotification(type=""){let notifDiv=document.getElementById(`friends-${type}-notification-div`);notifDiv.innerText=0;notifDiv.style.display="none";}
function showUserTagNotification(userTag,increment=true){console.log('adding');let notifDiv=document.querySelector(`[data-user-tag="${userTag}"]>.friends-user-tag-notification-div`);if(increment){notifDiv.innerText=parseInt(notifDiv.innerText)+1;}
notifDiv.style.display="flex";}
function resetUserTagNotification(userTagElem){let notifDiv=userTagElem.querySelector('span');notifDiv.innerText=0;notifDiv.style.display="none";}
function reqAddFriend(user_id){let formData=new FormData();formData.append('user_id',user_id);fetch('/friends/add_friend',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
function reqRemoveFriend(user_id){let formData=new FormData();formData.append('user_id',user_id);fetch('/friends/remove_friend',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
function reqGetFriendMessages(userTag){let formData=new FormData();formData.append('user_tag',userTag);fetch('/friends/get_friend_messages',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
function reqSendMessageToFriend(message,userTag){let formData=new FormData();formData.append('user_tag',userTag);formData.append('message',message);fetch('/friends/send_friend_message',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
let friendsListOpen=false;let messagesListOpen=false;function toggleFriendsList(){if(friendsListOpen){document.getElementById('friends-list').style.display='none';friendsListOpen=false;}else{document.getElementById('friends-list').style.display='flex';friendsListOpen=true;}}
function toggleMessagesList(){if(messagesListOpen){document.getElementById('friends-messages-list').style.display='none';messagesListOpen=false;}else{document.getElementById('friends-messages-list').style.display='flex';messagesListOpen=true;}}
function openFriendsList(){document.getElementById('friends-list').style.display='flex';friendsListOpen=true;}
function openMessagesList(){document.getElementById('friends-messages-list').style.display='flex';messagesListOpen=true;}
function closeFriendsList(){document.getElementById('friends-list').style.display='none';friendsListOpen=false;}
function closeMessagesList(){document.getElementById('friends-messages-list').style.display='none';messagesListOpen=false;}
function showFriendsListVariation(variation){hideAllFriendLists();document.getElementById(`friends-list-${variation}`).style.display='flex';}
function hideAllFriendLists(){for(let variation of['list','requests','blocked','recent']){document.getElementById(`friends-list-${variation}`).style.display='none';}}