  var ChatInput;

  ChatInput = $('.ChatInput-input');
  ChatInputSend = $('.ChatInput-btnSend');
  ChatWindow = $('.ChatWindow');
  startBtn = $('#start');

  ChatInput.keyup(function(e) {
    let element, newText, txt;
    if (e.shiftKey && e.which === 13) {
      e.preventDefault();
      return false;
    }
    element = $(this);
    if (e.which === 13) {
      newText = element.html();
      txt = element.text()
      element.html('');
      $('.ChatWindow').append('<div class="ChatItem ChatItem--expert"> <div class="ChatItem-meta"> <div class="ChatItem-avatar"> <img class="ChatItem-avatarImage" src="https://randomuser.me/api/portraits/women/0.jpg"> </div> </div> <div class="ChatItem-chatContent"> <div class="ChatItem-chatText">' + newText + '</div> <div class="ChatItem-timeStamp"><strong>Me</strong> · Today 05:49</div> </div> </div>');
      askBot(txt)
      return $('.ChatWindow').animate({
        scrollTop: 6000
      }, 700);

    }
  });

  ChatInputSend.click(function (e) {
    let element, newText, txt;

    element = ChatInput;

      newText = element.html();
      txt = element.text()
      element.html('');
      $('.ChatWindow').append(
          `<div class="ChatItem ChatItem--expert">
           <div class="ChatItem-meta"> 
           <div class="ChatItem-avatar"> 
           <img class="ChatItem-avatarImage" src="avatarrobot.png"> 
           </div> 
          </div> 
          <div class="ChatItem-chatContent"> 
          <div class="ChatItem-chatText">
          ${newText} 
          </div> 
          <div class="ChatItem-timeStamp">
          <strong>Customer</strong> · Today ${new Date().toLocaleTimeString()}
          </div> 
          </div> 
        </div>`
      );
      askBot(txt)
      return $('.ChatWindow').animate({
        scrollTop: $('.ChatWindow').prop("scrollHeight")
      }, 700);


  })

  console.log(startBtn)

  startBtn.click(function (e) {
    init_chat_area();
  });

  function askBot(newText){
    sendPost({
      "name": newText
    }, "http://localhost:8000/chatbot/ask/", (response)=>{
      ChatWindow.append(`
        <div class="ChatItem ChatItem--customer">
           <div class="ChatItem-meta"> 
           <div class="ChatItem-avatar"> 
           <img class="ChatItem-avatarImage" src="avatarrobot.png"> 
           </div> 
          </div> 
          <div class="ChatItem-chatContent"> 
          <div class="ChatItem-chatText">
          ${response} 
          </div> 
          <div class="ChatItem-timeStamp">
          <strong>Chatbot</strong> · Today ${new Date().toLocaleTimeString()}
          </div> 
          </div> 
        </div>`)
      console.log(response);
    })
  }

  function init_chat_area() {

    ChatWindow.html(`

<div class="ChatItem ChatItem--customer">
    <div class="ChatItem-meta">
      <div class="ChatItem-avatar">
        <img class="ChatItem-avatarImage" src="https://image.ibb.co/eTiXWa/avatarrobot.png">
      </div>
    </div>
    <div class="ChatItem-chatContent">
      <div class="ChatItem-chatText">hi there!</div>
      <div class="ChatItem-chatText">I would be happy to help you!</div>
      <div class="ChatItem-timeStamp"><strong>Chatbot</strong> • Today ${new Date().toLocaleTimeString()}</div>
    </div>
  </div>
  

  
`)
  }