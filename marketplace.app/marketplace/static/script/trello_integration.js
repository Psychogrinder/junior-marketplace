let trelloCardsCreator = function () {
  let trelloController = document.querySelectorAll('.trelloIntegration')


  let template = function (value) {
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


  let createButton = function () {
    let btn = document.createElement('button')
    btn.addEventListener('click', () => {
      var creationSuccess = function (data) {
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
 

  let TrelloController = function (container, id) {
    this.container = container
    this.id = id
    this._createdSelectors = this._createdSelectors.bind(this)
    this.onHandleBoardChange = this.onHandleBoardChange.bind(this)
    this.onHandleSubmit = this.onHandleSubmit.bind(this)
    this._init()
  }

  TrelloController.prototype = {

    authonticated(onSucces) {
      window.Trello.authorize({
        type: 'popup',
        name: 'Marketplace',
        scope: {
          read: 'true',
          write: 'true'
        },
        success: onSucces,
      });
    },

    getBoards(onSucces, onError) {
      return Trello.get('/member/me/boards', onSucces, onError);
    },

    getBoardLists(boardId, onSucces, onError) {
      return Trello.get(`/boards/${boardId}/lists`, onSucces, onError);
    },

    createCard(newCard, onSucces) {
      return Trello.post('/cards/', newCard, onSucces);
    },

    settingsBoardSelector(selector) {
      return new Promise((resolve, reject) => {
        this.setChild(selector, true)
        this.boardSelector = selector
        selector.classList.add('trello-select-board')
        selector.addEventListener('change', this.onHandleBoardChange)
        resolve()
      })
    },

    settingsListSelector(selector) {
      return new Promise((resolve, reject) => {
        selector.classList.add('trello-select-list')
        this.setChild(selector)
        this.listSelector = selector
        resolve()
      })
    },

    changeListsOptions(options) {
      this._cleanElement(this.listSelector)
      this._fillSelector(this.listSelector, options, 'Список')
    },

    setChild(child, clean = false) {
      if (clean) {
        this._cleanElement(this.container)
      }
      this.container.appendChild(child)
    },

    _createdSelectors() {
      this.getBoards()
        .then(data => this._createSelectElement(data, 'Доска'))
        .then(selector => this.settingsBoardSelector(selector))
        .then(() => this._createSelectElement([], 'Список'))
        .then(selector => this.settingsListSelector(selector))
        .then(() => this._createSubmitButton())
        .catch(data => console.log(data))
    },

    _createSubmitButton() {
      let btn = document.createElement('button')
      btn.innerHTML = 'Выбрать'
      btn.addEventListener('click', this.onHandleSubmit)
      this.setChild(btn)
    },

    _cleanElement(element) {
      while (element.firstChild) {
        element.removeChild(element.firstChild);
      }
    },

    _fillSelector(selector, options, name) {
      let disabledOpt = document.createElement('option')
      disabledOpt.style.disabled = true
      disabledOpt.text = name
      selector.add(disabledOpt)
      options.forEach(option => {
        let newOption = document.createElement('option')
        newOption.value = option.id
        newOption.text = option.name
        selector.add(newOption)
      })
    },

    _createSelectElement(options, name) {
      return new Promise((resolve, reject) => {
        let sel = document.createElement('select')
        this._fillSelector(sel, options, name)
        resolve(sel)
      })
    },

    onHandleBoardChange(event) {
      if (event.target.value.toLowerCase() === 'доска'){
        this.changeListsOptions([])
      } else {
        this.getBoardLists(event.target.value)
        .then(data => this.changeListsOptions(data))
        .catch(error => this.changeListsOptions([]))
      }
    },

    onHandleSubmit(event) {
      if (this.boardSelector.value.toLowerCase() !== 'доска' && this.listSelector.value.toLowerCase() !== 'список') {
        // this.createCard()
        console.log(this.boardSelector.value, this.listSelector.value)
      }
    },

    _init() {
      if (Trello.authorized()) {
        this._createdSelectors()
      } else {
        this.authonticated(this._createdSelectors)
      }
    }
  }

  let onHandleTrelloControllerFirstClick = function (event) {
    new TrelloController(event.target, event.target.dataOrderId)
    event.target.removeEventListener('click', onHandleTrelloControllerFirstClick)
  }

  if (trelloController.length > 0) {
    trelloController.forEach(cller => {
      cller.innerHTML = 'Нажмие для авторизации в Trello'
      cller.addEventListener('click', onHandleTrelloControllerFirstClick)
    })
  }
}