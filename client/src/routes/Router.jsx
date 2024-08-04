import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Main } from "../pages/Main";
import { Login } from "../pages/Login";
import { Signup } from "../pages/Signup";
import { NotFound } from "../pages/NotFound";

export const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
};
