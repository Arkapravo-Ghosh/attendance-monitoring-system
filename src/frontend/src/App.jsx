import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import reactLogo from "./assets/react.svg";

import Footer from "./components/Footer/Footer";
import Navbar from "./components/Navbar/Navbar";
import LandingPage from "./pages/Landing/Landing";

import { SheProvider } from "./context/sheContext";

import "./styles/App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <SheProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route exact path="/" element={<LandingPage />} />
          </Routes>
          <Footer />
        </Router>
      </SheProvider>
    </>
  );
}

export default App
