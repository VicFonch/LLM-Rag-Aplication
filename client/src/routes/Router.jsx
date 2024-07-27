import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ChatBot } from "../pages/ChatBot";
import { Login } from "../pages/Login";

export const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ChatBot />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
};
