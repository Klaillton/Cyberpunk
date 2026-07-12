const CPR_STAT_ORDER = [
  "INT",
  "REF",
  "DEX",
  "TECH",
  "COOL",
  "WILL",
  "LUCK",
  "MOVE",
  "BODY",
  "EMP",
];

const CPR_TIER_LABELS = {
  protagonist: "Protagonista",
  crew_full: "Crew CPR",
  npc_reference: "Referência",
  npc_generic: "Genérico",
};

function renderCprSheet(sheet, container) {
  if (!container || !sheet) return;
  container.innerHTML = "";
  const layout = sheet.layout || "cpr_reference";
  const root = document.createElement("div");
  root.className = `cpr-sheet cpr-sheet--${layout === "cpr_full" ? "full" : layout === "cpr_generic" ? "generic" : "reference"}`;

  const header = document.createElement("div");
  header.className = "cpr-sheet-header";

  if (sheet.id) {
    const portrait = document.createElement("img");
    portrait.className = "cpr-portrait";
    portrait.src = `/api/character-image/${sheet.id}`;
    portrait.alt = sheet.title || "Retrato";
    portrait.loading = "lazy";
    header.appendChild(portrait);
  }

  const meta = document.createElement("div");
  meta.className = "cpr-sheet-meta";
  const badge = document.createElement("div");
  badge.className = "cpr-tier-badge";
  badge.textContent = CPR_TIER_LABELS[sheet.tier] || sheet.tier || "Ficha";
  meta.appendChild(badge);
  if (sheet.title) {
    const name = document.createElement("h3");
    name.className = "cpr-sheet-title";
    name.textContent = sheet.title;
    meta.appendChild(name);
  }
  header.appendChild(meta);
  root.appendChild(header);

  if (layout === "cpr_full") {
    root.appendChild(renderStatsPanel(sheet));
    root.appendChild(renderSkillsPanel(sheet));
  } else if (layout === "cpr_generic") {
    root.appendChild(renderGenericPanel(sheet));
  } else {
    root.appendChild(renderReferencePanel(sheet));
  }

  container.appendChild(root);
}

function renderStatsPanel(sheet) {
  const panel = document.createElement("section");
  panel.className = "cpr-panel";
  const title = document.createElement("h4");
  title.textContent = "Atributos";
  panel.appendChild(title);

  const grid = document.createElement("div");
  grid.className = "cpr-stats-grid";
  const stats = sheet.stats || {};
  CPR_STAT_ORDER.forEach((key) => {
    const cell = document.createElement("div");
    cell.className = "cpr-stat";
    cell.innerHTML = `<span class="cpr-stat-label">${key}</span><span class="cpr-stat-value">${stats[key] ?? "—"}</span>`;
    grid.appendChild(cell);
  });
  panel.appendChild(grid);

  const derived = sheet.derived || {};
  const meta = document.createElement("div");
  meta.className = "cpr-derived";
  if (derived.hp) meta.innerHTML += `<span>HP ${derived.hp}</span>`;
  if (derived.seriouslyWounded) meta.innerHTML += `<span>SW ${derived.seriouslyWounded}</span>`;
  if (derived.deathSave) meta.innerHTML += `<span>Death Save ${derived.deathSave}</span>`;
  if (derived.humanityBase) meta.innerHTML += `<span>HL base ${derived.humanityBase}</span>`;
  panel.appendChild(meta);
  return panel;
}

function renderSkillsPanel(sheet) {
  const panel = document.createElement("section");
  panel.className = "cpr-panel";
  const title = document.createElement("h4");
  title.textContent = "Skills";
  panel.appendChild(title);

  const grid = document.createElement("div");
  grid.className = "cpr-skills-grid";
  const skills = sheet.skills || {};
  Object.entries(skills)
    .sort((a, b) => Number(b[1]) - Number(a[1]))
    .forEach(([name, level]) => {
      const row = document.createElement("div");
      row.textContent = `${name}: ${level}`;
      grid.appendChild(row);
    });
  if (!Object.keys(skills).length) {
    grid.textContent = "Sem skills parseadas.";
  }
  panel.appendChild(grid);
  return panel;
}

function renderReferencePanel(sheet) {
  const panel = document.createElement("section");
  panel.className = "cpr-panel";
  const title = document.createElement("h4");
  title.textContent = sheet.title || "NPC";
  panel.appendChild(title);
  const intro = (sheet.introLines || []).join("\n");
  if (intro) {
    const p = document.createElement("div");
    p.className = "md-content";
    p.textContent = intro;
    panel.appendChild(p);
  }
  return panel;
}

function renderGenericPanel(sheet) {
  const panel = renderReferencePanel(sheet);
  const note = document.createElement("p");
  note.textContent = "Arquétipo reutilizável — sem ficha individual.";
  note.style.opacity = "0.8";
  note.style.fontSize = "0.82rem";
  panel.appendChild(note);
  return panel;
}

window.renderCprSheet = renderCprSheet;