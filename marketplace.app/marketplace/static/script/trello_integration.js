let linkTrelloAccount = function (producer_id) {

  let inputBoardName = document.getElementsByClassName('trellointegration-input')[0]
  let trelloContainer = document.getElementsByClassName('trellointegration')[0]

  if (inputBoardName !== 'undefined' && inputBoardName.value.length > 0 && inputBoardName.value.length < 30) {

    let onSucces = function () {
      fetch(`/api/v1/producers/${producer_id}/trello-link`, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json; charset=utf-8",
          },
          body: JSON.stringify({
            'trello_token': Trello.token(),
            'board_name': inputBoardName.value
          }),
        })
        .then(data => trelloContainer.remove())
    }

    Trello.authorize({
      type: 'popup',
      name: 'Marketplace',
      persist: false,
      scope: {
        read: 'true',
        write: 'true'
      },
      expiration: 'never',
      success: onSucces
    })
  }


}
