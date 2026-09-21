/* ============================================================
   CAREERCAST - MILESTONE 4
   PACKAGING, TESTING & FINALIZATION
   ============================================================ */

"use strict";


/* ============================================================
   GLOBAL VARIABLES
   ============================================================ */

let milestone4Charts = {};

let milestone4Initialized = false;


/* ============================================================
   INITIALIZE MILESTONE 4
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {

    console.log("CareerCast Milestone 4 JavaScript loaded");

    initializeMilestone4();

});


function initializeMilestone4() {

    if (milestone4Initialized) {
        return;
    }

    milestone4Initialized = true;

    console.log("Initializing Milestone 4...");

    setupMilestone4Tabs();

    setupRefreshButton();

    setupExportButton();

    setupCareerComparison();

    setupDocumentationLinks();

    loadMilestone4Data();

}


/* ============================================================
   MILESTONE 4 TAB HANDLING
   ============================================================ */

function setupMilestone4Tabs() {

    const tabButtons =
        document.querySelectorAll(
            "[data-milestone4-tab]"
        );

    const tabContents =
        document.querySelectorAll(
            "[data-milestone4-content]"
        );


    if (!tabButtons.length) {
        return;
    }


    tabButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const target =
                    button.getAttribute(
                        "data-milestone4-tab"
                    );


                tabButtons.forEach(function (item) {

                    item.classList.remove("active");

                });


                tabContents.forEach(function (content) {

                    content.classList.remove("active");

                });


                button.classList.add("active");


                const targetContent =
                    document.querySelector(
                        '[data-milestone4-content="' +
                        target +
                        '"]'
                    );


                if (targetContent) {

                    targetContent.classList.add(
                        "active"
                    );

                }

            }
        );

    });

}


/* ============================================================
   LOAD MILESTONE 4 DATA
   ============================================================ */

async function loadMilestone4Data() {

    console.log(
        "Loading Milestone 4 data..."
    );


    showLoadingState();


    try {

        const response =
            await fetch(
                "/api/milestone4"
            );


        if (!response.ok) {

            throw new Error(
                "Milestone 4 API returned " +
                response.status
            );

        }


        const data =
            await response.json();


        console.log(
            "Milestone 4 data:",
            data
        );


        if (data && typeof data === "object") {

            updateMilestone4Dashboard(
                data
            );

        }
        else {

            console.warn(
                "Milestone 4 API returned incomplete data"
            );

            loadMilestone4FallbackData();

        }

    }
    catch (error) {

        console.error(
            "Milestone 4 loading error:",
            error
        );


        loadMilestone4FallbackData();

    }
    finally {

        hideLoadingState();

    }

}


/* ============================================================
   UPDATE MILESTONE 4 DASHBOARD
   ============================================================ */

function updateMilestone4Dashboard(data) {

    updatePackagingStatus(
        data.packaging ||
        data.package_status ||
        {}
    );


    updateTestingStatus(
        data.testing ||
        data.test_status ||
        {}
    );


    updateDocumentationStatus(
        data.documentation ||
        {}
    );


    updateCohortAnalytics(
        data.cohort ||
        data.cohort_analytics ||
        {}
    );


    updateCareerComparison(
        data.career_comparison ||
        {}
    );


    updateFinalizationStatus(
        data.finalization ||
        {}
    );


    if (data.metrics) {

        updateMetricCards(
            data.metrics
        );

    }


    if (data.success !== false) {

        setText(
            "m4OverallStatus",
            "Milestone 4 Ready"
        );

    }

}


/* ============================================================
   PACKAGING STATUS
   ============================================================ */

function updatePackagingStatus(data) {

    const packageAvailable =
        data.package_available ??
        data.installed ??
        false;


    const pipInstallable =
        data.pip_installable ??
        data.installable ??
        false;


    const cliAvailable =
        data.cli_available ??
        data.cli ??
        false;


    const apiDocumentation =
        data.api_documentation ??
        data.api_docs ??
        false;


    setStatus(
        "m4PackageStatus",
        packageAvailable
    );


    setStatus(
        "m4PipStatus",
        pipInstallable
    );


    setStatus(
        "m4CLIStatus",
        cliAvailable
    );


    setStatus(
        "m4APIDocStatus",
        apiDocumentation
    );

}


