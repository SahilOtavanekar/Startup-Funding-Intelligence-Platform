import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import Home from './pages/Home.jsx';
import Insights from './pages/Insights.jsx';

function App() {
    return (
        <BrowserRouter>
            <Dashboard>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/insights" element={<Insights />} />
                </Routes>
            </Dashboard>
        </BrowserRouter>
    );
}

export default App;
