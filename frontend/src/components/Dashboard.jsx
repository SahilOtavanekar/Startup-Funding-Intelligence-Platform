import { NavLink } from 'react-router-dom';
import './Dashboard.css';

/**
 * Dashboard layout — sidebar navigation + main content area.
 * Wraps all page routes.
 */
function Dashboard({ children }) {
    return (
        <div className="dashboard">
            {/* --- Sidebar ---------------------------------------------------- */}
            <aside className="sidebar">
                <div className="sidebar-brand">
                    <span className="brand-icon">🚀</span>
                    <h2 className="brand-title">FundingIQ</h2>
                </div>

                <nav className="sidebar-nav">
                    <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">🏠</span>
                        Home
                    </NavLink>
                    <NavLink to="/insights" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">📊</span>
                        Insights
                    </NavLink>
                    <NavLink to="/predict" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">🔮</span>
                        Predict
                    </NavLink>
                    <NavLink to="/startups" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">🏢</span>
                        Startups
                    </NavLink>
                </nav>

                <div className="sidebar-footer">
                    <div className="sidebar-divider"></div>
                    <p className="text-muted" style={{ fontSize: '0.7rem', textAlign: 'center', lineHeight: 1.5 }}>
                        v1.0.0<br />AI-Powered Analytics
                    </p>
                </div>
            </aside>

            {/* --- Main Content ----------------------------------------------- */}
            <main className="main-content">
                {children}
            </main>
        </div>
    );
}

export default Dashboard;
