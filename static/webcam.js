const constraints = { "video": true, "audio" : false };

var theStream;
var theRecorder;
var recordedChunks = [];

function startFunction() {
  navigator.mediaDevices.getUserMedia(constraints)
      .then(gotMedia)
      .catch(e => { console.error('getUserMedia() failed: ' + e); });
}

function gotMedia(stream) {
  theStream = stream;
  var video = document.querySelector('video');
  video.srcObject = stream;
  try {
  var options = {
    videoBitsPerSecond : 5000000,
    mimeType : 'video/webm'
    }
    var recorder = new MediaRecorder(stream, options);
  } catch (e) {
    console.error('Exception while creating MediaRecorder: ' + e);
    return;
  }

theRecorder = recorder;
recorder.ondataavailable =
    (event) => { recordedChunks.push(event.data); };
recorder.start(100);
setTimeout(download, 5000);
}

function download() {
  var username = document.getElementById("username").value;
  var attribute = document.getElementById("username").getAttribute("secret");
  theRecorder.stop();
  theStream.getTracks().forEach(track => { track.stop(); });
  var blob = new Blob(recordedChunks, {type: "video/mp4"});
  var formdata = new FormData();
  formdata.append('video', blob, username+".webm");
  formdata.append('username', username);
  formdata.append('attribute', attribute);
  $.ajax({
    url: 'http://127.0.0.1:5000/upload',
    method: 'post',
    processData: false,
    contentType: false,
    data: formdata,
    success: function(data) {console.log(data)},
    error: function(error) {console.log(error)}
    });
}