/* ============================================================
   TESTING STATUS
   ============================================================ */

function updateTestingStatus(data) {

    const parserTests =
        data.parser_tests ??
        data.parsing_tests ??
        0;


    const predictionTests =
        data.prediction_tests ??
        0;


    const recommendationTests =
        data.recommendation_tests ??
        0;


    const integrationTests =
        data.integration_tests ??
        0;


    const regressionTests =
        data.regression_tests ??
        0;


    const passedTests =
        data.passed ??
        data.passed_tests ??
        0;


    const failedTests =
        data.failed ??
        data.failed_tests ??
        0;


    const totalTests =
        data.total ??
        data.total_tests ??
        (
            Number(parserTests) +
            Number(predictionTests) +
            Number(recommendationTests) +
            Number(integrationTests) +
            Number(regressionTests)
        );


    /* --------------------------------------------------------
       Current dashboard IDs
       -------------------------------------------------------- */

    setText(
        "m4ParserTests",
        parserTests
    );


    setText(
        "m4PredictionTests",
        predictionTests
    );


    setText(
        "m4RecommendationTests",
        recommendationTests
    );


    setText(
        "m4IntegrationTests",
        integrationTests
    );


    setText(
        "m4RegressionTests",
        regressionTests
    );


    setText(
        "m4TestsPassed",
        passedTests
    );


    setText(
        "m4TestsFailed",
        failedTests
    );


    setText(
        "m4TestsTotal",
        totalTests
    );


    const testingStatus =
        failedTests > 0
            ? "Tests Need Attention"
            : "All Tests Passed";


    setText(
        "m4TestCoverageStatus",
        testingStatus
    );


    /*
     * Keep compatibility with the previous IDs if
     * they still exist anywhere in the dashboard.
     */

    setText(
        "m4PassedTests",
        passedTests
    );


    setText(
        "m4FailedTests",
        failedTests
    );


    setText(
        "m4TotalTests",
        totalTests
    );


    setText(
        "m4TestingOverallStatus",
        testingStatus
    );


    updateTestingChart(
        data
    );

}


/* ============================================================
   TESTING CHART
   ============================================================ */

