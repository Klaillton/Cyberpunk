const chatForm = document.getElementById("chatForm");
const playerInput = document.getElementById("playerInput");
const narrationFeed = document.getElementById("narrationFeed");
const chatModeLabel = document.getElementById("chatModeLabel");
const btnFicha = document.getElementById("btnFicha");
const btnJournal = document.getElementById("btnJournal");
const btnCanalNarracao = document.getElementById("btnCanalNarracao");
const btnCanalMestre = document.getElementById("btnCanalMestre");
const btnCanalSistema = document.getElementById("btnCanalSistema");
const channelButtons = [btnCanalNarracao, btnCanalMestre, btnCanalSistema];
const apiStatusBanner = document.getElementById("apiStatusBanner");
const mestreFeed = document.getElementById("mestreFeed");
const sistemaFeed = document.getElementById("sistemaFeed");
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
const briefSidebar = document.getElementById("briefSidebar");
const briefDrawer = document.getElementById("briefDrawer");
const briefDrawerTitle = document.getElementById("briefDrawerTitle");
const briefDrawerBody = document.getElementById("briefDrawerBody");
const briefDrawerSources = document.getElementById("briefDrawerSources");
const closeBriefBtn = document.getElementById("closeBriefBtn");
const btnComandos = document.getElementById("btnComandos");
const commandsSubmenu = document.getElementById("commandsSubmenu");
const commandsDrawer = document.getElementById("commandsDrawer");
const commandsCatalog = document.getElementById("commandsCatalog");
const closeCommandsBtn = document.getElementById("closeCommandsBtn");
const btnNpcs = document.getElementById("btnNpcs");
const npcSubmenu = document.getElementById("npcSubmenu");
const btnRouting = document.getElementById("btnRouting");
const routingDrawer = document.getElementById("routingDrawer");
const closeRoutingBtn = document.getElementById("closeRoutingBtn");
const routingPolicyLine = document.getElementById("routingPolicyLine");
const routingPreviewInput = document.getElementById("routingPreviewInput");
const routingCloudApproval = document.getElementById("routingCloudApproval");
const routingPreviewBtn = document.getElementById("routingPreviewBtn");
const routingPreviewStatus = document.getElementById("routingPreviewStatus");
const routingPreviewResult = document.getElementById("routingPreviewResult");
const btnAdmin = document.getElementById("btnAdmin");
const npcDrawer = document.getElementById("npcDrawer");
const npcDrawerTitle = document.getElementById("npcDrawerTitle");
const npcDrawerStatus = document.getElementById("npcDrawerStatus");
const npcCatalog = document.getElementById("npcCatalog");
const closeNpcBtn = document.getElementById("closeNpcBtn");
const adminDrawer = document.getElementById("adminDrawer");
const closeAdminBtn = document.getElementById("closeAdminBtn");
const btnGroupCampanha = document.getElementById("btnGroupCampanha");
const campanhaSubmenu = document.getElementById("campanhaSubmenu");
const btnGroupPersonagem = document.getElementById("btnGroupPersonagem");
const personagemSubmenu = document.getElementById("personagemSubmenu");
const btnGroupSessao = document.getElementById("btnGroupSessao");
const sessaoSubmenu = document.getElementById("sessaoSubmenu");
const btnGroupCanais = document.getElementById("btnGroupCanais");
const canaisSubmenu = document.getElementById("canaisSubmenu");

let activeChannel = "narracao";
const CHARACTER_ID = "ryan_wireghost_voss";
const RYAN_TOKEN_URL = `/api/character-image/${CHARACTER_ID}?variant=token`;
const RYAN_IMAGE_URL = `/api/character-image/${CHARACTER_ID}`;
const API_BASE =
  window.location.protocol.startsWith("http") && window.location.host
    ? `${window.location.protocol}//${window.location.host}`
    : "http://127.0.0.1:8787";
const modeButtons = [btnFicha, btnJournal, btnPropostas];
let profileLoaded = false;
let journalEntries = [];
let pendingProposals = [];
let activeLoadingCard = null;
let activeLoadingFeed = null;
let campaignBrief = null;
let npcCatalogData = [];
let sessionCommandsData = null;
let openingRendered = false;
let apiHealth = null;

const SESSION_COMMANDS_FALLBACK = {
  quick: [
    {
      id: "resumo_sessao",
      label: "Resumo da Sessão",
      text: "[Resumo da Sessão]",
    },
    {
      id: "pulso_1_dia",
      label: "Passar 1 dia (Pulso do Mundo)",
      text: "[Passagem de tempo — passou 1 dia in-game. Rodar o Pulso do Mundo conforme pulso_procedimento.md e narrar o que Ryan percebe ao retomar a cena.]",
    },
    {
      id: "finalizar_sessao",
      label: "Finalizar sessão e gerar resumo",
      text: "[Finalizar sessão e gerar resumo]",
    },
  ],
  categories: [
    {
      title: "Resumo e encerramento",
      commands: [
        {
          label: "Resumo da Sessão",
          text: "[Resumo da Sessão]",
          description: "Gera resumo estruturado da sessao atual.",
        },
        {
          label: "Finalizar sessão e gerar resumo",
          text: "[Finalizar sessão e gerar resumo]",
          description: "Encerra a sessao e propoe salvar o resumo.",
        },
      ],
    },
  ],
};

const CHANNEL_ENDPOINTS = {
  narracao: ["/api/narracao"],
  mestre: ["/api/mestre", "/api/narrador"],
  sistema: ["/api/sistema"],
};

const CHANNEL_LABELS = {
  narracao: { player: "HISTORIA", reply: "NARRADOR", name: "Narracao principal" },
  mestre: { player: "MESTRE", reply: "MESTRE (OFF-GAME)", name: "Mestre off-game" },
  sistema: { player: "SISTEMA", reply: "SISTEMA", name: "Sistema (meta-tecnico)" },
};

const ROUTING_PREVIEW_CHANNELS = {
  narracao: "narracao",
  mestre: "narrador",
  sistema: "gestor",
};

