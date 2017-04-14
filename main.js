var fileExt = {};
    fileExt[0]=".xml";
filelist = [];
var files=[];

function getfiles() {
   $.ajax({
    //This will retrieve the contents of the folder if the folder is configured as 'browsable'
    url: 'data/',
    success: function (data) {
       // $("#fileNames").html('<ul>');
       //List all png or jpg or gif file names in the page
       $(data).find("a:contains(" + fileExt[0] + ")").each(function () {
           var filename = this.href.replace(window.location.host, "").replace("http:///", "");
           // $("#fileNames").append( "<li>" + filename + "</li>");
           filename = filename.split('/')[1];
           files.push(filename);
       });
       console.log(files);
       var select = document.getElementById("select"); 
       var i;
       for(i = 0; i < files.length; i++) {
          var opt = files[i];
          var el = document.createElement("option");
          el.textContent = opt;
          el.value = opt;
          select.appendChild(el);
        }

       // $("#fileNames").append('</ul>');
     }     
  });
}

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        myFunction(this);
    }
};

function UserAction(text, callback) {
     var xhttp = new XMLHttpRequest();
     xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("demo").innerHTML = this.responseText;

        callback(Object(this.responseText));
    }
  };
  xhttp.open("POST", "http://10.17.250.250/services/extractMetadataFromText", true);
  // xhttp.setRequestHeader("Content-type", "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW");
  console.log(typeof(text.join()));
  console.log("------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n" + text.join() + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--");
  xhttp.send("'------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n" + text.join() + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'");

  }


function myFunction(xml) {
    var reg = "\\s[0-9][.][0-9]\\s";
    var re = new RegExp(reg, "g");
    var xmlDoc = xml.responseXML;
    // console.log(xmlDoc.getElementsByTagName("body")[0].textContent);
    document.getElementById("heading").innerHTML = xmlDoc.getElementsByTagName("title")[0].childNodes[0].nodeValue;
    var textContent = xmlDoc.getElementsByTagName("body")[0].textContent;
    var splittext = textContent.replace("\n\n", "").split(re);
    var headings = textContent.match(re);
    var finalText = {"0": splittext[0]};
    for(var i = 0; i<headings.length; i++) {
      finalText["<p>" + headings[i]] = splittext[i+1] + "</p>"; 
    }
    UserAction(Object.values(finalText), function(meta) {
      console.log(Object.values(meta));
      var keywords = meta.response.metadata.dc.subject;
      for(var i=0;i<keywords.length;i++) {
      textContent = textContent.replace(keywords[i],"<keyword>" + keywords[i] +"</keyword>")
    }
    });
    console.log(finalText);
    document.getElementById("outputbox").innerHTML = JSON.stringify(finalText, undefined, 2);

}

getfiles();

function submit() {
  var selected = document.getElementById("select").value;
  // $("#outputbox").load("data/" + selected);
  xhttp.open("GET", "data/" + selected, true);
  xhttp.send();
};