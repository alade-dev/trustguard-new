/* eslint-disable no-undef */
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      crypto: "empty-module",
      "@": path.resolve(__dirname, "./src"),
    },
  },
  define: {
    global: "globalThis",
  },
  build: {
    target: "esnext",
  },
  server: {
    allowedHosts: ["5173-gitpoddemos-votingapp-nqc5j80vipp.ws-eu117.gitpod.io"],
  },
});
