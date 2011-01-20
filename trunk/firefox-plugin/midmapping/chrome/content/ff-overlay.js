mindmapping.onFirefoxLoad = function(event) {
  document.getElementById("contentAreaContextMenu")
          .addEventListener("popupshowing", function (e){ mindmapping.showFirefoxContextMenu(e); }, false);
};

mindmapping.showFirefoxContextMenu = function(event) {
  // show or hide the menuitem based on what the context menu is on
  document.getElementById("context-mindmapping").hidden = gContextMenu.onImage;
};

window.addEventListener("load", mindmapping.onFirefoxLoad, false);
