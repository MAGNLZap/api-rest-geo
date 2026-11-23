/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string
}

declare module '@portal/*.svg' {
  const url: string
  export default url
}

declare module '@amenazas/*.png' {
  const url: string
  export default url
}
