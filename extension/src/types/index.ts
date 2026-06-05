export type Page = 'explain' | 'summary' | 'quiz' | 'notes' | 'dashboard'

export interface SelectedText {
  text: string
  url: string
  title: string
}

export interface ApiResponse {
  result: string
  error?: string
}