const ALL_DRAWERS = [
  fichaDrawer,
  journalDrawer,
  proposalsDrawer,
  routingDrawer,
  briefDrawer,
  commandsDrawer,
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

function normalizeAssetUrl(url) {
  const raw = String(url || "").trim();
  if (!raw) return raw;
  if (/^https?:\/\//i.test(raw) || raw.startsWith("/api/")) return raw;
  if (raw.startsWith("../imagens/")) return `/imagens/${raw.slice("../imagens/".length)}`;
  if (raw.startsWith("./imagens/")) return `/imagens/${raw.slice("./imagens/".length)}`;
  if (raw.startsWith("imagens/")) return `/${raw}`;
  if (raw.startsWith("/imagens/")) return raw;
  return raw;
}

function renderInlineMarkdown(text) {
  let html = escapeHtml(text);
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(
    /`([^`]+)`/g,
    "<code class=\"md-inline-code\">$1</code>",
  );
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_match, alt, src) => {
    const resolved = escapeHtml(normalizeAssetUrl(src));
    return `<img class="md-inline-image" src="${resolved}" alt="${alt}" loading="lazy" />`;
  });
  html = html.replace(
    /\[([^\]]+)\]\(([^)]+)\)/g,
    (_match, label, href) => {
      const resolved = normalizeAssetUrl(href);
      return `<a href="${resolved}" target="_blank" rel="noreferrer">${label}</a>`;
    },
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

    const imageOnly = trimmed.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if (imageOnly) {
      const src = escapeHtml(normalizeAssetUrl(imageOnly[2]));
      parts.push(
        `<figure class="md-figure"><img class="md-image" src="${src}" alt="${escapeHtml(imageOnly[1])}" loading="lazy" /></figure>`,
      );
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

const SPEAKER_ALIASES = [
  { pattern: /tio\s+gringo/i, name: "Tio Gringo", gender: "male" },
  { pattern: /\bvalk\b|lena\s*[\"']?valk/i, name: "Lena Valk", gender: "female" },
  { pattern: /\breyes\b/i, name: "Reyes", gender: "male" },
  { pattern: /\bmara\b/i, name: "Mara", gender: "female" },
  { pattern: /\belias\b/i, name: "Elias", gender: "male" },
  { pattern: /\btomas\b/i, name: "Tomas", gender: "male" },
  { pattern: /\bsasha\b/i, name: "Sasha", gender: "female" },
  { pattern: /\blira\b/i, name: "Lira", gender: "female" },
  { pattern: /\blina\b/i, name: "Lina", gender: "female" },
];

function resolveSpeakerFromCatalog(name) {
  const norm = normalizeName(name);
  if (!norm || !npcCatalogData.length) {
    return null;
  }
  const hit = npcCatalogData.find((npc) => {
    const npcNorm = normalizeName(npc.name);
    return npcNorm.includes(norm) || norm.includes(npcNorm);
  });
  if (!hit) {
    return null;
  }
  return {
    name: hit.name,
    gender: (hit.gender || "male").toLowerCase() === "female" ? "female" : "male",
  };
}

function detectSpeaker(contextText) {
  const slice = String(contextText || "").slice(-180);
  for (const alias of SPEAKER_ALIASES) {
    if (alias.pattern.test(slice)) {
      return { name: alias.name, gender: alias.gender };
    }
  }
  const nameMatch = slice.match(
    /\b((?:Tio\s+Gringo|Lena\s*[\"']?Valk|Reyes|Mara|Elias|Tomas|Sasha|Lira|Lina))\b/i,
  );
  if (nameMatch) {
    return resolveSpeakerFromCatalog(nameMatch[1]) || {
      name: nameMatch[1],
      gender: "male",
    };
  }
  return null;
}

function parseNpcTaggedLine(line) {
  const tagged = line.match(/^\[(NPC(?:-F|-M)?)\s*:\s*([^\]]+)\]\s*(.+)$/i);
  if (!tagged) {
    return null;
  }
  const tag = tagged[1].toUpperCase();
  const body = tagged[3].trim();
  const quotedLead = body.match(/^"([^"]+)"\s*(.*)$/s);
  const quoted = quotedLead ? null : body.match(/^"([^"]+)"$/);
  const starred = body.match(/^\*([^*]+)\*$/);
  const explicitAction = /^\(acao\)\s*/i.test(body);
  const speechText = quotedLead
    ? quotedLead[1]
    : quoted
      ? quoted[1]
      : starred
        ? starred[1].trim()
        : body.replace(/^\(acao\)\s*/i, "").trim();
  const remainder = quotedLead ? quotedLead[2].trim() : "";
  const rawName = tagged[2].trim();
  const resolved = resolveSpeakerFromCatalog(rawName);
  return {
    type: "npc",
    name: resolved?.name || rawName,
    gender: tag.includes("-F") ? "female" : resolved?.gender || "male",
    text: speechText,
    action: Boolean(starred || explicitAction),
    remainder,
  };
}

function isAttributionTail(text) {
  const trimmed = String(text || "").trim();
  return /^,\s*(diz|disse|fala|murmura|sussurra|pergunta|responde|continua|completa|adiciona|grita|nota)\b/i.test(
    trimmed,
  );
}

function isOrphanTagFragment(text) {
  const trimmed = String(text || "").trim();
  return /^[A-ZÀ-Ú][A-Za-zÀ-ú]{0,24}\]$/.test(trimmed) || /^\[NPC[^\]]*$/i.test(trimmed);
}

const NPC_SPEAKER_TAG_RE =
  /\[(?:NPC(?:-F|-M)?|[A-ZÀ-Ú][A-Za-zÀ-ú ."']+?(?:-F|-M)?)\s*:\s*([^\]]+)\]/gi;

function genderFromTagToken(tagToken) {
  if (/-F\b/i.test(tagToken)) {
    return "female";
  }
  if (/-M\b/i.test(tagToken)) {
    return "male";
  }
  return "male";
}

function extractNpcSpeechAfterTag(text, startIndex, rawName, tagToken) {
  const gender = genderFromTagToken(tagToken);
  const resolved = resolveSpeakerFromCatalog(rawName.trim());
  const name = resolved?.name || rawName.trim();
  const resolvedGender = resolved?.gender || gender;
  let rest = text.slice(startIndex).trimStart();
  let consumed = startIndex + (text.slice(startIndex).length - rest.length);

  const quoted = rest.match(/^"([^"]+)"/);
  if (quoted) {
    consumed += quoted[0].length;
    return {
      segment: {
        type: "npc",
        name,
        gender: resolvedGender,
        text: quoted[1].trim(),
        action: false,
      },
      endIndex: consumed,
    };
  }

  const nextTag = rest.search(
    /\[(?:NPC(?:-F|-M)?|[A-ZÀ-Ú][A-Za-zÀ-ú]+(?:-F|-M)?)\s*:/i,
  );
  const chunk = (nextTag >= 0 ? rest.slice(0, nextTag) : rest).trim();
  const speech = chunk.replace(/^[,;:\s]+/, "").trim();
  consumed += nextTag >= 0 ? nextTag : rest.length;
  return {
    segment: {
      type: "npc",
      name,
      gender: resolvedGender,
      text: speech,
      action: false,
    },
    endIndex: consumed,
  };
}

function segmentNarrationByNpcTags(text) {
  const tagRe = new RegExp(NPC_SPEAKER_TAG_RE.source, "gi");
  const segments = [];
  let lastIndex = 0;
  let match;

  while ((match = tagRe.exec(text)) !== null) {
    const narration = text.slice(lastIndex, match.index).trim();
    if (narration && !isOrphanTagFragment(narration)) {
      segments.push({ type: "narration", text: narration });
    }
    const extracted = extractNpcSpeechAfterTag(
      text,
      match.index + match[0].length,
      match[1],
      match[0],
    );
    if (extracted.segment.text) {
      segments.push(extracted.segment);
    }
    lastIndex = extracted.endIndex;
    tagRe.lastIndex = lastIndex;
  }

  const tail = text.slice(lastIndex).trim();
  if (tail && !isOrphanTagFragment(tail)) {
    segments.push({ type: "narration", text: tail });
  }
  return segments;
}

function coalesceNarrationSegments(segments) {
  const merged = [];
  segments.forEach((segment) => {
    if (segment.type === "narration" && isOrphanTagFragment(segment.text)) {
      return;
    }
    if (
      segment.type === "narration" &&
      isAttributionTail(segment.text) &&
      merged.length > 0
    ) {
      const previous = merged[merged.length - 1];
      const tail = segment.text.replace(/^,\s*/, "").trim();
      if (previous.type === "narration") {
        previous.text = `${previous.text} ${tail}`.trim();
        return;
      }
      if (previous.type === "npc") {
        merged.push({ type: "narration", text: tail });
        return;
      }
    }
    merged.push({ ...segment });
  });
  return merged.filter(
    (segment) => segment.type !== "narration" || segment.text.trim().length > 0,
  );
}

function segmentNarrationReply(reply) {
  const text = String(reply || "").trim();
  if (!text) {
    return [{ type: "narration", text: "" }];
  }

  if (
    /\[(?:NPC(?:-F|-M)?|[A-ZÀ-Ú][A-Za-zÀ-ú]+(?:-F|-M)?)\s*:/i.test(text)
  ) {
    const tagged = segmentNarrationByNpcTags(text);
    if (tagged.length) {
      return coalesceNarrationSegments(tagged);
    }
  }

  const wholeTagged = parseNpcTaggedLine(text);
  if (wholeTagged && text.match(/^\[NPC/i)) {
    return coalesceNarrationSegments([wholeTagged]);
  }

  const segments = [];
  let narrationBuffer = [];

  const flushNarration = () => {
    const chunk = narrationBuffer.join("\n\n").trim();
    if (chunk) {
      segments.push({ type: "narration", text: chunk });
    }
    narrationBuffer = [];
  };

  const paragraphs = text.split(/\n{2,}/);
  paragraphs.forEach((paragraph) => {
    const trimmed = paragraph.trim();
    if (!trimmed) {
      return;
    }

    const lineTagged = parseNpcTaggedLine(trimmed);
    if (lineTagged) {
      flushNarration();
      segments.push(lineTagged);
      if (lineTagged.remainder) {
        narrationBuffer.push(lineTagged.remainder.replace(/^,\s*/, "").trim());
      }
      return;
    }

    const quoteRe = /"([^"]+)"/g;
    let lastIndex = 0;
    let match;
    let foundQuote = false;
    while ((match = quoteRe.exec(trimmed)) !== null) {
      const insideNpcTag = (() => {
        const slice = trimmed.slice(0, match.index);
        const open = slice.lastIndexOf("[NPC");
        if (open < 0) {
          return false;
        }
        return slice.indexOf("]", open) < 0;
      })();
      if (insideNpcTag) {
        continue;
      }
      foundQuote = true;
      const before = trimmed.slice(lastIndex, match.index).trim();
      if (before) {
        narrationBuffer.push(before);
      }
      flushNarration();
      const speakerContext = before.replace(/\[NPC[^\]]*\]/gi, "");
      const speaker =
        detectSpeaker(speakerContext) ||
        detectSpeaker(trimmed.slice(0, match.index).replace(/\[NPC[^\]]*\]/gi, "")) ||
        detectSpeaker(trimmed);
      if (speaker) {
        segments.push({
          type: "npc",
          name: speaker.name,
          gender: speaker.gender,
          text: match[1].trim(),
          action: false,
        });
      } else {
        narrationBuffer.push(`"${match[1].trim()}"`);
      }
      lastIndex = match.index + match[0].length;
    }

    const tail = trimmed.slice(lastIndex).trim();
    if (foundQuote) {
      if (tail && !isAttributionTail(tail)) {
        narrationBuffer.push(tail);
      } else if (tail && isAttributionTail(tail)) {
        narrationBuffer.push(tail.replace(/^,\s*/, "").trim());
      }
      return;
    }

    const speakerLine = trimmed.match(/^([A-ZÀ-Ú][^:]{1,48}):\s*(.+)$/);
    if (speakerLine) {
      const speakerName = speakerLine[1].trim();
      const speakerNorm = normalizeName(speakerName);
      if (!["narrador", "mestre", "historia", "voce", "sistema"].includes(speakerNorm)) {
        flushNarration();
        const resolved = resolveSpeakerFromCatalog(speakerName) || {
          name: speakerName,
          gender: "male",
        };
        segments.push({
          type: "npc",
          name: resolved.name,
          gender: resolved.gender,
          text: speakerLine[2].trim().replace(/^"|"$/g, ""),
          action: false,
        });
        return;
      }
    }

    narrationBuffer.push(trimmed);
  });

  flushNarration();
  if (!segments.length) {
    segments.push({ type: "narration", text });
  }
  return coalesceNarrationSegments(segments);
}

function parseNpcReply(reply) {
  const segments = segmentNarrationReply(reply);
  if (segments.length === 1 && segments[0].type === "npc") {
    return {
      isNpc: true,
      name: segments[0].name,
      gender: segments[0].gender,
      text: segments[0].text,
    };
  }
  return { isNpc: false, text: reply };
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

function isOffGameChannel(channel = activeChannel) {
  return channel === "mestre" || channel === "sistema";
}

function activeFeed(channel = activeChannel) {
  if (channel === "mestre") {
    return mestreFeed;
  }
  if (channel === "sistema") {
    return sistemaFeed;
  }
  return narrationFeed;
}

function updateFeedVisibility(channel = activeChannel) {
  narrationFeed.classList.toggle("is-hidden", channel !== "narracao");
  mestreFeed.classList.toggle("is-hidden", channel !== "mestre");
  sistemaFeed.classList.toggle("is-hidden", channel !== "sistema");
}

function channelMeta(channel = activeChannel) {
  return CHANNEL_LABELS[channel] || CHANNEL_LABELS.narracao;
}

function autoResizeTextarea(textarea) {
  textarea.style.height = "auto";
  textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
}

function bindMultilineSubmit(textarea, onSubmit) {
  textarea.addEventListener("input", () => autoResizeTextarea(textarea));
  textarea.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.shiftKey || textarea.disabled) {
      return;
    }
    event.preventDefault();
    onSubmit();
  });
}

function stripPlayerPrefix(text) {
  return String(text || "")
    .replace(/^\[(?:HISTORIA|HISTÓRIA)\]\s*VOCE:\s*/i, "")
    .replace(/^VOCE:\s*/i, "")
    .trim();
}

function parsePlayerMessage(raw) {
  const text = stripPlayerPrefix(raw);
  const parsed = { actions: [], speeches: [], beats: [] };
  if (!text) {
    return parsed;
  }

  const tagRe = /^\[(ação|acao|fala|beat)\]\s*(.*)$/i;
  const beatInlineRe = /\*([^*]+)\*/g;

  const classifyLine = (line) => {
    const stripped = line.trim();
    if (!stripped) {
      return;
    }
    const tagMatch = stripped.match(tagRe);
    if (tagMatch) {
      const kind = tagMatch[1].toLowerCase().replace("á", "a").replace("ã", "a");
      const content = tagMatch[2].trim().replace(/^"|"$/g, "");
      if (!content) {
        return;
      }
      if (kind === "acao") {
        parsed.actions.push(content);
      } else if (kind === "fala") {
        parsed.speeches.push(content);
      } else {
        parsed.beats.push(content);
      }
      return;
    }
    if (stripped.startsWith("_")) {
      const rest = stripped.slice(1).trim();
      let beatMatch;
      const beats = [];
      const re = /\*([^*]+)\*/g;
      while ((beatMatch = re.exec(rest)) !== null) {
        beats.push(beatMatch[1].trim());
      }
      const speech = rest.replace(/\*[^*]+\*/g, "").trim().replace(/^"|"$/g, "");
      if (speech) {
        parsed.speeches.push(speech);
      }
      parsed.beats.push(...beats.filter(Boolean));
      return;
    }
    if (/^"[^"]+"$/.test(stripped)) {
      parsed.speeches.push(stripped.slice(1, -1).trim());
      return;
    }
    if (/^\*[^*]+\*$/.test(stripped)) {
      parsed.beats.push(stripped.slice(1, -1).trim());
      return;
    }
    const beats = [];
    let beatMatch;
    const re = /\*([^*]+)\*/g;
    while ((beatMatch = re.exec(stripped)) !== null) {
      beats.push(beatMatch[1].trim());
    }
    let remainder = stripped.replace(/\*[^*]+\*/g, "").trim();
    const quoted = remainder.match(/"([^"]+)"/g);
    if (quoted) {
      quoted.forEach((item) => parsed.speeches.push(item.slice(1, -1).trim()));
      remainder = remainder.replace(/"[^"]+"/g, "").trim();
    }
    if (remainder) {
      parsed.actions.push(remainder);
    }
    parsed.beats.push(...beats.filter(Boolean));
  };

  text.split("\n").forEach(classifyLine);
  if (
    parsed.actions.length === 0 &&
    parsed.speeches.length === 0 &&
    parsed.beats.length === 0
  ) {
    parsed.actions.push(text);
  }
  return parsed;
}

function renderPlayerMessageBody(parsed) {
  const parts = [];
  parsed.actions.forEach((item) => {
    parts.push(`<p class="player-action">${escapeHtml(item)}</p>`);
  });
  parsed.speeches.forEach((item) => {
    parts.push(`<p class="player-speech">"${escapeHtml(item)}"</p>`);
  });
  parsed.beats.forEach((item) => {
    parts.push(`<p class="player-beat"><em>${escapeHtml(item)}</em></p>`);
  });
  return parts.join("");
}

function splitSpeakerPrefix(text) {
  const raw = String(text || "");
  const match = raw.match(/^(.+?:)\s*([\s\S]*)$/);
  if (!match) {
    return { prefix: "", body: raw };
  }
  return { prefix: match[1].trim(), body: match[2].trim() };
}

function renderSubmenuFallback(submenu, triggerButton, message) {
  submenu.innerHTML = "";
  prependSubmenuBack(submenu, triggerButton);
  const li = document.createElement("li");
  const span = document.createElement("span");
  span.className = "submenu-empty";
  span.textContent = message;
  li.appendChild(span);
  submenu.appendChild(li);
}

function prependSubmenuBack(submenu, triggerButton) {
  const li = document.createElement("li");
  const button = document.createElement("button");
  button.type = "button";
  button.className = "submenu-item submenu-back";
  button.textContent = "← Voltar";
  button.addEventListener("click", () => {
    submenu.classList.add("is-hidden");
    triggerButton.setAttribute("aria-expanded", "false");
    triggerButton.focus();
  });
  li.appendChild(button);
  submenu.prepend(li);
}

function appendChatToken(card, tokenUrl, imageUrl, altLabel) {
  const tokenLink = document.createElement("a");
  tokenLink.className = "npc-token-link";
  tokenLink.href = imageUrl || tokenUrl;
  tokenLink.target = "_blank";
  tokenLink.rel = "noreferrer";
  tokenLink.title = `Abrir imagem de ${altLabel}`;

  const tokenImg = document.createElement("img");
  tokenImg.className = "npc-token";
  setCoverImage(tokenImg, tokenUrl, 192, 192);
  tokenImg.alt = `Token de ${altLabel}`;
  tokenLink.appendChild(tokenImg);
  card.appendChild(tokenLink);
}

function appendCard(text, role, options = {}) {
  const targetFeed = activeFeed();
  const card = document.createElement("article");
  const cardRole = options.cardRole || role;
  card.className = `narration-card ${role}${cardRole !== role ? ` ${cardRole}` : ""}`;

  if (options.playerTokenUrl) {
    card.classList.add("player-message-card", "has-token");
    appendChatToken(
      card,
      options.playerTokenUrl,
      options.playerImageUrl,
      options.playerName || "Ryan",
    );
  }

  if (options.npcTokenUrl) {
    card.classList.add("npc-message", options.npcAction ? "npc-action" : "npc-speech");
    appendChatToken(
      card,
      options.npcTokenUrl,
      options.npcImageUrl || options.npcTokenUrl,
      options.npcName || "NPC",
    );
  }

  const markdownBody = options.markdownContent || "";
  if (markdownBody) {
    const contentWrap = document.createElement("div");
    contentWrap.className = "message-content";
    const prefix = document.createElement("p");
    prefix.className = "narration-prefix";
    prefix.textContent = text;
    const body = document.createElement("div");
    body.className = "md-content narration-body";
    body.innerHTML = renderMarkdown(markdownBody);
    contentWrap.appendChild(prefix);
    contentWrap.appendChild(body);
    card.appendChild(contentWrap);
  } else if (role === "system" || role === "private") {
    const { prefix, body } = splitSpeakerPrefix(text);
    const contentWrap = document.createElement("div");
    contentWrap.className = "message-content";
    if (prefix) {
      const prefixEl = document.createElement("p");
      prefixEl.className = "narration-prefix";
      prefixEl.textContent = prefix;
      contentWrap.appendChild(prefixEl);
    }
    const bodyEl = document.createElement("div");
    bodyEl.className = "md-content narration-body";
    bodyEl.innerHTML = renderMarkdown(body || text);
    contentWrap.appendChild(bodyEl);
    card.appendChild(contentWrap);
  } else {
    const contentWrap = document.createElement("div");
    contentWrap.className = "message-content";
    const prefixMatch = text.match(/^(\[[^\]]+\]\s*VOCE:)\s*/i);
    const bodyText = prefixMatch ? text.slice(prefixMatch[0].length) : text;
    const parsed = parsePlayerMessage(bodyText);
    if (prefixMatch) {
      const prefixEl = document.createElement("p");
      prefixEl.className = "narration-prefix";
      prefixEl.textContent = prefixMatch[1];
      contentWrap.appendChild(prefixEl);
    }
    const body = document.createElement("div");
    body.className = "player-message-parsed";
    body.innerHTML = renderPlayerMessageBody(parsed);
    contentWrap.appendChild(body);
    card.appendChild(contentWrap);
  }

  if (options.qualityMeta) {
    appendTurnQualityMeta(card, options.qualityMeta);
  }

  targetFeed.appendChild(card);
  card.scrollIntoView({ behavior: "smooth", block: "end" });
}

function createLoadingCard(text) {
  const targetFeed = activeFeed();
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
  const placeholders = {
    narracao: "Digite sua acao...",
    mestre: "Fale com o Mestre (off-game): canon, planos, NPCs...",
    sistema: "Canal Sistema: LLM, API, comandos, arquivos...",
  };
  playerInput.placeholder = isBusy
    ? "Consultando narracao..."
    : placeholders[activeChannel] || placeholders.narracao;
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

const SESSION_SUMMARY_MARKERS = [
  "resumo da sessão",
  "resumo da sessao",
  "criar resumo da sessão atual",
  "criar resumo da sessao atual",
  "finalizar sessão e gerar resumo",
  "finalizar sessao e gerar resumo",
];

function isSessionSummaryCommand(message) {
  const normalized = String(message || "")
    .trim()
    .toLowerCase()
    .replace(/^\[|\]$/g, "");
  return SESSION_SUMMARY_MARKERS.some((marker) => normalized.includes(marker));
}

function feedForChannel(channel) {
  if (channel === "mestre") {
    return mestreFeed;
  }
  if (channel === "sistema") {
    return sistemaFeed;
  }
  return narrationFeed;
}

function shouldSkipHistoryCard(text) {
  const lowered = text.toLowerCase();
  return (
    lowered.includes("canal de narracao esta aberto") ||
    lowered.includes("canal de narração está aberto") ||
    lowered.includes("consultando o provider")
  );
}

function historyBodyText(contentEl) {
  const body = contentEl.querySelector(
    ".narration-body, .md-content, .player-message-parsed",
  );
  return (body?.textContent || "").replace(/\s+/g, " ").trim();
}

function extractCardHistoryText(card) {
  if (
    card.classList.contains("channel-intro") ||
    card.dataset.loading === "true" ||
    card.classList.contains("loading-card")
  ) {
    return null;
  }

  const contentEl = card.querySelector(".message-content");
  if (!contentEl) {
    return null;
  }

  if (card.classList.contains("player") || card.classList.contains("player-message-card")) {
    const bodyText = historyBodyText(contentEl);
    if (!bodyText || shouldSkipHistoryCard(bodyText)) {
      return null;
    }
    return { role: "user", content: bodyText };
  }

  if (card.classList.contains("narrator")) {
    const bodyText = historyBodyText(contentEl);
    if (!bodyText || shouldSkipHistoryCard(bodyText)) {
      return null;
    }
    return { role: "assistant", content: bodyText };
  }

  if (card.classList.contains("npc-speech") || card.classList.contains("npc-action")) {
    const prefix =
      contentEl.querySelector(".narration-prefix")?.textContent?.trim() || "";
    const bodyText = historyBodyText(contentEl);
    if (!bodyText) {
      return null;
    }
    const name = prefix.replace(/\s*\(acao\)\s*$/i, "").trim() || "NPC";
    const tagged = card.classList.contains("npc-action")
      ? `[NPC: ${name}] ${bodyText}`
      : `[NPC: ${name}] "${bodyText}"`;
    return { role: "assistant", content: tagged };
  }

  const prefix =
    contentEl.querySelector(".narration-prefix")?.textContent?.trim() || "";
  const bodyText = historyBodyText(contentEl);
  const combined = [prefix, bodyText].filter(Boolean).join(" ").replace(/\s+/g, " ").trim();
  if (!combined || shouldSkipHistoryCard(combined)) {
    return null;
  }
  if (/VOCE\s*:/i.test(prefix) || /VOCE\s*:/i.test(combined)) {
    return {
      role: "user",
      content: combined.replace(/^(\[[^\]]+\]\s*)?VOCE:\s*/i, "").trim(),
    };
  }
  return {
    role: "assistant",
    content: combined.replace(/^NARRADOR:\s*/i, "").trim(),
  };
}

function extractOpeningSceneContext(feed) {
  const opening = feed.querySelector(".narration-card.opening-scene .opening-body");
  if (!opening) {
    return null;
  }
  const text = opening.textContent?.replace(/\s+/g, " ").trim();
  if (!text || text.length < 24) {
    return null;
  }
  return { role: "assistant", content: `Cena de abertura: ${text}` };
}

function collectChannelHistory(channel, limit = 24) {
  const feed = feedForChannel(channel);
  const cards = feed.querySelectorAll(".narration-card");
  const history = [];
  let pendingAssistant = [];

  const flushAssistant = () => {
    if (!pendingAssistant.length) {
      return;
    }
    history.push({
      role: "assistant",
      content: pendingAssistant.join("\n\n"),
    });
    pendingAssistant = [];
  };

  cards.forEach((card) => {
    const extracted = extractCardHistoryText(card);
    if (!extracted?.content) {
      return;
    }
    if (extracted.role === "user") {
      flushAssistant();
      history.push(extracted);
      return;
    }
    pendingAssistant.push(extracted.content);
  });
  flushAssistant();
  const opening = extractOpeningSceneContext(feed);
  if (opening) {
    history.unshift(opening);
  }
  return history.slice(-limit);
}

function buildRequestOptions(message) {
  const summaryCommand = isSessionSummaryCommand(message);
  if (
    activeChannel === "narracao" ||
    activeChannel === "mestre" ||
    activeChannel === "sistema" ||
    summaryCommand
  ) {
    return {
      history: collectChannelHistory(activeChannel),
      forceHistory: summaryCommand,
    };
  }
  return {};
}

async function postChannelMessage(endpoint, message, options = {}) {
  const payload = {
    message,
    mode: activeChannel,
  };
  if (options.history?.length || options.forceHistory) {
    payload.history = options.history || [];
  }
  return fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

async function callChannelApi(message, requestOptions = {}) {
  const endpoints = CHANNEL_ENDPOINTS[activeChannel] || CHANNEL_ENDPOINTS.narracao;
  let response = null;
  let endpointUsed = endpoints[0];

  for (const endpoint of endpoints) {
    endpointUsed = endpoint;
    response = await postChannelMessage(endpoint, message, requestOptions);
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
  return {
    reply: data.reply || "Sem resposta do servidor.",
    meta: data,
  };
}

function routingPreviewChannel() {
  return ROUTING_PREVIEW_CHANNELS[activeChannel] || "narracao";
}

async function fetchRoutingPolicy() {
  const response = await fetch(`${API_BASE}/api/routing/policy`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Falha ao carregar politica: ${response.status}`);
  }
  return response.json();
}

