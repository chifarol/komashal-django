import "./index.css";
import { createRoot } from "react-dom/client";
import React from "react";
import App from "./components/App";

const container = document.querySelector("#app");

const root = createRoot(container);

root.render(<App />);