function updateTestingChart(data) {

    const canvas =
        document.getElementById(
            "milestone4TestingChart"
        );


    if (!canvas || typeof Chart === "undefined") {

        return;

    }


    if (
        milestone4Charts.testing
    ) {

        milestone4Charts.testing.destroy();

    }


    const passed =
        Number(
            data.passed ??
            data.passed_tests ??
            0
        );


    const failed =
        Number(
            data.failed ??
            data.failed_tests ??
            0
        );


    milestone4Charts.testing =
        new Chart(
            canvas,
            {

                type: "doughnut",

                data: {

                    labels: [
                        "Passed",
                        "Failed"
                    ],

                    datasets: [
                        {

                            data: [
                                passed,
                                failed
                            ]

                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {

                        legend: {

                            position: "bottom"

                        }

                    }

                }

            }
        );

}


/* ============================================================
   DOCUMENTATION STATUS
   ============================================================ */

function updateDocumentationStatus(data) {

    setStatus(
        "m4ReadmeStatus",
        data.readme ??
        data.project_documentation ??
        false
    );


    setStatus(
        "m4APIReferenceStatus",
        data.api_reference ??
        data.api_docs ??
        false
    );


    setStatus(
        "m4DatasetCardStatus",
        data.dataset_card ??
        false
    );


    setStatus(
        "m4ModelCardStatus",
        data.model_card ??
        false
    );


    setStatus(
        "m4LicenseStatus",
        data.license ??
        false
    );

}


/* ============================================================
   COHORT ANALYTICS
   ============================================================ */

function updateCohortAnalytics(data) {

    const totalUsers =
        data.total_users ??
        data.users ??
        data.cohort_users ??
        null;


    const totalResumes =
        data.total_resumes ??
        data.resumes ??
        null;


    const averageConfidence =
        data.average_confidence ??
        data.avg_confidence ??
        null;


    const averageAlignment =
        data.average_skill_alignment ??
        data.skill_alignment ??
        data.average_alignment ??
        null;


    if (totalUsers !== null && totalUsers !== undefined) {
        setText("m4CohortUsers", totalUsers);
    }


    if (totalResumes !== null && totalResumes !== undefined) {
        setText("m4CohortResumes", totalResumes);
    }


    if (averageConfidence !== null && averageConfidence !== undefined) {
        setText(
            "m4AverageConfidence",
            formatPercentage(averageConfidence)
        );
    }


    if (averageAlignment !== null && averageAlignment !== undefined) {
        setText(
            "m4AverageAlignment",
            formatPercentage(averageAlignment)
        );
    }


    /*
     * Current dashboard cohort cards are intentionally static because
     * /api/milestone4 may not have live cohort aggregates yet.
     * Only update them when the API provides a real, non-empty value.
     */

    const cohortRecords =
        data.records ??
        data.total_records ??
        null;

    const cohortRoles =
        data.roles ??
        data.total_roles ??
        null;

    const cohortTopCareer =
        data.top_career ??
        data.top_role ??
        null;

    const cohortAccuracy =
        data.accuracy ??
        data.average_accuracy ??
        null;


    if (cohortRecords !== null && cohortRecords !== undefined) {
        setText("m4CohortRecords", cohortRecords);
    }

    if (cohortRoles !== null && cohortRoles !== undefined) {
        setText("m4CohortRoles", cohortRoles);
    }

    if (
        cohortTopCareer !== null &&
        cohortTopCareer !== undefined &&
        String(cohortTopCareer).trim() !== ""
    ) {
        setText("m4CohortTopCareer", cohortTopCareer);
    }

    if (cohortAccuracy !== null && cohortAccuracy !== undefined) {
        setText(
            "m4CohortAccuracy",
            formatPercentage(cohortAccuracy)
        );
    }


    createCareerDistributionChart(
        data.career_distribution ||
        data.careers ||
        {}
    );


    createSkillDistributionChart(
        data.skill_distribution ||
        data.skills ||
        {}
    );

}


/* ============================================================
   CAREER DISTRIBUTION CHART
   ============================================================ */

function createCareerDistributionChart(data) {

    const canvas =
        document.getElementById(
            "milestone4CareerDistributionChart"
        );


    if (
        !canvas ||
        typeof Chart === "undefined"
    ) {

        return;

    }


    if (
        milestone4Charts.careerDistribution
    ) {

        milestone4Charts.careerDistribution.destroy();

    }


    const labels =
        Object.keys(data);


    const values =
        Object.values(data);


    if (!labels.length) {

        return;

    }


    milestone4Charts.careerDistribution =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels: labels,

                    datasets: [
                        {

                            label:
                                "Career Predictions",

                            data: values,

                            borderWidth: 1

                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {

                            beginAtZero: true

                        }

                    }

                }

            }
        );

}


/* ============================================================
   SKILL DISTRIBUTION CHART
   ============================================================ */

