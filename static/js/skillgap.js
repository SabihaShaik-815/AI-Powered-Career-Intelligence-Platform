/* =========================================================
   SKILL GAP ANALYSIS
   static/js/skillgap.js
   ========================================================= */

let latestSkillGapData = null;


/* =========================================================
   LOAD DATA FROM SESSION STORAGE
   ========================================================= */

function loadSkillGapFromStorage() {

    try {

        const savedData =
            sessionStorage.getItem(
                "latestSkillGapData"
            );

        if (savedData) {

            latestSkillGapData =
                JSON.parse(savedData);

            console.log(
                "Skill Gap Data Loaded:",
                latestSkillGapData
            );

            renderSkillGapTab();

        } else {

            showNoResumeMessage();

        }

    } catch (error) {

        console.error(
            "Could not load Skill Gap data:",
            error
        );

        showNoResumeMessage();

    }

}


/* =========================================================
   SHOW EMPTY STATE
   ========================================================= */

function showNoResumeMessage() {

    const emptyState =
        document.getElementById(
            "sgEmptyState"
        );

    const content =
        document.getElementById(
            "sgContent"
        );


    if (emptyState) {

        emptyState.style.display =
            "block";

    }


    if (content) {

        content.style.display =
            "none";

    }

}


/* =========================================================
   RENDER SKILL GAP TAB
   ========================================================= */

function renderSkillGapTab() {

    if (!latestSkillGapData) {

        showNoResumeMessage();

        return;

    }


    const emptyState =
        document.getElementById(
            "sgEmptyState"
        );

    const content =
        document.getElementById(
            "sgContent"
        );


    if (emptyState) {

        emptyState.style.display =
            "none";

    }


    if (content) {

        content.style.display =
            "block";

    }


    renderSkillGapStatistics();

    renderSkillAlignment();

    renderMatchedSkills();

    renderMissingSkills();

    renderRequiredSkills();

    renderLearningPath();

    renderTopRoles();

}


/* =========================================================
   STATISTICS
   ========================================================= */

function renderSkillGapStatistics() {

    const data =
        latestSkillGapData;


    const targetRole =
        document.getElementById(
            "sgTargetRole"
        );

    const alignment =
        document.getElementById(
            "sgAlignment"
        );

    const matchedCount =
        document.getElementById(
            "sgMatchedCount"
        );

    const missingCount =
        document.getElementById(
            "sgMissingCount"
        );


    const role =
        data.top_role ||
        data.target_role ||
        data.targetRole ||
        data.predicted_career ||
        data.best_role ||
        "Not Available";


    const alignmentValue =
        Number(
            data.alignment ??
            data.skill_alignment ??
            data.skillAlignment ??
            0
        );


    const matched =
        data.your_skills ||
        data.matched_skills ||
        data.matchedSkills ||
        [];


    const missing =
        data.missing_skills ||
        data.missingSkills ||
        [];


    if (targetRole) {

        targetRole.textContent =
            role;

    }


    if (alignment) {

        alignment.textContent =
            `${Math.round(
                alignmentValue
            )}%`;

    }


    if (matchedCount) {

        matchedCount.textContent =
            matched.length;

    }


    if (missingCount) {

        missingCount.textContent =
            missing.length;

    }

}


/* =========================================================
   ALIGNMENT PROGRESS
   ========================================================= */

function renderSkillAlignment() {

    const data =
        latestSkillGapData;


    const progressBar =
        document.getElementById(
            "sgProgressBar"
        );


    const alignment =
        Number(
            data.alignment ??
            data.skill_alignment ??
            data.skillAlignment ??
            0
        );


    const safeValue =
        Math.max(
            0,
            Math.min(
                100,
                alignment
            )
        );


    if (progressBar) {

        progressBar.style.width =
            `${safeValue}%`;

    }

}


/* =========================================================
   MATCHED SKILLS
   ========================================================= */

