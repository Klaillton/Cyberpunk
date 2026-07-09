// @ts-check
const { test, expect } = require("@playwright/test");

test.describe("Propostas de atualizacao", () => {
  test("ingere proposta via API e aprova pela UI", async ({ page, request }) => {
    const rationale = `Validacao e2e ${Date.now()}`;
    const narrative = `Cena de teste e2e.

---UPDATE_PROPOSALS---
\`\`\`json
[
  {
    "target_path": "heat.md",
    "target_section": "Heat por Personagem",
    "change_type": "insert_row",
    "payload": {
      "personagem": "E2E Runner",
      "nivel": "Baixa",
      "justificativa": "Teste playwright"
    },
    "rationale": "${rationale}",
    "confidence": 0.95
  }
]
\`\`\``;

    const pending = await request.get("/api/proposals");
    if (pending.ok()) {
      const pendingBody = await pending.json();
      const ids = (pendingBody.proposals || []).map((item) => item.id).filter(Boolean);
      if (ids.length) {
        await request.post("/api/save", {
          data: { proposal_ids: ids, approved: false },
        });
      }
    }

    const ingest = await request.post("/api/proposals/ingest", {
      data: { narrative },
    });
    expect(ingest.ok()).toBeTruthy();
    const ingestBody = await ingest.json();
    expect(ingestBody.proposals.length).toBeGreaterThan(0);

    await page.goto("/");
    await page.locator("#btnGroupSessao").click();
    await page.locator('[data-testid="sessao-propostas"]').click();
    const drawer = page.locator("#proposalsDrawer");
    await expect(drawer.getByText(rationale)).toBeVisible();
    await drawer.getByRole("button", { name: "Aprovar", exact: true }).click();

    await expect(drawer.getByText("Nenhuma proposta pendente.")).toBeVisible({
      timeout: 5000,
    });
  });
});