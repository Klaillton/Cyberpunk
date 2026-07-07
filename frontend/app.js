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

function renderSectionNode(section, container) {
  const article = document.createElement("article");
  article.className = "sheet-card sheet-section";
  article.dataset.level = String(section.level || 2);

  const title = document.createElement(section.level >= 4 ? "h4" : "h3");
  title.textContent = section.title;
  article.appendChild(title);

  if (section.content) {
    const body = document.createElement("div");
    body.className = "sheet-section-body";
    body.textContent = section.content;
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
    intro.className = "sheet-section-body sheet-hero-body";
    intro.textContent = introText;
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

function openDrawer(drawer) {
  closeDrawer(fichaDrawer);
  closeDrawer(journalDrawer);
  closeDrawer(proposalsDrawer);
  drawer.classList.remove("is-hidden");
  document.body.classList.add("sheet-active");
}

function closeDrawer(drawer) {
  drawer.classList.add("is-hidden");
  const hasOpenSheet =
    !fichaDrawer.classList.contains("is-hidden") ||
    !journalDrawer.classList.contains("is-hidden") ||
    !proposalsDrawer.classList.contains("is-hidden");
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

document.querySelectorAll(".sheet-backdrop").forEach((backdrop) => {
  backdrop.addEventListener("click", () => {
    const target = backdrop.getAttribute("data-close");
    if (target === "ficha") {
      closeDrawer(fichaDrawer);
    } else if (target === "journal") {
      closeDrawer(journalDrawer);
    } else if (target === "proposals") {
      closeDrawer(proposalsDrawer);
    }
  });
});

document.addEventListener("click", (event) => {
  const target = event.target;
  if (!(target instanceof Element)) {
    return;
  }
  const closeType = target.getAttribute("data-close");
  if (closeType === "ficha") {
    closeDrawer(fichaDrawer);
  }
  if (closeType === "journal") {
    closeDrawer(journalDrawer);
  }
  if (closeType === "proposals") {
    closeDrawer(proposalsDrawer);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  closeDrawer(fichaDrawer);
  closeDrawer(journalDrawer);
  closeDrawer(proposalsDrawer);
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
  } catch (err) {
    console.error(err);
    window.alert(extractFriendlyError(err));
  }
});

renderJournal();
fetchPendingProposals().catch((err) => console.error(err));
updateMestreButton();
ensureCharacterProfileLoaded();

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
