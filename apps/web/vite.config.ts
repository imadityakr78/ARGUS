import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@argus/contracts': '../../packages/contracts/typescript/index.ts',
    },
  },
})
