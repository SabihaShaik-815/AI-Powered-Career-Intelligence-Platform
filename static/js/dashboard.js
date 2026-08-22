"use strict";

/* ============================================================
   CAREERCAST - DASHBOARD.JS
   COMPLETE CORRECTED VERSION
   ============================================================ */

/* ============================================================
   GLOBAL DATA
   ============================================================ */

let latestAnalysis = null;
let modelComparisonChart = null;
let skillEmbeddingChart = null;

/* ============================================================
   API CONFIGURATION
   ============================================================ */

const MILESTONE3_API_BASE = window.MILESTONE3_API_BASE || "";

/* ============================================================
   HELPER FUNCTIONS
   ============================================================ */

function $(id) {
    return document.getElementById(id);
}

function escapeHtml(value) {
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

function normalizePercentage(value) {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return 0;
    }

    let text = String(value).trim();

    if (text.endsWith("%")) {
        text = text.substring(0, text.length - 1);
    }

    let number = parseFloat(text);

    if (Number.isNaN(number)) {
        return 0;
    }

    // Convert decimals like 0.85 -> 85
    if (number > 0 && number <= 1) {
        number *= 100;
    }

    return Math.max(0, Math.min(100, number));
}

function formatPercentage(value) {
    return normalizePercentage(value).toFixed(1) + "%";
}

function showStatus(elementId, message, type = "") {
    const element = $(elementId);

    if (!element) {
        return;
    }

    element.textContent = message;
    element.className = "status-msg";

    if (type) {
        element.classList.add(type);
    }
}

/* ============================================================
   API URL
   ============================================================ */

function apiUrl(path) {
    const base = MILESTONE3_API_BASE.replace(/\/$/, "");

    if (!path.startsWith("/")) {
        path = "/" + path;
    }

    return base + path;
}

/* ============================================================
   SAFE JSON FETCH
   ============================================================ */

async function fetchJson(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        cache: "no-store"
    });

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    if (!response.ok) {
        const fetchError = new Error("HTTP " + response.status);
        fetchError.status = response.status;
        fetchError.data = data;
        throw fetchError;
    }

    return data;
}

/* ============================================================
   TAB SYSTEM
   ============================================================ */

function initializeTabs() {
    const buttons = document.querySelectorAll(".tab-btn");
    const panels = document.querySelectorAll(".tab-panel");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            const target = button.dataset.tab;

            buttons.forEach(function (btn) {
                btn.classList.remove("active");
            });

            panels.forEach(function (panel) {
                panel.classList.remove("active");
            });

            button.classList.add("active");

            const targetPanel = document.getElementById(
                "tab-" + target
            );

            if (targetPanel) {
                targetPanel.classList.add("active");
            }

            if (target === "analytics") {
                loadAdvancedMetrics();
            }

            if (target === "milestone3") {
                checkMilestone3API();
            }
        });
    });
}

function switchToTab(tabName) {
    const button = document.querySelector(
        `.tab-btn[data-tab="${tabName}"]`
    );

    if (button) {
        button.click();
    }
}

/* ============================================================
   RESUME UPLOAD
   ============================================================ */

