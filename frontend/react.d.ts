/// <reference types="react" />
/// <reference types="react-dom" />

declare module 'react' {
  export function useState<T>(initialState: T | (() => T)): [T, (newState: T | ((prevState: T) => T)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void;
  
  namespace JSX {
    interface IntrinsicElements {
      [elemName: string]: any
    }
  }
}
