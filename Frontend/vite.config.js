import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig(function (_a) {
    var _b;
    var mode = _a.mode;
    var env = loadEnv(mode, process.cwd(), "");
    var backendUrl = (_b = env.VITE_BACKEND_URL) !== null && _b !== void 0 ? _b : "http://127.0.0.1:8000";
    return {
        plugins: [react()],
        server: {
            host: "0.0.0.0",
            port: 5173,
            proxy: {
                "/api": {
                    target: backendUrl,
                    changeOrigin: true,
                    rewrite: function (path) { return path.replace(/^\/api/, ""); },
                },
            },
        },
    };
});
