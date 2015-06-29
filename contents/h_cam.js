var img = document.getElementById("liveImg");
var debug = document.getElementById('debug');
var arrayBuffer;

var ws = new WebSocket('ws://localhost:8884/camera');
ws.binaryType = 'arraybuffer';

ws.onopen = function(){
  console.log("connection was established");
};

ws.onmessage = function(evt){
  var ctx = img.getContext('2d');
  var imageData = ctx.createImageData(480, 360);
  var pixels = imageData.data;

  var buffer = new Uint8Array(evt.data);
  for (var i=0; i < pixels.length; i++) {
    pixels[i] = buffer[i];
  }
  ctx.putImageData(imageData, 0, 0);
  console.log(buffer);
};

window.onbeforeunload = function(){
  ws.close(1000);
};

function encode(input){
  var i = 0;
  var output = '';
  while(i < input.length){
    chr1 = input[i++];
    output += chr1
  }
  return output;
}
