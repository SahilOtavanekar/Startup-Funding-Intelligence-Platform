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
                    <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">🏠</span>
                        Home
                    </NavLink>
                    <NavLink to="/insights" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
                        <span className="nav-icon">📊</span>
                        Insights
                    </NavLink>
                </nav>

                <div className="sidebar-footer">
                    <p className="text-muted" style={{ fontSize: '0.75rem' }}>
                        v1.0.0 — AI-Powered Analytics
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