async function fetchRoutingPreview(message) {
  const response = await fetch(`${API_BASE}/api/routing/preview`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      channel: routingPreviewChannel(),
      user_approved_cloud: routingCloudApproval.checked,
    }),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Falha ${response.status}`);
  }
  return data;
}

function renderRoutingPolicy(policy) {
  if (!policy) {
    routingPolicyLine.textContent = "Politica indisponivel.";
    return;
  }
  const cloud = policy.cloud_fallback_enabled ? "cloud habilitado" : "cloud desabilitado";
  routingPolicyLine.textContent =
    `Politica: ${policy.policy} · padrao: ${policy.default_provider} · ${cloud}`;
}

function renderRoutingPreviewResult(preview) {
  routingPreviewResult.classList.remove("is-hidden");
  routingPreviewResult.innerHTML = "";

  const decision = preview.decision || {};
  const entities = preview.entities || {};
  const rows = [
    ["Provider", decision.provider || "—"],
    ["Modelo", decision.model || "—"],
    ["Tier", decision.tier || "—"],
    ["Score", decision.score ?? "—"],
    ["Politica", decision.policy || "—"],
    [
      "Escalonaria cloud",
      preview.would_escalate_to_cloud ? "sim" : "nao",
    ],
    ["Contexto (chars)", String(preview.context_chars ?? 0)],
  ];

  rows.forEach(([label, value]) => {
    const p = document.createElement("p");
    p.className = "routing-preview-row";
    p.innerHTML = `<strong>${escapeHtml(label)}:</strong> ${escapeHtml(String(value))}`;
    routingPreviewResult.appendChild(p);
  });

  if (Array.isArray(decision.reasons) && decision.reasons.length > 0) {
    const reasonsTitle = document.createElement("p");
    reasonsTitle.className = "routing-preview-row";
    reasonsTitle.innerHTML = "<strong>Motivos:</strong>";
    routingPreviewResult.appendChild(reasonsTitle);

    const reasonsList = document.createElement("ul");
    reasonsList.className = "routing-preview-reasons";
    decision.reasons.forEach((reason) => {
      const li = document.createElement("li");
      li.textContent = reason;
      reasonsList.appendChild(li);
    });
    routingPreviewResult.appendChild(reasonsList);
  }

  const entityBits = [];
  if (Array.isArray(entities.npc_ids) && entities.npc_ids.length > 0) {
    entityBits.push(`NPCs: ${entities.npc_ids.join(", ")}`);
  }
  if (Array.isArray(entities.character_ids) && entities.character_ids.length > 0) {
    entityBits.push(`Personagens: ${entities.character_ids.join(", ")}`);
  }
  if (Array.isArray(entities.keywords) && entities.keywords.length > 0) {
    entityBits.push(`Keywords: ${entities.keywords.join(", ")}`);
  }
  if (entityBits.length > 0) {
    const entityRow = document.createElement("p");
    entityRow.className = "routing-preview-row";
    entityRow.innerHTML = `<strong>Entidades:</strong> ${escapeHtml(entityBits.join(" · "))}`;
    routingPreviewResult.appendChild(entityRow);
  }
}

async function openRoutingDrawer() {
  routingPreviewStatus.textContent = "";
  routingPreviewResult.classList.add("is-hidden");
  routingPreviewResult.innerHTML = "";
  routingPreviewInput.value = playerInput.value.trim();
  openDrawer(routingDrawer);
  routingPreviewInput.focus();

  try {
    const policy = await fetchRoutingPolicy();
    renderRoutingPolicy(policy);
  } catch (err) {
    console.error(err);
    routingPolicyLine.textContent = "Nao foi possivel carregar a politica de roteamento.";
  }
}

async function runRoutingPreview() {
  const message = routingPreviewInput.value.trim();
  if (!message) {
    routingPreviewStatus.textContent = "Informe uma mensagem para simular.";
    routingPreviewResult.classList.add("is-hidden");
    return;
  }

  routingPreviewBtn.disabled = true;
  routingPreviewStatus.textContent = "Simulando roteamento...";
  routingPreviewResult.classList.add("is-hidden");

  try {
    const preview = await fetchRoutingPreview(message);
    renderRoutingPreviewResult(preview);
    routingPreviewStatus.textContent = `Canal: ${channelMeta().name}`;
  } catch (err) {
    console.error(err);
    routingPreviewStatus.textContent = err.message || "Falha ao simular roteamento.";
  } finally {
    routingPreviewBtn.disabled = false;
  }
}

function appendTurnQualityMeta(card, metaText) {
  const metaEl = document.createElement("div");
  metaEl.className = "turn-quality-meta";
  metaEl.setAttribute("aria-label", "Metadados do turno LLM");
  const parts = String(metaText || "")
    .split(" · ")
    .map((part) => part.trim())
    .filter(Boolean);
  parts.forEach((part, index) => {
    const item = document.createElement("span");
    item.className = "turn-quality-meta-item";
    item.textContent = part;
    metaEl.appendChild(item);
    if (index < parts.length - 1) {
      const sep = document.createElement("span");
      sep.className = "turn-quality-meta-sep";
      sep.setAttribute("aria-hidden", "true");
      sep.textContent = "·";
      metaEl.appendChild(sep);
    }
  });
  card.appendChild(metaEl);
}

function formatTurnQualityMeta(meta) {
  if (!meta || activeChannel !== "narracao") {
    return "";
  }
  const parts = [];
  const routing = meta.routing_decision;
  if (routing?.provider) {
    const tier = routing.tier ? ` · ${routing.tier}` : "";
    parts.push(`LLM: ${routing.provider}${tier}`);
  }
  if (meta.quality_passed === true) {
    parts.push("validacao: ok");
  } else if (meta.quality_passed === false) {
    parts.push("validacao: revisada");
  }
  if (meta.turn_attempts > 1) {
    parts.push(`tentativas: ${meta.turn_attempts}`);
  }
  if (
    Array.isArray(routing?.reasons) &&
    routing.reasons.some((reason) => String(reason).includes("quality_gate:rescue_cloud"))
  ) {
    parts.push("resgate: grok compacto");
  }
  return parts.join(" · ");
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
  btnGroupSessao.classList.toggle("has-badge", count > 0);
  if (!btnGroupSessao.querySelector(".badge")) {
    const badge = document.createElement("span");
    badge.className = "badge is-hidden";
    badge.id = "sessaoProposalsBadge";
    btnGroupSessao.appendChild(badge);
  }
  const sessaoBadge = btnGroupSessao.querySelector(".badge");
  if (sessaoBadge) {
    sessaoBadge.textContent = String(count);
    sessaoBadge.classList.toggle("is-hidden", count === 0);
  }
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

async function fetchCharacterSheet(characterId) {
  const response = await fetch(`${API_BASE}/api/characters/${characterId}/sheet`);
  if (!response.ok) {
    return null;
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

function renderFicha(profile, sheetData) {
  fichaSections.innerHTML = "";
  fichaRefs.innerHTML = "";

  if (sheetData && typeof renderCprSheet === "function") {
    const cprHost = document.createElement("div");
    cprHost.className = "sheet-card cpr-sheet-host";
    fichaSections.appendChild(cprHost);
    renderCprSheet(sheetData, cprHost);
  }

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
    const sheetData = await fetchCharacterSheet(profile.characterId || CHARACTER_ID);
    renderFicha(profile, sheetData);
    profileLoaded = true;
  } catch (err) {
    const detail = err instanceof Error ? err.message : String(err);
    fichaStatus.textContent =
      `Nao foi possivel carregar a ficha: ${detail}`;
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
  card.className = "narration-card system opening-scene channel-intro reveal";
  const body = document.createElement("div");
  body.className = "md-content opening-body";
  body.innerHTML = renderMarkdown(openingText);
  card.appendChild(body);
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
  campanhaSubmenu.innerHTML = "";
  prependSubmenuBack(campanhaSubmenu, btnGroupCampanha);
  const items = Array.isArray(briefData?.briefs) ? briefData.briefs : [];
  if (items.length === 0) {
    renderSubmenuFallback(campanhaSubmenu, btnGroupCampanha, "Resumo indisponivel.");
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item";
    button.textContent = item.title;
    button.title = item.teaser || item.title;
    button.addEventListener("click", () => {
      closeAllSubmenus();
      openBriefDetail(item);
    });
    li.appendChild(button);
    campanhaSubmenu.appendChild(li);
  });
}

async function refreshBrief() {
  try {
    campaignBrief = await fetchCampaignBrief();
    renderBriefButtons(campaignBrief);
    renderOpeningMessage(campaignBrief.opening);
  } catch (err) {
    console.error(err);
    renderSubmenuFallback(
      campanhaSubmenu,
      btnGroupCampanha,
      "Nao foi possivel carregar o resumo.",
    );
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
  prependSubmenuBack(npcSubmenu, btnNpcs);
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
    renderSubmenuFallback(npcSubmenu, btnNpcs, "NPCs indisponiveis");
  }
}

async function fetchSessionCommands() {
  const response = await fetch(`${API_BASE}/api/session-commands`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar comandos: ${response.status}`);
  }
  return response.json();
}