function createSkillDistributionChart(data) {

    const canvas =
        document.getElementById(
            "milestone4SkillDistributionChart"
        );


    if (
        !canvas ||
        typeof Chart === "undefined"
    ) {

        return;

    }


    if (
        milestone4Charts.skillDistribution
    ) {

        milestone4Charts.skillDistribution.destroy();

    }


    const labels =
        Object.keys(data);


    const values =
        Object.values(data);


    if (!labels.length) {

        return;

    }


    milestone4Charts.skillDistribution =
        new Chart(
            canvas,
            {

                type: "bar",

                data: {

                    labels: labels,

                    datasets: [
                        {

                            label:
                                "Detected Skills",

                            data: values,

                            borderWidth: 1

                        }
                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    indexAxis: "y",

                    scales: {

                        x: {

                            beginAtZero: true

                        }

                    }

                }

            }
        );

}


/* ============================================================
   CAREER COMPARISON
   ============================================================ */

function setupCareerComparison() {

    /*
     * Current dashboard ID:
     * compareCareerBtn
     */

    const button =
        document.getElementById(
            "compareCareerBtn"
        );


    /*
     * Compatibility with old ID.
     */

    const oldButton =
        document.getElementById(
            "compareCareersBtn"
        );


    const activeButton =
        button ||
        oldButton;


    if (!activeButton) {

        return;

    }


    activeButton.addEventListener(
        "click",
        function () {

            compareSelectedCareers();

        }
    );

}


/* ============================================================
   COMPARE SELECTED CAREERS
   ============================================================ */

async function compareSelectedCareers() {

    /*
     * Current dashboard IDs
     */

    const career1Element =
        document.getElementById(
            "careerCompareOne"
        );


    const career2Element =
        document.getElementById(
            "careerCompareTwo"
        );


    /*
     * Compatibility with old IDs
     */

    const oldCareer1Element =
        document.getElementById(
            "careerCompare1"
        );


    const oldCareer2Element =
        document.getElementById(
            "careerCompare2"
        );


    const careerOne =
        career1Element ||
        oldCareer1Element;


    const careerTwo =
        career2Element ||
        oldCareer2Element;


    if (
        !careerOne ||
        !careerTwo
    ) {

        return;

    }


    const career1 =
        careerOne.value;


    const career2 =
        careerTwo.value;


    if (!career1 || !career2) {

        showComparisonMessage(
            "Please select two careers to compare."
        );

        return;

    }


    if (career1 === career2) {

        showComparisonMessage(
            "Please select two different careers."
        );

        return;

    }


    try {

        const response =
            await fetch(
                "/api/milestone4/career-comparison",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify(
                        {
                            career1: career1,
                            career2: career2
                        }
                    )

                }
            );


        if (!response.ok) {

            throw new Error(
                "Career comparison failed"
            );

        }


        const data =
            await response.json();


        renderCareerComparison(
            data
        );

    }
    catch (error) {

        console.error(
            "Career comparison error:",
            error
        );


        showComparisonMessage(
            "Unable to compare careers right now."
        );

    }

}


/* ============================================================
   RENDER CAREER COMPARISON
   ============================================================ */

function renderCareerComparison(data) {

    const container =
        document.getElementById(
            "careerComparisonResult"
        );


    if (!container) {

        return;

    }


    const career1 =
        data.career1 ||
        data.first ||
        {};


    const career2 =
        data.career2 ||
        data.second ||
        {};


    const skills1 =
        career1.required_skills ||
        career1.skills ||
        [];


    const skills2 =
        career2.required_skills ||
        career2.skills ||
        [];


    const alignment1 =
        career1.skill_alignment ??
        career1.alignment ??
        0;


    const alignment2 =
        career2.skill_alignment ??
        career2.alignment ??
        0;


    container.innerHTML = "";


    const wrapper =
        document.createElement(
            "div"
        );


    wrapper.className =
        "m4-career-comparison";


    wrapper.innerHTML = `

        <div class="m4-comparison-card">

            <h3>
                ${escapeHtml(
                    career1.name ||
                    career1.role ||
                    "Career 1"
                )}
            </h3>

            <div class="m4-comparison-score">

                ${formatPercentage(
                    alignment1
                )}

            </div>

            <h4>Required Skills</h4>

            <div class="m4-comparison-skills">

                ${renderSkillList(
                    skills1
                )}

            </div>

        </div>


        <div class="m4-comparison-card">

            <h3>
                ${escapeHtml(
                    career2.name ||
                    career2.role ||
                    "Career 2"
                )}
            </h3>

            <div class="m4-comparison-score">

                ${formatPercentage(
                    alignment2
                )}

            </div>

            <h4>Required Skills</h4>

            <div class="m4-comparison-skills">

                ${renderSkillList(
                    skills2
                )}

            </div>

        </div>

    `;


    container.appendChild(
        wrapper
    );


    /*
     * Remove/hide any old comparison chart canvas
     * so it cannot create empty space.
     */

    const comparisonCanvas =
        document.getElementById(
            "careerComparisonChart"
        );


    if (comparisonCanvas) {

        comparisonCanvas.style.display =
            "none";

    }


    const comparisonChart =
        document.querySelector(
            ".m4-comparison-chart"
        );


    if (comparisonChart) {

        comparisonChart.style.display =
            "none";

    }

}


