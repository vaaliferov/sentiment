function ajax_get(url, callback) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            console.log('responseText:' + xmlhttp.responseText);
            try {
                var data = JSON.parse(xmlhttp.responseText);
            } catch(err) {
                console.log(err.message + ' in ' + xmlhttp.responseText);
                return;
            }
            callback(data);
        }
    };
    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function ge(id) { 
    return document.getElementById(id);
}

function check_sentiment() {
    url = '/sentiment?text=' + ge('text').value;
    ajax_get(url, function(d){ge('sentiment').innerText = d.label;});
}
