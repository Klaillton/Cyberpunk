// @ts-check
const { test, expect } = require("@playwright/test");

test.describe("Propostas de atualizacao", () => {
  test("ingere proposta via API e aprova pela UI", async ({ page, request }) => {
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
    "rationale": "Validacao e2e",
    "confidence": 0.95
  }
]
\`\`\``;

    const ingest = await request.post("/api/proposals/ingest", {
      data: { narrative },
    });
    expect(ingest.ok()).toBeTruthy();
    const ingestBody = await ingest.json();
    expect(ingestBody.proposals.length).toBeGreaterThan(0);

    await page.goto("/");
    await page.getByRole("button", { name: /Propostas/i }).click();
    await expect(page.getByText("Validacao e2e")).toBeVisible();
    await page.getByRole("button", { name: "Aprovar", exact: true }).first().click();

    await expect(page.getByText("Nenhuma proposta pendente.")).toBeVisible({
      timeout: 5000,
    });
  });
});