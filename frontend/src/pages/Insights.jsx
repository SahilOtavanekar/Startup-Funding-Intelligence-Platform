import Charts from '../components/Charts.jsx';

/**
 * Insights Page — funding trends, top industries, geographic distribution.
 */
function Insights() {
    return (
        <div className="insights-page animate-in">
            <h1 className="mb-lg">
                Industry <span className="text-accent">Insights</span>
            </h1>
            <p className="text-muted mb-xl" style={{ maxWidth: 600 }}>
                Explore funding trends, discover top-funded industries, and understand the startup ecosystem.
            </p>

            <Charts />
        </div>
    );
}

export default Insights;
