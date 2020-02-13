function speak(playbackString) {
  console.log(speechSynthesis.getVoices());
  var msg = new SpeechSynthesisUtterance();
  var voices = window.speechSynthesis.getVoices();
  console.log(voices);
  msg.voice = voices[0]; // Note: some voices don't support altering params
  msg.voiceURI = 'native';
  msg.volume = 1; // 0 to 1
  msg.rate = 1; // 0.1 to 10
  msg.pitch = 1; //0 to 2
  msg.text = playbackString;
  msg.lang = 'en-US';
  speechSynthesis.speak(msg);
}
