document.querySelector('#friends-general-btn').addEventListener('click',(e)=>{toggleFriendsList();resetFriendsNotification('general');});document.querySelector('#friends-messages-btn').addEventListener('click',(e)=>{toggleMessagesList();resetFriendsNotification('messages');});document.querySelector('#friends-party-btn').addEventListener('click',(e)=>{togglePartyList();resetFriendsNotification('party');});for(let type of['list','requests','blocked','recent']){document.getElementById(`friends-${type}-btn`).addEventListener('click',()=>{showFriendsListVariation(type);resetFriendsNotification(type);});}
document.querySelectorAll('.friends-list-friend').forEach((el)=>el.addEventListener('click',clickUserTagInFriendsList));document.querySelectorAll('#friends-messages-friends-friends div').forEach((el)=>el.addEventListener('click',clickUserTagInMessages));function clickUserTagInFriendsList(e){openMessagesList();closeFriendsList();let userTag=(e.target.firstChild.innerText===undefined)?e.target.innerText:e.target.firstChild.innerText;let userTagElem=getElemFromUserTag(userTag);focusUserTag(userTag);resetUserTagNotification(userTagElem);}
function clickUserTagInMessages(e){let userTagElem=e.target;let userTag=userTagElem.dataset.userTag;focusUserTag(userTag);resetUserTagNotification(userTagElem);}
document.addEventListener("DOMContentLoaded",function(){document.getElementById('send-friend-message-input').addEventListener('keydown',(e)=>{if(e.key==='Enter'||e.key==='NumpadEnter'){reqSendMessageToFriend(e.target.value,friendUserTagSelected);addMessageToFriendMessages(e.target.value,"self");scrollMessagesToBottom();clearInput(e.target);}});document.getElementById('send-party-message-input').addEventListener('keydown',(e)=>{if(e.key==='Enter'||e.key==='NumpadEnter'){reqSendPartyMessage(e.target.value);scrollPartyToBottom();clearInput(e.target);}});});document.addEventListener("DOMContentLoaded",function(){socket.on('friend_request',(data)=>{let elem=htmlToElement(`<li>${data.user_tag}<span style="float:right"><button>+</button></span></li>`)
document.getElementById('friends-list-requests').appendChild(elem)
elem.querySelector('span > button').addEventListener('click',()=>{reqAddFriend(data.user_id)});showFriendsNotification('general');showFriendsNotification('requests');});});document.addEventListener("DOMContentLoaded",function(){socket.on('friend_message',(data)=>{console.log(data);let userTag=data.user_tag
let msg=data.message;if(!getElemFromUserTag(userTag)){addUserTagToMessages(data.user_tag);}
if(messagesListOpen){let focusedFriendTag=getFocusedFriendTagMessages();if(focusedFriendTag!=userTag){showUserTagNotification(userTag);}else{addMessageToFriendMessages(msg,"friend");scrollMessagesToBottom();}}else{showFriendsNotification('messages');showUserTagNotification(userTag);let focusedFriendTag=getFocusedFriendTagMessages();if(focusedFriendTag!=userTag){showUserTagNotification(userTag);}else{addMessageToFriendMessages(msg,"friend");}}});});document.addEventListener("DOMContentLoaded",function(){socket.on('party_invite',(data)=>{document.getElementById('friends-party-invite-container').appendChild(getPartyInviteHtml(data.user_tag));});socket.on('party_message',(data)=>{console.log(data);addMessageToPartyMessages(data.message_dict);});});function setMessagesUserTagActive(userTag){userTagElem=getElemFromUserTag(userTag).classList.add('active');}
function addActiveToMessageUserTag(elem){elem.classList.add('active');}
function removeActiveFromMessageUserTags(){document.querySelectorAll('#friends-messages-friends-friends div').forEach((el)=>el.classList.remove('active'));}
function clearInput(elem){elem.value='';}
function moveChildToFirstChild(child,parent){parent.removeChild(child);parent.insertBefore(child,parent.firstChild);}
function setMessagesInFriendMessagesDiv(messages){let elem=document.getElementById('friends-messages-user-messages')
elem.innerHTML='';elem.appendChild(htmlToElement(getFriendMessagesHtml(messages)));}
function setMessagesInFriendPartyDiv(messages){let elem=document.getElementById('friends-party-user-messages');elem.innerHTML='';elem.appendChild(htmlToElement(getFriendPartyMessagesHtml(messages)));}
function setNotInPartyInPartyDiv(){let elem=document.getElementById('friends-party-user-messages');elem.innerHTML='Not in party.';}
function addMessageToFriendMessages(message,type="self"){document.querySelector('#friends-messages-user-messages > div').appendChild((type=="self")?htmlToElement(getSelfMessageHtml(message)):htmlToElement(getFriendMessageHtml(message)))}
function addMessageToPartyMessages(messageDict){let elem=document.getElementById('friends-party-user-messages');elem.appendChild(htmlToElement(getFriendPartyMessageHtml(messageDict)));}
function addUserTagToMessages(userTag){let list=document.getElementById('friends-messages-friends-friends');let userTagElem=htmlToElement(`<div data-user-tag="${userTag}">${userTag}<span class="friends-user-tag-notification-div">0</span></div>`);list.insertBefore(userTagElem,list.firstChild);userTagElem.addEventListener('click',clickUserTagInMessages);return userTagElem;}
function getElemFromUserTag(userTag){return document.querySelector(`[data-user-tag="${userTag.trim()}"]`);}
async function focusUserTag(userTag){let userTagElem=getElemFromUserTag(userTag);if(!userTagElem){userTagElem=addUserTagToMessages(userTag)
initializeUserTagElem(userTagElem);}
let list=document.getElementById('friends-messages-friends-friends');let messages=await reqGetFriendMessages(userTag);setMessagesInFriendMessagesDiv(messages);moveChildToFirstChild(userTagElem,list);removeActiveFromMessageUserTags();addActiveToMessageUserTag(userTagElem);friendUserTagSelected=userTag;scrollMessagesToBottom('auto');}
async function focusParty(){let list=document.getElementById('friends-party-friends-friends');let messages=await reqGetFriendPartyMessages();if(messages==="not in party"){setNotInPartyInPartyDiv();return;}
setMessagesInFriendPartyDiv(messages);scrollPartyToBottom('auto');}
function getFocusedFriendTagMessages(){return document.querySelector(`[data-user-tag].active`).dataset.userTag;}
let friendUserTagSelected;function initializeUserTagElem(userTagElem){userTagElem.addEventListener('click',(e)=>{clickUserTagInMessages(e)});}
function getFriendMessageHtml(message){return`<div class="friends-messages-friend-message">${message}</div>`}
function getSelfMessageHtml(message){return`<div class="friends-messages-self-message">${message}</div>`}
function getFriendMessagesHtml(messages){let html='<div>';for(let msg of messages){html+=(msg.who=='self')?getSelfMessageHtml(msg.message):getFriendMessageHtml(msg.message);}
html+='</div>'
return html;}
function getFriendPartyMessageHtml(msg){return`<div class="friends-party-message">${msg.user_tag}:&ensp;${msg.message}</div>`}
function getFriendPartyMessagesHtml(messages){let html='<div>';for(let msg of messages){html+=getFriendPartyMessageHtml(msg);}
html+='</div>'
return html;}
function showFriendsNotification(type="",increment=true){let notifDiv=document.getElementById(`friends-${type}-notification-div`);if(increment){notifDiv.innerText=parseInt(notifDiv.innerText)+1;}
notifDiv.style.display="flex";}
function resetFriendsNotification(type=""){let notifDiv=document.getElementById(`friends-${type}-notification-div`);notifDiv.innerText=0;notifDiv.style.display="none";}
function showUserTagNotification(userTag,increment=true){console.log('adding');let notifDiv=document.querySelector(`[data-user-tag="${userTag}"]>.friends-user-tag-notification-div`);if(increment){notifDiv.innerText=parseInt(notifDiv.innerText)+1;}
notifDiv.style.display="flex";}
function resetUserTagNotification(userTagElem){let notifDiv=userTagElem.querySelector('span');notifDiv.innerText=0;notifDiv.style.display="none";}
let hasPulledPartyMessages=false;function pullPartyMessages(){if(!hasPulledPartyMessages){hasPulledPartyMessages=true;reqGetFriendPartyMessages();}}
function sendPartyInvite(e,userId){e.stopPropagation();reqSendPartyInvite(userId);}
function getPartyInviteHtml(userTag){let htmlString=`<div class="friends-party-invite"data-party-invite-user-tag=${userTag}><h6>Party Invite</h6><h4>${userTag}</h4><div><button onclick="acceptPartyInvite('${userTag}')">Accept</button><button onclick="declinePartyInvite('${userTag}')">Decline</button></div></div>`.replace(/>\s+</g,"><");return htmlToElement(htmlString);}
function removePartyInvite(userTag){document.querySelector(`[data-party-invite-user-tag="${userTag}"]`).remove();}
function acceptPartyInvite(userTag){reqAcceptPartyInvite(userTag);removePartyInvite(userTag);}
function declinePartyInvite(userTag){reqDeclinePartyInvite(userTag);removePartyInvite(userTag);}
function reqAddFriend(user_id){let formData=new FormData();formData.append('user_id',user_id);fetch('/friends/add_friend',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
function reqRemoveFriend(user_id){let formData=new FormData();formData.append('user_id',user_id);fetch('/friends/remove_friend',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
async function reqGetFriendMessages(userTag){let formData=new FormData();formData.append('user_tag',userTag);const res=await fetch('/friends/get_friend_messages',{method:"POST",body:formData})
const result=await res.json();const messages=await result.messages;return messages;}
function reqSendMessageToFriend(message,userTag){let formData=new FormData();formData.append('user_tag',userTag);formData.append('message',message);fetch('/friends/send_friend_message',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
async function reqGetFriendPartyMessages(){const res=await fetch('/friends/get_party_messages',{method:"GET",})
const result=await res.json();console.log(result);const messages=await result.messages;return messages;}
async function reqSendPartyInvite(userId){let formData=new FormData();formData.append('user_id',userId);const res=await fetch('/friends/send_party_invite',{method:"POST",body:formData})
const result=await res.json();console.log(result);try{console.log(socket);if(result.success){socket.emit('join_party_room',{'room':result.party_sid});}}catch(error){}}
async function reqDeclinePartyInvite(userTag){let formData=new FormData();formData.append('user_tag',userTag);const res=await fetch('/friends/decline_party_invite',{method:"POST",body:formData})
const result=await res.json();console.log(result);}
async function reqAcceptPartyInvite(userTag){let formData=new FormData();formData.append('user_tag',userTag);const res=await fetch('/friends/accept_party_invite',{method:"POST",body:formData});const result=await res.json();console.log(result);try{console.log(socket);socket.emit('join_party_room',{'room':result.party_sid})
console.log("joined party socket room");}catch(error){}}
function reqSendPartyMessage(message){let formData=new FormData();formData.append('message',message);fetch('/friends/send_party_message',{method:"POST",body:formData}).then(res=>res.json()).then(json=>console.log(json)).catch(error=>console.warn(error));}
async function reqLeaveParty(){const res=await fetch('/friends/leave_party',{method:"POST",});const result=await res.json();console.log(result);addNotification(result,3000);try{}catch(error){}}
function scrollMessagesToBottom(behavior='smooth'){document.querySelector('#friends-messages-user-messages').scrollTo({top:999999,left:100,behavior:behavior});}
function scrollPartyToBottom(behavior='smooth'){document.querySelector('#friends-party-user-messages').scrollTo({top:999999,left:100,behavior:behavior});}
let friendsListOpen=false;let messagesListOpen=false;let partyListOpen=false;function toggleFriendsList(){(friendsListOpen)?closeFriendsList():openFriendsList();}
function toggleMessagesList(){(messagesListOpen)?closeMessagesList():openMessagesList();}
function togglePartyList(){(partyListOpen)?closePartyList():openPartyList();}
function openFriendsList(){document.getElementById('friends-list').style.display='flex';friendsListOpen=true;}
function openMessagesList(){document.getElementById('friends-messages-list').style.display='flex';messagesListOpen=true;scrollMessagesToBottom();}
function closeFriendsList(){document.getElementById('friends-list').style.display='none';friendsListOpen=false;}
function closeMessagesList(){document.getElementById('friends-messages-list').style.display='none';messagesListOpen=false;}
function openPartyList(){document.getElementById('friends-party-list').style.display='flex';focusParty();partyListOpen=true;scrollPartyToBottom();}
function closePartyList(){document.getElementById('friends-party-list').style.display='none';partyListOpen=false;}
function showFriendsListVariation(variation){hideAllFriendLists();document.getElementById(`friends-list-${variation}`).style.display='flex';}
function hideAllFriendLists(){for(let variation of['list','requests','blocked','recent']){document.getElementById(`friends-list-${variation}`).style.display='none';}}