const CASCADE_MENU_GROUPS = [
  [btnGroupCampanha, campanhaSubmenu],
  [btnGroupPersonagem, personagemSubmenu],
  [btnGroupSessao, sessaoSubmenu],
  [btnGroupCanais, canaisSubmenu],
];

function syncMenuOpenState() {
  const anyOpen = CASCADE_MENU_GROUPS.some(
    ([, submenu]) => !submenu.classList.contains("is-hidden"),
  );
  document.body.classList.toggle("menu-open", anyOpen);
}

function closeAllSubmenus() {
  CASCADE_MENU_GROUPS.forEach(([trigger, submenu]) => {
    submenu.classList.add("is-hidden");
    trigger.setAttribute("aria-expanded", "false");
  });
  commandsSubmenu.classList.add("is-hidden");
  npcSubmenu.classList.add("is-hidden");
  syncMenuOpenState();
}

function bindCascadeMenu(trigger, submenu) {
  trigger.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = !submenu.classList.contains("is-hidden");
    CASCADE_MENU_GROUPS.forEach(([otherTrigger, otherSubmenu]) => {
      if (otherSubmenu !== submenu) {
        otherSubmenu.classList.add("is-hidden");
        otherTrigger.setAttribute("aria-expanded", "false");
      }
    });
    submenu.classList.toggle("is-hidden", isOpen);
    trigger.setAttribute("aria-expanded", isOpen ? "false" : "true");
    syncMenuOpenState();
  });
}

