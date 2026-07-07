const chatForm = document.getElementById("chatForm");
const playerInput = document.getElementById("playerInput");
const narrationFeed = document.getElementById("narrationFeed");
const narratorFeed = document.getElementById("narratorFeed");
const chatModeLabel = document.getElementById("chatModeLabel");
const btnFicha = document.getElementById("btnFicha");
const btnJournal = document.getElementById("btnJournal");
const btnNarrador = document.getElementById("btnNarrador");
const btnPropostas = document.getElementById("btnPropostas");
const proposalsBadge = document.getElementById("proposalsBadge");
const proposalsDrawer = document.getElementById("proposalsDrawer");
const closeProposalsBtn = document.getElementById("closeProposalsBtn");
const proposalsList = document.getElementById("proposalsList");
const approveAllProposalsBtn = document.getElementById("approveAllProposalsBtn");
const fichaDrawer = document.getElementById("fichaDrawer");
const journalDrawer = document.getElementById("journalDrawer");
const closeFichaBtn = document.getElementById("closeFichaBtn");
const closeJournalBtn = document.getElementById("closeJournalBtn");
const journalForm = document.getElementById("journalForm");
const journalInput = document.getElementById("journalInput");
const journalList = document.getElementById("journalList");
const characterPortrait = document.getElementById("characterPortrait");
const fichaStatus = document.getElementById("fichaStatus");
const fichaSections = document.getElementById("fichaSections");
const fichaRefs = document.getElementById("fichaRefs");
const storyBrief = document.getElementById("storyBrief");
const briefDrawer = document.getElementById("briefDrawer");
const briefDrawerTitle = document.getElementById("briefDrawerTitle");
const briefDrawerBody = document.getElementById("briefDrawerBody");
const briefDrawerSources = document.getElementById("briefDrawerSources");
const closeBriefBtn = document.getElementById("closeBriefBtn");
const btnNpcs = document.getElementById("btnNpcs");
const npcSubmenu = document.getElementById("npcSubmenu");
const btnAdmin = document.getElementById("btnAdmin");
const npcDrawer = document.getElementById("npcDrawer");
const npcDrawerTitle = document.getElementById("npcDrawerTitle");
const npcDrawerStatus = document.getElementById("npcDrawerStatus");
const npcCatalog = document.getElementById("npcCatalog");
const closeNpcBtn = document.getElementById("closeNpcBtn");
const adminDrawer = document.getElementById("adminDrawer");
const closeAdminBtn = document.getElementById("closeAdminBtn");

let activeChannel = "narracao";
const CHARACTER_ID = "ryan_wireghost_voss";
const API_BASE =
  window.location.protocol.startsWith("http") && window.location.host
    ? `${window.location.protocol}//${window.location.host}`
    : "http://127.0.0.1:8787";
const modeButtons = [btnFicha, btnJournal, btnNarrador, btnPropostas];
let profileLoaded = false;
let journalEntries = [];
let pendingProposals = [];
let activeLoadingCard = null;
let activeLoadingFeed = null;
let campaignBrief = null;
let npcCatalogData = [];
let openingRendered = false;

