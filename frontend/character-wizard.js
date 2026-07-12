async function fetchCreationCatalog() {
  const response = await fetch(`${API_BASE}/api/character-creation/catalog`);
  if (!response.ok) throw new Error(`Catalogo indisponivel: ${response.status}`);
  return response.json();
}

function defaultStats() {
  return {
    INT: 5,
    REF: 5,
    DEX: 5,
    TECH: 5,
    COOL: 5,
    WILL: 5,
    LUCK: 5,
    MOVE: 5,
    BODY: 5,
    EMP: 5,
  };
}

function statPointsUsed(stats) {
  return Object.values(stats).reduce((sum, v) => sum + Number(v || 0), 0);
}

function openCharacterWizard() {
  const existing = document.getElementById("characterWizardDrawer");
  if (existing) {
    existing.classList.remove("is-hidden");
    return;
  }
  buildCharacterWizardDrawer();
}

function buildCharacterWizardDrawer() {
  const drawer = document.createElement("section");
  drawer.id = "characterWizardDrawer";
  drawer.className = "sheet";
  drawer.setAttribute("aria-label", "Criar protagonista");
  drawer.innerHTML = `
    <div class="sheet-backdrop" data-close="wizard"></div>
    <div class="sheet-panel">
      <header class="sheet-header">
        <h2>Novo protagonista (Complete Package)</h2>
        <button type="button" class="close-btn" data-close="wizard">X</button>
      </header>
      <div class="sheet-content" id="wizardContent">
        <p class="utility-hint">Distribua 62 STATs e 86 Skills. Role Ability inicia em 4.</p>
        <form id="characterWizardForm" class="wizard-form"></form>
        <div id="wizardValidation" class="wizard-validation"></div>
        <div class="wizard-actions">
          <button type="button" id="wizardValidateBtn">Validar</button>
          <button type="button" id="wizardCreateBtn">Criar e jogar</button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(drawer);
  drawer.querySelector("[data-close='wizard']").addEventListener("click", () => {
    drawer.classList.add("is-hidden");
  });
  drawer.querySelector(".close-btn").addEventListener("click", () => {
    drawer.classList.add("is-hidden");
  });
  populateWizardForm();
  document.getElementById("wizardValidateBtn").addEventListener("click", validateWizardDraft);
  document.getElementById("wizardCreateBtn").addEventListener("click", createWizardCharacter);
}

async function populateWizardForm() {
  const catalog = await fetchCreationCatalog();
  const form = document.getElementById("characterWizardForm");
  const roles = catalog.roles || [];
  const roleOptions = roles
    .map((r) => `<option value="${r.id}">${r.label} — ${r.ability}</option>`)
    .join("");

  form.innerHTML = `
    <label>Nome <input name="name" required /></label>
    <label>Handle <input name="handle" /></label>
    <label>Slug (id) <input name="slug" required placeholder="meu_personagem" /></label>
    <label>Role <select name="role">${roleOptions}</select></label>
    <label>Conceito <textarea name="concept" rows="2"></textarea></label>
    <label>Aparência <textarea name="appearance" rows="3"></textarea></label>
    <label>Background <textarea name="background" rows="4"></textarea></label>
    <fieldset><legend>STATs (62)</legend><div id="wizardStats" class="wizard-stats"></div><p id="wizardStatCount"></p></fieldset>
    <label>Skills (formato: Nome: nivel, uma por linha)</label>
    <textarea name="skillsText" rows="8" placeholder="Perception: 6&#10;Streetwise: 4"></textarea>
    <p id="wizardSkillCount"></p>
  `;

  const statsDiv = document.getElementById("wizardStats");
  const stats = defaultStats();
  CPR_STAT_ORDER.forEach((key) => {
    const label = document.createElement("label");
    label.innerHTML = `${key} <input type="number" min="2" max="8" data-stat="${key}" value="${stats[key]}" />`;
    statsDiv.appendChild(label);
    label.querySelector("input").addEventListener("input", updateWizardCounters);
  });
  form.querySelector("[name='skillsText']").addEventListener("input", updateWizardCounters);
  form.querySelector("[name='role']").addEventListener("change", syncRoleAbility);
  updateWizardCounters();
}

function syncRoleAbility() {
  /* role ability filled on submit from catalog */
}

function parseSkillsText(raw) {
  const skills = {};
  String(raw || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const idx = line.lastIndexOf(":");
      if (idx < 1) return;
      const name = line.slice(0, idx).trim();
      const level = parseInt(line.slice(idx + 1).trim(), 10);
      if (name && !Number.isNaN(level)) skills[name] = level;
    });
  return skills;
}

function collectWizardDraft() {
  const form = document.getElementById("characterWizardForm");
  const stats = {};
  form.querySelectorAll("[data-stat]").forEach((input) => {
    stats[input.dataset.stat] = parseInt(input.value, 10) || 0;
  });
  const roleId = form.querySelector("[name='role']").value;
  const catalogRole = (window.__wizardCatalog?.roles || []).find((r) => r.id === roleId);
  return {
    name: form.querySelector("[name='name']").value.trim(),
    slug: form.querySelector("[name='slug']").value.trim().toLowerCase(),
    handle: form.querySelector("[name='handle']").value.trim(),
    role: roleId,
    role_label: catalogRole?.label || roleId,
    role_ability: catalogRole?.ability || "",
    role_ability_rank: 4,
    concept: form.querySelector("[name='concept']").value.trim(),
    appearance: form.querySelector("[name='appearance']").value.trim(),
    background: form.querySelector("[name='background']").value.trim(),
    stats,
    skills: parseSkillsText(form.querySelector("[name='skillsText']").value),
  };
}

function updateWizardCounters() {
  const form = document.getElementById("characterWizardForm");
  if (!form) return;
  const stats = {};
  form.querySelectorAll("[data-stat]").forEach((input) => {
    stats[input.dataset.stat] = parseInt(input.value, 10) || 0;
  });
  const statEl = document.getElementById("wizardStatCount");
  if (statEl) statEl.textContent = `STATs: ${statPointsUsed(stats)} / 62`;
  const skills = parseSkillsText(form.querySelector("[name='skillsText']").value);
  const skillTotal = Object.values(skills).reduce((s, v) => s + v, 0);
  const skillEl = document.getElementById("wizardSkillCount");
  if (skillEl) skillEl.textContent = `Skills: ${skillTotal} / 86`;
}

async function validateWizardDraft() {
  const draft = collectWizardDraft();
  const response = await fetch(`${API_BASE}/api/character-creation/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(draft),
  });
  const data = await response.json();
  const box = document.getElementById("wizardValidation");
  if (data.passed) {
    box.textContent = "Ficha valida.";
    box.className = "wizard-validation ok";
    return;
  }
  box.className = "wizard-validation err";
  box.innerHTML = (data.issues || []).map((i) => `<div>${i.message}</div>`).join("");
}

async function createWizardCharacter() {
  const draft = collectWizardDraft();
  const response = await fetch(`${API_BASE}/api/characters`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(draft),
  });
  const data = await response.json();
  if (!response.ok) {
    const box = document.getElementById("wizardValidation");
    box.className = "wizard-validation err";
    box.textContent = data.detail?.error || data.error || `Erro ${response.status}`;
    return;
  }
  await fetch(`${API_BASE}/api/characters/${data.id}/protagonist`, { method: "PUT" });
  window.location.reload();
}

fetchCreationCatalog().then((c) => {
  window.__wizardCatalog = c;
});

window.openCharacterWizard = openCharacterWizard;