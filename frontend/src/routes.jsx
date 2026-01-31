import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Pages/Home";

import Navbar from "./Components/Common/Navbar";
import Result from "./Pages/Result";
import Footer from "./Components/Common/Footer";
import ChatFab from "./Components/Common/ChatFab";
import Chat from "./Pages/Chat";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/result" element={<Result/>} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
      <ChatFab/>
      <Footer/>
    </BrowserRouter>
  );
}
