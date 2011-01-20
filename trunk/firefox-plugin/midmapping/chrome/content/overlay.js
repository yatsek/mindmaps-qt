var mindmapping = {
  onLoad: function() {
    // initialization code
    this.initialized = true;
    this.strings = document.getElementById("mindmapping-strings");
  },

  onMenuItemCommand: function(e) {
		//read preferences
		var prefManager = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefBranch);
		var programPath = prefManager.getCharPref("extensions.mindmapping.programPath");
		//get selected text
		var selectedText=content.getSelection().toString();
		if (selectedText.length > 5)
		{
			alert(selectedText);
			var file=Components.classes["@mozilla.org/file/local;1"].createInstance(Components.interfaces.nsILocalFile);
			file.initWithPath('/usr/bin/python');
			var process=Components.classes["@mozilla.org/process/util;1"].createInstance(Components.interfaces.nsIProcess);
			process.init(file);
			var argument='\"' + selectedText + '\"';
			var args= [programPath, '--text', argument];
			process.run(false,args,3);


		}

    var promptService = Components.classes["@mozilla.org/embedcomp/prompt-service;1"]
                                  .getService(Components.interfaces.nsIPromptService);
    promptService.alert(window, this.strings.getString("helloMessageTitle"),
                                this.strings.getString("helloMessage"));
  },

  onToolbarButtonCommand: function(e) {
    // just reuse the function above.  you can change this, obviously!
    mindmapping.onMenuItemCommand(e);
  }
};

window.addEventListener("load", mindmapping.onLoad, false);

