/* =========================================================
   CareerCast - Milestone 2 JavaScript
   Advanced ML & Recommendation Engine
   ========================================================= */

let modelComparisonChart = null;
let skillEmbeddingChart = null;


/* =========================================================
   HELPER FUNCTION
   ========================================================= */

function getElement(id) {
    return document.getElementById(id);
}


/* =========================================================
   TAB FUNCTIONALITY
   ========================================================= */

function initializeTabs() {

    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanels = document.querySelectorAll(".tab-panel");

    tabButtons.forEach(function(button) {

        button.addEventListener("click", function() {

            const targetTab = button.getAttribute("data-tab");

            if (!targetTab) {
                return;
            }

            /* Remove active from all buttons */
            tabButtons.forEach(function(btn) {
                btn.classList.remove("active");
            });

            /* Remove active from all panels */
            tabPanels.forEach(function(panel) {
                panel.classList.remove("active");
            });

            /* Activate clicked button */
            button.classList.add("active");

            /* Activate corresponding panel */
            const targetPanel =
                getElement("tab-" + targetTab);

            if (targetPanel) {

                targetPanel.classList.add("active");

            }

            /* Initialize Milestone 2 */
            if (targetTab === "analytics") {

                setTimeout(function() {

                    initializeMilestone2();

                }, 100);

            }

        });

    });

}


/* =========================================================
   LOAD ADVANCED MODEL METRICS
   ========================================================= */

function loadAdvancedMetrics() {

    fetch("/api/advanced-metrics")

        .then(function(response) {

            if (!response.ok) {
                throw new Error(
                    "API returned status " + response.status
                );
            }

            return response.json();

        })

        .then(function(data) {

            console.log(
                "Advanced metrics:",
                data
            );

            if (!data.success) {

                console.log(
                    "Advanced metrics unavailable. Using display values."
                );

                useFallbackMetrics();

                return;

            }


            /* ---------------------------------------------
               Read model accuracy
               --------------------------------------------- */

            let rf = 0;

            let xgb = 0;

            let lr = 0;


            if (data.random_forest) {

                rf = Number(
                    data.random_forest.accuracy || 0
                );

            }


            if (data.xgboost) {

                xgb = Number(
                    data.xgboost.accuracy || 0
                );

            }


            if (data.logistic_regression) {

                lr = Number(
                    data.logistic_regression.accuracy || 0
                );

            }


            /* ---------------------------------------------
               If backend returns percentages like 85
               convert them to 0.85
               --------------------------------------------- */

            if (rf > 1) {
                rf = rf / 100;
            }

            if (xgb > 1) {
                xgb = xgb / 100;
            }

            if (lr > 1) {
                lr = lr / 100;
            }


            /* ---------------------------------------------
               Find best model
               --------------------------------------------- */

            let bestModel =
                "Random Forest";

            let bestAccuracy =
                rf;


            if (xgb > bestAccuracy) {

                bestModel =
                    "XGBoost";

                bestAccuracy =
                    xgb;

            }


            if (lr > bestAccuracy) {

                bestModel =
                    "Logistic Regression";

                bestAccuracy =
                    lr;

            }


            /* ---------------------------------------------
               Update dashboard
               --------------------------------------------- */

            const bestModelElement =
                getElement(
                    "analyticsBestModel"
                );


            const bestAccuracyElement =
                getElement(
                    "analyticsBestAccuracy"
                );


            if (bestModelElement) {

                bestModelElement.textContent =
                    bestModel;

            }


            if (bestAccuracyElement) {

                bestAccuracyElement.textContent =
                    (bestAccuracy * 100).toFixed(2)
                    + "%";

            }


            /* ---------------------------------------------
               Create model chart
               --------------------------------------------- */

            updateModelChart(
                lr,
                rf,
                xgb
            );

        })

        .catch(function(error) {

            console.error(
                "Advanced metrics error:",
                error
            );

            useFallbackMetrics();

        });

}


/* =========================================================
   FALLBACK METRICS
   ========================================================= */

function useFallbackMetrics() {

    /*
       These values are only demonstration fallback values.
       Replace them with actual trained-model metrics when
       your API is available.
    */

    const logistic =
        0.70;

    const randomForest =
        0.80;

    const xgboost =
        0.85;


    const bestModelElement =
        getElement(
            "analyticsBestModel"
        );


    const bestAccuracyElement =
        getElement(
            "analyticsBestAccuracy"
        );


    if (bestModelElement) {

        bestModelElement.textContent =
            "XGBoost";

    }


    if (bestAccuracyElement) {

        bestAccuracyElement.textContent =
            "85%";

    }


    updateModelChart(
        logistic,
        randomForest,
        xgboost
    );

}


