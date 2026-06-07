// Background Service Worker
let selectedText = ''
let currentTabUrl: string = ''

chrome.tabs.query({active: true, lastFocusedWindow: true}, (tabs) => {
  if (tabs[0]?.url) {
    currentTabUrl = tabs[0].url
  }
})

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

  if (message.type === 'SET_TAB_URL') {
    currentTabUrl = message.url
    sendResponse({ status: 'ok' })
    return true
  }

  if (message.type === 'GET_TAB_INFO') {
    chrome.tabs.query({active: true, lastFocusedWindow: true}, (tabs) => {
      const url = tabs[0]?.url || ''
      const isYouTube = url.includes('youtube.com/watch')
      console.log('Tab URL:', url, 'isYouTube:', isYouTube)
      sendResponse({ url, isYouTube })
    })
    return true
  }

  return true
})

chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab.url) {
      currentTabUrl = tab.url
    }
  })
})

chrome.tabs.onUpdated.addListener((_tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.active && tab.url) {
    currentTabUrl = tab.url
  }
})