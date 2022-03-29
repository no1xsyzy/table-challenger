import { browser } from '$app/env'

export function localStore<T>(
  key: string,
  defaultValue: T,
  serializer: { stringify: (t: T) => string; parse: (s: string) => T } = JSON,
) {
  let strVal: string
  if (browser) strVal = localStorage.getItem(key)
  if (strVal == null) {
    strVal = serializer.stringify(defaultValue)
    if (browser) localStorage.setItem(key, strVal)
  }

  const subscribers: Record<string, (value: T) => void> = {}

  const emit = (value: string) => {
    for (const subscriber of Object.values(subscribers)) {
      subscriber(serializer.parse(value))
    }
  }

  if (browser)
    window.addEventListener('storage', (e) => {
      if (e.storageArea === localStorage && e.key === key) {
        emit(e.newValue)
      }
    })

  const next_subscriber_key = () => {
    for (let i = 0; ; i++) {
      if (!(`${i}` in subscribers)) {
        return `${i}`
      }
    }
  }

  return {
    subscribe(f: (value: T) => void): () => void {
      const sk = next_subscriber_key()
      subscribers[sk] = f
      f(serializer.parse(strVal))
      return () => {
        delete subscribers[sk]
      }
    },
    set(value: T): void {
      if (browser) localStorage.setItem(key, serializer.stringify(value))
      else emit(serializer.stringify(value))
    },
  }
}
