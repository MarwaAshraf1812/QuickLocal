import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import LandingPage from './pages/LandingPage';
import CategoriesPage from './pages/CategoriesPage';
import ProductsPage from './pages/ProductsPage';
import Footer from './components/Footer';

function App() {
  return (
    <div>
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/category-products" element={<ProductsPage />} />
          <Route path="/shop" element={<h1>shop</h1>} />
          <Route path="/products" element={<h1>products</h1>} />
          <Route path="/contactUs" element={<h1>contact</h1>} />
        </Routes>
        <Footer />
      </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
