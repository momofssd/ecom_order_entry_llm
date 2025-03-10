import "bootstrap-icons/font/bootstrap-icons.css";
import { Container } from "react-bootstrap";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Header from "./components/Header";
import LoginPage from "./pages/LoginPage";
import MainExternal from "./pages/MainExternal";
import MainInternal from "./pages/MainInternal";
import OrderEntryAdmin from "./pages/adminview/OrderEntryAdmin";
import OrderRecords from "./pages/adminview/OrderRecords";
import POuploadAdmin from "./pages/adminview/POuploadAdmin";
import POupload from "./pages/userview/POupload";
const App = () => {
  return (
    <Router>
      <Header />
      <main className="py-3">
        <Container>
          <Routes>
            <Route path="/" element={<LoginPage />} /> {/* Redirect root to Login */}
            <Route path="/MainInternal" element={<MainInternal />} />
            <Route path="/MainExternal" element={<MainExternal />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/admin-Order-Tracking" element={<OrderRecords />} />
            <Route path="/admin-Order-Entry" element={<OrderEntryAdmin />} />
            <Route path="/admin-Purchase-Order-Upload" element={<POuploadAdmin />} />
            <Route path="/user-Purchase-Order-Upload" element={<POupload />} />
          </Routes>
        </Container>
      </main>
    </Router>
  );
};

export default App;
