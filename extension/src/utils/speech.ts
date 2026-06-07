const cleanText = (text: string): string => {
  return text
    .replace(/\*\*(.*?)\*\*/g, '$1')
    .replace(/\*(.*?)\*/g, '$1')
    .replace(/#{1,6}\s/g, '')
    .replace(/`{1,3}(.*?)`{1,3}/g, '$1')
    .replace(/^\s*[-*•]\s/gm, '')
    .replace(/^\s*\d+\.\s/gm, '')
    .replace(/\n+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

export const speakText = (text: string, lang = 'en-US') => {
  window.speechSynthesis.cancel()
  const cleaned = cleanText(text)
  const utterance = new SpeechSynthesisUtterance(cleaned)
  utterance.lang = lang
  utterance.rate = 0.9
  window.speechSynthesis.speak(utterance)
}

export const stopSpeech = () => window.speechSynthesis.cancel()

export const isSpeaking = () => window.speechSynthesis.speaking