const ALL_DRAWERS = [
  fichaDrawer,
  journalDrawer,
  proposalsDrawer,
  briefDrawer,
  npcDrawer,
  adminDrawer,
];

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function renderInlineMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(
    /`([^`]+)`/g,
    "<code class=\"md-inline-code\">$1</code>",
  );
  html = html.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    '<a href="$2" target="_blank" rel="noreferrer">$1</a>',
  );
  return html;
}

function isTableRow(line) {
  return line.trim().startsWith("|") && line.trim().endsWith("|");
}

function isTableSeparator(line) {
  const trimmed = line.trim();
  return /^\|[\s:|-]+\|$/.test(trimmed);
}

function renderMarkdown(text) {
  const lines = String(text || "").split("\n");
  const parts = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();

    if (!trimmed) {
      index += 1;
      continue;
    }

    if (/^---+$/.test(trimmed)) {
      parts.push("<hr class=\"md-hr\" />");
      index += 1;
      continue;
    }

    const heading = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = Math.min(heading[1].length + 1, 6);
      parts.push(
        `<h${level} class="md-heading">${renderInlineMarkdown(heading[2])}</h${level}>`,
      );
      index += 1;
      continue;
    }

    if (isTableRow(trimmed)) {
      const tableLines = [];
      while (index < lines.length && isTableRow(lines[index].trim())) {
        tableLines.push(lines[index].trim());
        index += 1;
      }
      const rows = tableLines.filter((row) => !isTableSeparator(row));
      if (rows.length > 0) {
        const headerCells = rows[0]
          .slice(1, -1)
          .split("|")
          .map((cell) => cell.trim());
        const bodyRows = rows.slice(1);
        const thead = `<thead><tr>${headerCells
          .map((cell) => `<th>${renderInlineMarkdown(cell)}</th>`)
          .join("")}</tr></thead>`;
        const tbody = bodyRows
          .map((row) => {
            const cells = row
              .slice(1, -1)
              .split("|")
              .map((cell) => cell.trim());
            return `<tr>${cells
              .map((cell) => `<td>${renderInlineMarkdown(cell)}</td>`)
              .join("")}</tr>`;
          })
          .join("");
        parts.push(
          `<div class="md-table-wrap"><table class="md-table">${thead}<tbody>${tbody}</tbody></table></div>`,
        );
      }
      continue;
    }

    if (/^[-*]\s+/.test(trimmed)) {
      const items = [];
      while (index < lines.length && /^[-*]\s+/.test(lines[index].trim())) {
        items.push(lines[index].trim().replace(/^[-*]\s+/, ""));
        index += 1;
      }
      parts.push(
        `<ul class="md-list">${items
          .map((item) => `<li>${renderInlineMarkdown(item)}</li>`)
          .join("")}</ul>`,
      );
      continue;
    }

    const paragraph = [];
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^#{1,6}\s+/.test(lines[index].trim()) &&
      !isTableRow(lines[index].trim()) &&
      !/^[-*]\s+/.test(lines[index].trim()) &&
      !/^---+$/.test(lines[index].trim())
    ) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    parts.push(`<p>${renderInlineMarkdown(paragraph.join(" "))}</p>`);
  }

  return parts.join("");
}

function normalizeName(value) {
  return (value || "")
    .toLowerCase()
    .replace(/\(off-record\)/gi, "")
    .replace(/[^a-z0-9 ]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseNpcReply(reply) {
  const text = String(reply || "").trim();
  const tagged = text.match(/^\[(NPC(?:-F|-M)?)\s*:\s*([^\]]+)\]\s*(.+)$/i);
  if (tagged) {
    const tag = tagged[1].toUpperCase();
    return {
      isNpc: true,
      name: tagged[2].trim(),
      gender: tag.includes("-F") ? "female" : "male",
      text: tagged[3].trim(),
    };
  }

  const plain = text.match(/^([^:]{2,60}):\s*(.+)$/);
  if (!plain) {
    return { isNpc: false, text };
  }

  const speaker = plain[1].trim();
  const speakerNorm = normalizeName(speaker);
  if (["narrador", "mestre", "historia", "voce", "sistema"].includes(speakerNorm)) {
    return { isNpc: false, text };
  }

  return {
    isNpc: true,
    name: speaker,
    gender: "male",
    text: plain[2].trim(),
  };
}

async function fetchNpcAsset(name, gender) {
  const response = await fetch(
    `${API_BASE}/api/npc-asset?name=${encodeURIComponent(name)}&gender=${encodeURIComponent(gender || "male")}`,
  );
  if (!response.ok) {
    throw new Error(`Falha ao carregar token NPC: ${response.status}`);
  }
  return response.json();
}

function loadImage(sourceUrl) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.crossOrigin = "anonymous";
    image.onload = () => resolve(image);
    image.onerror = () =>
      reject(new Error(`Falha ao carregar imagem: ${sourceUrl}`));
    image.src = sourceUrl;
  });
}

function resizeImageToCover(sourceImage, targetWidth, targetHeight) {
  const canvas = document.createElement("canvas");
  canvas.width = targetWidth;
  canvas.height = targetHeight;

  const context = canvas.getContext("2d");
  if (!context) {
    throw new Error("Canvas indisponivel");
  }

  const sourceRatio = sourceImage.width / sourceImage.height;
  const targetRatio = targetWidth / targetHeight;
  let drawWidth = sourceImage.width;
  let drawHeight = sourceImage.height;
  let offsetX = 0;
  let offsetY = 0;

  if (sourceRatio > targetRatio) {
    drawWidth = sourceImage.height * targetRatio;
    offsetX = (sourceImage.width - drawWidth) / 2;
  } else {
    drawHeight = sourceImage.width / targetRatio;
    offsetY = (sourceImage.height - drawHeight) / 2;
  }

  context.drawImage(
    sourceImage,
    offsetX,
    offsetY,
    drawWidth,
    drawHeight,
    0,
    0,
    targetWidth,
    targetHeight,
  );

  return canvas.toDataURL("image/png");
}

async function setCoverImage(
  imageElement,
  sourceUrl,
  targetWidth,
  targetHeight,
) {
  try {
    const image = await loadImage(sourceUrl);
    imageElement.src = resizeImageToCover(image, targetWidth, targetHeight);
  } catch (error) {
    console.error(error);
    imageElement.src = sourceUrl;
  }
}

function appendCard(text, role, options = {}) {
  const targetFeed =
    activeChannel === "mestre" ? narratorFeed : narrationFeed;
  const card = document.createElement("article");
  card.className = `narration-card ${role}`;

  if (options.npcTokenUrl) {
    card.classList.add("npc-message");
    const tokenLink = document.createElement("a");
    tokenLink.className = "npc-token-link";
    tokenLink.href = options.npcImageUrl || options.npcTokenUrl;
    tokenLink.target = "_blank";
    tokenLink.rel = "noreferrer";
    tokenLink.title = `Abrir imagem de ${options.npcName || "NPC"}`;

    const tokenImg = document.createElement("img");
    tokenImg.className = "npc-token";
    setCoverImage(tokenImg, options.npcTokenUrl, 192, 192);
    tokenImg.alt = `Token de ${options.npcName || "NPC"}`;
    tokenLink.appendChild(tokenImg);
    card.appendChild(tokenLink);
  }

  const p = document.createElement("p");
  p.textContent = text;
  card.appendChild(p);

  targetFeed.appendChild(card);
  card.scrollIntoView({ behavior: "smooth", block: "end" });
}

function createLoadingCard(text) {
  const targetFeed =
    activeChannel === "mestre" ? narratorFeed : narrationFeed;
  const card = document.createElement("article");
  card.className = "narration-card loading";
  card.dataset.loading = "true";

  const indicator = document.createElement("span");
  indicator.className = "loading-indicator";
  indicator.setAttribute("aria-hidden", "true");

  const label = document.createElement("p");
  label.className = "loading-text";
  label.textContent = text;

  card.appendChild(indicator);
  card.appendChild(label);
  targetFeed.appendChild(card);
  card.scrollIntoView({ behavior: "smooth", block: "end" });

  activeLoadingCard = card;
  activeLoadingFeed = targetFeed;
  return card;
}

function removeLoadingCard() {
  if (activeLoadingCard) {
    activeLoadingCard.remove();
  }
  activeLoadingCard = null;
  activeLoadingFeed = null;
}

function setChatBusy(isBusy) {
  playerInput.disabled = isBusy;
  chatForm.querySelector("button[type='submit']").disabled = isBusy;
  playerInput.placeholder = isBusy
    ? "Consultando narracao..."
    : activeChannel === "mestre"
      ? "Fale com o Mestre (off-game): duvidas, canon, ajustes..."
      : "Digite sua acao...";
}

function extractFriendlyError(error) {
  const message = String(error?.message || error || "");
  if (/402|payment required|balance exhausted|provider grok/i.test(message)) {
    return "Grok indisponivel no momento. O saldo do provider foi esgotado. Selecione outro provider ou tente mais tarde.";
  }
  if (/provider de teste/i.test(message)) {
    return "Provider de teste selecionado sem integracao real.";
  }
  return "Nao foi possivel consultar a narracao agora. Tente novamente em instantes.";
}

function mestreEndpoints() {
  return ["/api/mestre", "/api/narrador"];
}

async function postChannelMessage(endpoint, message) {
  return fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      mode: activeChannel,
    }),
  });
}

async function callChannelApi(message) {
  const endpoints =
    activeChannel === "mestre" ? mestreEndpoints() : ["/api/narracao"];
  let response = null;
  let endpointUsed = endpoints[0];

  for (const endpoint of endpoints) {
    endpointUsed = endpoint;
    response = await postChannelMessage(endpoint, message);
    if (response.ok || (response.status !== 404 && response.status !== 405)) {
      break;
    }
  }

  if (!response.ok) {
    let errorBody = null;
    const contentType = response.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      try {
        errorBody = await response.json();
      } catch (error) {
        errorBody = null;
      }
    } else {
      errorBody = await response.text();
    }

    const serverMessage =
      typeof errorBody === "string"
        ? errorBody
        : errorBody?.error || errorBody?.reply || errorBody?.message || "";
    if (response.status === 405 || response.status === 404) {
      throw new Error(
        `Endpoint ${endpointUsed} indisponivel (${response.status}). Reinicie a API (python scripts/narracao_api.py ou docker compose restart motor).`,
      );
    }
    throw new Error(serverMessage || `Falha ${response.status}`);
  }

  const data = await response.json();
  if (Array.isArray(data.update_proposals) && data.update_proposals.length > 0) {
    pendingProposals = data.update_proposals;
    updateProposalsBadge();
  }
  return data.reply || "Sem resposta do servidor.";
}

async function fetchPendingProposals() {
  const response = await fetch(`${API_BASE}/api/proposals`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar propostas: ${response.status}`);
  }
  const data = await response.json();
  pendingProposals = Array.isArray(data.proposals) ? data.proposals : [];
  updateProposalsBadge();
  return pendingProposals;
}

