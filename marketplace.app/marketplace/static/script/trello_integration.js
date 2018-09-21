let trelloCardsCreator = function() {
  let trelloController = document.querySelectorAll('.trelloIntegration')


let template = function(value){
  return `> **Продукт**: ${value.productName}\n
          > **Артикул**: ${value.article}\n
          > **Количество**: ${value.count}\n
          \`\`\`

          Доставка:  ${value.delivery}\n
          Покупатель: ${value.consumer}\n
          Адрес: ${value.addres}\n
          Телефон: ${value.phone}\n
          Почта: ${value.mail}\n
          \`\`\`
          `
}

  let authenticationSuccess = function() {
    console.log('Successful authentication');
    showListBoards()
  };

  let authenticationFailure = function() {
    console.log('Failed authentication');
  };


  let cleanElement = elem => {
    while (elem.firstChild) {
      elem.removeChild(elem.firstChild);
    }
  }


  let createSelectElement = function(options, name) {
    let sel = document.createElement('select')
    let disabledOpt = document.createElement('option')
    disabledOpt.style.disabled = true
    disabledOpt.text = name
    sel.add(disabledOpt)
    options.forEach(option = > {
      let newOption = document.createElement('option')
      newOption.value = option.id
      newOption.text = option.name
      sel.add(newOption)
    })
    return sel
  }

  let createButton = function() {
    let btn = document.createElement('button')
    btn.addEventListener('click', () => {
      var creationSuccess = function(data) {
        console.log('Card created successfully.');
        console.log(JSON.stringify(data, null, 2));
      };
      var newCard = {
        name: 'New Test Card',
        desc: 'This is the description of our new card.',
        idList: '5b6be850405f2875e5fdfeca',
        pos: 'bottom'
      }
      Trello.post('/cards/', newCard, creationSuccess);
    })
    btn.innerHTML = 'Выбрать'
    return btn
  }


  let getBoardLists = function(event) {
    let success = msg => {
      console.log(msg)
      let selectElementLists = createSelectElement(msg, 'Выберите список')
      selectElementLists.classList.add('trello-select-lists')
      trelloController.forEach(cller => {
        let deletElement = document.querySelector('.trello-select-lists')
        if (deletElement) cller.removeChild(deletElement)
        cller.appendChild(selectElementLists)
      })
    }
    Trello.get(`/boards/${event.target.value}/lists`, success);
  }

  let showListBoards = function() {
    let success = msg => {
      console.log(msg)
      let selectElementBoards = createSelectElement(msg, 'Выберите доску')
      selectElementBoards.classList.add('trello-select-board')
      selectElementBoards.addEventListener('change', getBoardLists)
      trelloController.forEach(cller => {
        cller.removeEventListener('click', onHandleAuthentication)
        cleanElement(cller)
        cller.appendChild(selectElementBoards)
        cller.appendChild(createButton())
      })
    }
    let error = msg => {
      console.log(msg)
    }
    Trello.get('/member/me/boards', success, error);
  }

  let onHandleAuthentication = function(event) {
    window.Trello.authorize({
      type: 'popup',
      name: 'Marketplace',
      scope: {
        read: 'true',
        write: 'true'
      },
      success: authenticationSuccess,
      error: authenticationFailure
    });
  }



  if (trelloController.length > 0) {
    if (Trello.authorized()) {
      console.log('authorized')
    } else {
      console.log('not authorized')
      trelloController.forEach(cller => {
        cller.innerHTML = 'Нажмие для авторизации в Trello'
        cller.addEventListener('click', onHandleAuthentication)
      })
    }
  }
}
