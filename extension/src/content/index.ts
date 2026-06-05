// Content Script
// Pehle background worker ko wake up karo, phir message bhejo

const sendSelectedText = (text: string) => {
  chrome.runtime.sendMessage(
    { type: 'TEXT_SELECTED', text },
    () => {
      if (chrome.runtime.lastError) {
        // Worker so gaya tha, retry karo
        setTimeout(() => {
          chrome.runtime.sendMessage({ type: 'TEXT_SELECTED', text })
        }, 500)
      }
    }
  )
}

document.addEventListener('mouseup', () => {
  const selection = window.getSelection()
  const text = selection?.toString().trim()

  if (text && text.length > 0) {
    sendSelectedText(text)
  }
})