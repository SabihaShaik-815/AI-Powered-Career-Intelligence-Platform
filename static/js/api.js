/*
 * CareerCast - Milestone 3 API Integration
 * Connects the dashboard frontend with the FastAPI backend.
 */

const API_BASE_URL = "http://127.0.0.1:8000";

/* =========================================================
   GENERIC API REQUEST
   ========================================================= */

async function apiRequest(endpoint, method = "GET", data = null) {
    try {
        const options = {
            method: method,
            headers: {
                "Accept": "application/json"
            }
        };

        if (data !== null) {
            options.headers["Content-Type"] = "application/json";
            options.body = JSON.stringify(data);
        }

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

        let result;

        try {
            result = await response.json();
        } catch (error) {
            throw new Error("Server returned an invalid JSON response.");
        }

        if (!response.ok) {
            const message =
                result.detail ||
                result.message ||
                `API request failed with status ${response.status}`;

            throw new Error(message);
        }

        return result;

    } catch (error) {
        console.error(`API Error [${endpoint}]:`, error);
        throw error;
    }
}


/* =========================================================
   HEALTH CHECK
   ========================================================= */

async function checkAPIHealth() {
    try {
        const result = await apiRequest("/health");

        console.log("CareerCast API Health:", result);

        return result;

    } catch (error) {
        console.error("API health check failed:", error);

        return {
            status: "unavailable",
            error: error.message
        };
    }
}


/* =========================================================
   CAREER PREDICTION
   POST /predict
   ========================================================= */

async function predictCareer(text, topK = 5) {

    if (!text || text.trim().length === 0) {
        throw new Error("Resume text cannot be empty.");
    }

    const data = {
        text: text.trim(),
        top_k: topK
    };

    return await apiRequest("/predict", "POST", data);
}


/* =========================================================
   CAREER RECOMMENDATIONS
   POST /recommend
   ========================================================= */

async function getCareerRecommendations(text, topK = 5) {

    if (!text || text.trim().length === 0) {
        throw new Error("Resume text cannot be empty.");
    }

    const data = {
        text: text.trim(),
        top_k: topK
    };

    return await apiRequest("/recommend", "POST", data);
}


/* =========================================================
   SKILL GAP ANALYSIS
   POST /skill-gap
   ========================================================= */

async function getSkillGap(role, skills = []) {

    if (!role || role.trim().length === 0) {
        throw new Error("Career role is required.");
    }

    const data = {
        role: role.trim(),
        skills: Array.isArray(skills) ? skills : []
    };

    return await apiRequest("/skill-gap", "POST", data);
}


/* =========================================================
   COMPLETE CAREER REPORT
   POST /report
   ========================================================= */

async function generateCareerReport(text, topK = 5) {

    if (!text || text.trim().length === 0) {
        throw new Error("Resume text cannot be empty.");
    }

    const data = {
        text: text.trim(),
        top_k: topK
    };

    return await apiRequest("/report", "POST", data);
}


/* =========================================================
   MODEL METRICS
   GET /metrics
   ========================================================= */

async function getModelMetrics() {
    return await apiRequest("/metrics");
}


/* =========================================================
   COMPLETE CAREER ANALYSIS
   ========================================================= */

async function analyzeCareer(text, topK = 5) {

    if (!text || text.trim().length === 0) {
        throw new Error("Please provide resume text.");
    }

    try {

        /*
         * Run prediction and recommendations together.
         * This reduces waiting time.
         */

        const [prediction, recommendations] = await Promise.all([
            predictCareer(text, topK),
            getCareerRecommendations(text, topK)
        ]);

        /*
         * Get skill gap for the predicted top role.
         */

        let skillGap = null;

        if (prediction && prediction.top_role) {

            skillGap = await getSkillGap(
                prediction.top_role,
                prediction.skills || []
            );
        }

        return {
            success: true,
            prediction: prediction,
            recommendations: recommendations,
            skillGap: skillGap
        };

    } catch (error) {

        console.error("Career analysis failed:", error);

        return {
            success: false,
            error: error.message
        };
    }
}