function initializeResumeUpload() {
    const dropzone = $("dropzone");
    const fileInput = $("resumeFile");
    const selectedFile = $("selectedFile");
    const removeFileBtn = $("removeFileBtn");

    if (!dropzone || !fileInput) {
        return;
    }

    dropzone.addEventListener("click", function (event) {
        if (
            event.target === removeFileBtn ||
            (
                event.target.closest &&
                event.target.closest("#removeFileBtn")
            )
        ) {
            return;
        }

        fileInput.click();
    });

    fileInput.addEventListener("change", function () {
        if (
            fileInput.files &&
            fileInput.files.length > 0
        ) {
            handleSelectedFile(fileInput.files[0]);
        }
    });

    dropzone.addEventListener("dragover", function (event) {
        event.preventDefault();
        dropzone.classList.add("dragover");
    });

    dropzone.addEventListener("dragleave", function (event) {
        event.preventDefault();
        dropzone.classList.remove("dragover");
    });

    dropzone.addEventListener("drop", function (event) {
        event.preventDefault();
        dropzone.classList.remove("dragover");

        const files = event.dataTransfer.files;

        if (!files || files.length === 0) {
            return;
        }

        const file = files[0];

        const allowedExtensions = [
            ".pdf",
            ".docx",
            ".txt"
        ];

        const filename = file.name.toLowerCase();

        const valid = allowedExtensions.some(function (extension) {
            return filename.endsWith(extension);
        });

        if (!valid) {
            alert("Please upload a PDF, DOCX or TXT file.");
            return;
        }

        try {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        } catch (error) {
            console.warn(
                "Could not assign dropped file:",
                error
            );
        }

        handleSelectedFile(file);
    });

    if (removeFileBtn) {
        removeFileBtn.addEventListener(
            "click",
            function (event) {
                event.preventDefault();
                event.stopPropagation();

                fileInput.value = "";

                if (selectedFile) {
                    selectedFile.style.display = "none";
                }
            }
        );
    }
}

function handleSelectedFile(file) {
    const selectedFile = $("selectedFile");
    const selectedFileName = $("selectedFileName");

    if (!file) {
        return;
    }

    if (selectedFileName) {
        selectedFileName.textContent = file.name;
    }

    if (selectedFile) {
        selectedFile.style.display = "flex";
    }
}

/* ============================================================
   ANALYZE BUTTON
   ============================================================ */

function initializeAnalyzeButton() {
    const analyzeBtn = $("analyzeBtn");

    if (!analyzeBtn) {
        return;
    }

    analyzeBtn.addEventListener(
        "click",
        analyzeResume
    );
}

async function analyzeResume() {
    const fileInput = $("resumeFile");
    const resumeText = $("resumeText");

    const text = resumeText
        ? resumeText.value.trim()
        : "";

    const hasFile =
        fileInput &&
        fileInput.files &&
        fileInput.files.length > 0;

    if (!hasFile && !text) {
        showStatus(
            "analyzeStatus",
            "Please upload a resume or paste resume text.",
            "error"
        );
        return;
    }

    const button = $("analyzeBtn");

    if (button) {
        button.disabled = true;
        button.textContent = "Analyzing...";
    }

    showStatus(
        "analyzeStatus",
        "Analyzing resume..."
    );

    try {
        let response;

        if (hasFile) {
            const formData = new FormData();

            formData.append(
                "resume_file",
                fileInput.files[0]
            );

            response = await fetch(
                apiUrl("/api/analyze"),
                {
                    method: "POST",
                    body: formData
                }
            );
        } else {
            response = await fetch(
                apiUrl("/api/analyze"),
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        text: text
                    })
                }
            );
        }

        let data = {};

        try {
            data = await response.json();
        } catch (error) {
            throw new Error(
                "Invalid response received from server."
            );
        }

        if (
            !response.ok ||
            data.success === false
        ) {
            throw new Error(
                data.error ||
                "Resume analysis failed."
            );
        }

        latestAnalysis = data;

        displayAnalysis(data);

        showStatus(
            "analyzeStatus",
            "Resume analyzed successfully.",
            "success"
        );

        switchToTab("results");

        updateAnalyticsFromAnalysis(data);

    } catch (error) {
        console.error(
            "Resume analysis error:",
            error
        );

        showStatus(
            "analyzeStatus",
            error.message ||
            "Could not analyze resume.",
            "error"
        );

    } finally {
        if (button) {
            button.disabled = false;
            button.textContent = "Analyze Resume";
        }
    }
}

/* ============================================================
   DISPLAY ANALYSIS
   ============================================================ */

