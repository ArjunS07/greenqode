function searchOnGoogle() {
    var itemName = document.getElementById('item-detail-name').value 
    if (itemName) {
      var googleLink = "https://www.google.com/search?q=" + itemName;
      window.open(googleLink)
    }
    
  }

  document.getElementById("google-search-href").addEventListener("click", searchOnGoogle)