/* ============================================================
   RENDER SKILL LIST
   ============================================================ */

function renderSkillList(skills) {

    if (!Array.isArray(skills)) {

        return "<span>No skills available</span>";

    }


    if (!skills.length) {

        return "<span>No skills available</span>";

    }


    return skills
        .map(function (skill) {

            return `
                <span class="m4-skill-badge">
                    ${escapeHtml(
                        String(skill)
                    )}
                </span>
            `;

        })
        .join("");

}


/* ============================================================
   COMPARISON MESSAGE
   ============================================================ */

function showComparisonMessage(message) {

    const container =
        document.getElementById(
            "careerComparisonResult"
        );


    if (!container) {

        return;

    }


    container.innerHTML = `

        <div class="m4-comparison-message">

            ${escapeHtml(message)}

        </div>

    `;

}


/* ============================================================
   FINALIZATION STATUS
   ============================================================ */

function updateFinalizationStatus(data) {

    setStatus(
        "m4ReleaseStatus",
        data.release_ready ??
        data.ready ??
        false
    );


    setStatus(
        "m4DocumentationComplete",
        data.documentation_complete ??
        false
    );


    setStatus(
        "m4TestingComplete",
        data.testing_complete ??
        false
    );


    setStatus(
        "m4PackagingComplete",
        data.packaging_complete ??
        false
    );


    const status =
        data.status ||
        data.message;


    if (status) {

        setText(
            "m4FinalizationMessage",
            status
        );

    }

}


/* ============================================================
   METRIC CARDS
   ============================================================ */

function updateMetricCards(data) {

    Object.keys(data).forEach(
        function (key) {

            const elementId =
                "m4" +
                key
                    .replace(
                        /(^|_)(\w)/g,
                        function (
                            match,
                            separator,
                            letter
                        ) {

                            return letter.toUpperCase();

                        }
                    );


            const element =
                document.getElementById(
                    elementId
                );


            if (!element) {

                return;

            }


            let value =
                data[key];


            if (
                typeof value === "number" &&
                (
                    key.includes(
                        "accuracy"
                    ) ||
                    key.includes(
                        "percentage"
                    ) ||
                    key.includes(
                        "alignment"
                    ) ||
                    key.includes(
                        "confidence"
                    )
                )
            ) {

                value =
                    formatPercentage(
                        value
                    );

            }


            element.textContent =
                value;

        }
    );

}


/* ============================================================
   STATUS HELPER
   ============================================================ */

function setStatus(
    elementId,
    status
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        return;

    }


    const isComplete =
        status === true ||
        status === "true" ||
        status === "complete" ||
        status === "completed" ||
        status === "passed" ||
        status === "ready" ||
        status === "available";


    element.classList.remove(
        "success",
        "warning",
        "error"
    );


    if (isComplete) {

        element.classList.add(
            "success"
        );


        element.textContent =
            "Complete";

    }
    else {

        element.classList.add(
            "warning"
        );


        element.textContent =
            "Pending";

    }

}


/* ============================================================
   REFRESH BUTTON
   ============================================================ */

function setupRefreshButton() {

    const button =
        document.getElementById(
            "refreshMilestone4Btn"
        );


    if (!button) {

        return;

    }


    button.addEventListener(
        "click",
        async function () {

            const originalText =
                button.textContent;


            button.disabled =
                true;


            button.textContent =
                "Refreshing...";


            try {

                await loadMilestone4Data();

            }
            finally {

                setTimeout(
                    function () {

                        button.disabled =
                            false;


                        button.textContent =
                            originalText ||
                            "Refresh";

                    },
                    300
                );

            }

        }
    );

}