function displayAnalysis(data) {
    const noResults = $("noResults");
    const resultsGrid = $("resultsGrid");
    const skillGapCard = $("skillGapCard");

    if (noResults) {
        noResults.style.display = "none";
    }

    if (resultsGrid) {
        resultsGrid.style.display = "grid";
    }

    if (skillGapCard) {
        skillGapCard.style.display = "block";
    }

    const parsedText = $("parsedText");

    if (parsedText) {
        parsedText.textContent =
            data.text ||
            data.parsed_text ||
            "No resume text available.";
    }

    renderSkills(
        data.skills || [],
        "skillBadges"
    );

    renderEducation(
        data.education || []
    );

    const predictions = getCareerList(data);

    renderPredictions(predictions);

    const bestRole = $("bestRole");
    const bestConf = $("bestConf");

    const topPrediction =
        predictions.length > 0
            ? predictions[0]
            : null;

    const topRole =
        data.top_role ||
        data.prediction ||
        (
            topPrediction
                ? topPrediction.role
                : ""
        );

    if (bestRole) {
        bestRole.textContent =
            topRole || "No prediction";
    }

    if (bestConf) {
        bestConf.textContent =
            topPrediction
                ? formatPercentage(
                    topPrediction.confidence
                ) + " confidence"
                : "";
    }

    updateSkillAlignment(
        data.skill_alignment ??
        data.skill_alignment_score ??
        0
    );

    renderSkillGap(
        topRole,
        data.skill_gap || {}
    );

    renderCareerRecommendations(
        predictions
    );

    renderConfidenceList(
        predictions
    );
}

/* ============================================================
   CAREER LIST
   ============================================================ */

function getCareerList(data) {
    if (
        data &&
        Array.isArray(data.predictions) &&
        data.predictions.length > 0
    ) {
        return data.predictions;
    }

    if (
        data &&
        Array.isArray(data.recommendations) &&
        data.recommendations.length > 0
    ) {
        return data.recommendations;
    }

    if (
        data &&
        data.prediction
    ) {
        return [
            {
                role: data.prediction,
                confidence: data.confidence || 0
            }
        ];
    }

    return [];
}

/* ============================================================
   SKILLS
   ============================================================ */

function renderSkills(skills, elementId) {
    const container = $(elementId);

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (
        !Array.isArray(skills) ||
        skills.length === 0
    ) {
        container.innerHTML =
            `<span class="muted">No skills detected.</span>`;
        return;
    }

    skills.forEach(function (skill) {
        const badge = document.createElement("span");

        badge.className = "skill-badge";

        badge.textContent =
            typeof skill === "string"
                ? skill
                : (
                    skill.name ||
                    skill.skill ||
                    JSON.stringify(skill)
                );

        container.appendChild(badge);
    });
}

/* ============================================================
   EDUCATION
   ============================================================ */

function renderEducation(education) {
    const list = $("educationList");

    if (!list) {
        return;
    }

    list.innerHTML = "";

    if (
        !Array.isArray(education) ||
        education.length === 0
    ) {
        list.innerHTML =
            `<li class="muted">
                No education information detected.
            </li>`;
        return;
    }

    education.forEach(function (item) {
        const li = document.createElement("li");

        li.textContent =
            typeof item === "string"
                ? item
                : (
                    item.degree ||
                    item.name ||
                    JSON.stringify(item)
                );

        list.appendChild(li);
    });
}

/* ============================================================
   PREDICTION BARS
   ============================================================ */

