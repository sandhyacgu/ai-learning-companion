// Background Service Worker
let selectedText = ''

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  
  if (message.type === 'TEXT_SELECTED') {
    selectedText = message.text
    sendResponse({ status: 'ok' })
    return true
  }

  if (message.type === 'GET_SELECTED_TEXT') {
    sendResponse({ text: selectedText })
    return true
  }

  return true
})