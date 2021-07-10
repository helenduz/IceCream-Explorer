/* sets different search area divs for different search conditions */
function changeSearchArea(name) {
  clearAll();
  if (name === "brand") {
    document.getElementById("brand-search").style.display = "flex";
  }
  else if (name === "name") {
    document.getElementById("site-search").style.display = "flex";
    document.getElementById("site-search-text").placeholder='Enter a product name/subhead, eg. Cannoli';
  }
  else if (name === "ingredients") {
    document.getElementById("site-search").style.display = "flex";
    document.getElementById("site-search-text").placeholder='Enter an ingredient, eg. chocolate';
  }
  else if (name === "advance"){
    document.getElementById("advance-search").style.display = "block";
  }
}


/* initiates the search area by clearing all divs that correspond to other search conditions */
function clearAll(){
    var seachDropDown = document.getElementById("brand-search");
    var searchBar = document.getElementById("site-search");
    var advanceSearch = document.getElementById("advance-search");

    seachDropDown.style.display = "none";
    searchBar.style.display = "none";
    advanceSearch.style.display = "none";
}