function renderPredictions(predictions) {
    const container = $("predictionBars");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (
        !Array.isArray(predictions) ||
        predictions.length === 0
    ) {
        container.innerHTML =
            `<p class="muted">
                No predictions available.
            </p>`;
        return;
    }

    predictions
        .slice(0, 5)
        .forEach(function (item, index) {
            const role =
                item.role ||
                item.prediction ||
                "Unknown Career";

            const percentage =
                normalizePercentage(
                    item.confidence
                );

            const row =
                document.createElement("div");

            row.className =
                "prediction-row";

            row.innerHTML = `
                <div class="prediction-header">
                    <span class="prediction-role">
                        ${index + 1}. ${escapeHtml(role)}
                    </span>

                    <strong class="prediction-confidence">
                        ${percentage.toFixed(1)}%
                    </strong>
                </div>

                <div class="prediction-track">
                    <div
                        class="prediction-fill"
                        style="width:${percentage}%"
                    ></div>
                </div>
            `;

            container.appendChild(row);
        });
}

/* ============================================================
   CAREER RECOMMENDATIONS
   ============================================================ */

function renderCareerRecommendations(predictions) {
    const container =
        $("careerRecommendations");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (
        !Array.isArray(predictions) ||
        predictions.length === 0
    ) {
        container.innerHTML =
            `<p class="muted">
                Analyze a resume to see recommendations.
            </p>`;
        return;
    }

    predictions
        .slice(0, 5)
        .forEach(function (item, index) {
            const role =
                item.role ||
                item.prediction ||
                "Unknown Career";

            const confidence =
                normalizePercentage(
                    item.confidence
                );

            const recommendation =
                document.createElement("div");

            recommendation.className =
                "career-recommendation";

            recommendation.innerHTML = `
                <div class="career-rec-header">
                    <span>
                        ${index + 1}. ${escapeHtml(role)}
                    </span>

                    <strong>
                        ${confidence.toFixed(1)}%
                    </strong>
                </div>

                <div class="confidence-track">
                    <div
                        class="confidence-fill"
                        style="width:${confidence}%"
                    ></div>
                </div>
            `;

            container.appendChild(
                recommendation
            );
        });
}

/* ============================================================
   CONFIDENCE LIST
   ============================================================ */

function renderConfidenceList(predictions) {
    const container =
        $("confidenceList");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    if (
        !Array.isArray(predictions) ||
        predictions.length === 0
    ) {
        container.innerHTML =
            `<p class="muted">
                Analyze a resume to see confidence.
            </p>`;
        return;
    }

    predictions
        .slice(0, 5)
        .forEach(function (item, index) {
            const role =
                item.role ||
                item.prediction ||
                "Unknown Career";

            const confidence =
                normalizePercentage(
                    item.confidence
                );

            const row =
                document.createElement("div");

            row.className =
                "confidence-row";

            row.innerHTML = `
                <div class="confidence-header">
                    <span>
                        ${index + 1}. ${escapeHtml(role)}
                    </span>

                    <strong>
                        ${confidence.toFixed(1)}%
                    </strong>
                </div>

                <div class="confidence-track">
                    <div
                        class="confidence-fill"
                        style="width:${confidence}%"
                    ></div>
                </div>
            `;

            container.appendChild(row);
        });
}

/* ============================================================
   SKILL GAP
   ============================================================ */

function renderSkillGap(role, skillGap) {
    const roleElement =
        $("skillGapRole");

    if (roleElement) {
        roleElement.textContent =
            role
                ? " - " + role
                : "";
    }

    renderSkills(
        skillGap.matched || [],
        "matchedBadges"
    );

    renderSkills(
        skillGap.missing || [],
        "missingBadges"
    );
}

/* ============================================================
   SKILL ALIGNMENT
   ============================================================ */

function updateSkillAlignment(alignment) {
    const value =
        normalizePercentage(alignment);

    const circle =
        $("skillAlignmentCircle");

    const analyticsValue =
        $("analyticsSkillAlignment");

    const list =
        $("skillAlignmentList");

    if (circle) {
        circle.textContent =
            value.toFixed(1) + "%";
    }

    if (analyticsValue) {
        analyticsValue.textContent =
            value.toFixed(1) + "%";
    }

    if (list) {
        list.innerHTML = `
            <div class="alignment-bar">
                <div
                    class="alignment-fill"
                    style="width:${value}%"
                ></div>
            </div>

            <p class="muted">
                ${value.toFixed(1)}% of the required
                skills are matched.
            </p>
        `;
    }
}