function renderPersonagemSubmenu() {
  personagemSubmenu.innerHTML = "";
  prependSubmenuBack(personagemSubmenu, btnGroupPersonagem);

  const fichaItem = document.createElement("li");
  const fichaBtn = document.createElement("button");
  fichaBtn.type = "button";
  fichaBtn.className = "submenu-item";
  fichaBtn.textContent = "Ficha";
  fichaBtn.addEventListener("click", async () => {
    closeAllSubmenus();
    await ensureCharacterProfileLoaded();
    openDrawer(fichaDrawer);
  });
  fichaItem.appendChild(fichaBtn);
  personagemSubmenu.appendChild(fichaItem);

  const journalItem = document.createElement("li");
  const journalBtn = document.createElement("button");
  journalBtn.type = "button";
  journalBtn.className = "submenu-item";
  journalBtn.textContent = "Journal";
  journalBtn.addEventListener("click", async () => {
    closeAllSubmenus();
    try {
      journalEntries = await fetchJournalEntries();
    } catch (err) {
      console.error(err);
    }
    renderJournal();
    openDrawer(journalDrawer);
    journalInput.focus();
  });
  journalItem.appendChild(journalBtn);
  personagemSubmenu.appendChild(journalItem);

  const npcsItem = document.createElement("li");
  const npcsBtn = document.createElement("button");
  npcsBtn.type = "button";
  npcsBtn.className = "submenu-item submenu-more";
  npcsBtn.textContent = "NPCs...";
  npcsBtn.addEventListener("click", () => {
    closeAllSubmenus();
    openNpcCatalogDrawer();
  });
  npcsItem.appendChild(npcsBtn);
  personagemSubmenu.appendChild(npcsItem);
}