async function saveProposals(proposalIds, approved = true) {
  const response = await fetch(`${API_BASE}/api/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ proposal_ids: proposalIds, approved }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || data.validation_issues?.[0]?.message || `Falha ${response.status}`);
  }
  return data;
}

function updateProposalsBadge() {
  const count = pendingProposals.length;
  proposalsBadge.textContent = String(count);
  proposalsBadge.classList.toggle("is-hidden", count === 0);
  btnPropostas.classList.toggle("has-badge", count > 0);
}

function renderProposals() {
  proposalsList.innerHTML = "";
  if (pendingProposals.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Nenhuma proposta pendente.";
    proposalsList.appendChild(li);
    return;
  }

  pendingProposals.forEach((proposal) => {
    const li = document.createElement("li");
    li.className = "proposal-item";

    const title = document.createElement("strong");
    title.textContent = `${proposal.change_type} → ${proposal.target_path}`;

    const detail = document.createElement("p");
    detail.className = "proposal-detail";
    const payload = proposal.payload || {};
    const payloadHint =
      payload.personagem || payload.name || payload.text || payload.content || "";
    detail.textContent =
      proposal.rationale ||
      payloadHint ||
      JSON.stringify(proposal.payload);

    const meta = document.createElement("p");
    meta.className = "proposal-meta";
    meta.textContent = `confianca ${Math.round((proposal.confidence || 0) * 100)}%`;

    const actions = document.createElement("div");
    actions.className = "proposal-item-actions";

    const approveBtn = document.createElement("button");
    approveBtn.type = "button";
    approveBtn.className = "proposal-approve";
    approveBtn.textContent = "Aprovar";
    approveBtn.dataset.proposalId = proposal.id;

    const rejectBtn = document.createElement("button");
    rejectBtn.type = "button";
    rejectBtn.className = "proposal-reject";
    rejectBtn.textContent = "Rejeitar";
    rejectBtn.dataset.proposalId = proposal.id;

    actions.appendChild(approveBtn);
    actions.appendChild(rejectBtn);
    li.appendChild(title);
    li.appendChild(detail);
    li.appendChild(meta);
    li.appendChild(actions);
    proposalsList.appendChild(li);
  });
}

async function fetchCharacterProfile() {
  const response = await fetch(`${API_BASE}/api/character-profile`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar ficha: ${response.status}`);
  }
  return response.json();
}