/* ============================================================
   MILESTONE 2 - ADVANCED METRICS
   ============================================================ */

async function loadAdvancedMetrics() {
    try {
        const data = await fetchJson(
            apiUrl("/api/advanced-metrics"),
            {
                method: "GET"
            }
        );

        if (data.success === false) {
            throw new Error(
                data.error ||
                "Could not load metrics."
            );
        }

        displayAdvancedMetrics(data);

    } catch (error) {
        console.error(
            "Advanced metrics error:",
            error
        );
    }
}

/* ============================================================
   DISPLAY ADVANCED METRICS
   ============================================================ */

function displayAdvancedMetrics(data) {
    const bestModel =
        $("analyticsBestModel");

    const bestAccuracy =
        $("analyticsBestAccuracy");

    if (bestModel) {
        bestModel.textContent =
            data.best_model ||
            data.model ||
            "--";
    }

    if (bestAccuracy) {
        bestAccuracy.textContent =
            data.best_accuracy !== undefined
                ? formatPercentage(
                    data.best_accuracy
                )
                : "--";
    }

    if (latestAnalysis) {
        const topCareer =
            $("analyticsTopCareer");

        if (topCareer) {
            topCareer.textContent =
                latestAnalysis.top_role ||
                latestAnalysis.prediction ||
                "--";
        }

        if (
            latestAnalysis.skill_alignment !==
            undefined
        ) {
            updateSkillAlignment(
                latestAnalysis.skill_alignment
            );
        }
    }

    renderModelChart(data);
    renderEmbeddingChart();
}

/* ============================================================
   MODEL COMPARISON CHART
   ============================================================ */

function renderModelChart(data) {
    const canvas =
        $("modelComparisonChart");

    if (!canvas) {
        return;
    }

    if (typeof Chart === "undefined") {
        console.warn(
            "Chart.js is not loaded."
        );
        return;
    }

    const context =
        canvas.getContext("2d");

    if (modelComparisonChart) {
        modelComparisonChart.destroy();
    }

    function getAccuracy(model) {
        if (!model) {
            return 0;
        }

        if (typeof model === "number") {
            return normalizePercentage(model);
        }

        return normalizePercentage(
            model.accuracy ??
            model.value ??
            model
        );
    }

    modelComparisonChart = new Chart(
        context,
        {
            type: "bar",

            data: {
                labels: [
                    "Logistic Regression",
                    "Random Forest",
                    "XGBoost"
                ],

                datasets: [
                    {
                        label: "Accuracy (%)",

                        data: [
                            getAccuracy(
                                data.logistic_regression
                            ),
                            getAccuracy(
                                data.random_forest
                            ),
                            getAccuracy(
                                data.xgboost
                            )
                        ],

                        borderWidth: 1,
                        borderRadius: 8
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                plugins: {
                    legend: {
                        display: true
                    }
                },

                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,

                        ticks: {
                            callback: function (value) {
                                return value + "%";
                            }
                        }
                    }
                }
            }
        }
    );
}

/* ============================================================
   SBERT / SKILL EMBEDDING CHART
   ============================================================ */

