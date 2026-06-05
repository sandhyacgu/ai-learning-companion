export const speakText = (text: string, lang = 'en-US') => {
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;
  utterance.rate = 0.9;
  window.speechSynthesis.speak(utterance);
};

export const stopSpeech = () => window.speechSynthesis.cancel();

export const isSpeaking = () => window.speechSynthesis.speaking;