function renderSessaoSubmenu() {
  sessaoSubmenu.innerHTML = "";
  prependSubmenuBack(sessaoSubmenu, btnGroupSessao);

  const quick = sessionCommandsData?.quick || SESSION_COMMANDS_FALLBACK.quick;
  quick.forEach((command) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item";
    button.textContent = command.label;
    button.addEventListener("click", () => {
      closeAllSubmenus();
      void sendPlayerMessage(command.text);
    });
    li.appendChild(button);
    sessaoSubmenu.appendChild(li);
  });

  const tools = [
    { label: "Todos os comandos...", testId: "sessao-comandos-todos", action: () => openCommandsDrawer() },
    { label: "Roteamento LLM", testId: "sessao-roteamento", action: () => openRoutingDrawer() },
    { label: "Propostas", testId: "sessao-propostas", action: async () => {
      try {
        await fetchPendingProposals();
      } catch (err) {
        console.error(err);
      }
      renderProposals();
      openDrawer(proposalsDrawer);
    }},
    { label: "Admin", testId: "sessao-admin", action: () => openDrawer(adminDrawer) },
  ];

  tools.forEach((tool) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item submenu-more";
    button.textContent = tool.label;
    if (tool.testId) {
      button.dataset.testid = tool.testId;
    }
    button.addEventListener("click", () => {
      closeAllSubmenus();
      tool.action();
    });
    li.appendChild(button);
    sessaoSubmenu.appendChild(li);
  });
}