function renderEmbeddingChart() {
    const canvas =
        $("skillEmbeddingChart");

    if (!canvas) {
        return;
    }

    if (typeof Chart === "undefined") {
        console.warn(
            "Chart.js is not loaded."
        );
        return;
    }

    const context =
        canvas.getContext("2d");

    if (skillEmbeddingChart) {
        skillEmbeddingChart.destroy();
    }

    skillEmbeddingChart = new Chart(
        context,
        {
            type: "scatter",

            data: {
                datasets: [
                    {
                        label:
                            "Software Engineering",

                        data: [
                            { x: 1, y: 5 },
                            { x: 2, y: 4 },
                            { x: 1.5, y: 4.5 }
                        ],

                        pointRadius: 7
                    },

                    {
                        label:
                            "Data Science",

                        data: [
                            { x: 5, y: 5 },
                            { x: 4.5, y: 4 },
                            { x: 5.5, y: 4.5 }
                        ],

                        pointRadius: 7
                    },

                    {
                        label: "AI / ML",

                        data: [
                            { x: 3, y: 2 },
                            { x: 3.5, y: 2.5 },
                            { x: 2.5, y: 2 }
                        ],

                        pointRadius: 7
                    },

                    {
                        label: "Research",

                        data: [
                            { x: 7, y: 2 },
                            { x: 6.5, y: 2.5 }
                        ],

                        pointRadius: 7
                    },

                    {
                        label: "Finance",

                        data: [
                            { x: 8, y: 5 },
                            { x: 8.5, y: 4 }
                        ],

                        pointRadius: 7
                    }
                ]
            },

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    x: {
                        min: 0,
                        max: 10,

                        title: {
                            display: true,
                            text:
                                "Embedding Dimension 1"
                        }
                    },

                    y: {
                        min: 0,
                        max: 6,

                        title: {
                            display: true,
                            text:
                                "Embedding Dimension 2"
                        }
                    }
                }
            }
        }
    );
}

/* ============================================================
   UPDATE ANALYTICS FROM ANALYSIS
   ============================================================ */

function updateAnalyticsFromAnalysis(data) {
    const topCareer =
        $("analyticsTopCareer");

    const topRole =
        data.top_role ||
        data.prediction ||
        "";

    if (topCareer) {
        topCareer.textContent =
            topRole || "--";
    }

    updateSkillAlignment(
        data.skill_alignment ??
        data.skill_alignment_score ??
        0
    );

    const predictions =
        getCareerList(data);

    renderCareerRecommendations(
        predictions
    );

    renderConfidenceList(
        predictions
    );
}

/* ============================================================
   PROFILE FORM
   ============================================================ */

function initializeProfileForm() {
    const form =
        $("profileForm");

    if (!form) {
        return;
    }

    loadProfile();

    form.addEventListener(
        "submit",
        async function (event) {
            event.preventDefault();

            const formData =
                new FormData(form);

            const data = {
                name:
                    formData.get("name") || "",

                email:
                    formData.get("email") || "",

                years_experience:
                    formData.get(
                        "years_experience"
                    ) || "",

                education_level:
                    formData.get(
                        "education_level"
                    ) || "",

                skills:
                    formData.get("skills") || "",

                current_role:
                    formData.get(
                        "current_role"
                    ) || "",

                desired_role:
                    formData.get(
                        "desired_role"
                    ) || "",

                location:
                    formData.get(
                        "location"
                    ) || ""
            };

            try {
                const result =
                    await fetchJson(
                        apiUrl("/api/profile"),
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(data)
                        }
                    );

                if (
                    result.success === false
                ) {
                    throw new Error(
                        result.error ||
                        "Profile could not be saved."
                    );
                }

                showStatus(
                    "profileStatus",
                    "Profile saved successfully.",
                    "success"
                );

            } catch (error) {
                console.error(
                    "Profile save error:",
                    error
                );

                showStatus(
                    "profileStatus",
                    error.message ||
                    "Could not save profile.",
                    "error"
                );
            }
        }
    );
}

/* ============================================================
   LOAD PROFILE
   ============================================================ */

async function loadProfile() {
    try {
        const data =
            await fetchJson(
                apiUrl("/api/profile")
            );

        if (
            !data ||
            typeof data !== "object"
        ) {
            return;
        }

        setValue(
            "pf_name",
            data.name
        );

        setValue(
            "pf_email",
            data.email
        );

        setValue(
            "pf_years",
            data.years_experience
        );

        setValue(
            "pf_education",
            data.education_level
        );

        setValue(
            "pf_skills",
            data.skills
        );

        setValue(
            "pf_current_role",
            data.current_role
        );

        setValue(
            "pf_desired_role",
            data.desired_role
        );

        setValue(
            "pf_location",
            data.location
        );

    } catch (error) {
        console.warn(
            "Profile loading failed:",
            error
        );
    }
}