function setMarkdownContent(element, markdownText) {
  element.classList.add("md-content");
  element.innerHTML = renderMarkdown(markdownText);
}

function renderSectionNode(section, container) {
  const article = document.createElement("article");
  article.className = "sheet-card sheet-section";
  article.dataset.level = String(section.level || 2);

  const title = document.createElement(section.level >= 4 ? "h4" : "h3");
  title.textContent = section.title;
  article.appendChild(title);

  if (section.content) {
    const body = document.createElement("div");
    body.className = "sheet-section-body md-content";
    body.innerHTML = renderMarkdown(section.content);
    article.appendChild(body);
  }

  if (Array.isArray(section.children) && section.children.length > 0) {
    const nested = document.createElement("div");
    nested.className = "sheet-subsections";
    section.children.forEach((child) => renderSectionNode(child, nested));
    article.appendChild(nested);
  }

  container.appendChild(article);
}

function renderFicha(profile) {
  fichaSections.innerHTML = "";
  fichaRefs.innerHTML = "";

  const hero = document.createElement("article");
  hero.className = "sheet-card sheet-hero";

  const heroTitle = document.createElement("h3");
  heroTitle.textContent = profile.hero?.title || "Ficha do Personagem";
  hero.appendChild(heroTitle);

  const introText = Array.isArray(profile.hero?.introLines)
    ? profile.hero.introLines.join("\n").trim()
    : "";
  if (introText) {
    const intro = document.createElement("div");
    intro.className = "sheet-section-body sheet-hero-body md-content";
    intro.innerHTML = renderMarkdown(introText);
    hero.appendChild(intro);
  }

  fichaSections.appendChild(hero);

  (profile.sections || []).forEach((section) => {
    renderSectionNode(section, fichaSections);
  });

  const references = profile.references || [];
  if (references.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Sem referencias cruzadas detectadas.";
    fichaRefs.appendChild(li);
  } else {
    references.forEach((ref) => {
      const li = document.createElement("li");
      li.textContent = `${ref.label} (${ref.path})`;
      fichaRefs.appendChild(li);
    });
  }

  fichaStatus.textContent = `Fonte: ${profile.sourceSheet}`;
  if (profile.imageUrl) {
    characterPortrait.src = profile.imageUrl;
    characterPortrait.loading = "eager";
  }
}

