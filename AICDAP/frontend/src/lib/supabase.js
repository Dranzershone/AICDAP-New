import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://astybhpwqlexxadjrpct.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzdHliaHB3cWxleHhhZGpycGN0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjg1NDMsImV4cCI6MjA3NTY0NDU0M30.IXyX2nAd_XXawl5Fr3m7DZXUNMhNqtMgwIzI8_uTTXg'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