function setValue(id, value) {
    const element = $(id);

    if (
        element &&
        value !== undefined &&
        value !== null
    ) {
        element.value = value;
    }
}

/* ============================================================
   MILESTONE 3 API HEALTH
   ============================================================ */

async function checkMilestone3API() {
    console.log(
        "Checking CareerCast Milestone 3 API..."
    );

    const statusBadge =
        $("milestone3StatusBadge");

    const apiStatus =
        $("apiStatus");

    const predictionStatus =
        $("predictionApiStatus");

    const recommendationStatus =
        $("recommendationApiStatus");

    const deploymentStatus =
        $("deploymentStatus");

    const healthResult =
        $("apiHealthResult");

    const responseBox =
        $("apiResponseBox");

    const serviceName =
        $("apiServiceName");

    if (statusBadge) {
        statusBadge.textContent =
            "● Checking API";

        statusBadge.classList.remove(
            "api-online"
        );
    }

    if (apiStatus) {
        apiStatus.textContent =
            "Checking...";
    }

    if (predictionStatus) {
        predictionStatus.textContent =
            "Checking...";
    }

    if (recommendationStatus) {
        recommendationStatus.textContent =
            "Checking...";
    }

    if (deploymentStatus) {
        deploymentStatus.textContent =
            "Checking...";
    }

    if (healthResult) {
        healthResult.textContent =
            "Checking API connection...";
    }

    const healthEndpoints = [
        "/api/milestone3",
        "/api/milestone3/health",
        "/api/health",
        "/api/status",
        "/health",
        "/status"
    ];

    let data = null;
    let successfulEndpoint = null;
    let lastError = null;

    for (const endpoint of healthEndpoints) {
        try {
            console.log(
                "Trying endpoint:",
                apiUrl(endpoint)
            );

            const result =
                await fetchJson(
                    apiUrl(endpoint),
                    {
                        method: "GET"
                    }
                );

            if (
                result &&
                (
                    result.api_status ||
                    result.prediction_api ||
                    result.recommendation_api ||
                    result.deployment ||
                    result.status === "ok" ||
                    result.status === "healthy"
                )
            ) {
                data = result;
                successfulEndpoint =
                    endpoint;

                console.log(
                    "Milestone 3 API FOUND:",
                    endpoint
                );

                break;
            }

        } catch (error) {
            lastError = error;

            console.warn(
                "Endpoint failed:",
                endpoint,
                error.message
            );
        }
    }

    if (!data) {
        const message =
            lastError
                ? lastError.message
                : "Milestone 3 API endpoint not found.";

        setMilestone3Offline(
            message
        );

        return;
    }

    const apiStatusText =
        String(
            data.api_status ||
            data.status ||
            ""
        ).toLowerCase();

    const predictionText =
        String(
            data.prediction_api ||
            ""
        ).toLowerCase();

    const isOnline =
        data.success !== false &&
        (
            apiStatusText === "online" ||
            apiStatusText === "working" ||
            apiStatusText === "running" ||
            apiStatusText === "ok" ||
            apiStatusText === "healthy" ||
            predictionText === "working" ||
            predictionText === "online"
        );

    if (serviceName) {
        serviceName.textContent =
            data.service ||
            "CareerCast API";
    }

    if (apiStatus) {
        apiStatus.textContent =
            data.api_status ||
            data.status ||
            (
                isOnline
                    ? "Online"
                    : "Offline"
            );
    }

    if (predictionStatus) {
        predictionStatus.textContent =
            data.prediction_api ||
            (
                isOnline
                    ? "Working"
                    : "Unavailable"
            );
    }

    if (recommendationStatus) {
        recommendationStatus.textContent =
            data.recommendation_api ||
            (
                isOnline
                    ? "Working"
                    : "Unavailable"
            );
    }

    if (deploymentStatus) {
        deploymentStatus.textContent =
            data.deployment ||
            (
                isOnline
                    ? "Running"
                    : "Stopped"
            );
    }

    if (healthResult) {
        healthResult.textContent =
            data.message ||
            (
                isOnline
                    ? "Milestone 3 API is running successfully."
                    : "Milestone 3 API responded but is offline."
            );
    }

    if (statusBadge) {
        if (isOnline) {
            statusBadge.textContent =
                "● API Online";

            statusBadge.classList.add(
                "api-online"
            );
        } else {
            statusBadge.textContent =
                "● API Offline";

            statusBadge.classList.remove(
                "api-online"
            );
        }
    }

    if (responseBox) {
        responseBox.textContent =
            JSON.stringify(
                {
                    endpoint:
                        successfulEndpoint,
                    ...data
                },
                null,
                2
            );
    }

    window.milestone3Health = data;

    console.log(
        "CareerCast Milestone 3 status:",
        data
    );
}