async function ensureCharacterProfileLoaded() {
  if (profileLoaded) {
    return;
  }
  try {
    const profile = await fetchCharacterProfile();
    renderFicha(profile);
    profileLoaded = true;
  } catch (err) {
    fichaStatus.textContent =
      "Nao foi possivel carregar a ficha do personagem a partir dos arquivos de referencia.";
    console.error(err);
  }
}

async function fetchJournalEntries() {
  const response = await fetch(`${API_BASE}/api/journal/${CHARACTER_ID}`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar journal: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data.entries) ? data.entries : [];
}

async function saveJournalEntry(text) {
  const payload = {
    timestamp: new Date().toLocaleString("pt-BR"),
    text,
  };
  const response = await fetch(`${API_BASE}/api/journal/${CHARACTER_ID}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    throw new Error(`Falha ao salvar journal: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data.entries) ? data.entries : [];
}

async function deleteJournalEntry(entryId) {
  const response = await fetch(
    `${API_BASE}/api/journal/${CHARACTER_ID}/${encodeURIComponent(entryId)}`,
    {
      method: "DELETE",
    },
  );
  if (!response.ok) {
    throw new Error(`Falha ao excluir entrada: ${response.status}`);
  }
  const data = await response.json();
  return Array.isArray(data.entries) ? data.entries : [];
}

function renderJournal() {
  journalList.innerHTML = "";
  if (journalEntries.length === 0) {
    const li = document.createElement("li");
    li.textContent = "Sem entradas ainda.";
    journalList.appendChild(li);
    return;
  }

  journalEntries
    .slice()
    .reverse()
    .forEach((entry) => {
      const li = document.createElement("li");
      li.className = "journal-item";

      const text = document.createElement("span");
      text.className = "journal-item-text";
      text.textContent = `${entry.timestamp} - ${entry.text}`;

      const removeBtn = document.createElement("button");
      removeBtn.type = "button";
      removeBtn.className = "journal-delete";
      removeBtn.textContent = "Excluir";
      removeBtn.dataset.entryId = entry.id || "";

      li.appendChild(text);
      li.appendChild(removeBtn);
      journalList.appendChild(li);
    });
}