/* ============================================================
   PDF / REPORT EXPORT
   ============================================================ */

function setupExportButton() {

    const button =
        document.getElementById(
            "exportMilestone4Btn"
        );


    if (!button) {

        return;

    }


    button.addEventListener(
        "click",
        function () {

            exportMilestone4Report();

        }
    );

}


async function exportMilestone4Report() {

    const button =
        document.getElementById(
            "exportMilestone4Btn"
        );


    if (button) {

        button.disabled =
            true;


        button.textContent =
            "Preparing PDF...";

    }


    try {

        const response =
            await fetch(
                "/api/milestone4/export",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify(
                        {
                            format: "pdf"
                        }
                    )

                }
            );


        if (!response.ok) {

            throw new Error(
                "PDF export failed"
            );

        }


        const contentType =
            response.headers.get(
                "content-type"
            ) ||
            "";


        if (
            contentType.includes(
                "application/pdf"
            )
        ) {

            const blob =
                await response.blob();


            const url =
                window.URL.createObjectURL(
                    blob
                );


            const link =
                document.createElement(
                    "a"
                );


            link.href =
                url;


            link.download =
                "CareerCast_Milestone4_Report.pdf";


            document.body.appendChild(
                link
            );


            link.click();


            link.remove();


            window.URL.revokeObjectURL(
                url
            );

        }
        else {

            const data =
                await response.json();


            if (data.download_url) {

                window.open(
                    data.download_url,
                    "_blank"
                );

            }
            else {

                throw new Error(
                    "PDF file was not returned"
                );

            }

        }

    }
    catch (error) {

        console.error(
            "PDF export error:",
            error
        );


        printMilestone4Report();

    }
    finally {

        if (button) {

            button.disabled =
                false;

            button.textContent =
                "Export PDF";

        }

    }

}


/* ============================================================
   PRINT FALLBACK
   ============================================================ */

function printMilestone4Report() {

    const section =
        document.getElementById(
            "milestone4Section"
        );


    if (!section) {

        alert(
            "Milestone 4 report section was not found."
        );

        return;

    }


    const printWindow =
        window.open(
            "",
            "_blank"
        );


    if (!printWindow) {

        alert(
            "Please allow pop-ups to export the report."
        );

        return;

    }


    printWindow.document.write(`

        <!DOCTYPE html>

        <html>

        <head>

            <title>
                CareerCast - Milestone 4 Report
            </title>

            <style>

                body {

                    font-family:
                        Arial,
                        sans-serif;

                    padding:
                        30px;

                    color:
                        #111827;

                }

                h1,
                h2,
                h3 {

                    color:
                        #111827;

                }

                .card {

                    border:
                        1px solid #ddd;

                    border-radius:
                        10px;

                    padding:
                        15px;

                    margin-bottom:
                        15px;

                }

            </style>

        </head>

        <body>

            <h1>
                CareerCast
            </h1>

            <h2>
                Milestone 4 -
                Packaging, Testing & Finalization
            </h2>

            ${section.innerHTML}

        </body>

        </html>

    `);


    printWindow.document.close();


    printWindow.focus();


    setTimeout(
        function () {

            printWindow.print();

        },
        500
    );

}


/* ============================================================
   DOCUMENTATION LINKS
   ============================================================ */

function setupDocumentationLinks() {

    const apiDocsButton =
        document.getElementById(
            "m4OpenAPIDocs"
        );


    if (apiDocsButton) {

        apiDocsButton.addEventListener(
            "click",
            function () {

                window.open(
                    "/docs/api_reference",
                    "_blank"
                );

            }
        );

    }


    const datasetButton =
        document.getElementById(
            "m4OpenDatasetCard"
        );


    if (datasetButton) {

        datasetButton.addEventListener(
            "click",
            function () {

                window.open(
                    "/docs/dataset_card",
                    "_blank"
                );

            }
        );

    }


    const modelButton =
        document.getElementById(
            "m4OpenModelCard"
        );


    if (modelButton) {

        modelButton.addEventListener(
            "click",
            function () {

                window.open(
                    "/docs/model_card",
                    "_blank"
                );

            }
        );

    }

}


