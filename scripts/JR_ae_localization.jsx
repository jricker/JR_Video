// Global Variables
var tcd_origParentFolder, tcd_parentFolder, tcd_fixExp, tcd_maxDepth, tcd_copyNum, tcd_progDlg;
var tcd_scriptName = "Localization Script";
var tcd_version = "3.9.5";
var tcd_folderNameDef = "Duplicated Comps";
var tcd_strHelpHeader = tcd_scriptName + " v" + tcd_version;
var tcd_strHelpText = "NO HELP FOR YOU!.";
var previousComps = [];
var previousFolders = [];
var previousFootage = [];
var tcd_prefsToSave = [];
var tcd_expFixCount = 0;
var tcd_fixExp = 1
var copyTxt = "1";
var check = ''
// newNamespreSufChk
var preSufChk = 0;
var preSufTxt = "";
////////////////////
var replChk = false;
var replSrchTxt = "";
var replReplTxt =  "";
var incChk = true;
var incDrp = "Last";
var colDrp = "Red";
var colChk = 0
var preSufDrp = "Prefix"
// optionsGrp
var grpFldChk = 0; // change this to true for the test
var grpFldTxt = ""; // add a folder name for the test
////////////////////////////////////////////
var incExcChk = false;
var incExcDrp = "Prefix";
var incExcTxt = "_";
var tcd_maxDepth = -1
var depChk = false;
var depTxt = "1";
var expChk = 1;
var dupFtgChk = false;
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// -- Prototypes
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}