/* ============================================================
   MILESTONE 3 OFFLINE
   ============================================================ */

function setMilestone3Offline(errorMessage) {
    const statusBadge =
        $("milestone3StatusBadge");

    const apiStatus =
        $("apiStatus");

    const predictionStatus =
        $("predictionApiStatus");

    const recommendationStatus =
        $("recommendationApiStatus");

    const deploymentStatus =
        $("deploymentStatus");

    const healthResult =
        $("apiHealthResult");

    const responseBox =
        $("apiResponseBox");

    if (statusBadge) {
        statusBadge.textContent =
            "● API Offline";

        statusBadge.classList.remove(
            "api-online"
        );
    }

    if (apiStatus) {
        apiStatus.textContent =
            "Offline";
    }

    if (predictionStatus) {
        predictionStatus.textContent =
            "Unavailable";
    }

    if (recommendationStatus) {
        recommendationStatus.textContent =
            "Unavailable";
    }

    if (deploymentStatus) {
        deploymentStatus.textContent =
            "Stopped";
    }

    if (healthResult) {
        healthResult.textContent =
            "API connection failed: " +
            errorMessage;
    }

    if (responseBox) {
        responseBox.textContent =
            JSON.stringify(
                {
                    success: false,
                    api_status: "Offline",
                    error: errorMessage
                },
                null,
                2
            );
    }

    window.milestone3Health = {
        success: false,
        api_status: "Offline",
        error: errorMessage
    };
}

/* ============================================================
   MANUAL API CHECK BUTTON
   ============================================================ */

function initializeApiCheckButton() {
    const button =
        $("checkApiBtn");

    if (!button) {
        return;
    }

    button.addEventListener(
        "click",
        async function () {
            button.disabled = true;
            button.textContent =
                "Checking...";

            try {
                await checkMilestone3API();

            } finally {
                button.disabled = false;
                button.textContent =
                    "Check API";
            }
        }
    );
}

/* ============================================================
   INITIALIZATION
   ============================================================ */

document.addEventListener(
    "DOMContentLoaded",
    function () {
        console.log(
            "=============================================="
        );

        console.log(
            "CareerCast Dashboard JS loaded."
        );

        console.log(
            "Milestone 3 endpoint:",
            apiUrl("/api/milestone3")
        );

        console.log(
            "=============================================="
        );

        // Tabs
        initializeTabs();

        // Resume Upload
        initializeResumeUpload();

        // Analyze Button
        initializeAnalyzeButton();

        // Profile
        initializeProfileForm();

        // API Check Button
        initializeApiCheckButton();

        // Milestone 2
        loadAdvancedMetrics();

        // Milestone 3
        checkMilestone3API();
    }
);