/* =========================================================
   UI HELPER FUNCTIONS
   ========================================================= */

function showLoading(elementId, message = "Analyzing...") {

    const element = document.getElementById(elementId);

    if (!element) {
        return;
    }

    element.innerHTML = `
        <div class="api-loading">
            <div class="loading-spinner"></div>
            <span>${escapeHTML(message)}</span>
        </div>
    `;
}


/* =========================================================
   ERROR DISPLAY
   ========================================================= */

function showAPIError(elementId, message) {

    const element = document.getElementById(elementId);

    if (!element) {
        console.error(message);
        return;
    }

    element.innerHTML = `
        <div class="api-error">
            <strong>Analysis Error</strong>
            <p>${escapeHTML(message)}</p>
        </div>
    `;
}


/* =========================================================
   DISPLAY PREDICTION
   ========================================================= */

function displayPrediction(result, elementId = "predictionResults") {

    const container = document.getElementById(elementId);

    if (!container || !result) {
        return;
    }

    const predictions = result.predictions || [];

    let html = "";

    if (result.top_role) {

        const topPrediction = predictions.length > 0
            ? predictions[0]
            : null;

        const confidence = topPrediction
            ? topPrediction.confidence_percentage
            : 0;

        html += `
            <div class="prediction-main-card">

                <div class="prediction-label">
                    Predicted Career
                </div>

                <div class="prediction-role">
                    ${escapeHTML(result.top_role)}
                </div>

                <div class="prediction-confidence">
                    Confidence:
                    <strong>${Number(confidence).toFixed(2)}%</strong>
                </div>

            </div>
        `;
    }


    if (predictions.length > 0) {

        html += `
            <div class="prediction-list">
                <h3>Top Career Predictions</h3>
        `;

        predictions.forEach((prediction, index) => {

            const confidence =
                Number(prediction.confidence_percentage || 0);

            html += `
                <div class="prediction-item">

                    <div class="prediction-rank">
                        ${index + 1}
                    </div>

                    <div class="prediction-info">

                        <div class="prediction-role-name">
                            ${escapeHTML(prediction.role)}
                        </div>

                        <div class="prediction-progress">
                            <div
                                class="prediction-progress-bar"
                                style="width:${Math.min(confidence, 100)}%"
                            ></div>
                        </div>

                    </div>

                    <div class="prediction-percent">
                        ${confidence.toFixed(2)}%
                    </div>

                </div>
            `;
        });

        html += `</div>`;
    }


    /*
     * Extracted skills
     */

    if (Array.isArray(result.skills) && result.skills.length > 0) {

        html += `
            <div class="skills-section">
                <h3>Extracted Skills</h3>

                <div class="skills-container">
        `;

        result.skills.forEach(skill => {

            html += `
                <span class="skill-tag">
                    ${escapeHTML(skill)}
                </span>
            `;
        });

        html += `
                </div>
            </div>
        `;
    }


    container.innerHTML = html;
}


/* =========================================================
   DISPLAY RECOMMENDATIONS
   ========================================================= */

