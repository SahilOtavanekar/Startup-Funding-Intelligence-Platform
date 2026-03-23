import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard.jsx';
import Home from './pages/Home.jsx';
import Insights from './pages/Insights.jsx';
import Trending from './pages/Trending.jsx';
import Startups from './pages/Startups.jsx';

function App() {
    return (
        <BrowserRouter>
            <Dashboard>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/insights" element={<Insights />} />
                    <Route path="/trending" element={<Trending />} />
                    <Route path="/startups" element={<Startups />} />
                </Routes>
            </Dashboard>
        </BrowserRouter>
    );
}

export default App;