function renderMatchedSkills() {

    const container =
        document.getElementById(
            "sgMatchedSkills"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const skills =
        latestSkillGapData.your_skills ||
        latestSkillGapData.matched_skills ||
        latestSkillGapData.matchedSkills ||
        [];


    if (!skills.length) {

        container.innerHTML =
            `
            <p class="sg-empty-message">
                No matched skills detected.
            </p>
            `;

        return;

    }


    skills.forEach(
        function (skill) {

            const badge =
                document.createElement(
                    "span"
                );

            badge.className =
                "sg-badge sg-badge-matched";

            badge.textContent =
                `✓ ${skill}`;

            container.appendChild(
                badge
            );

        }
    );

}


/* =========================================================
   MISSING SKILLS
   ========================================================= */

function renderMissingSkills() {

    const container =
        document.getElementById(
            "sgMissingSkills"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const skills =
        latestSkillGapData.missing_skills ||
        latestSkillGapData.missingSkills ||
        [];


    if (!skills.length) {

        container.innerHTML =
            `
            <p class="sg-empty-message">
                No major skill gaps detected.
            </p>
            `;

        return;

    }


    skills.forEach(
        function (skill) {

            const badge =
                document.createElement(
                    "span"
                );

            badge.className =
                "sg-badge sg-badge-missing";

            badge.textContent =
                `+ ${skill}`;

            container.appendChild(
                badge
            );

        }
    );

}


/* =========================================================
   REQUIRED SKILLS
   ========================================================= */

function renderRequiredSkills() {

    const container =
        document.getElementById(
            "sgRequiredSkills"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const required =
        latestSkillGapData.required_skills ||
        latestSkillGapData.requiredSkills ||
        [];


    const matched =
        latestSkillGapData.your_skills ||
        latestSkillGapData.matched_skills ||
        latestSkillGapData.matchedSkills ||
        [];


    if (!required.length) {

        container.innerHTML =
            `
            <p class="sg-empty-message">
                Required career skills are not available.
            </p>
            `;

        return;

    }


    required.forEach(
        function (skill) {

            const badge =
                document.createElement(
                    "span"
                );


            const isMatched =
                matched.some(
                    function (item) {

                        return String(
                            item
                        ).toLowerCase().trim() ===
                        String(
                            skill
                        ).toLowerCase().trim();

                    }
                );


            badge.className =
                isMatched
                    ? "sg-badge sg-badge-matched"
                    : "sg-badge sg-badge-required";


            badge.textContent =
                isMatched
                    ? `✓ ${skill}`
                    : `○ ${skill}`;


            container.appendChild(
                badge
            );

        }
    );

}


/* =========================================================
   LEARNING PATH
   ========================================================= */

function renderLearningPath() {

    const container =
        document.getElementById(
            "sgLearningPath"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    let learningPath =
        latestSkillGapData.learning_path ||
        latestSkillGapData.learningPath ||
        [];


    const missing =
        latestSkillGapData.missing_skills ||
        latestSkillGapData.missingSkills ||
        [];


    /*
       If backend does not provide
       a learning path, create one.
    */

    if (!learningPath.length) {

        learningPath =
            missing.map(
                function (skill) {

                    return {

                        skill:
                            skill,

                        priority:
                            "Medium",

                        resource:
                            `Learn ${skill}`,

                        description:
                            `Learn the fundamentals of ${skill}.`,

                        duration:
                            "2–4 Weeks"

                    };

                }
            );

    }


    if (!learningPath.length) {

        container.innerHTML =
            `
            <p class="sg-empty-message">
                Your profile currently has
                no major learning gaps.
            </p>
            `;

        return;

    }


    learningPath.forEach(
        function (
            item,
            index
        ) {

            let skill;
            let priority;
            let resource;
            let description;
            let duration;


            if (
                typeof item ===
                "string"
            ) {

                skill =
                    item;

                priority =
                    "Medium";

                resource =
                    `Learn ${item}`;

                description =
                    `Learn the fundamentals of ${item}.`;

                duration =
                    "2–4 Weeks";

            } else {

                skill =
                    item.skill ||
                    item.name ||
                    item.title ||
                    "Skill";


                priority =
                    item.priority ||
                    item.level ||
                    "Medium";


                resource =
                    item.resource ||
                    `Learn ${skill}`;


                description =
                    item.description ||
                    `Learn the fundamentals of ${skill}.`;


                duration =
                    item.duration ||
                    item.time ||
                    "2–4 Weeks";

            }


            const card =
                document.createElement(
                    "div"
                );

            card.className =
                "sg-learning-card";


            card.innerHTML =
                `

                <div class="sg-step-number">
                    ${index + 1}
                </div>

                <div class="sg-learning-content">

                    <h4>
                        ${escapeHtml(skill)}
                    </h4>

                    <p>
                        <strong>Priority:</strong>
                        ${escapeHtml(priority)}
                    </p>

                    <p>
                        <strong>Resource:</strong>
                        ${escapeHtml(resource)}
                    </p>

                    <p>
                        ${escapeHtml(description)}
                    </p>

                    <p>
                        <strong>Estimated Time:</strong>
                        ${escapeHtml(duration)}
                    </p>

                </div>

                `;


            container.appendChild(
                card
            );

        }
    );

}


/* =========================================================
   TOP PREDICTED ROLES
   ========================================================= */

function renderTopRoles() {

    const container =
        document.getElementById(
            "sgTopRoles"
        );


    if (!container) {

        return;

    }


    container.innerHTML = "";


    const roles =
        latestSkillGapData.predictions ||
        latestSkillGapData.top_roles ||
        latestSkillGapData.topRoles ||
        latestSkillGapData.recommendations ||
        latestSkillGapData.careers ||
        [];


    if (!roles.length) {

        const targetRole =
            latestSkillGapData.top_role ||
            latestSkillGapData.target_role ||
            latestSkillGapData.targetRole ||
            latestSkillGapData.predicted_career;


        if (targetRole) {

            createRoleItem(

                container,

                targetRole,

                latestSkillGapData.confidence ||
                0

            );

        } else {

            container.innerHTML =
                `
                <p class="sg-empty-message">
                    No predicted career roles available.
                </p>
                `;

        }

        return;

    }


    roles.forEach(
        function (roleData) {

            let roleName;
            let confidence;


            if (
                typeof roleData ===
                "string"
            ) {

                roleName =
                    roleData;

                confidence =
                    0;

            } else {

                roleName =
                    roleData.role ||
                    roleData.career ||
                    roleData.title ||
                    roleData.name ||
                    "Career Role";


                confidence =
                    Number(
                        roleData.confidence ??
                        roleData.score ??
                        roleData.probability ??
                        0
                    );

            }


            createRoleItem(

                container,

                roleName,

                confidence

            );

        }
    );

}


/* =========================================================
   CREATE ROLE ITEM
   ========================================================= */

function createRoleItem(
    container,
    roleName,
    confidence
) {

    const item =
        document.createElement(
            "div"
        );

    item.className =
        "sg-role-item";


    let confidenceText;


    if (confidence > 0) {

        let value =
            confidence;


        /*
           Convert decimal confidence
           such as 0.86 into 86%.
        */

        if (value <= 1) {

            value =
                value * 100;

        }


        confidenceText =
            `${Math.round(
                value
            )}%`;

    } else {

        confidenceText =
            "Recommended";

    }


    item.innerHTML =
        `

        <span class="sg-role-name">
            ${escapeHtml(roleName)}
        </span>

        <span class="sg-role-confidence">
            ${confidenceText}
        </span>

        `;


    container.appendChild(
        item
    );

}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHtml(value) {

    return String(
        value
    )
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


/* =========================================================
   LOAD DATA FROM BACKEND
   ========================================================= */

async function fetchSkillGapResults() {

    try {

        const response =
            await fetch(
                "/api/skill-gap-results",
                {
                    method:
                        "GET",

                    credentials:
                        "same-origin"
                }
            );


        const data =
            await response.json();


        if (
            response.ok &&
            data.success
        ) {

            latestSkillGapData =
                data;


            sessionStorage.setItem(

                "latestSkillGapData",

                JSON.stringify(
                    latestSkillGapData
                )

            );


            renderSkillGapTab();

            console.log(
                "Skill Gap Data Loaded From API:",
                data
            );

            return;

        }


        showNoResumeMessage();

    } catch (error) {

        console.error(
            "Could not fetch Skill Gap results:",
            error
        );

        /*
           If API fails, try session storage.
        */

        loadSkillGapFromStorage();

    }

}


/* =========================================================
   INITIAL PAGE LOAD
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        /*
           First try existing
           session storage data.
        */

        loadSkillGapFromStorage();


        /*
           Refresh data from API
           when Skill Gap tab opens.
        */

        document
            .querySelectorAll(
                ".tab-btn"
            )
            .forEach(
                function (button) {

                    button.addEventListener(
                        "click",
                        function () {

                            const tab =
                                button.dataset.tab;


                            if (
                                tab ===
                                "skillgap"
                            ) {

                                fetchSkillGapResults();

                            }

                        }
                    );

                }
            );

    }
);


/* =========================================================
   LISTEN FOR NEW RESUME ANALYSIS DATA
   ========================================================= */

window.addEventListener(
    "skillGapUpdated",
    function (event) {

        if (!event.detail) {

            return;

        }


        latestSkillGapData =
            event.detail;


        sessionStorage.setItem(

            "latestSkillGapData",

            JSON.stringify(
                latestSkillGapData
            )

        );


        renderSkillGapTab();


        console.log(
            "Skill Gap Data Updated:",
            latestSkillGapData
        );

    }
);