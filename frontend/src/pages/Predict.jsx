import PredictionForm from '../components/PredictionForm.jsx';

/**
 * Predict Page — dedicated prediction tool page.
 */
function Predict() {
    return (
        <div className="predict-page animate-in" style={{ maxWidth: 800 }}>
            <h1 className="mb-md">
                Funding <span className="text-accent">Predictor</span>
            </h1>
            <p className="text-muted mb-xl" style={{ maxWidth: 550 }}>
                Enter your startup details below and our trained XGBoost model will
                estimate the probability of securing funding.
            </p>

            <PredictionForm />

            <div className="glass-card" style={{ marginTop: 'var(--space-xl)', padding: 'var(--space-lg)' }}>
                <h4 className="mb-md">ℹ️ How it works</h4>
                <ul className="text-muted" style={{ paddingLeft: '1.2rem', lineHeight: '2', fontSize: '0.9rem' }}>
                    <li>The model was trained on <strong>500+ startup records</strong> with real-world-like distributions.</li>
                    <li>Features include industry, team size, startup age, investor count, and more.</li>
                    <li>An <strong>XGBoost classifier</strong> evaluates patterns correlating with funding success.</li>
                    <li>Feature importance reveals which factors drive each prediction.</li>
                </ul>
            </div>
        </div>
    );
}

export default Predict;