function renderCanaisSubmenu() {
  canaisSubmenu.innerHTML = "";
  prependSubmenuBack(canaisSubmenu, btnGroupCanais);
  [
    { id: "narracao", label: "Narracao principal" },
    { id: "mestre", label: "Mestre off-game" },
    { id: "sistema", label: "Sistema (meta)" },
  ].forEach((channel) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item";
    button.textContent = channel.label;
    button.addEventListener("click", () => {
      closeAllSubmenus();
      setActiveChannel(channel.id);
    });
    li.appendChild(button);
    canaisSubmenu.appendChild(li);
  });
}

function initCascadeMenus() {
  renderPersonagemSubmenu();
  renderSessaoSubmenu();
  renderCanaisSubmenu();
  CASCADE_MENU_GROUPS.forEach(([trigger, submenu]) => bindCascadeMenu(trigger, submenu));
}

function buildCommandCard(command) {
  const card = document.createElement("article");
  card.className = "command-card sheet-card";

  const title = document.createElement("h3");
  title.textContent = command.label;
  card.appendChild(title);

  const description = document.createElement("p");
  description.className = "command-description";
  description.textContent = command.description || "";
  card.appendChild(description);

  if (command.behavior) {
    const behavior = document.createElement("p");
    behavior.className = "command-behavior";
    behavior.textContent = command.behavior;
    card.appendChild(behavior);
  }

  if (command.source) {
    const source = document.createElement("p");
    source.className = "command-source utility-hint";
    source.textContent = `Fonte: ${command.source}`;
    card.appendChild(source);
  }

  const preview = document.createElement("code");
  preview.className = "command-preview";
  preview.textContent = command.text;
  card.appendChild(preview);

  const actions = document.createElement("div");
  actions.className = "command-actions";

  const sendBtn = document.createElement("button");
  sendBtn.type = "button";
  sendBtn.className = "command-send";
  sendBtn.textContent = "Enviar";
  sendBtn.addEventListener("click", () => {
    void sendPlayerMessage(command.text);
    closeDrawer(commandsDrawer);
  });
  actions.appendChild(sendBtn);
  card.appendChild(actions);
  return card;
}

function renderCommandsCatalog(data) {
  commandsCatalog.innerHTML = "";
  const categories = Array.isArray(data?.categories) ? data.categories : [];
  categories.forEach((category) => {
    const section = document.createElement("section");
    section.className = "command-category";

    const heading = document.createElement("h3");
    heading.className = "command-category-title";
    heading.textContent = category.title;
    section.appendChild(heading);

    const list = document.createElement("div");
    list.className = "command-category-list";
    (category.commands || []).forEach((command) => {
      list.appendChild(buildCommandCard(command));
    });
    section.appendChild(list);
    commandsCatalog.appendChild(section);
  });
}

function renderCommandsSubmenu(quickCommands) {
  commandsSubmenu.innerHTML = "";
  prependSubmenuBack(commandsSubmenu, btnComandos);
  const items = Array.isArray(quickCommands) ? quickCommands : [];
  items.forEach((command) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "submenu-item";
    button.textContent = command.label;
    button.addEventListener("click", () => {
      closeAllSubmenus();
      void sendPlayerMessage(command.text);
    });
    li.appendChild(button);
    commandsSubmenu.appendChild(li);
  });

  const more = document.createElement("li");
  const moreBtn = document.createElement("button");
  moreBtn.type = "button";
  moreBtn.className = "submenu-item submenu-more";
  moreBtn.textContent = "Ver todos...";
  moreBtn.addEventListener("click", () => {
    closeAllSubmenus();
    openCommandsDrawer();
  });
  more.appendChild(moreBtn);
  commandsSubmenu.appendChild(more);
}

function openCommandsDrawer() {
  if (sessionCommandsData) {
    renderCommandsCatalog(sessionCommandsData);
  }
  openDrawer(commandsDrawer);
}

async function ensureSessionCommandsLoaded() {
  if (sessionCommandsData) {
    renderSessaoSubmenu();
    return;
  }
  try {
    sessionCommandsData = await fetchSessionCommands();
    renderSessaoSubmenu();
  } catch (err) {
    console.error(err);
    sessionCommandsData = SESSION_COMMANDS_FALLBACK;
    renderSessaoSubmenu();
  }
}

