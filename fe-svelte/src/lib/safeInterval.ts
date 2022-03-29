type CancelFunc = () => void

export function safeInterval(func: () => void, interval: number): CancelFunc {
  let t: NodeJS.Timeout
  let cancelled = false
  const wrapped = () => {
    if (cancelled) return
    func()
    t = setTimeout(wrapped, interval)
  }
  setTimeout(wrapped, interval)
  return () => {
    cancelled = true
    clearTimeout(t)
  }
}
