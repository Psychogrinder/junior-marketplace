let trelloCardsCreator = function (orders) {
  let trelloController = document.querySelectorAll('.trelloIntegration')

  let TrelloController = function (container, orderData) {
    this.container = container
    this.orderData = orderData
    this._createdSelectors = this._createdSelectors.bind(this)
    this.onHandleBoardChange = this.onHandleBoardChange.bind(this)
    this.onHandleSubmit = this.onHandleSubmit.bind(this)
    this._closeIfCardAddedOrInitController = this._closeIfCardAddedOrInitController.bind(this)
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
      btn.classList.add('trello-btn-submit')
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

    renderTemplate(value) {
      let productItems = value.items.map( product => {
        return `> **Продукт**: ${product.name}\n
                > **Артикул**: ${product.id}\n
                > **Количество**: ${product.quantity}\n`
      })
      let desc = `
                  \n\`\`\`\n
                  Доставка:  ${value.delivery_method}
                  Покупатель: ${value.first_name}  ${value.last_name}
                  Адрес: ${value.delivery_address}
                  Телефон: ${value.consumer_phone}
                  Почта: ${value.consumer_email}
                  \`\`\`\n
                  \`Статус: ${value.status}\`\n
                  `;
              
      return productItems.join('\n---\n') + desc
            
    },

    onHandleBoardChange(event) {
      if (event.target.value.toLowerCase() === 'доска') {
        this.changeListsOptions([])
      } else {
        this.getBoardLists(event.target.value)
          .then(data => this.changeListsOptions(data))
          .catch(error => this.changeListsOptions([]))
      }
    },

    onHandleSubmit(event) {
      if (this.listSelector.value.toLowerCase() !== 'список') {
        let newCard = {
          name: 'Заказ #'+this.orderData.id,
          desc: this.renderTemplate(this.orderData),
          idList: this.listSelector.value,
          pos: 'bottom'
        }
        this.createCard(newCard)
          .then(data => {
            this.addOrderIdToLocalStorage()
            this.cardDone()
          })
      }
    },

    cardDone(){
      let div = document.createElement('div')
      div.classList.add('trello-card-done')
      this.setChild(div ,true)
    },

    isAlreadyAdded(){
      let ordersIds = JSON.parse(localStorage.getItem('trelloOrderIdsAdded')) || []
      if (ordersIds.indexOf(this.orderData.id) > -1) return true
      return false
    },

    addOrderIdToLocalStorage(){
      let ordersIds = JSON.parse(localStorage.getItem('trelloOrderIdsAdded')) || []
      ordersIds.push(this.orderData.id)
      localStorage.setItem('trelloOrderIdsAdded', JSON.stringify(ordersIds))
    },

    _closeIfCardAddedOrInitController(){
      if (this.isAlreadyAdded()){
        this.cardDone()
      } else {
        this._createdSelectors()
      }
    },

    _init() {
      if (Trello.authorized()) {
        this._closeIfCardAddedOrInitController()
      } else {
        this.authonticated(this._closeIfCardAddedOrInitController)
      }
    }
  }

  let onHandleTrelloControllerFirstClick = function (event) {
    let order = orders.find(el => {
      if (el.id === Number.parseInt(event.target.dataset.orderId)) return el
    })
    new TrelloController(event.target, order)
    event.target.classList.remove('trello-init')
    event.target.removeEventListener('click', onHandleTrelloControllerFirstClick)
  }

  if (trelloController.length > 0) {
    trelloController.forEach(cller => {
      // let div = document.createElement('div')
      cller.classList.add('trello-init')
      // cller.appendChild(div)
      cller.addEventListener('click', onHandleTrelloControllerFirstClick)
    })
  }
}