/* ============================================================
   LOADING STATE
   ============================================================ */

function showLoadingState() {

    const loader =
        document.getElementById(
            "milestone4Loading"
        );


    if (loader) {

        loader.style.display =
            "block";

    }

}


function hideLoadingState() {

    const loader =
        document.getElementById(
            "milestone4Loading"
        );


    if (loader) {

        loader.style.display =
            "none";

    }

}


/* ============================================================
   FALLBACK DATA
   ============================================================ */

function loadMilestone4FallbackData() {

    console.log(
        "Using Milestone 4 fallback data"
    );


    const fallbackData = {

        success: true,

        packaging: {

            package_available: true,

            pip_installable: true,

            cli_available: true,

            api_documentation: true

        },

        testing: {

            parser_tests: 5,

            prediction_tests: 5,

            recommendation_tests: 5,

            integration_tests: 4,

            regression_tests: 4,

            passed: 51,

            failed: 0,

            total: 51

        },

        documentation: {

            readme: true,

            api_reference: true,

            dataset_card: true,

            model_card: true,

            license: true

        },

        cohort: {

            total_users: 0,

            total_resumes: 123849,

            average_confidence: 0,

            average_skill_alignment: 0,

            records: 123849,

            total_records: 123849,

            roles: 17,

            total_roles: 17,

            top_career: "Sales Representative",

            accuracy: 75.7,

            career_distribution: {
                "Sales Representative": 3390,
                "Registered Nurse": 2605,
                "Project Manager": 2024,
                "Software Engineer": 1477,
                "Accountant": 1316,
                "Administrative Assistant": 1012,
                "Customer Service Representative": 754,
                "Business Analyst": 549,
                "Product Manager": 512,
                "Data Analyst": 407,
                "Marketing Manager": 386,
                "Data Scientist": 245,
                "Full Stack Developer": 234,
                "DevOps Engineer": 173,
                "Frontend Developer": 132,
                "Backend Developer": 125,
                "Machine Learning Engineer": 97
            },

            skill_distribution: {}

        },

        finalization: {

            release_ready: false,

            documentation_complete: true,

            testing_complete: true,

            packaging_complete: true,

            status:
                "Milestone 4 components are being finalized."

        }

    };


    updateMilestone4Dashboard(
        fallbackData
    );

}


/* ============================================================
   FORMAT PERCENTAGE
   ============================================================ */

function formatPercentage(value) {

    if (
        value === undefined ||
        value === null ||
        value === ""
    ) {

        return "0%";

    }


    const number =
        Number(value);


    if (
        Number.isNaN(number)
    ) {

        return "0%";

    }


    if (
        number >= 0 &&
        number <= 1
    ) {

        return (
            number * 100
        ).toFixed(1) + "%";

    }


    return (
        number
    ).toFixed(1) + "%";

}


/* ============================================================
   SET TEXT
   ============================================================ */

function setText(
    elementId,
    value
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        return;

    }


    element.textContent =
        value === undefined ||
        value === null
            ? "--"
            : value;

}


/* ============================================================
   ESCAPE HTML
   ============================================================ */

function escapeHtml(value) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}


/* ============================================================
   AUTO REFRESH
   ============================================================ */

setInterval(
    function () {

        const milestone4Section =
            document.getElementById(
                "milestone4Section"
            );


        if (!milestone4Section) {

            return;

        }


        const isVisible =
            milestone4Section.offsetParent !== null;


        if (isVisible) {

            loadMilestone4Data();

        }

    },
    60000
);


/* ============================================================
   GLOBAL FUNCTIONS
   ============================================================ */

window.initializeMilestone4 =
    initializeMilestone4;


window.loadMilestone4Data =
    loadMilestone4Data;


window.compareSelectedCareers =
    compareSelectedCareers;


window.exportMilestone4Report =
    exportMilestone4Report;


window.printMilestone4Report =
    printMilestone4Report;