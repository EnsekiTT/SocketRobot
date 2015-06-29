var ws = new WebSocket('ws://localhost:8884/audio');
var ctx = new AudioContext
var scheduledTime = 0;
var initialDelay = 0;
ws.binaryType = 'arraybuffer';

ws.onopen = function(){
  console.log("connection was established");
};

ws.onmessage = function(evt){
  if (evt.data.constructor !== ArrayBuffer) throw 'expecting ArrayBuffer';
  playAudioStream(new Float32Array(evt.data));
};

window.onbeforeunload = function(){
  ws.close(1000);
};

var playAudioStream = function(float32audio) {
  var audioBuffer = ctx.createBuffer(1, float32audio.length, 44100),
    audioSource = ctx.createBufferSource(), currentTime = ctx.currentTime;

  audioBuffer.getChannelData(0).set(float32audio);

  audioSource.buffer = audioBuffer;
  audioSource.connect(ctx.destination);
  if (currentTime < scheduledTime) {
    audioSource.start(scheduledTime);
    scheduledTime += audioBuffer.duration;
  } else {
    audioSource.start(currentTime);
    scheduledTime += currentTime + audioBuffer.duration + initialDelay;
  }
}

var init = function() {
    try{
        audioContext = new AudioContext();
    } catch(e) {
        console.log(e);
    }
    audioContext.samplingRate = 48000;
}

init();