if (typeof String.prototype.endsWith != 'function') {
  String.prototype.endsWith = function (str){
    return this.slice(-str.length) == str;
  };
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// -- Functions
function escapeRegExp(str) {
  return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
}

// Get the names of the label colors in order 1-16
function tcd_getColorNames() {
    var colors = [];
    
    // Locate valid label preferences key
    var prefKeyBase = "Label Preference Text Section ";
    var prefKey = null;
    for (var i=1; i<=10; i++) {
        var newPrefKey = prefKeyBase + i;
        if (parseFloat(app.version) >= 12) {
            // After Effects CC splits up preference files into different groups
            // Adding the third parameter specifies which preference file to look in
            if (app.preferences.havePref(newPrefKey, "Label Text ID 2 # 1", PREFType.PREF_Type_MACHINE_INDEPENDENT)) {
                prefKey = newPrefKey;
                break;
            }
        } else {
            if (app.preferences.havePref(newPrefKey, "Label Text ID 2 # 1")) {
                prefKey = newPrefKey;
                break;
            }            
        }
    }  
    if (prefKey) {
        if (parseFloat(app.version) >= 12) {
            for (var i=1; i<=16; i++) {
                if (app.preferences.havePref(newPrefKey, "Label Text ID 2 # " + i, PREFType.PREF_Type_MACHINE_INDEPENDENT)) {
                    var col = app.preferences.getPrefAsString(prefKey , "Label Text ID 2 # " + i, PREFType.PREF_Type_MACHINE_INDEPENDENT);
                    colors.push(col);
                }
            }
        } else {
            for (var i=1; i<=16; i++) {
                if (app.preferences.havePref(newPrefKey, "Label Text ID 2 # " + i)) {
                    var col = app.preferences.getPrefAsString(prefKey , "Label Text ID 2 # " + i);
                    colors.push(col);
                }
            }
        }
    } else {
        //$.writeln("prefkey not found");
    }
    return colors;
}
function tcd_loadAndRegPref(prop, def) {
    // Load and register a setting stored in preferences
    // Setting name is auto determined based on property name in GUI

    // Get the property's name
    var name = null;
    for (var child in prop.parent) {
        if (prop.parent[child] == prop) {
            name = child;
        }
    }

    if (name != null) {
        var value = def;
        if (app.settings.haveSetting(tcd_scriptName, name)) {
            value = app.settings.getSetting(tcd_scriptName, name);
        }
        
        // Apply the value based on the type of control
        if (prop instanceof Checkbox) {
            prop.value =! (/^true$/i).test(value); // Opposite because notify() will invert
            prop.notify(); // Updates Enable/Disable
        } else if (prop instanceof EditText) {
            prop.text = value;
        } else if (prop instanceof DropDownList) {
            for (var i=0; i<prop.items.length; i++) {
                if (prop.items[i].text === value) {
                    prop.selection = i;
                }
            }
        }
    }
    
    tcd_prefsToSave.push(prop);
}

function tcd_savePrefs() {
    // Save all of the prefs found in tcd_prefsToSave

    for (var i=0; i<tcd_prefsToSave.length; i++) {
        var prop = tcd_prefsToSave[i];

        // Get the value based on the type of control
        var value = "";
        if (prop instanceof Checkbox) {
            value = prop.value;
        } else if (prop instanceof EditText) {
            value = prop.text;
        } else if (prop instanceof DropDownList) {
            value = prop.selection.text;
        }
        
        // Get the property's name
        var name = null;
        for (var child in prop.parent) {
            if (prop.parent[child] == prop) {
                name = child;
            }
        }
        
        // Save the value to the preferences
        if (name != null) {
            app.settings.saveSetting(tcd_scriptName, name, value);
        }
    }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function tcd_buildUI(thisObj) {
    if (thisObj instanceof Panel) {
        var myPal = thisObj;
    } else {
        var myPal = new Window("palette","test script", [300,100,553,410]);
    }

    if (myPal != null) {
        var res =
        "group { \
                alignment: ['fill', 'fill'], \
                alignChildren: ['left','top'], \
                orientation: 'column', \
            newNamesGrp: Panel { \
                alignment: ['fill','top'], \
                alignChildren: ['left','top'], \
                text:'Regions', \
                allGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    allChk: Checkbox {text:''}, \
                    allLbl: StaticText {text:'SELECT ALL', aligment:['left','left']}, \
                }, \
                ukGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    ukChk: Checkbox {text:''}, \
                    ukLbl: StaticText {text:'UK', aligment:['left','left']}, \
                }, \
                itGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    itChk: Checkbox {text:''}, \
                    itLbl: StaticText {text:'Italy', aligment:['left','left']}, \
                }, \
                frGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    frChk: Checkbox {text:''}, \
                    frLbl: StaticText {text:'France', aligment:['left','left']}, \
                }, \
                spGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    spChk: Checkbox {text:''}, \
                    spLbl: StaticText {text:'Spain', aligment:['left','left']}, \
                }, \
                gerGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    gerChk: Checkbox {text:''}, \
                    gerLbl: StaticText {text:'Germany', aligment:['left','left']}, \
                }, \
                ruGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    ruChk: Checkbox {text:''}, \
                    ruLbl: StaticText {text:'Russia', aligment:['left','left']}, \
                }, \
                japGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    japChk: Checkbox {text:''}, \
                    japLbl: StaticText {text:'Japan', aligment:['left','left']}, \
                }, \
                polGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    polChk: Checkbox {text:''}, \
                    polLbl: StaticText {text:'Poland', aligment:['left','left']}, \
                }, \
                auGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    auChk: Checkbox {text:''}, \
                    auLbl: StaticText {text:'Australia', aligment:['left','left']}, \
                }, \
                naGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    naChk: Checkbox {text:''}, \
                    naLbl: StaticText {text:'North America', aligment:['left','left']}, \
                }, \
                wwGrp: Group { \
                    orientation: 'row', \
                    alignment: ['fill','top'], \
                    wwChk: Checkbox {text:''}, \
                    wwLbl: StaticText {text:'World Wide (General)', aligment:['left','left']}, \
                }, \
            }, \
            excelGrp: Group { \
                orientation: 'row', \
                alignment: ['fill','top'], \
                excelBtn: Button {text:'Create Excel Document', alignment:['left','top']}, \
            } \
            btnGrp: Group { \
                orientation: 'row', \
                alignment: ['fill','top'], \
                fileBtn: Button {text:'Select File', alignment:['left','top']}, \
                fileTxt: StaticText {alignment:['fill','left'], text:' ...'}, \
            } \
            goGrp: Group { \
                orientation: 'row', \
                alignment: ['fill','top'], \
                goBtn: Button {text:' Create ', alignment:['left','top']}, \
            } \
        }";
        // VARIABLES
        var userHomeFolder = "C:/Users/" +system.userName;
        //var textFile = new File(userHomeFolder+"desktop", "mytext.txt");
        //alert(userHomeFolder)
        myPal.grp = myPal.add(res);
        var listOfRegions = {'uk':0, 'na':0, 'it':0, 'fr':0, 'sp':0, 'ger':0, 'ru':0, 'jap':0, 'pol':0, 'au':0, 'ww':0}
        var regionsToConvert = []
        // -- Enable/Disable items based on checkboxes
        //for (var i in listOfRegions){
        //    if (listOfRegions[i] == 1){
        //        alert('there is one here');
        //    } else {
        //        alert(listOfRegions[i]);
        //    }
        //}
        //alert(listOfRegions.value)

        // Select All
        //myPal.grp.newNamesGrp.preSufGrp.preSufpreSufChk.enabled.value;
        //myPal.grp.newNamesGrp.preSufGrp.preSufpreSufChk.enabled.value;
        myPal.grp.newNamesGrp.allGrp.allChk.onClick = function() {
            myPal.grp.newNamesGrp.naGrp.naChk.value = this.value;
            myPal.grp.newNamesGrp.ukGrp.ukChk.value = this.value;
            myPal.grp.newNamesGrp.itGrp.itChk.value = this.value;
            myPal.grp.newNamesGrp.frGrp.frChk.value = this.value;
            myPal.grp.newNamesGrp.spGrp.spChk.value = this.value;
            myPal.grp.newNamesGrp.gerGrp.gerChk.value = this.value;
            myPal.grp.newNamesGrp.ruGrp.ruChk.value = this.value;
            myPal.grp.newNamesGrp.japGrp.japChk.value = this.value;
            myPal.grp.newNamesGrp.polGrp.polChk.value = this.value;
            myPal.grp.newNamesGrp.auGrp.auChk.value = this.value;
            myPal.grp.newNamesGrp.wwGrp.wwChk.value = this.value;
            listOfRegions['na'] = this.value;
            listOfRegions['uk'] = this.value;
            listOfRegions['it'] = this.value;
            listOfRegions['fr'] = this.value;
            listOfRegions['sp'] = this.value;
            listOfRegions['ger'] = this.value;
            listOfRegions['ru'] = this.value;
            listOfRegions['jap'] = this.value;
            listOfRegions['pol'] = this.value;
            listOfRegions['au'] = this.value;
            listOfRegions['ww'] = this.value;
        }
        myPal.grp.newNamesGrp.naGrp.naChk.onClick = function() {
            myPal.grp.newNamesGrp.naGrp.naChk.value = this.value
            listOfRegions['na'] = this.value;
            //alert(listOfRegions['na']);
        }
        myPal.grp.newNamesGrp.ukGrp.ukChk.onClick = function() {
            myPal.grp.newNamesGrp.ukGrp.ukChk.value = this.value
            listOfRegions['uk'] = this.value;
            //alert(listOfRegions['uk']);
        }
        myPal.grp.newNamesGrp.itGrp.itChk.onClick = function() {
            myPal.grp.newNamesGrp.itGrp.itChk.value = this.value;
            listOfRegions['it'] = this.value
            //alert(listOfRegions['it']);
        }
        myPal.grp.newNamesGrp.frGrp.frChk.onClick = function() {
            myPal.grp.newNamesGrp.frGrp.frChk.value = this.value;
            listOfRegions['fr'] = this.value
            //alert(listOfRegions['fr']);
        }
        myPal.grp.newNamesGrp.spGrp.spChk.onClick = function() {
            myPal.grp.newNamesGrp.spGrp.spChk.value = this.value;
            listOfRegions['sp'] = this.value
            //alert(listOfRegions['sp']);
        }
        myPal.grp.newNamesGrp.gerGrp.gerChk.onClick = function() {
            myPal.grp.newNamesGrp.gerGrp.gerChk.value = this.value;
            listOfRegions['ger'] = this.value
            //alert(listOfRegions['ger']);
        }
        myPal.grp.newNamesGrp.ruGrp.ruChk.onClick = function() {
            myPal.grp.newNamesGrp.ruGrp.ruChk.value = this.value;
            listOfRegions['ru'] = this.value
            //alert(listOfRegions['ru']);
        }
        myPal.grp.newNamesGrp.japGrp.japChk.onClick = function() {
            myPal.grp.newNamesGrp.japGrp.japChk.value = this.value;
            listOfRegions['jap'] = this.value
            //alert(listOfRegions['jap']);
        }
        myPal.grp.newNamesGrp.polGrp.polChk.onClick = function() {
            myPal.grp.newNamesGrp.polGrp.polChk.value = this.value;
            listOfRegions['pol'] = this.value
            //alert(listOfRegions['pol']);
        }
        myPal.grp.newNamesGrp.auGrp.auChk.onClick = function() {
            myPal.grp.newNamesGrp.auGrp.auChk.value = this.value;
            listOfRegions['au'] = this.value
            //alert(listOfRegions['au']);
        }
        myPal.grp.newNamesGrp.wwGrp.wwChk.onClick = function() {
            myPal.grp.newNamesGrp.wwGrp.wwChk.value = this.value;
            listOfRegions['ww'] = this.value
            //alert(listOfRegions['ww']);
        }
        // -- Load and Register Settings
        var grp = myPal.grp
        // btnGrp
        // newNamesGrp
        // btnGrp
        //tcd_loadAndRegPref(grp.btnGrp.copyTxt, "1");
        // button variables from original        
        // btnGrp
        //tcd_loadAndRegPref(copyTxt, "1");
        //tcd_loadAndRecopyTxt, "1");
        var projOne, itemTotalOne, curItemOne, ItemAryOne;
        ItemAryOne = new Array();
        projOne = app.project;
        itemTotalOne = projOne.numItems;
        for (var i=1; i<=itemTotalOne; i++){
            curItemOne = projOne.item(i);
            if (curItemOne instanceof CompItem){
                ItemAryOne[ItemAryOne.length] = curItemOne;
            }
        }
        // -- Buttons
        myPal.grp.excelGrp.excelBtn.onClick = function () {
            //writeLn(app.project.item(1).layer(1).source.name + " THIS IS THE SOURCE NAME")
            var compIdent = "text";
            var fantastic = new Array();
            //writeLn(fantastic.toString() + "TESTING")
            for (var x in ItemAryOne){
                //if(ItemAryOne[x].name.indexOf(compIdent) >= 0 ){ // this gets into the comps which have "text" in their names
                    totalLayers = ItemAryOne[x].numLayers;
                    //writeLn(totalLayers + " THIS IS THE LAYER COUNT TO THE CURRENT LAYER" + ItemAryOne[x].name);
                    // need to find a way to shift through the layers which are text layres
                    for (var y = 1; y<=totalLayers; y++){
                        curLayer = ItemAryOne[x].layer(y)
                        //writeLn(" THIS IS THE CURRENT LAYER " + curLayer.name)
                        if (curLayer instanceof TextLayer){
                            //writeLn ("TEXT ONLY CURRENT LAYERS == " + curLayer.name)
                            var tests = ItemAryOne[x].layer(y).property("Text").property("sourceText").value
                            //var tests2 = (ItemAryOne[x].name.toString() + ":_:" +tests.toString())
                            fantastic[fantastic.length] = (ItemAryOne[x].name.toString() + ":_:" +tests.toString())
                            //alert(ItemAryOne[x].name.toString() + ":_:" +tests.toString())
                            //writeLn(tests2)
                            //alert(ItemAryOne[x].layer(y).property("Text").property("sourceText").value + ItemAryOne[x])
                        //}
                        }
                    }
                    //writeLn(ItemAryOne[x].layer(1).property("Text").property("sourceText").value)
                    //ItemAryOne[x].layer(1).property("Text").property("sourceText").setValue("TESTING");
                }
            //var fh = fopen(userHomeFolder+"MyFile.txt", 3); // Open the file for writing
            //var fantastic = ["hi","test"]
            var fantasticLength = fantastic.length
            var wholeList = ''
            for (var x in fantastic){
                wholeList+=fantastic[x]
                if (x < fantasticLength-1){
                    wholeList+= "--B--"
                }
            }
            var final_list = ''
            for (var i=0; i<wholeList.length; i++) {
                if(wholeList[i] == '&'){
                    final_list += '%26'
                }else if(wholeList[i] == '>'){
                    final_list += '%'+'3E'
                }else if(wholeList[i] == '<'){
                    final_list += '%'+'3C'
                }else if(wholeList[i] == '|'){
                    final_list += '%'+'7C'
                }else if(wholeList[i] == '\\'){
                    final_list += '%'+'5C'
                } else {
                    final_list += wholeList[i]
                }
            }
            //
            system.callSystem(userHomeFolder+"\\Documents\\GitHub\\JR_Video\\scripts\\JR_AE_Generate.bat " + final_list);
        }
        myPal.grp.btnGrp.fileBtn.onClick = function () {
            var myFile = File.openDialog("Select a text file to open.", "");//, "TEXT txt")
            var fileOK = myFile.open("r","TEXT","????");
            var fileName = myFile.fsName;
            myPal.grp.btnGrp.fileTxt.text = fileName;
            //alert(fileOK.type)
        }
        // Duplicate Selected
        myPal.grp.goGrp.goBtn.onClick = function() {
            tcd_expFixCount = 0; // Reset
            clearOutput();
            var expErrors = [];
            regionsToConvert = [] //reset it
            if (myPal.grp.btnGrp.fileTxt.text ==' ...'){
                alert("Please Select File")
                //replaceText()
            } else {
                for (var i in listOfRegions){
                    if (listOfRegions[i] == 1){
                        regionsToConvert.push(i)
                        //alert(i + '  will be converted ');
                    }
                }
                var numberOfRegions = regionsToConvert.length
                var errors = [];
                var selItems = app.project.selection.slice(0); // Make a copy for safety
                var copies = parseInt(copyTxt);
                for (var iii = 0; iii < numberOfRegions; iii++){
                    //alert(iii)
                    //writeLn(i)
                    grpFldChk = 1
                    grpFldTxt = regionsToConvert[iii]
                    //writeLn(regionsToConvert[i])
                    preSufChk = 1;
                    preSufTxt = regionsToConvert[iii] + "_";
                    //alert(regionsToConvert[i])    
                    // -- Validate the inputs
                    // Prefix/Suffix
                    if (preSufChk) {
                        if (preSufTxt === "") {
                            errors.push("No value supplied for Prefix or Suffix");
                        }
                    }
                    // Search/Replace
                    if (replChk.value) {
                        if (replSrchTxt === "" ||
                            replReplTxt == "") {
                            errors.push("No value supplied for Search and Replace");
                        }
                    }
                    // Exclude
                    if (incExcChk.value) {
                        if (incExcTxt == "") {
                            errors.push("No value supplied for Include Exclude ");
                        }
                        if (incExcDrp == "Matching Regex") {
                            // Make sure the regex is valid
                            try {
                                var re = new RegExp(incExcTxt, "g");
                            } catch(e) {
                                errors.push("Invalid regex for exclude: JR");
                            }
                        }
                    }
                    // Group items into folder
                    if (grpFldChk) {
                        if (grpFldTxt == "") {
                            errors.push("No value supplied for folder");
                        }
                    }
                    // -- Make sure there are items selected in the project panel
                    if (selItems.length <= 0) {
                        errors.push("No item selected in the project panel.");
                    }
                    // -- Save Settings
                    // These were registered to be saved when they were loaded
                    tcd_savePrefs();
                    // Determine whether to fix expressions during replaceSource           
                    // Determine max depth
                    if (depChk.value) {
                        tcd_maxDepth = depTxt.text;
                    } else {
                        tcd_maxDepth = -1;
                    }            
                    // Determine the number of copies
                    // -- Duplicate selected if no errors
                    if (errors.length > 0) {
                        alert("Error\n" + errors.join("\n"));
                    } else {
                        app.beginUndoGroup("True Comp Duplicator");
                        app.beginSuppressDialogs();
                        //
                        var max = app.project.numItems * copies;
                        if (tcd_fixExp) { max = max * 2; }
                        tcd_progDlg = new progressDlg().create("Duplicating Selected...", max);
                        var newComps = [];
                        var newFolders = [];
                        var newFootage = [];
                        try {
                            for (var c=0; c<copies; c++) {
                                tcd_progDlg.setTitle("Duplicating Selected...");                        
                                // Reset the list for each successive run
                                previousComps = []; previousFolders = []; previousFootage = [];
                                // Store the copy number so other functions can access it
                                tcd_copyNum = c;
                                // Create the group folder if specified
                                if (grpFldChk) {
                                    tcd_createGroupFolder(selItems[0]);
                                }
                                // Duplicate the item
                                var result = {};
                                for (var s=0; s<selItems.length; s++) {
                                    result = tcd_duplicate(selItems[s]);
                                }                 
                                // Compile a list of the new comps
                                for (var i=0; i<result.comps.length; i++) {
                                    newComps.push(result.comps[i].dest);
                                }                       
                                // Compile a list of the new folders
                                for (var i=0; i<result.folders.length; i++) {
                                    newFolders.push(result.folders[i].dest);
                                }                   
                                // Compile a list of the new footage
                                for (var i=0; i<result.footage.length; i++) {
                                    newFootage.push(result.footage[i].dest);
                                }                    
                                // Fix the expressions if needed
                                if (tcd_fixExp){
                                    tcd_progDlg.setTitle("Updating Expressions...");
                                    var expComps = [];
                                    for (var i=0; i<result.comps.length; i++) {
                                        expComps.push(result.comps[i].dest);
                                    }
                                    var errors = tcd_updateExpressions(expComps);
                                    expErrors.push.apply(expErrors, errors);
                                }                   
                                // Set label colors for comps
                                if (colChk.value) {
                                    // newComps
                                    colValueCheck = 0
                                    for (var i=0; i<newComps.length; i++) {
                                        //var index = colDrp.selection.index + 1;
                                        var index = colValueCheck + 1;
                                        newComps[i].label = index;
                                    }                        
                                    // newFolders
                                    for (var i=0; i<newFolders.length; i++) {
                                        //var index = colDrp.selection.index + 1;
                                        var index = colValueCheck + 1;
                                        newFolders[i].label = index;
                                    }                        
                                    // newFootage
                                    for (var i=0; i<newFootage.length; i++) {
                                        //var index = colDrp.selection.index + 1;
                                        var index = colValueCheck + 1;
                                        newFootage[i].label = index;
                                    }
                                }
                            }
                        } catch (err) {
                            alert(err);
                        }                
                        var statusTxt = (newComps.length + newFolders.length + newFootage.length) + " items duplicated";
                        if (tcd_fixExp) {
                            statusTxt = statusTxt + ", " + tcd_expFixCount + " expressions updated";
                        }
                        tcd_progDlg.complete("Process Complete!", statusTxt);
                        app.endSuppressDialogs(false);
                        app.endUndoGroup();
                    }
                    if (expErrors.length > 0) {
                        new expErrWindow().run(expErrors);
                    }
                }   
            }
            excelDocuent = myPal.grp.btnGrp.fileTxt.text
            regionsToConvert.unshift(excelDocuent)
            var excelVarList = ''
            var regionsToConvertLength = regionsToConvert.length
            for (var x in regionsToConvert){
                excelVarList+=regionsToConvert[x]
                if (x < regionsToConvertLength-1){
                    excelVarList+= ","
                }
            }
            // CALL REPLACE FUNCTION
            //alert(excelVarList)
            system.callSystem(userHomeFolder+"\\Documents\\GitHub\\JR_Video\\scripts\\JR_AE_Replace.bat " + excelVarList)
            replaceText()
        }
        // -- Final Cleanup
        myPal.layout.layout(true);
        myPal.layout.resize();
        myPal.onResizing = myPal.onResize = function () {this.layout.resize();}
    }
    return myPal;
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function myTrim(x) {
    return x.replace(/^\s+|\s+$/gm,'');
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function replaceText() {
    // data text file is saved to desktop
    var myFile = new File("~/Desktop/data.txt")
    projOne = app.project;
    itemTotalOne = projOne.numItems;
    // open file
    var xx = 0
    var fileOK = myFile.open("r","TEXT","????");
    if (fileOK){
        var curItemOne
        // read text lines
        // until end-of-file is reached
        while (!myFile.eof){
            t = myFile.readln();
            var line = t.split(':,:,:');
            for (var i=1; i<=itemTotalOne; i++){
                curItemOne = projOne.item(i);
                if (curItemOne instanceof CompItem){
                    if ("'"+curItemOne.name+"'" == line[0]){
                        compLayers = curItemOne.numLayers;
                        for (var y = 1; y<=compLayers; y++){
                            curLayer = curItemOne.layer(y)
                            if (curLayer instanceof TextLayer) {
                                xx++
                                replace = myTrim(line[1].slice(1,-1))
                                //alert(replace)
                                //s = myTrim(curLayer.name)
                                AA = curLayer.property("Text").property("sourceText").value;
                                //s = new String(AA);
                                source = myTrim(String(AA) )
                                //BB = String.valueOf(AA)
                                //alert(BB)
                                //BB = replace.slice(1,-1)
                                //alert(BB)
                                //if (source.toLowerCase() == replace.toLowerCase() ){
                                //alert(xx)
                                //alert(String(line[0]) + ' ' + String(line[1]) + ' ' + String(line[2]))
                                //alert(source + 'SOURCE')
                                //alert(replace + 'REPLACE')
                                if (source.toLowerCase() == replace.toLowerCase()){
                                    //alert('yes')
                                    //alert(curLayer.property("Text").property("sourceText").value)
                                    //alert(replace.slice(1,-1))
                                    curLayer.property("Text").property("sourceText").setValue(line[2].slice(1,-1))
                                }
                            }
                        }
                    }
                }
            }
        }
    //myFile.close();
    } else {
        alert("File open failed!");
    }
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// -- Progress Dialog
function progressDlg() {
    this.windowRef = null;
}
function progressDlgClose() {
    win.close();
}

progressDlg.prototype.create = function(title, max) {
    var win = new Window("palette", tcd_scriptName + " Progress",undefined,{resizeable:true, closeButton:false});  // bounds = [left, top, right, bottom]
    this.windowRef = win;

    var res =
    "group { \
        alignment: ['fill', 'fill'], \
        alignChildren: ['left','top'], \
        orientation: 'column', \
        titleTxt: StaticText {text:'"+title+"', alignment:['fill','left']}, \
        statusTxt: StaticText {text:'', alignment:['fill','left']}, \
        progGrp: Group { \
            orientation: 'row', \
            alignment: ['fill','top'], \
            progBar: Progressbar {alignment:['fill','center'], preferredSize:[200,-1], maxvalue:'"+max+"'}, \
            progBtn: Button {text:'Cancel', alignment:['right','center'], properties:{name:’cancel’}}, \
        }, \
    }";
    
    win.grp = win.add(res);
    
    // Cancel Button
    this.cancel = false;
    win.grp.progGrp.progBtn.onClick = function() {
        this.cancel = true;
        win.close();
    }
    //if (window.opener.win){
    //    win.close();
    //}
    // -- Final Cleanup
    win.layout.layout(true);
    win.layout.resize();
    win.onResizing = win.onResize = function () {this.layout.resize();}

    // Display the window
    win.center();
    win.show();
    return this;        
}
progressDlg.prototype.setTitle = function(titleTxt) {
    this.windowRef.grp.titleTxt.text = titleTxt;
}

progressDlg.prototype.update = function(increment, statusTxt) {
    this.windowRef.grp.progGrp.progBar.value = this.windowRef.grp.progGrp.progBar.value + increment;
    this.windowRef.grp.statusTxt.text = statusTxt;
}

progressDlg.prototype.close = function() {
    this.windowRef.close();
}

progressDlg.prototype.complete = function(titleTxt, statusTxt) {
    this.windowRef.grp.titleTxt.text = titleTxt;
    this.windowRef.grp.statusTxt.text = statusTxt;
    this.windowRef.grp.progGrp.progBar.value = this.windowRef.grp.progGrp.progBar.maxvalue;
    this.windowRef.grp.progGrp.progBtn.text = "Ok";
    this.windowRef.close();
}

// -- Help Window
function helpWindow() {
    this.windowRef = null;
}
//setTimeout(function closeWindow() {
//    this.windowRef.close();
//}, 2000);

helpWindow.prototype.run = function() {
    var win = new Window("palette", tcd_scriptName,[100,0,580,600]);  // bounds = [left, top, right, bottom]
    this.windowRef = win;
    win.btnPanel = win.add("group", [10,10,600,600]);
    win.btnPanel.text = win.btnPanel.add("statictext", [10,10,400,25], tcd_strHelpHeader);
    win.btnPanel.warnBtn = win.btnPanel.add("edittext", [10,40,450,540], tcd_strHelpText, {multiline:true});
    win.btnPanel.aesBtn = win.btnPanel.add("button", [310, 550,450, 580], "http://aescripts.com");

    win.btnPanel.aesBtn.onClick = function() {
        openURL("http://aescripts.com");    
    };

    // Display the window
    win.center();
    win.show();
    return true;        
}

// -- Expression Error Window
function expErrWindow() {
    this.windowRef = null;
}

expErrWindow.prototype.run = function(expErrors) {
    var win = new Window("palette", tcd_scriptName + " - Expression Errors",[100,0,580,600]);  // bounds = [left, top, right, bottom]
    this.windowRef = win;
    win.btnPanel = win.add("group", [10,10,600,600]);
    win.btnPanel.text = win.btnPanel.add("statictext", [10,10,400,25], "Duplication complete, but with " + expErrors.length + " expression error(s)...");
    win.btnPanel.warnBtn = win.btnPanel.add("edittext", [10,40,450,540], expErrors.join("\n\n"), {multiline:true});
    win.btnPanel.aesBtn = win.btnPanel.add("button", [310, 550,450, 580], "Ok");

    win.btnPanel.aesBtn.onClick = function() {
        win.close();
    };

    // Display the window
    win.center();
    win.show();
    return true;
}


function openURL(url)  // This function open a URL in a browser - Copyright (c) 2006-2007 redefinery (Jeffrey R. Almasol). All rights reserved.
{   
    if ($.os.indexOf("Windows") != -1){
        system.callSystem("cmd /c \""+ Folder.commonFiles.parent.fsName + "\\Internet Explorer\\iexplore.exe" + "\" " + url);
    } else {
        var cmd = "open \"" + url + "\"";  // Switched to open, tad bit faster
        // $.writeln("cmd: " + cmd);
        system.callSystem(cmd);
    }
}

function tcd_saveProjItmSel() {
    // Save the current selection of items in the project panel
    var result = app.project.selection.slice(0); // Make a copy
    return result;
}

function tcd_loadProjItmSel(sel) {
    // Load a saved selection of items in the project panel    
    for (var i=0; i<sel.length; i++) { sel[i].selected = true; }
}

function tcd_clearProjItmSel() {
    // Deselect all project items
    for (var i=1; i<=app.project.numItems; i++) { app.project.item(i).selected = false; }
}

function tcd_duplicateProjItem(item) {
    // Duplicate the supplied project item
    // There isn't a direct way to duplicate footage items
    // through the JavaScript framework, so we'll use the menu
    // command to do it.
    
    var chk = tcd_checkPreviousFootage(item);
    
    var result = [];
    if (chk == null) {
        
        // Make sure the project panel is visible or this won't work
        app.project.showWindow(true);
        
        // Save current selection
        var sel = tcd_saveProjItmSel();
        
        // Deselect all items
        tcd_clearProjItmSel();
        
        // Store a list of item ids
        var beforeIDs = [];
        for (var d=1; d<=app.project.numItems; d++) {
            beforeIDs.push(app.project.item(d).id);
        }
        
        // Select specificied item
        item.selected = true;

        // Duplicate it using the menu command
        // To find the command ID use:
        //      app.findMenuCommandId("Duplicate"); // Result: 2080;
        // However, this will change depending on the language, so we will use the result
        app.executeCommand(2080);
        
        // Compare the saved list of ids to the current
        for (var d=1; d<=app.project.numItems; d++) {
            var itm = app.project.item(d);
            
            var found = false;
            for (var i=0; i<beforeIDs.length; i++) {
                if (itm.id == beforeIDs[i]) { found = true; }
            }
        
            if (found == false) { result.push(itm); }
        }
        // Reload the selection
        tcd_clearProjItmSel(); tcd_loadProjItmSel(sel);

        if (result.length > 0 && result[0] != null) {
            // Change the items name
            for (var r=0; r<result.length; r++) {
                result[r].name = tcd_changeName(item.name);
            }
            
            // Check if folder structure should be duplicated
            if (tcd_progDlg.cancel == false && grpFldChk) {
                // Duplicate the folder structure
                result[0].parentFolder = tcd_duplicateFolderStructure(result[0].parentFolder);
            }
            
            // Store the footage in previousFootage
            var ftg = {};
            ftg.source = item;
            ftg.dest = result[0];
            previousFootage.push(ftg);
        }
        
    } else {
        result.push(chk);
    }
    
    // Return the new item
    if (result.length > 1) { return result;
    } else if (result.length == 1) { return result[0];
    } else { return null; };
}

function tcd_duplicateCompStructure(comp, tcd_depth) {
    // Duplicate the supplied comp structure
    
    // -- Duplicate the incoming comp and set its name
    var newCompName = tcd_changeName(comp.name);
    var compResult = {};
    compResult.source = comp;
    var comp = comp.duplicate();
    if (preSufChk ||
        replChk.value ||
        incChk.value) {
            comp.name = newCompName;
    }
    compResult.dest = comp;
    previousComps.push(compResult);
    
    // -- Iterate through the comp and check for subcomps
    // and footage item's that need to be duplicated
    for (var i=1; i<=comp.numLayers; i++) {
        var layer = comp.layer(i);

        if (tcd_progDlg.cancel) { break; }
        tcd_progDlg.update(1, newCompName);
        
        if (layer instanceof AVLayer && tcd_incExcFilter(layer.source.name)) {
            if (layer.source && layer.source instanceof CompItem) {
                // Layer is a comp

                // Make sure we are still complying with the depth limit
                if (tcd_maxDepth == -1 || tcd_depth < tcd_maxDepth) {
                    // Check if this comp has already been duplicated
                    check = tcd_checkPreviousComps(layer.source);

                    if (check != null) {
                        // If so, replace the source with the already duplicated comp
                        tcd_replaceSource(layer, check, tcd_fixExp);
                    } else {
                        // If not, duplicate it

                        // Update: Store the previousComps as an object
                        // This allows for faster processing later.
                        var compResult = {};
                        compResult.source = layer.source;
                                        
                        // Replace the source of the layer, and recursively check in that subcomp for sub-subcomps
                        var newComp = tcd_duplicateCompStructure(layer.source, tcd_depth+1);
                        tcd_replaceSource(layer, newComp, tcd_fixExp);

                        compResult.dest = layer.source;
                        previousComps.push(compResult);
                    }
                }
            } else if (layer.source.mainSource instanceof FileSource) {
                // Layer is an AVLayer and has a FileSource, so we'll duplicate it
                // There doesn't seem to be a benefit for duplicating solids, so we won't
                if (dupFtgChk.value) {
                    
                    var newItem = tcd_duplicateProjItem(layer.source);
                    if (newItem != null) {
                        tcd_replaceSource(layer, newItem, tcd_fixExp);
                    }
                }
            }
        }
    }
    
    // Check if folder structure should be duplicated
    if (tcd_progDlg.cancel == false && grpFldChk) {
        // Duplicate the folder structure
        comp.parentFolder = tcd_duplicateFolderStructure(comp.parentFolder);
     }

    // For the recursion, return the duplicate comp
    return comp;
}

function tcd_replaceSource(layer, newItem, fixExp) {
    // Replace Source, placeholder for any future improvements needed in this area
    layer.replaceSource(newItem, fixExp);
}

function tcd_incExcFilter(name) {
    // Determine whether to skip duplicating the specified item
    // Returns true to duplicate, false to skip
    
    // Make sure exclude was checked
    if (incExcChk.value) {
        // Determine whether we're looking for a prefix or suffix or matching regex
        // Then return the result if true
        var preSufTypeB = incExcDrp;
        var preSufTxt = incExcTxt;
        if (preSufTypeB.toLowerCase() == "prefix") {
            if (name.startsWith(preSufTxt)) {
                return false;
            }
        } else if (preSufTypeB.toLowerCase() == "suffix") {
            if (name.endsWith(preSufTxt)) {
                return false;
            }
        } else if (preSufTypeB.toLowerCase() == "matching regex") {
            var re = new RegExp(preSufTxt,"g");
           // $.writeln("Regex match: "+ re.test(name) );
            if (re.test(name) ) {
                return false;
            }
        }
    }

    return true;
}

function tcd_duplicateFolderStructure(folder) {
    // Duplicate the supplied folder structure
    
    // Check if the parent folder is root
    var check = tcd_checkPreviousFolders(folder);

    // If the folder hasn't been duplicated yet...
    if (folder == tcd_origParentFolder) {
        return tcd_parentFolder;
    } else if (check == null) {
        var sourceID = folder.id;
        var newFolder = app.project.items.addFolder(tcd_changeName(folder.name));
        var destID = newFolder.id;
        
        var fldr = {};
        fldr.source = folder;
        fldr.dest = newFolder;
        previousFolders.push(fldr);

        if (folder.parentFolder != null) {
            newFolder.parentFolder = tcd_duplicateFolderStructure(folder.parentFolder);
        }

        return newFolder;
    } else {
        return check;
    }
}

function tcd_checkPreviousComps(comp) {
    // Check the list of previous comps for the specified item's ID
    // to make sure it isn't duplicated twice
    for (var i=0; i<previousComps.length; i++) {
        if (previousComps[i].source.id == comp.id) { return previousComps[i].dest; }
    }
    return null;
}

function tcd_checkPreviousFolders(folder) {
    // Check the list of previous folders for the specified item's ID
    // to make sure it isn't duplicated twice
    for (var i=0; i<previousFolders.length; i++) {
        if (previousFolders[i].source.id == folder.id) { return previousFolders[i].dest; }
    }
    return null;
}

function tcd_checkPreviousFootage(footage) {
    // Check the list of previous footage for the specified item's ID
    // to make sure it isn't duplicated twice
    for (var i=0; i<previousFootage.length; i++) {
        if (previousFootage[i].source.id == footage.id) { return previousFootage[i].dest; }
    }
    return null;
}

function tcd_getItemWithID(id) {
    // Returns the proect item with the specified ID
    for (x=1; x<=app.project.numItems; x++) {
        if (app.project.item(x).id == id) { return app.project.item(x); }
    }
    return null;
}

function tcd_changeName(name) {
    // Adjust name based on New Item Naming values
    // $.writeln("tcd_changeName: " + name);
    var origName = name;
    
    // Prefix/Suffix
    if (preSufChk) {
        // Determine whether to use prefix or suffix
        var typ = preSufDrp
        //var typ = TRUECOMPDUP_PALETTE.grp.newNamesGrp.preSufGrp.preSufDrp.selection.text;
        var txt = preSufTxt;
        
        if (typ.toLowerCase() == "prefix") {
            name = txt + name;
            if (parseFloat(app.version) < 9) name = name.substring(0,29); // CS3 has a 31 character limit
        } else if (typ.toLowerCase() == "suffix") {
            // CS3 31 character limit, we'll trim beforehand so the suffix get's applied
            if (parseFloat(app.version) < 9) name = name.substring(0,29-txt.length); // CS3 has a 31 character limit
            name = name + txt;
        }
    }

    // Search/Replace
    if (replChk.value) {
        // $.writeln("name: " + name);
        var srchTxt = replSrchTxt;
        var replTxt = replReplTxt;
        // $.writeln("srchTxt: " + srchTxt);
        // $.writeln("replTxt: " + replTxt);
        
        var srchClean = srchTxt.replace(/[-[\]{}()*+?.\\^$|,#\:\s]/g, "\\$&");  // escape REGEX Special Characters
        // $.writeln("srchClean: " + srchClean);
        var srchTermRegex = new RegExp (srchClean, "gi");
        // $.writeln(srchTermRegex);
        //$.writeln("srchTermRegex: " + srchTermRegex);
        name = name.replace(srchTermRegex, replTxt);
        // $.writeln("result name: " + name);
        if (parseFloat(app.version) < 9) name = name.substring(0,29);  // CS3 has a 31 character limit
    }


    // Increment Last Number
    //$.writeln(incChk.value);
    if (incChk.value) {
        
        if (incDrp == "First" ) {
            // $.writeln("Before first increment: " + name);
            name = name.replace(/(\d+)/ ,
                function(match, c1) {
                    var num = ++c1 + tcd_copyNum;
                    return tcd_pad(num, match.length);
                }
            );
            // $.writeln("After first increment: " + name);

        } else if (incDrp == "Last" ) {
            //$.writeln("Before increment: " + name);
            name = name.replace(/(\d+)(?=\D*$)/g ,
                function(match, c1) {
                    var num = ++c1 + tcd_copyNum;
                    return tcd_pad(num, match.length);
                }
            );
            //$.writeln("After increment: " + name);
        }
    };
    
    // $.writeln("tcd_changeName Result: " + name);
    return name;
}

function tcd_updateExpressions (newComps) {
    // Loop through each duplicated comp and send each layer to tcd_processExpressions()

    var expErrors = [];
    for (var i=0; i < newComps.length; i++) {
        if (tcd_progDlg.cancel) break;

        if (newComps[i] != null) {
            var myComp = newComps[i]; 

            for (var j=1; j <= myComp.numLayers; j++) { 
                if (tcd_progDlg.cancel) break;
                tcd_progDlg.update(1,"Comp: " + myComp.name + " - Layer: " + myComp.layer(j).name)
                var errors = tcd_processExpressions(myComp.layer(j),myComp,tcd_progDlg);
                if (errors.length > 0) {
                    for (var e=0; e<errors.length; e++) {
                        expErrors.push(errors[e]);
                    }
                }
            }
        }
    }
    return expErrors;
}

function tcd_processExpressions (myLayer,myComp) {
    // Process each layer's expressions, also supports property groups for myLayer for recursion

    var errors = [];
    for (var j=1; j<= myLayer.numProperties; j++) { //loop through the parent properties

        if (tcd_progDlg.cancel) break;

        if (myLayer.property(j).numProperties != undefined && myLayer.property(j).numProperties > 0) {
            //Property group with children, let's recurse
            var err = tcd_processExpressions (myLayer.property(j),myComp);
            errors.push.apply(errors, err);
        }

        if (myLayer.property(j).canSetExpression &&  myLayer.property(j).expression != "") {
            // $.writeln ("Expression Found:\n" + myComp.name + ": "+ myLayer.name + ": "+ myLayer.property(j).name);

            var origExpression =  myLayer.property(j).expression;
            // $.writeln("Original Expression:\n" + origExpression);

            if (myLayer.property(j).expressionEnabled && myLayer.property(j).expressionError == "") {
                var changed = false;
                var expression = origExpression;
                
                // --------------------------------------------------------------------------------------
                // First, fix any comp("**") references
                // --------------------------------------------------------------------------------------
                for (var k=0; k < previousComps.length; k++) {
                    if (tcd_progDlg.cancel) break;

                    var oldCompName = previousComps[k].source.name;
                    var origNameRegExp = new RegExp ("comp\\\(\\\""+escapeRegExp(oldCompName)+"\\\"\\\)", "g"); 
                    var newCompName = previousComps[k].dest.name;
                    // $.writeln("ExpUpdate: " + oldCompName + " -> " + newCompName);

                    expression = expression.replace(origNameRegExp,"comp\(\""+newCompName+"\"\)");
                }

                // --------------------------------------------------------------------------------------
                // Second, fix any thisComp.layer("**") or comp("**").layer("**")  references
                // We'll do this line by line so our regex returns the correct results
                // --------------------------------------------------------------------------------------

                var expLines = expression.split(/\r|\n/g);  // Make sure newlines are split
                
                var result = null;
                for (var l=0; l<expLines.length; l++) {
                    // Check for thisComp.layer("**") references
                    var thisCompLyrRegEx = /thisComp.layer\(\"(.+?)\"\)/g;
                    result = thisCompLyrRegEx.exec(expLines[l]);
                    if (result != null) {
                        var sourceLayerName = result[1];
                        var sourceComp = null;
                        for (var c=0; c < previousComps.length; c++) {
                            if (previousComps[c].dest == myComp) {
                                sourceComp = previousComps[c].source;
                            }
                        }
                        if (sourceComp != null) {
                            expLines[l] = fixLyrExpr(expLines[l], sourceLayerName, sourceComp, myComp);
                        }
                    }
                
                    // Check for comp("**").layer("**")  references
                    result = null;
                    var compLyrRegEx = /comp\(\"(.+?)\"\)\.layer\(\"(.+?)\"\)/g;
                    while (result = compLyrRegEx.exec(expLines[l])) {
                        var sourceComp = null;
                        var destComp = null;
                        for (var c=0; c < previousComps.length; c++) {
                            if (previousComps[c].dest.name == result[1]) {
                                destComp = previousComps[c].dest;
                                sourceComp = previousComps[c].source;
                            }
                        }
                        var sourceLayerName = result[2];
                        if (sourceComp != null && destComp != null) {
                            expLines[l] = fixLyrExpr(expLines[l], sourceLayerName, sourceComp, destComp);
                        }
                    }
                }
            
                // TODO: Check for comp("***")
                
                expression = expLines.join("\r");
                
                if (expression === origExpression) {
                    // $.writeln("No expression update needed.");
                } else {
                    try {
                        myLayer.property(j).expression = expression;
                    } catch(err) {
                        errors.push(err.toString().replace("\r\r","\n"));
                    }
                    tcd_expFixCount++;
                }
            }
        }
    }
    return errors;
}

function fixLyrExpr(expression, layerName, sourceComp, destComp) {
    // Update a layer expression based on the source and destination comps
    /*
    Get the layer number of the layer with the specified name in the source comp
    Get the layer name of the layer with the specified number in the new comp
    Replace the layer name in the expression with the new name
      */

    // $.writeln("fixLyrExpr Source: " + expression);

    // Get the layer number of layer with the lyrName in the sourceComp
    var lyrNum = null;
    for (var l=1; l<=sourceComp.numLayers; l++) {
        if (sourceComp.layer(l).name === layerName) {
            lyrNum = sourceComp.layer(l).index;
        }
    }

    var newLyrName = null;
    if (lyrNum != null) {
        // Get the layer name of the layer with the same index in the destComp
        newLyrName = destComp.layer(lyrNum).name;
    }

    // Replace the layer name in the expression
    if (newLyrName != null) {
        // $.writeln("fixLyrExpr Replace: " + "layer\(\""+layerName+"\"\)" + "->" + "layer\(\""+newLyrName+"\"\)");
        expression = expression.replace("layer\(\""+layerName+"\"\)", "layer\(\""+newLyrName+"\"\)");
    }

    // $.writeln("fixLyrExpr Result: " + expression);
    return expression;
}

function tcd_createGroupFolder(sampleItem) {
    // Create the group folder based on the hierarchy level of the sampleItem

    var folderName = grpFldTxt
    // Increment Folder Name's Last Number for copies
    if (tcd_copyNum > 0) {
        if (/\d+(?!.*\d)/.test(folderName) != true) { folderName = folderName + "0"; }
    }
    var num = /\d+(?!.*\d)/.exec(folderName);
    var numPadding = 1;
    if (num != null) {
        var numPadding = num.toString().length;
    }
    folderName = folderName.replace(/\d+(?!.*\d)/, function(n){ return (tcd_pad((++n + tcd_copyNum - 1), numPadding)) });
    tcd_parentFolder = app.project.items.addFolder(folderName);
    
    // Store this in previous folders as the root
    var fldr = {}
    fldr.source = {id:'0',name:'root'};
    fldr.dest = tcd_parentFolder;
    previousFolders.push(fldr);
    
    // If the item is not in the root of the project,
    // then put the new folder on the same heirarchy level
    // as the original item's parent folder
    if (sampleItem.parentFolder.parentFolder) {
        tcd_parentFolder.parentFolder = sampleItem.parentFolder.parentFolder;
    } else {
        tcd_parentFolder.parentFolder = sampleItem.parentFolder;
    }
    
    var folder = {};
    folder.source = sampleItem.parentFolder;
    folder.dest = tcd_parentFolder;
    previousFolders.push(folder);
    // previousFolders[selItems[0].parentFolder.id] = tcd_parentFolder.id;
    tcd_origParentFolder = sampleItem.parentFolder;
    //
    return tcd_parentFolder;
}

function tcd_duplicate(item) {
    // Main duplicate function
    if (item instanceof CompItem) {
        // -- Duplicate Comp Item
        tcd_duplicateCompStructure(item, 0); // 0 is the start depth
    } else {
        // -- Duplicate the project item       
        tcd_duplicateProjItem(item);
    }
    //
    // Return the the new comps
    var result = {};
    result.comps = previousComps.slice(0); // Make a copies
    result.folders = previousFolders.slice(0);
    result.footage = previousFootage.slice(0);
    //
    return result;
}

function tcd_pad(num, size) {
    // $.writeln("pad_num");
    // $.writeln(num);
    // $.writeln("pad_size");
    // $.writeln(size);
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
}
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function doBigOppBool(windo, bool) {
    windo.lineSpaLbl.enabled = !bool;
    windo.lineSpaAmtLbl.enabled = !bool;
    windo.dnBtn.enabled = !bool;
    windo.upBtn.enabled = !bool;
    windo.dnTenBtn.enabled = !bool;
    windo.upTenBtn.enabled = !bool;
    windo.liveLeadCheck.value = false;
    windo.liveLeadCheck.enabled = !bool;
}
//
function buildUI() {
    if (win != null) {
        win.textOpsPnl = win.add('panel', [10,35,244,221], '');
        win.oneFileCheck = win.add('checkbox', [52,8,202,28], 'Import as One Layer');
        win.oneFileCheck.onClick = function () { doBigOppBool(win, this.value); };
        //
        //
        win.liveLeadCheck = win.add('checkbox', [52,8+223,202,28+223], 'Add "Live Leading"');
        
        win.okBtn = win.add('button', [160,267,240,289], 'OK', {name:'OK'});
        win.okBtn.onClick = function () {main(win);this.parent.close(1)};
        win.cancBtn = win.add('button', [66,267,146,289], 'Cancel', {name:'Cancel'});
        win.cancBtn.onClick = function () {this.parent.close(0)};
    }
    return win
}
//
function main(winDough) {
    inManyLayers = !winDough.oneFileCheck.value;
    withLiveLeading = winDough.liveLeadCheck.value;
    
    // create undo group
    app.beginUndoGroup("Text from File (v3.2)");
    
    // Prompt user to select text file
    
    var myFile = File.openDialog("Select a text file to open.", "");//, "TEXT txt");
    
    if (myFile != null){
        // create project if necessary
        
        var proj = app.project;
        if (!proj) proj = app.newProject();
        var activeItem = proj.activeItem;
        var compBG = [.8,.8,.8] // comp background color
        
        // create new comp named 'text_comp'
        // or use the selected comp
        if (activeItem != null && (activeItem instanceof CompItem)){
            var myComp = activeItem;
            
        } else {
            //8.5x11 inches @ 72dpi
            var compW = 1920; // comp width
            var compH = 1080; // comp height
            
            var compL = 15;  // comp length (seconds)
            var compRate = 29.97; // comp frame rate
            
            var myItemCollection = app.project.items;
            var myComp = myItemCollection.addComp('text_comp',compW,compH,1,compL,compRate);
        }
        myComp.bgColor = compBG;
        lineSpa = 12;
        
        if (inManyLayers) {
            lineSpa = 200
            //lineSpa = parseFloat(winDough.lineSpaAmtLbl.text);
        }
        topSpa = 100;           
        //topSpa = parseFloat(winDough.topSpaAmtLbl.text);
        leftSpa = 200
        //leftSpa = parseFloat(winDough.leftSpaAmtLbl.text);
        
        // open file
        var fileOK = myFile.open("r","TEXT","????");
        if (fileOK){
            
            var allText = "";
            var o = 1;
            var addForLead = 0;
            
            // read text lines
            // until end-of-file is reached
            var textCollection = new Array();
            
            while (!myFile.eof){
                write("Reading and writing line #" + o + " ... ");
                text = myFile.readln();
                // script will likely throw amusing error*
                // if line is empty
                // * "having to focus on ourselves"
                if (text == "") { text = "\r" ;}
                
                if (inManyLayers) {
                    // if user chose 'many layers' option, make new text layer each iteration
                    thisText = myComp.layers.addText(text);
                    thisText.property("Position").setValue([(leftSpa), ( (lineSpa * o) + topSpa)]);
                    if (o != 1) {thisText.moveAfter(myComp.layer(o));}
                    
                    // I figure, why use the memory if we don't need to:
                    if (inManyLayers) { textCollection[(o-1)] = thisText; }
                    
                } else {
                    // if user chose 'one layer' option, keep appending text variable:
                    allText = (allText + text + "\r");
                }
                o = (o + 1);
                /////////////////////////////////////////////clearOutput();
            }
             /////////////////////////////////////////////clearOutput();
            
            if (! inManyLayers) {
                // if user chose 'one layer' option, now make one text layer:
                bigTextLayer = myComp.layers.addText(allText);
                bigTextLayer.property("Position").setValue([leftSpa, topSpa]);
            }
            // close the file before exiting
            myFile.close();
            
            if (withLiveLeading) {
                //add null
                leadingNull = myComp.layers.addNull();
                leadingNull.name = "Text Parent & Leading (Adjust Slider)";
                fxGrp = leadingNull("Effects");
                nullYEffect=fxGrp.addProperty("ADBE Slider Control");
                
                nullYEffect.name="Leading Adjustment";
                
                //give text expression for adjustable line spacing
                for (t = 0; t < (textCollection.length);t++) {
                    textCollection[t].property("position").expression = 
                    "v=value;"+
                    "\r[value[0], "+
                    "(value[1]+thisComp.layer('Text Parent & Leading (Adjust Slider)').effect('Leading Adjustment')('Slider')*(index-2) )];";
                    textCollection[t].parent=leadingNull;
                }
                leadingNull.selected=true;
                leadingNull("Effects")("ADBE Slider Control")("Slider").expression="value;";
                alert("Adjust the leading (line spacing) by adjusting the top layer's \"Leading Adjustment\" slider control.\r (Don't forget, kids: \"Leading\" rhymes with \"heading\"!)");
            } else {
                pNull = myComp.layers.addNull();
                pNull.name = "Text Parent";
                for (t = 0; t < (textCollection.length);t++) {
                    textCollection[t].parent=pNull;
                }
                pNull.selected=true;
            }//if with live leading
            
        } else {
            alert("File open failed!");
        }
    }else{
        alert("No text file selected.");
    }
    
    app.endUndoGroup();
}

function changeSpaNumber(theField, amt) {
    i = parseFloat(theField.text);
    i = (i + parseFloat(amt));
    theField.text = i;
}
// -- Main
var TRUECOMPDUP_PALETTE = tcd_buildUI(this);
if (parseFloat(app.version) < 8) {
    alert("This script requires Adobe After Effects CS3 or later.", "testing script");
} else {
    if (TRUECOMPDUP_PALETTE != null && TRUECOMPDUP_PALETTE instanceof Window) { TRUECOMPDUP_PALETTE.show(); }
}
