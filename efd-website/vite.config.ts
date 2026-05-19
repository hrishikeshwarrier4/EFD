import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: process.env.NODE_ENV === "development" ? process.env.DEV_SERVER_BASE_PATH : undefined,
  server: {
    port: Number(process.env.DEV_SERVER_PORT ?? 8080),
    host: process.env.DEV_SERVER_HOST,
    allowedHosts: process.env.DEV_SERVER_DOMAIN != null ? [process.env.DEV_SERVER_DOMAIN] : undefined,
  },
});
