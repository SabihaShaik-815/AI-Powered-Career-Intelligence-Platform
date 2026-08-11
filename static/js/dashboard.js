/* =========================================================
   CAREERCAST DASHBOARD JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("CareerCast dashboard.js loaded");

    /* =====================================================
       TAB SWITCHING
       ===================================================== */

    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanels = document.querySelectorAll(".tab-panel");

    function openTab(tabName) {

        console.log("Opening tab:", tabName);

        tabButtons.forEach(function (button) {
            button.classList.remove("active");
        });

        tabPanels.forEach(function (panel) {
            panel.classList.remove("active");
        });

        const selectedButton = document.querySelector(
            '.tab-btn[data-tab="' + tabName + '"]'
        );

        if (selectedButton) {
            selectedButton.classList.add("active");
        }

        const selectedPanel = document.getElementById(
            "tab-" + tabName
        );

        if (selectedPanel) {
            selectedPanel.classList.add("active");
        }

        /* Milestone 2 */
        if (
            tabName === "analytics" &&
            typeof initializeMilestone2 === "function"
        ) {
            setTimeout(function () {
                initializeMilestone2();
            }, 100);
        }
    }

    tabButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const tabName =
                button.getAttribute("data-tab");

            openTab(tabName);

        });

    });


    /* =====================================================
       RESUME UPLOAD / DROPZONE
       ===================================================== */

    const dropzone =
        document.getElementById("dropzone");

    const resumeFile =
        document.getElementById("resumeFile");


    if (dropzone && resumeFile) {

        console.log("Upload system initialized");


        /* Click dropzone */

        dropzone.addEventListener(
            "click",
            function (event) {

                /*
                 * Prevent clicking the selected-file
                 * text from opening the file picker again.
                 */

                if (
                    event.target.closest(".selected-file")
                ) {
                    return;
                }

                resumeFile.click();

            }
        );


        /* File selected */

        resumeFile.addEventListener(
            "change",
            function () {

                if (resumeFile.files.length > 0) {

                    const file =
                        resumeFile.files[0];

                    console.log(
                        "Selected file:",
                        file.name
                    );

                    showFileName(file);
                }

            }
        );


        /* Drag over */

        dropzone.addEventListener(
            "dragover",
            function (event) {

                event.preventDefault();

                dropzone.classList.add("dragover");

            }
        );


        /* Drag leave */

        dropzone.addEventListener(
            "dragleave",
            function () {

                dropzone.classList.remove(
                    "dragover"
                );

            }
        );


        /* Drop */

        dropzone.addEventListener(
            "drop",
            function (event) {

                event.preventDefault();

                dropzone.classList.remove(
                    "dragover"
                );

                const files =
                    event.dataTransfer.files;

                if (files.length > 0) {

                    const file = files[0];

                    console.log(
                        "Dropped file:",
                        file.name
                    );

                    try {

                        const dataTransfer =
                            new DataTransfer();

                        dataTransfer.items.add(file);

                        resumeFile.files =
                            dataTransfer.files;

                    }
                    catch (error) {

                        console.error(
                            "Could not assign dropped file:",
                            error
                        );

                    }

                    showFileName(file);
                }

            }
        );

    }


    /* =====================================================
       SHOW SELECTED FILE
       ===================================================== */

    function showFileName(file) {

        if (!dropzone) {
            return;
        }

        const oldMessage =
            dropzone.querySelector(
                ".selected-file"
            );

        if (oldMessage) {
            oldMessage.remove();
        }

        const fileMessage =
            document.createElement("p");

        fileMessage.className =
            "selected-file";

        fileMessage.innerHTML =
            "Selected: <strong>" +
            escapeHtml(file.name) +
            "</strong>";

        dropzone.appendChild(
            fileMessage
        );

    }


    /* =====================================================
       ANALYZE BUTTON
       ===================================================== */

    const analyzeButton =
        document.getElementById(
            "analyzeBtn"
        );


    if (analyzeButton) {

        analyzeButton.addEventListener(
            "click",
            function () {

                analyzeResume();

            }
        );

    }


    /* =====================================================
       ANALYZE RESUME
       ===================================================== */

    function analyzeResume() {

        const fileInput =
            document.getElementById(
                "resumeFile"
            );

        const textInput =
            document.getElementById(
                "resumeText"
            );

        const status =
            document.getElementById(
                "analyzeStatus"
            );


        const file =
            fileInput &&
            fileInput.files.length > 0
                ? fileInput.files[0]
                : null;


        const text =
            textInput
                ? textInput.value.trim()
                : "";


        /* Nothing entered */

        if (!file && !text) {

            setStatus(
                status,
                "Please upload a resume or paste resume text.",
                "error"
            );

            return;
        }


        setStatus(
            status,
            "Analyzing resume...",
            ""
        );


        if (analyzeButton) {
            analyzeButton.disabled = true;
        }


        /* =================================================
           IMPORTANT FLASK CONNECTION

           Flask route:

           POST /api/analyze

           Flask expects:

           resume_file
           text
           ================================================= */


        const formData =
            new FormData();


        if (file) {

            formData.append(
                "resume_file",
                file
            );

        }


        if (text) {

            formData.append(
                "text",
                text
            );

        }


        console.log(
            "Sending resume to /api/analyze"
        );


        fetch(
            "/api/analyze",
            {
                method: "POST",
                body: formData
            }
        )

        .then(function (response) {

            console.log(
                "API status:",
                response.status
            );


            if (!response.ok) {

                return response.json()
                    .then(function (errorData) {

                        throw new Error(
                            errorData.error ||
                            "Server returned " +
                            response.status
                        );

                    })
                    .catch(function () {

                        throw new Error(
                            "Server returned " +
                            response.status
                        );

                    });

            }


            return response.json();

        })


        .then(function (data) {

            console.log(
                "Analysis response:",
                data
            );


            displayResults(data);


            setStatus(
                status,
                "Resume analyzed successfully.",
                "success"
            );


            /* Open Results tab */

            openTab("results");

        })


        .catch(function (error) {

            console.error(
                "Analysis error:",
                error
            );


            setStatus(
                status,
                error.message ||
                "Unable to analyze resume.",
                "error"
            );

        })


        .finally(function () {

            if (analyzeButton) {
                analyzeButton.disabled = false;
            }

        });

    }


    /* =====================================================
       DISPLAY RESULTS
       ===================================================== */

    function displayResults(data) {

        console.log(
            "Displaying results:",
            data
        );


        const noResults =
            document.getElementById(
                "noResults"
            );


        const resultsGrid =
            document.getElementById(
                "resultsGrid"
            );


        if (noResults) {

            noResults.style.display =
                "none";

        }


        if (resultsGrid) {

            resultsGrid.style.display =
                "grid";

        }


        /* =================================================
           PARSED / HIGHLIGHTED TEXT
           ================================================= */

        const parsedText =
            document.getElementById(
                "parsedText"
            );


        if (parsedText) {

            /*
             * Flask returns highlighted_html.
             * Use innerHTML so highlighted skills
             * appear correctly.
             */

            if (data.highlighted_html) {

                parsedText.innerHTML =
                    data.highlighted_html;

            }
            else {

                parsedText.textContent =
                    "No parsed text available.";

            }

        }


        /* =================================================
           SKILLS
           ================================================= */

        const skillBadges =
            document.getElementById(
                "skillBadges"
            );


        if (skillBadges) {

            skillBadges.innerHTML = "";


            const skills =
                data.skills || [];


            if (skills.length === 0) {

                skillBadges.innerHTML =
                    "<span>No skills detected.</span>";

            }


            skills.forEach(function (skill) {

                const badge =
                    document.createElement(
                        "span"
                    );

                badge.className =
                    "badge";

                badge.textContent =
                    skill;

                skillBadges.appendChild(
                    badge
                );

            });

        }


        /* =================================================
           EDUCATION
           ================================================= */

        const educationList =
            document.getElementById(
                "educationList"
            );


        if (educationList) {

            educationList.innerHTML = "";


            const education =
                data.education || [];


            if (education.length === 0) {

                const li =
                    document.createElement(
                        "li"
                    );

                li.textContent =
                    "No education information detected.";

                educationList.appendChild(
                    li
                );

            }


            education.forEach(
                function (item) {

                    const li =
                        document.createElement(
                            "li"
                        );


                    if (
                        typeof item ===
                        "object"
                    ) {

                        li.textContent =
                            item.degree +
                            (
                                item.institution
                                    ? " - " +
                                      item.institution
                                    : ""
                            );

                    }
                    else {

                        li.textContent =
                            item;

                    }


                    educationList.appendChild(
                        li
                    );

                }
            );

        }


        /* =================================================
           BEST ROLE
           ================================================= */

        const bestRole =
            document.getElementById(
                "bestRole"
            );


        if (bestRole) {

            /*
             * Flask returns top_role.
             */

            bestRole.textContent =
                data.top_role ||
                "Not available";

        }


        /* =================================================
           BEST CONFIDENCE
           ================================================= */

        const bestConf =
            document.getElementById(
                "bestConf"
            );


        if (bestConf) {

            let confidence = 0;


            /*
             * Flask returns predictions:
             *
             * [
             *   {
             *      role: "...",
             *      confidence: 0.XX
             *   }
             * ]
             */

            if (
                data.predictions &&
                data.predictions.length > 0
            ) {

                confidence =
                    Number(
                        data.predictions[0]
                            .confidence || 0
                    );

            }


            if (confidence <= 1) {

                confidence =
                    confidence * 100;

            }


            bestConf.textContent =
                confidence.toFixed(2) +
                "% confidence";

        }


        /* =================================================
           PREDICTION BARS
           ================================================= */

        displayPredictionBars(
            data.predictions || []
        );


        /* =================================================
           SKILL GAP
           ================================================= */

        displaySkillGap(data);

    }


    /* =====================================================
       PREDICTION BARS
       ===================================================== */

    function displayPredictionBars(
        predictions
    ) {

        const container =
            document.getElementById(
                "predictionBars"
            );


        if (!container) {
            return;
        }


        container.innerHTML = "";


        if (
            !Array.isArray(predictions) ||
            predictions.length === 0
        ) {

            container.innerHTML =
                "<p>No career predictions available.</p>";

            return;

        }


        predictions.forEach(
            function (prediction) {

                const role =
                    prediction.role ||
                    "Career";


                let confidence =
                    Number(
                        prediction.confidence || 0
                    );


                if (confidence <= 1) {

                    confidence =
                        confidence * 100;

                }


                /* Keep percentage between 0 and 100 */

                confidence =
                    Math.max(
                        0,
                        Math.min(
                            100,
                            confidence
                        )
                    );


                const row =
                    document.createElement(
                        "div"
                    );


                row.className =
                    "bar-row";


                row.innerHTML =
                    '<div class="bar-label">' +
                        '<span>' +
                            escapeHtml(role) +
                        '</span>' +
                        '<span>' +
                            confidence.toFixed(1) +
                            '%' +
                        '</span>' +
                    '</div>' +

                    '<div class="bar-track">' +

                        '<div ' +
                        'class="bar-fill" ' +
                        'style="width:' +
                        confidence +
                        '%">' +
                        '</div>' +

                    '</div>';


                container.appendChild(
                    row
                );

            }
        );

    }


    /* =====================================================
       SKILL GAP
       ===================================================== */

    function displaySkillGap(data) {

        const card =
            document.getElementById(
                "skillGapCard"
            );


        if (!card) {
            return;
        }


        /*
         * Flask returns:
         *
         * skill_gap: {
         *    matched: [],
         *    missing: []
         * }
         */

        const gap =
            data.skill_gap || {};


        const matched =
            gap.matched || [];


        const missing =
            gap.missing || [];


        if (
            matched.length === 0 &&
            missing.length === 0
        ) {

            card.style.display =
                "none";

            return;

        }


        card.style.display =
            "block";


        /* =================================================
           ROLE NAME
           ================================================= */

        const skillGapRole =
            document.getElementById(
                "skillGapRole"
            );


        if (skillGapRole) {

            skillGapRole.textContent =
                data.top_role
                    ? " - " + data.top_role
                    : "";

        }


        /* =================================================
           MATCHED
           ================================================= */

        const matchedContainer =
            document.getElementById(
                "matchedBadges"
            );


        if (matchedContainer) {

            matchedContainer.innerHTML =
                "";


            matched.forEach(
                function (skill) {

                    const badge =
                        document.createElement(
                            "span"
                        );


                    badge.className =
                        "badge";


                    badge.textContent =
                        skill;


                    matchedContainer.appendChild(
                        badge
                    );

                }
            );

        }


        /* =================================================
           MISSING
           ================================================= */

        const missingContainer =
            document.getElementById(
                "missingBadges"
            );


        if (missingContainer) {

            missingContainer.innerHTML =
                "";


            missing.forEach(
                function (skill) {

                    const badge =
                        document.createElement(
                            "span"
                        );


                    badge.className =
                        "badge-missing";


                    badge.textContent =
                        skill;


                    missingContainer.appendChild(
                        badge
                    );

                }
            );

        }

    }


    /* =====================================================
       PROFILE FORM
       ===================================================== */

    const profileForm =
        document.getElementById(
            "profileForm"
        );


    if (profileForm) {

        profileForm.addEventListener(
            "submit",
            function (event) {

                event.preventDefault();


                const status =
                    document.getElementById(
                        "profileStatus"
                    );


                const skillsText =
                    document.getElementById(
                        "pf_skills"
                    ).value;


                const skills =
                    skillsText
                        .split(",")
                        .map(function (skill) {

                            return skill.trim();

                        })
                        .filter(function (skill) {

                            return skill.length > 0;

                        });


                const profileData = {

                    name:
                        document.getElementById(
                            "pf_name"
                        ).value.trim(),

                    email:
                        document.getElementById(
                            "pf_email"
                        ).value.trim(),

                    years_experience:
                        document.getElementById(
                            "pf_years"
                        ).value,

                    education_level:
                        document.getElementById(
                            "pf_education"
                        ).value,

                    skills:
                        skills,

                    current_role:
                        document.getElementById(
                            "pf_current_role"
                        ).value.trim(),

                    desired_role:
                        document.getElementById(
                            "pf_desired_role"
                        ).value.trim(),

                    location:
                        document.getElementById(
                            "pf_location"
                        ).value.trim()

                };


                console.log(
                    "Saving profile:",
                    profileData
                );


                setStatus(
                    status,
                    "Saving profile...",
                    ""
                );


                fetch(
                    "/api/profile",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                profileData
                            )
                    }
                )


                .then(function (response) {

                    return response.json()
                        .then(function (result) {

                            if (!response.ok) {

                                throw new Error(
                                    result.errors
                                        ? result.errors.join(", ")
                                        : "Could not save profile."
                                );

                            }

                            return result;

                        });

                })


                .then(function (result) {

                    console.log(
                        "Profile saved:",
                        result
                    );


                    setStatus(
                        status,
                        "Profile saved successfully.",
                        "success"
                    );

                })


                .catch(function (error) {

                    console.error(
                        "Profile error:",
                        error
                    );


                    setStatus(
                        status,
                        error.message ||
                        "Could not save profile.",
                        "error"
                    );

                });

            }
        );

    }


    /* =====================================================
       LOAD SAVED PROFILE
       ===================================================== */

    function loadProfile() {

        fetch("/api/profile")

            .then(function (response) {

                if (!response.ok) {
                    throw new Error(
                        "Could not load profile."
                    );
                }

                return response.json();

            })

            .then(function (data) {

                console.log(
                    "Loaded profile:",
                    data
                );


                if (!data || !data.name) {
                    return;
                }


                const name =
                    document.getElementById(
                        "pf_name"
                    );

                const email =
                    document.getElementById(
                        "pf_email"
                    );

                const years =
                    document.getElementById(
                        "pf_years"
                    );

                const education =
                    document.getElementById(
                        "pf_education"
                    );

                const skills =
                    document.getElementById(
                        "pf_skills"
                    );

                const currentRole =
                    document.getElementById(
                        "pf_current_role"
                    );

                const desiredRole =
                    document.getElementById(
                        "pf_desired_role"
                    );

                const location =
                    document.getElementById(
                        "pf_location"
                    );


                if (name) {
                    name.value =
                        data.name || "";
                }

                if (email) {
                    email.value =
                        data.email || "";
                }

                if (years) {
                    years.value =
                        data.years_experience || "";
                }

                if (education) {
                    education.value =
                        data.education_level || "";
                }

                if (skills) {
                    skills.value =
                        Array.isArray(data.skills)
                            ? data.skills.join(", ")
                            : "";
                }

                if (currentRole) {
                    currentRole.value =
                        data.current_role || "";
                }

                if (desiredRole) {
                    desiredRole.value =
                        data.desired_role || "";
                }

                if (location) {
                    location.value =
                        data.location || "";
                }

            })

            .catch(function (error) {

                console.log(
                    "Profile loading:",
                    error.message
                );

            });

    }


    /* =====================================================
       STATUS MESSAGE
       ===================================================== */

    function setStatus(
        element,
        message,
        type
    ) {

        if (!element) {
            return;
        }


        element.textContent =
            message;


        element.className =
            "status-msg";


        if (type) {

            element.classList.add(
                type
            );

        }

    }


    /* =====================================================
       HTML ESCAPE
       ===================================================== */

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


    /* =====================================================
       OPEN UPLOAD TAB
       ===================================================== */

    openTab("upload");


    /* =====================================================
       LOAD PROFILE
       ===================================================== */

    loadProfile();


    console.log(
        "CareerCast dashboard initialized successfully."
    );

});
