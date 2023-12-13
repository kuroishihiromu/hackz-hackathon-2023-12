import React from "react";
import { createBrowserRouter } from "react-router-dom";
import {Top} from "./components/Top"
import {Home} from "./components/Home"

export const router = createBrowserRouter([
    {path: "/", element: <Top />},
    {path: "home", element: <Home />},
])