async function fetchCampaignBrief() {
  const response = await fetch(`${API_BASE}/api/brief`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar brief: ${response.status}`);
  }
  return response.json();
}

function renderOpeningMessage(openingText) {
  if (openingRendered || !openingText) {
    return;
  }
  const card = document.createElement("article");
  card.className = "narration-card system reveal";
  const p = document.createElement("p");
  p.textContent = openingText;
  card.appendChild(p);
  narrationFeed.prepend(card);
  openingRendered = true;
}

function openBriefDetail(briefItem) {
  briefDrawerTitle.textContent = briefItem.title;
  setMarkdownContent(briefDrawerBody, briefItem.detail || briefItem.teaser || "");
  const sources = Array.isArray(briefItem.sources) ? briefItem.sources : [];
  briefDrawerSources.textContent = sources.length
    ? `Fontes: ${sources.join(" · ")}`
    : "";
  openDrawer(briefDrawer);
}

function renderBriefButtons(briefData) {
  storyBrief.innerHTML = "";
  const items = Array.isArray(briefData?.briefs) ? briefData.briefs : [];
  if (items.length === 0) {
    const hint = document.createElement("p");
    hint.className = "utility-hint";
    hint.textContent = "Resumo da campanha indisponivel.";
    storyBrief.appendChild(hint);
    return;
  }

  items.forEach((item) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "brief-btn";
    button.dataset.briefId = item.id;

    const title = document.createElement("span");
    title.className = "brief-btn-title";
    title.textContent = item.title;

    const teaser = document.createElement("span");
    teaser.className = "brief-btn-teaser";
    teaser.textContent = item.teaser || "Ver detalhes";

    button.appendChild(title);
    button.appendChild(teaser);
    button.addEventListener("click", () => openBriefDetail(item));
    storyBrief.appendChild(button);
  });
}

async function refreshBrief() {
  try {
    campaignBrief = await fetchCampaignBrief();
    renderBriefButtons(campaignBrief);
    renderOpeningMessage(campaignBrief.opening);
  } catch (err) {
    console.error(err);
    storyBrief.innerHTML =
      '<p class="utility-hint">Nao foi possivel carregar o resumo da campanha.</p>';
  }
}

async function fetchNpcCatalog() {
  const response = await fetch(`${API_BASE}/api/npcs`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar NPCs: ${response.status}`);
  }
  return response.json();
}

function renderNpcSubmenu(npcs) {
  npcSubmenu.innerHTML = "";
  const featured = npcs.filter((npc) => npc.featured).slice(0, 6);
  const list = featured.length > 0 ? featured : npcs.slice(0, 6);
  list.forEach((npc) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item";
    button.textContent = npc.name;
    button.addEventListener("click", () => {
      npcSubmenu.classList.add("is-hidden");
      btnNpcs.setAttribute("aria-expanded", "false");
      openNpcDetail(npc);
    });
    li.appendChild(button);
    npcSubmenu.appendChild(li);
  });
  const more = document.createElement("li");
  const moreBtn = document.createElement("button");
  moreBtn.type = "button";
  moreBtn.className = "submenu-item submenu-more";
  moreBtn.textContent = "Ver todos...";
  moreBtn.addEventListener("click", () => {
    npcSubmenu.classList.add("is-hidden");
    btnNpcs.setAttribute("aria-expanded", "false");
    openNpcCatalogDrawer();
  });
  more.appendChild(moreBtn);
  npcSubmenu.appendChild(more);
}

function buildNpcCard(npc) {
  const card = document.createElement("article");
  card.className = "npc-card";
  card.tabIndex = 0;

  const media = document.createElement("div");
  media.className = "npc-card-media";
  const img = document.createElement("img");
  img.className = "npc-card-image";
  img.alt = `Retrato de ${npc.name}`;
  img.loading = "lazy";
  img.src = npc.imageUrl || npc.tokenUrl;
  media.appendChild(img);

  const body = document.createElement("div");
  body.className = "npc-card-body";
  const title = document.createElement("h3");
  title.textContent = npc.name;
  body.appendChild(title);

  if (npc.role) {
    const role = document.createElement("p");
    role.className = "npc-card-role";
    role.textContent = npc.role;
    body.appendChild(role);
  }
  if (npc.relation) {
    const relation = document.createElement("p");
    relation.className = "npc-card-relation";
    relation.textContent = `Relacao: ${npc.relation}`;
    body.appendChild(relation);
  }
  const summary = document.createElement("div");
  summary.className = "npc-card-summary md-content";
  summary.innerHTML = renderMarkdown(npc.summary || "Sem resumo disponivel.");
  body.appendChild(summary);

  card.appendChild(media);
  card.appendChild(body);
  card.addEventListener("click", () => openNpcDetail(npc));
  card.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openNpcDetail(npc);
    }
  });
  return card;
}

function openNpcDetail(npc) {
  npcDrawerTitle.textContent = npc.name;
  npcCatalog.innerHTML = "";
  npcCatalog.appendChild(buildNpcCard(npc));
  npcDrawerStatus.textContent = npc.sheetPath
    ? `Ficha: ${npc.sheetPath}`
    : "Sem ficha vinculada.";
  openDrawer(npcDrawer);
}

