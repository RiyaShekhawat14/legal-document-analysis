import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./Components/Common/Navbar";
import Footer from "./Components/Common/Footer";
import ChatFab from "./Components/Common/ChatFab";
import Home from "./Pages/Home";
import Result from "./Pages/Result";
import Chat from "./Pages/Chat";
import Compare from "./Pages/Compare";
import History from "./Pages/History";
import Auth from "./Pages/Auth";
import ProtectedRoute from "./Components/Common/ProtectedRoute";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/result" element={<Result />} />
            <Route
              path="/chat"
              element={
                <ProtectedRoute>
                  <Chat />
                </ProtectedRoute>
              }
            />
            <Route
              path="/compare"
              element={
                <ProtectedRoute>
                  <Compare />
                </ProtectedRoute>
              }
            />
            <Route
              path="/history"
              element={
                <ProtectedRoute>
                  <History />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
        <ChatFab />
        <Footer />
      </div>
    </BrowserRouter>
  );
}