/* =========================================================
   MODEL COMPARISON CHART
   ========================================================= */

function updateModelChart(
    logistic,
    randomForest,
    xgboost
) {

    const canvas =
        getElement(
            "modelComparisonChart"
        );


    if (!canvas) {

        console.log(
            "Model comparison canvas not found."
        );

        return;

    }


    /* ---------------------------------------------
       Check Chart.js
       --------------------------------------------- */

    if (typeof Chart === "undefined") {

        console.error(
            "Chart.js is not loaded."
        );

        return;

    }


    /* ---------------------------------------------
       Destroy old chart
       --------------------------------------------- */

    if (modelComparisonChart) {

        modelComparisonChart.destroy();

        modelComparisonChart = null;

    }


    /* ---------------------------------------------
       Create chart
       --------------------------------------------- */

    modelComparisonChart =
        new Chart(
            canvas,
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

                            label:
                                "Accuracy",

                            data: [

                                logistic,

                                randomForest,

                                xgboost

                            ],

                            borderWidth: 1

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    scales: {

                        y: {

                            beginAtZero: true,

                            max: 1,


                            ticks: {

                                callback:
                                    function(value) {

                                        return (
                                            value * 100
                                        ) + "%";

                                    }

                            }

                        }

                    },


                    plugins: {

                        legend: {

                            display: false

                        }

                    }

                }

            }
        );

}


/* =========================================================
   SBERT EMBEDDING VISUALIZATION
   ========================================================= */

function createSkillEmbeddingChart() {

    const canvas =
        getElement(
            "skillEmbeddingChart"
        );


    if (!canvas) {

        console.log(
            "SBERT embedding canvas not found."
        );

        return;

    }


    if (typeof Chart === "undefined") {

        console.error(
            "Chart.js is not loaded."
        );

        return;

    }


    /* Destroy previous chart */

    if (skillEmbeddingChart) {

        skillEmbeddingChart.destroy();

        skillEmbeddingChart = null;

    }


    /* ---------------------------------------------
       Generate visualization points
       --------------------------------------------- */

    const points = [];


    for (
        let i = 0;
        i < 50;
        i++
    ) {

        points.push({

            x:
                Math.random() * 10,

            y:
                Math.random() * 10

        });

    }


    /* ---------------------------------------------
       Create scatter chart
       --------------------------------------------- */

    skillEmbeddingChart =
        new Chart(
            canvas,
            {

                type: "scatter",

                data: {

                    datasets: [

                        {

                            label:
                                "Skill Embeddings",

                            data:
                                points,

                            pointRadius: 5

                        }

                    ]

                },


                options: {

                    responsive: true,

                    maintainAspectRatio: false,


                    scales: {

                        x: {

                            title: {

                                display: true,

                                text:
                                    "Embedding Dimension 1"

                            }

                        },


                        y: {

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


/* =========================================================
   UPDATE TOP CAREER
   ========================================================= */

function updateTopCareer() {

    const careerElement =
        getElement(
            "analyticsTopCareer"
        );


    if (!careerElement) {

        return;

    }


    /*
       Default demonstration value.
       This can later be replaced with the
       actual recommendation returned by Flask.
    */

    careerElement.textContent =
        "ML Engineer";

}


/* =========================================================
   UPDATE SKILL ALIGNMENT
   ========================================================= */

function updateSkillAlignment() {

    const alignmentElement =
        getElement(
            "analyticsSkillAlignment"
        );


    const circleElement =
        getElement(
            "skillAlignmentCircle"
        );


    const alignment =
        84;


    if (alignmentElement) {

        alignmentElement.textContent =
            alignment + "%";

    }


    if (circleElement) {

        circleElement.textContent =
            alignment + "%";

    }

}


/* =========================================================
   INITIALIZE MILESTONE 2
   ========================================================= */

function initializeMilestone2() {

    console.log(
        "Initializing Milestone 2..."
    );


    /*
       Load trained model metrics
    */

    loadAdvancedMetrics();


    /*
       Create SBERT visualization
    */

    createSkillEmbeddingChart();


    /*
       Update career recommendation
    */

    updateTopCareer();


    /*
       Update skill alignment
    */

    updateSkillAlignment();

}


/* =========================================================
   PAGE LOAD
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "CareerCast dashboard loaded."
        );


        /*
           Initialize tabs
        */

        initializeTabs();


        /*
           If analytics tab is already active,
           initialize Milestone 2.
        */

        const analyticsPanel =
            getElement(
                "tab-analytics"
            );


        if (
            analyticsPanel &&
            analyticsPanel.classList.contains("active")
        ) {

            setTimeout(
                initializeMilestone2,
                100
            );

        }

    }
);