function renderNpcCatalog(npcs) {
  npcCatalog.innerHTML = "";
  npcs.forEach((npc) => {
    npcCatalog.appendChild(buildNpcCard(npc));
  });
}

async function openNpcCatalogDrawer() {
  try {
    if (npcCatalogData.length === 0) {
      const data = await fetchNpcCatalog();
      npcCatalogData = Array.isArray(data.npcs) ? data.npcs : [];
    }
    npcDrawerTitle.textContent = "NPCs da Campanha";
    npcDrawerStatus.textContent = `${npcCatalogData.length} personagens carregados dos arquivos da campanha.`;
    renderNpcCatalog(npcCatalogData);
    openDrawer(npcDrawer);
  } catch (err) {
    console.error(err);
    npcDrawerStatus.textContent = "Nao foi possivel carregar o catalogo de NPCs.";
  }
}

async function ensureNpcCatalogLoaded() {
  try {
    const data = await fetchNpcCatalog();
    npcCatalogData = Array.isArray(data.npcs) ? data.npcs : [];
    renderNpcSubmenu(npcCatalogData);
  } catch (err) {
    console.error(err);
    npcSubmenu.innerHTML =
      '<li><span class="submenu-empty">NPCs indisponiveis</span></li>';
  }
}

function openDrawer(drawer) {
  ALL_DRAWERS.forEach((item) => {
    if (item !== drawer) {
      item.classList.add("is-hidden");
    }
  });
  drawer.classList.remove("is-hidden");
  document.body.classList.add("sheet-active");
}

function closeDrawer(drawer) {
  drawer.classList.add("is-hidden");
  const hasOpenSheet = ALL_DRAWERS.some(
    (item) => !item.classList.contains("is-hidden"),
  );
  if (!hasOpenSheet) {
    document.body.classList.remove("sheet-active");
  }
}

function updateMestreButton() {
  const active = activeChannel === "mestre";
  btnNarrador.classList.toggle("is-active", active);
  if (active) {
    btnNarrador.textContent = "Mestre (ON)";
    chatModeLabel.textContent = "Canal atual: Mestre off-game";
    playerInput.placeholder = "Fale com o Mestre (off-game): duvidas, canon, ajustes...";
  } else {
    btnNarrador.textContent = "Mestre";
    chatModeLabel.textContent = "Canal atual: Narracao principal";
    playerInput.placeholder = "Digite sua acao...";
  }

  narrationFeed.classList.toggle("is-hidden", active);
  narratorFeed.classList.toggle("is-hidden", !active);
}

btnFicha.addEventListener("click", async () => {
  await ensureCharacterProfileLoaded();
  openDrawer(fichaDrawer);
});
btnJournal.addEventListener("click", async () => {
  try {
    journalEntries = await fetchJournalEntries();
  } catch (err) {
    console.error(err);
  }
  renderJournal();
  openDrawer(journalDrawer);
  journalInput.focus();
});
btnNarrador.addEventListener("click", () => {
  activeChannel = activeChannel === "mestre" ? "narracao" : "mestre";
  updateMestreButton();
});
btnNpcs.addEventListener("click", (event) => {
  event.stopPropagation();
  const isOpen = !npcSubmenu.classList.contains("is-hidden");
  npcSubmenu.classList.toggle("is-hidden", isOpen);
  btnNpcs.setAttribute("aria-expanded", isOpen ? "false" : "true");
});

btnAdmin.addEventListener("click", () => openDrawer(adminDrawer));

btnPropostas.addEventListener("click", async () => {
  try {
    await fetchPendingProposals();
  } catch (err) {
    console.error(err);
  }
  renderProposals();
  openDrawer(proposalsDrawer);
});

closeFichaBtn.addEventListener("click", () => closeDrawer(fichaDrawer));
closeJournalBtn.addEventListener("click", () => closeDrawer(journalDrawer));
closeProposalsBtn.addEventListener("click", () => closeDrawer(proposalsDrawer));
closeBriefBtn.addEventListener("click", () => closeDrawer(briefDrawer));
closeNpcBtn.addEventListener("click", () => closeDrawer(npcDrawer));
closeAdminBtn.addEventListener("click", () => closeDrawer(adminDrawer));

const drawerByKey = {
  ficha: fichaDrawer,
  journal: journalDrawer,
  proposals: proposalsDrawer,
  brief: briefDrawer,
  npcs: npcDrawer,
  admin: adminDrawer,
};

