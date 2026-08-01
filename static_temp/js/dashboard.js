// ---------------------------------------------------------------------------
// Tabs
// ---------------------------------------------------------------------------
document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
        document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
        btn.classList.add("active");
        document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
    });
});

// ---------------------------------------------------------------------------
// Upload: dropzone + file picker
// ---------------------------------------------------------------------------
const dropzone = document.getElementById("dropzone");
const resumeFileInput = document.getElementById("resumeFile");
const resumeTextArea = document.getElementById("resumeText");

let selectedFile = null;

dropzone.addEventListener("click", () => resumeFileInput.click());

resumeFileInput.addEventListener("change", () => {
    if (resumeFileInput.files.length > 0) {
        selectedFile = resumeFileInput.files[0];
        dropzone.querySelector("p strong").textContent = `Selected: ${selectedFile.name}`;
    }
});

["dragover", "dragenter"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
    })
);
["dragleave", "drop"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
    })
);
dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length > 0) {
        selectedFile = e.dataTransfer.files[0];
        dropzone.querySelector("p strong").textContent = `Selected: ${selectedFile.name}`;
    }
});

// ---------------------------------------------------------------------------
// Analyze
// ---------------------------------------------------------------------------
const analyzeBtn = document.getElementById("analyzeBtn");
const analyzeStatus = document.getElementById("analyzeStatus");

analyzeBtn.addEventListener("click", async () => {
    const pastedText = resumeTextArea.value.trim();

    if (!selectedFile && !pastedText) {
        setStatus(analyzeStatus, "Please upload a file or paste resume text.", "error");
        return;
    }

    setStatus(analyzeStatus, "Analyzing...", "");
    analyzeBtn.disabled = true;

    try {
        let response;
        if (selectedFile) {
            const formData = new FormData();
            formData.append("resume_file", selectedFile);
            response = await fetch("/api/analyze", { method: "POST", body: formData });
        } else {
            response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: pastedText }),
            });
        }

        const data = await response.json();

        if (!response.ok) {
            setStatus(analyzeStatus, data.error || "Something went wrong.", "error");
            return;
        }

        renderResults(data);
        setStatus(analyzeStatus, "Analysis complete — see the 'Parsing & Prediction' tab.", "success");

        // Switch to results tab automatically
        document.querySelector('[data-tab="results"]').click();
    } catch (err) {
        setStatus(analyzeStatus, "Network or server error: " + err.message, "error");
    } finally {
        analyzeBtn.disabled = false;
    }
});

function setStatus(el, message, kind) {
    el.textContent = message;
    el.className = "status-msg" + (kind ? " " + kind : "");
}

// ---------------------------------------------------------------------------
// Render results
// ---------------------------------------------------------------------------
function renderResults(data) {
    document.getElementById("noResults").style.display = "none";
    document.getElementById("resultsGrid").style.display = "grid";

    document.getElementById("parsedText").innerHTML = data.highlighted_html;

    const skillBadges = document.getElementById("skillBadges");
    skillBadges.innerHTML = data.skills.length
        ? data.skills.map((s) => `<span class="badge">${escapeHtml(s)}</span>`).join("")
        : '<span class="muted">No skills detected from the gazetteer.</span>';

    const eduList = document.getElementById("educationList");
    eduList.innerHTML = data.education.length
        ? data.education
              .map((e) => `<li><strong>${escapeHtml(e.degree)}</strong>, ${escapeHtml(e.institution || "—")}</li>`)
              .join("")
        : '<li class="muted">No education entries detected.</li>';

    // Prediction bars
    const barsContainer = document.getElementById("predictionBars");
    barsContainer.innerHTML = data.predictions
        .map((p) => {
            const pct = Math.max(2, Math.round(p.confidence * 100));
            return `
                <div class="bar-row">
                    <div class="bar-label"><span>${escapeHtml(p.role)}</span><span>${pct}%</span></div>
                    <div class="bar-track"><div class="bar-fill" style="width:${pct}%;"></div></div>
                </div>
            `;
        })
        .join("");

    if (data.top_role) {
        document.getElementById("bestRole").textContent = data.top_role;
        const topPred = data.predictions.find((p) => p.role === data.top_role);
        document.getElementById("bestConf").textContent = topPred
            ? `Confidence: ${Math.round(topPred.confidence * 100)}%`
            : "";
    }

    // Skill gap
    const skillGapCard = document.getElementById("skillGapCard");
    if (data.skill_gap) {
        skillGapCard.style.display = "block";
        document.getElementById("skillGapRole").textContent = "— " + data.top_role;

        const matchedEl = document.getElementById("matchedBadges");
        matchedEl.innerHTML = data.skill_gap.matched.length
            ? data.skill_gap.matched.map((s) => `<span class="badge">${escapeHtml(s)}</span>`).join("")
            : '<span class="muted">No overlap with the required profile yet.</span>';

        const missingEl = document.getElementById("missingBadges");
        missingEl.innerHTML = data.skill_gap.missing.length
            ? data.skill_gap.missing.map((s) => `<span class="badge-missing">${escapeHtml(s)}</span>`).join("")
            : '<span class="muted">Fully covers the required profile</span>';
    } else {
        skillGapCard.style.display = "none";
    }
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// ---------------------------------------------------------------------------
// Profile form
// ---------------------------------------------------------------------------
const profileForm = document.getElementById("profileForm");
const profileStatus = document.getElementById("profileStatus");

// Load existing profile on page load
(async function loadProfile() {
    try {
        const res = await fetch("/api/profile");
        const data = await res.json();
        if (data && data.name) {
            document.getElementById("pf_name").value = data.name || "";
            document.getElementById("pf_email").value = data.email || "";
            document.getElementById("pf_years").value = data.years_experience || "";
            document.getElementById("pf_education").value = data.education_level || "high school";
            document.getElementById("pf_skills").value = (data.skills || []).join(", ");
            document.getElementById("pf_current_role").value = data.current_role || "";
            document.getElementById("pf_desired_role").value = data.desired_role || "";
            document.getElementById("pf_location").value = data.location || "";
        }
    } catch (e) {
        // no existing profile yet - fine
    }
})();

profileForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        name: document.getElementById("pf_name").value.trim(),
        email: document.getElementById("pf_email").value.trim(),
        years_experience: parseFloat(document.getElementById("pf_years").value || "0"),
        education_level: document.getElementById("pf_education").value,
        skills: document.getElementById("pf_skills").value
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean),
        current_role: document.getElementById("pf_current_role").value.trim(),
        desired_role: document.getElementById("pf_desired_role").value.trim(),
        location: document.getElementById("pf_location").value.trim(),
    };

    try {
        const res = await fetch("/api/profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await res.json();

        if (!res.ok) {
            setStatus(profileStatus, (data.errors || ["Save failed."]).join(" "), "error");
            return;
        }
        setStatus(profileStatus, "Profile saved.", "success");
    } catch (err) {
        setStatus(profileStatus, "Network error: " + err.message, "error");
    }
});