function displayRecommendations(
    result,
    elementId = "recommendationResults"
) {

    const container = document.getElementById(elementId);

    if (!container || !result) {
        return;
    }

    const recommendations = result.recommendations || [];

    if (recommendations.length === 0) {

        container.innerHTML = `
            <div class="empty-state">
                No career recommendations available.
            </div>
        `;

        return;
    }

    let html = `
        <div class="recommendation-list">
    `;

    recommendations.forEach((recommendation, index) => {

        const confidence =
            Number(recommendation.confidence_percentage || 0);

        const alignment =
            Number(
                recommendation.skill_alignment_percentage || 0
            );

        const score =
            Number(recommendation.recommendation_score || 0);

        html += `
            <div class="recommendation-card">

                <div class="recommendation-header">

                    <div class="recommendation-rank">
                        #${index + 1}
                    </div>

                    <div class="recommendation-role">
                        ${escapeHTML(recommendation.role)}
                    </div>

                </div>

                <div class="recommendation-metrics">

                    <div class="metric">
                        <span>Confidence</span>
                        <strong>${confidence.toFixed(2)}%</strong>
                    </div>

                    <div class="metric">
                        <span>Skill Alignment</span>
                        <strong>${alignment.toFixed(2)}%</strong>
                    </div>

                    <div class="metric">
                        <span>Recommendation Score</span>
                        <strong>${score.toFixed(4)}</strong>
                    </div>

                </div>

                <div class="skill-alignment-bar">

                    <div
                        class="skill-alignment-fill"
                        style="width:${Math.min(alignment, 100)}%"
                    ></div>

                </div>
        `;


        /*
         * Matched skills
         */

        if (
            Array.isArray(recommendation.matched_skills) &&
            recommendation.matched_skills.length > 0
        ) {

            html += `
                <div class="matched-skills">
                    <h4>Matched Skills</h4>
                    <div class="skills-container">
            `;

            recommendation.matched_skills.forEach(skill => {

                html += `
                    <span class="skill-tag matched">
                        ✓ ${escapeHTML(skill)}
                    </span>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        }


        /*
         * Missing skills
         */

        if (
            Array.isArray(recommendation.missing_skills) &&
            recommendation.missing_skills.length > 0
        ) {

            html += `
                <div class="missing-skills">
                    <h4>Skills to Develop</h4>
                    <div class="skills-container">
            `;

            recommendation.missing_skills.forEach(skill => {

                html += `
                    <span class="skill-tag missing">
                        ✗ ${escapeHTML(skill)}
                    </span>
                `;
            });

            html += `
                    </div>
                </div>
            `;
        }

        html += `
            </div>
        `;
    });

    html += `</div>`;

    container.innerHTML = html;
}


/* =========================================================
   DISPLAY SKILL GAP
   ========================================================= */

function displaySkillGap(result, elementId = "skillGapResults") {

    const container = document.getElementById(elementId);

    if (!container || !result) {
        return;
    }

    const alignment =
        Number(result.skill_alignment_percentage || 0);

    let html = `
        <div class="skill-gap-card">

            <div class="skill-gap-header">

                <div>
                    <span class="skill-gap-label">
                        Skill Alignment
                    </span>

                    <h2>
                        ${alignment.toFixed(2)}%
                    </h2>
                </div>

                <div class="skill-gap-role">
                    ${escapeHTML(result.role || "Unknown Role")}
                </div>

            </div>

            <div class="skill-gap-progress">

                <div
                    class="skill-gap-progress-fill"
                    style="width:${Math.min(alignment, 100)}%"
                ></div>

            </div>
    `;


    /*
     * Matched skills
     */

    if (
        Array.isArray(result.matched_skills) &&
        result.matched_skills.length > 0
    ) {

        html += `
            <div class="skill-gap-section">

                <h3>Matched Skills</h3>

                <div class="skills-container">
        `;

        result.matched_skills.forEach(skill => {

            html += `
                <span class="skill-tag matched">
                    ✓ ${escapeHTML(skill)}
                </span>
            `;
        });

        html += `
                </div>
            </div>
        `;
    }


    /*
     * Missing skills
     */

    if (
        Array.isArray(result.missing_skills) &&
        result.missing_skills.length > 0
    ) {

        html += `
            <div class="skill-gap-section">

                <h3>Missing Skills</h3>

                <div class="skills-container">
        `;

        result.missing_skills.forEach(skill => {

            html += `
                <span class="skill-tag missing">
                    ✗ ${escapeHTML(skill)}
                </span>
            `;
        });

        html += `
                </div>
            </div>
        `;
    }


    /*
     * Required skills
     */

    if (
        Array.isArray(result.required_skills) &&
        result.required_skills.length > 0
    ) {

        html += `
            <div class="skill-gap-section">

                <h3>Required Skills</h3>

                <div class="skills-container">
        `;

        result.required_skills.forEach(skill => {

            html += `
                <span class="skill-tag">
                    ${escapeHTML(skill)}
                </span>
            `;
        });

        html += `
                </div>
            </div>
        `;
    }

    html += `</div>`;

    container.innerHTML = html;
}


/* =========================================================
   DISPLAY MODEL METRICS
   ========================================================= */

function displayModelMetrics(result, elementId = "modelMetrics") {

    const container = document.getElementById(elementId);

    if (!container || !result) {
        return;
    }

    const rf =
        Number(result.models?.random_forest?.accuracy || 0);

    const xgb =
        Number(result.models?.xgboost?.accuracy || 0);

    const bestModel =
        result.best_model || "N/A";

    const bestAccuracy =
        Number(result.best_accuracy || 0);


    container.innerHTML = `

        <div class="model-metrics-grid">

            <div class="model-card">

                <h3>Random Forest</h3>

                <div class="model-accuracy">
                    ${rf.toFixed(2)}%
                </div>

            </div>


            <div class="model-card">

                <h3>XGBoost</h3>

                <div class="model-accuracy">
                    ${xgb.toFixed(2)}%
                </div>

            </div>


            <div class="model-card best-model">

                <h3>Best Model</h3>

                <div class="model-name">
                    ${escapeHTML(bestModel)}
                </div>

                <div class="model-accuracy">
                    ${bestAccuracy.toFixed(2)}%
                </div>

            </div>

        </div>
    `;
}


/* =========================================================
   DISPLAY COMPLETE REPORT
   ========================================================= */

function displayCareerReport(result, elementId = "careerReport") {

    const container = document.getElementById(elementId);

    if (!container || !result) {
        return;
    }

    const report = result.report || result;

    const profile =
        report.candidate_profile || {};

    const prediction =
        report.career_prediction || {};

    const recommendations =
        report.career_recommendations || [];

    const modelInfo =
        report.model_information || {};


    let html = `

        <div class="career-report">

            <div class="report-header">

                <h2>Career Intelligence Report</h2>

                <p>
                    AI-powered career analysis generated by CareerCast
                </p>

            </div>


            <div class="report-summary">

                <div class="report-stat">

                    <span>Top Career</span>

                    <strong>
                        ${escapeHTML(prediction.top_role || "N/A")}
                    </strong>

                </div>


                <div class="report-stat">

                    <span>Skills Detected</span>

                    <strong>
                        ${profile.skill_count || 0}
                    </strong>

                </div>


                <div class="report-stat">

                    <span>Primary Model</span>

                    <strong>
                        ${escapeHTML(modelInfo.primary_model || "N/A")}
                    </strong>

                </div>

            </div>
    `;


    /*
     * Extracted skills
     */

    if (
        Array.isArray(profile.extracted_skills) &&
        profile.extracted_skills.length > 0
    ) {

        html += `

            <div class="report-section">

                <h3>Extracted Skills</h3>

                <div class="skills-container">
        `;

        profile.extracted_skills.forEach(skill => {

            html += `
                <span class="skill-tag">
                    ${escapeHTML(skill)}
                </span>
            `;
        });

        html += `
                </div>

            </div>
        `;
    }


    /*
     * Career predictions
     */

    if (Array.isArray(prediction.top_predictions)) {

        html += `

            <div class="report-section">

                <h3>Career Predictions</h3>

                <div class="prediction-list">
        `;

        prediction.top_predictions.forEach((item, index) => {

            const confidence =
                Number(item.confidence_percentage || 0);

            html += `

                <div class="prediction-item">

                    <div class="prediction-rank">
                        ${index + 1}
                    </div>

                    <div class="prediction-info">

                        <div class="prediction-role-name">
                            ${escapeHTML(item.role)}
                        </div>

                        <div class="prediction-progress">

                            <div
                                class="prediction-progress-bar"
                                style="width:${Math.min(confidence, 100)}%"
                            ></div>

                        </div>

                    </div>

                    <div class="prediction-percent">
                        ${confidence.toFixed(2)}%
                    </div>

                </div>
            `;
        });

        html += `
                </div>

            </div>
        `;
    }


    /*
     * Recommendations
     */

    if (recommendations.length > 0) {

        html += `

            <div class="report-section">

                <h3>Career Recommendations</h3>
        `;

        recommendations.forEach(item => {

            const alignment =
                Number(item.skill_alignment || 0) * 100;

            html += `

                <div class="report-recommendation">

                    <div class="report-recommendation-title">
                        ${escapeHTML(item.role)}
                    </div>

                    <div class="report-recommendation-alignment">
                        Skill Alignment:
                        <strong>
                            ${alignment.toFixed(2)}%
                        </strong>
                    </div>
        `;


            if (
                Array.isArray(item.matched_skills) &&
                item.matched_skills.length > 0
            ) {

                html += `
                    <div class="skills-container">
                `;

                item.matched_skills.forEach(skill => {

                    html += `
                        <span class="skill-tag matched">
                            ✓ ${escapeHTML(skill)}
                        </span>
                    `;
                });

                html += `</div>`;
            }


            if (
                Array.isArray(item.missing_skills) &&
                item.missing_skills.length > 0
            ) {

                html += `
                    <div class="skills-container">
                `;

                item.missing_skills.forEach(skill => {

                    html += `
                        <span class="skill-tag missing">
                            ✗ ${escapeHTML(skill)}
                        </span>
                    `;
                });

                html += `</div>`;
            }

            html += `
                </div>
            `;
        });

        html += `
            </div>
        `;
    }


    html += `

            <div class="report-footer">

                <span>
                    ${escapeHTML(modelInfo.primary_model || "AI Model")}
                </span>

                <span>
                    ${escapeHTML(modelInfo.milestone || "Milestone 3")}
                </span>

            </div>

        </div>
    `;


    container.innerHTML = html;
}


/* =========================================================
   ESCAPE HTML
   Prevents unsafe text from being inserted into the page.
   ========================================================= */

function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* =========================================================
   GLOBAL CAREERCAST API OBJECT
   ========================================================= */

window.CareerCastAPI = {

    request: apiRequest,

    health: checkAPIHealth,

    predict: predictCareer,

    recommend: getCareerRecommendations,

    skillGap: getSkillGap,

    report: generateCareerReport,

    metrics: getModelMetrics,

    analyze: analyzeCareer,

    displayPrediction: displayPrediction,

    displayRecommendations: displayRecommendations,

    displaySkillGap: displaySkillGap,

    displayMetrics: displayModelMetrics,

    displayReport: displayCareerReport

};


/* =========================================================
   AUTOMATIC API HEALTH CHECK
   ========================================================= */

document.addEventListener("DOMContentLoaded", async function () {

    console.log("==========================================");
    console.log("CareerCast Milestone 3 API Integration");
    console.log("==========================================");
    console.log("API:", API_BASE_URL);

    try {

        const health = await checkAPIHealth();

        if (health.status === "healthy") {

            console.log("✓ CareerCast API is healthy");

            if (health.models) {

                console.log(
                    "Loaded models:",
                    health.models
                );
            }

        } else {

            console.warn(
                "⚠ CareerCast API is not healthy."
            );
        }

    } catch (error) {

        console.warn(
            "⚠ Could not connect to CareerCast API."
        );

        console.warn(
            "Make sure FastAPI is running at:",
            API_BASE_URL
        );
    }

});