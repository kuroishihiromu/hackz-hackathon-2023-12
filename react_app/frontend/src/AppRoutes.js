//AppRouter.js
import React from "react";
import { createBrowserRouter } from "react-router-dom";
import Top from "./components/Top";
import Home from "./Home";

const AppRouter = createBrowserRouter([
    {path: "/", element: <Top />},
    {path: "/home", element: <Home />},
])

export default AppRouter