document.querySelectorAll(".sheet-backdrop").forEach((backdrop) => {
  backdrop.addEventListener("click", () => {
    const target = backdrop.getAttribute("data-close");
    if (target && drawerByKey[target]) {
      closeDrawer(drawerByKey[target]);
    }
  });
});

document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }
  if (!btnNpcs.contains(target) && !npcSubmenu.contains(target)) {
    npcSubmenu.classList.add("is-hidden");
    btnNpcs.setAttribute("aria-expanded", "false");
  }
  const closeType = target.getAttribute("data-close");
  if (closeType && drawerByKey[closeType]) {
    closeDrawer(drawerByKey[closeType]);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  ALL_DRAWERS.forEach((drawer) => closeDrawer(drawer));
  npcSubmenu.classList.add("is-hidden");
  btnNpcs.setAttribute("aria-expanded", "false");
});

approveAllProposalsBtn.addEventListener("click", async () => {
  if (pendingProposals.length === 0) {
    return;
  }
  try {
    await saveProposals(pendingProposals.map((item) => item.id), true);
    pendingProposals = await fetchPendingProposals();
    renderProposals();
    updateProposalsBadge();
    await refreshBrief();
  } catch (err) {
    console.error(err);
    window.alert(extractFriendlyError(err));
  }
});

proposalsList.addEventListener("click", async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) {
    return;
  }
  const proposalId = target.dataset.proposalId;
  if (!proposalId) {
    return;
  }
  const approved = target.classList.contains("proposal-approve");
  try {
    await saveProposals([proposalId], approved);
    pendingProposals = await fetchPendingProposals();
    renderProposals();
    updateProposalsBadge();
    if (approved) {
      await refreshBrief();
    }
  } catch (err) {
    console.error(err);
    window.alert(extractFriendlyError(err));
  }
});

renderJournal();
fetchPendingProposals().catch((err) => console.error(err));
updateMestreButton();
ensureCharacterProfileLoaded();
refreshBrief();
ensureNpcCatalogLoaded();

journalForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const note = journalInput.value.trim();
  if (!note) {
    return;
  }

  try {
    journalEntries = await saveJournalEntry(note);
    renderJournal();
  } catch (err) {
    console.error(err);
    return;
  }

  journalInput.value = "";
  journalInput.focus();
});

journalList.addEventListener("click", async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) {
    return;
  }
  if (!target.classList.contains("journal-delete")) {
    return;
  }
  const entryId = target.dataset.entryId;
  if (!entryId) {
    return;
  }

  const confirmed = window.confirm("Deseja excluir esta anotacao do journal?");
  if (!confirmed) {
    return;
  }

  try {
    journalEntries = await deleteJournalEntry(entryId);
    renderJournal();
  } catch (err) {
    console.error(err);
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = playerInput.value.trim();
  if (!message) {
    return;
  }

  const channelLabel = activeChannel === "mestre" ? "MESTRE" : "HISTORIA";
  appendCard(`[${channelLabel}] VOCE: ${message}`, "player");
  setChatBusy(true);
  createLoadingCard("Consultando o provider...");

  try {
    const reply = await callChannelApi(message);
    const prefix =
      activeChannel === "mestre" ? "MESTRE (OFF-GAME)" : "NARRADOR";
    const parsedNpc = parseNpcReply(reply);
    if (parsedNpc.isNpc) {
      try {
        const npcAsset = await fetchNpcAsset(parsedNpc.name, parsedNpc.gender);
        appendCard(`${parsedNpc.name}: ${parsedNpc.text}`, "system", {
          npcName: parsedNpc.name,
          npcTokenUrl: npcAsset.tokenUrl,
          npcImageUrl: npcAsset.imageUrl,
        });
      } catch (assetErr) {
        console.error(assetErr);
        appendCard(`${parsedNpc.name}: ${parsedNpc.text}`, "system");
      }
    } else {
      appendCard(`${prefix}: ${reply}`, "system");
    }
  } catch (err) {
    const fallbackPrefix =
      activeChannel === "mestre" ? "MESTRE (OFF-GAME)" : "NARRADOR";
    appendCard(`${fallbackPrefix}: ${extractFriendlyError(err)}`, "private");
    console.error(err);
  } finally {
    removeLoadingCard();
    setChatBusy(false);
  }

  playerInput.value = "";
  playerInput.focus();
});
