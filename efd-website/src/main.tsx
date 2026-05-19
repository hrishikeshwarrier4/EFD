import { Suspense } from "react";
import ReactDOM from "react-dom/client";
import { Toaster } from "react-hot-toast";
import { OsdkProvider } from "@osdk/react";
import client from "@/client";
import AppShell from "@/components/layout/AppShell";
import { AppProvider } from "@/context/AppContext";
import "leaflet/dist/leaflet.css";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Root element not found");

ReactDOM.createRoot(rootElement).render(
  <OsdkProvider client={client}>
    <Suspense fallback={<div className="flex items-center justify-center h-screen bg-[#0F1117]"><p className="text-sm text-gray-400">Initializing FraudGuard...</p></div>}>
      <AppProvider>
        <AppShell />
        <Toaster position="bottom-right" />
      </AppProvider>
    </Suspense>
  </OsdkProvider>
);