async function appendNpcSegment(segment, qualityMeta = "") {
  const label = segment.action ? `${segment.name} (acao)` : segment.name;
  try {
    const npcAsset = await fetchNpcAsset(segment.name, segment.gender);
    appendCard(label, "system", {
      cardRole: segment.action ? "npc-action" : "npc-speech",
      markdownContent: segment.text,
      npcName: segment.name,
      npcTokenUrl: npcAsset.tokenUrl,
      npcImageUrl: npcAsset.imageUrl,
      npcAction: segment.action,
      qualityMeta,
    });
  } catch (assetErr) {
    console.error(assetErr);
    appendCard(label, "system", {
      cardRole: segment.action ? "npc-action" : "npc-speech",
      markdownContent: segment.text,
      qualityMeta,
    });
  }
}

async function renderChannelReply(reply, meta) {
  const qualityMeta = formatTurnQualityMeta(meta);
  if (activeChannel !== "narracao") {
    const prefix = channelMeta().reply;
    appendCard(`${prefix}:`, "system", { markdownContent: reply, qualityMeta });
    return;
  }

  const segments = segmentNarrationReply(reply);
  for (let index = 0; index < segments.length; index += 1) {
    const segment = segments[index];
    const segmentMeta = index === segments.length - 1 ? qualityMeta : "";
    if (segment.type === "npc") {
      await appendNpcSegment(segment, segmentMeta);
      continue;
    }
    appendCard("NARRADOR:", "system", {
      cardRole: "narrator",
      markdownContent: segment.text,
      qualityMeta: segmentMeta,
    });
  }
}

async function sendPlayerMessage(message) {
  const text = String(message || "").trim();
  if (!text || playerInput.disabled) {
    return;
  }

  const labels = channelMeta();
  const requestOptions = buildRequestOptions(text);
  appendCard(`[${labels.player}] VOCE: ${text}`, "player", {
    playerTokenUrl: RYAN_TOKEN_URL,
    playerImageUrl: RYAN_IMAGE_URL,
    playerName: "Ryan",
  });
  setChatBusy(true);
  createLoadingCard("Consultando o provider...");

  try {
    const { reply, meta } = await callChannelApi(text, requestOptions);
    await renderChannelReply(reply, meta);
  } catch (err) {
    const fallbackPrefix = channelMeta().reply;
    appendCard(`${fallbackPrefix}: ${extractFriendlyError(err)}`, "private");
    console.error(err);
  } finally {
    removeLoadingCard();
    setChatBusy(false);
  }

  playerInput.value = "";
  playerInput.focus();
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

function setActiveChannel(channel) {
  activeChannel = CHANNEL_ENDPOINTS[channel] ? channel : "narracao";
  channelButtons.forEach((button) => {
    const isActive = button.dataset.channel === activeChannel;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", isActive ? "true" : "false");
  });
  const channelShort = channelMeta().name.replace(" (meta-tecnico)", "");
  btnGroupCanais.textContent = `Canais · ${channelShort.split(" ")[0]}`;
  chatModeLabel.textContent = `Canal atual: ${channelMeta().name}`;
  updateFeedVisibility(activeChannel);
  setChatBusy(playerInput.disabled);
}

async function fetchApiHealth() {
  const response = await fetch(`${API_BASE}/api/health`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

function showApiStatus(message, isError = true) {
  if (!message) {
    apiStatusBanner.classList.add("is-hidden");
    apiStatusBanner.textContent = "";
    return;
  }
  apiStatusBanner.textContent = message;
  apiStatusBanner.classList.toggle("api-status-error", isError);
  apiStatusBanner.classList.remove("is-hidden");
}

function apiHasFeature(feature) {
  return Array.isArray(apiHealth?.features) && apiHealth.features.includes(feature);
}

function buildOllamaHealthWarning(health) {
  const ollama = health?.ollama;
  if (!ollama) {
    return "";
  }
  if (!ollama.reachable) {
    return `Ollama offline em ${ollama.base_url || "127.0.0.1:11434"}. Inicie o app Ollama.`;
  }
  if (!ollama.narration_ready) {
    const model = ollama.configured_narration || "modelo de narracao";
    return `Modelo '${model}' nao instalado. Rode: ollama pull ${model}`;
  }
  return "";
}

async function bootstrapApi() {
  try {
    apiHealth = await fetchApiHealth();
    const missing = ["brief", "session-commands", "npcs"].filter(
      (feature) => !apiHasFeature(feature),
    );
    if (missing.length > 0) {
      showApiStatus(
        `API desatualizada (faltam: ${missing.join(", ")}). Reinicie: python scripts/narracao_api.py`,
      );
      sessionCommandsData = SESSION_COMMANDS_FALLBACK;
      renderSessaoSubmenu();
      return;
    }
    const ollamaWarning = buildOllamaHealthWarning(apiHealth);
    if (ollamaWarning) {
      showApiStatus(ollamaWarning);
    } else {
      showApiStatus("");
    }
    await Promise.all([refreshBrief(), ensureNpcCatalogLoaded(), ensureSessionCommandsLoaded()]);
    renderSessaoSubmenu();
  } catch (err) {
    console.error(err);
    showApiStatus(
      "Nao foi possivel contactar a API em " +
        API_BASE +
        ". Inicie: python scripts/narracao_api.py",
    );
    sessionCommandsData = SESSION_COMMANDS_FALLBACK;
    renderSessaoSubmenu();
  }
}

routingPreviewBtn.addEventListener("click", () => {
  runRoutingPreview();
});

// Botoes legados (ocultos) — compatibilidade e2e
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
channelButtons.forEach((button) => {
  button.addEventListener("click", () => {
    setActiveChannel(button.dataset.channel || "narracao");
  });
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
closeRoutingBtn.addEventListener("click", () => closeDrawer(routingDrawer));
closeBriefBtn.addEventListener("click", () => closeDrawer(briefDrawer));
closeCommandsBtn.addEventListener("click", () => closeDrawer(commandsDrawer));
closeNpcBtn.addEventListener("click", () => closeDrawer(npcDrawer));
closeAdminBtn.addEventListener("click", () => closeDrawer(adminDrawer));

const openCharacterWizardBtn = document.getElementById("openCharacterWizardBtn");
if (openCharacterWizardBtn && typeof openCharacterWizard === "function") {
  openCharacterWizardBtn.addEventListener("click", () => {
    closeDrawer(adminDrawer);
    openCharacterWizard();
  });
}

const drawerByKey = {
  ficha: fichaDrawer,
  journal: journalDrawer,
  proposals: proposalsDrawer,
  routing: routingDrawer,
  brief: briefDrawer,
  commands: commandsDrawer,
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
  const insideCascade = CASCADE_MENU_GROUPS.some(([trigger, submenu]) => {
    return trigger.contains(target) || submenu.contains(target);
  });
  if (!insideCascade) {
    closeAllSubmenus();
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
  closeAllSubmenus();
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
initCascadeMenus();
setActiveChannel("narracao");
ensureCharacterProfileLoaded();
bootstrapApi();

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

bindMultilineSubmit(playerInput, () => {
  if (!playerInput.disabled) {
    chatForm.requestSubmit();
  }
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = playerInput.value.trim();
  if (!message) {
    return;
  }
  playerInput.value = "";
  autoResizeTextarea(playerInput);
  await sendPlayerMessage(message);
});

bindMultilineSubmit(journalInput, () => {
  if (!journalInput.disabled) {
    journalForm.requestSubmit();
  }
});

autoResizeTextarea(playerInput);
