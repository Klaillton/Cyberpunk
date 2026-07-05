const { test, expect } = require("@playwright/test");

test.describe("Drawers de Ficha e Journal", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("abre e fecha Journal pelo botao close", async ({ page }) => {
    const journalDrawer = page.locator("#journalDrawer");
    await expect(journalDrawer).toHaveClass(/is-hidden/);

    await page.locator("#btnJournal").click();
    await expect(journalDrawer).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#closeJournalBtn")).toBeVisible();

    await page.locator("#closeJournalBtn").click();
    await expect(journalDrawer).toHaveClass(/is-hidden/);
  });

  test("abre e fecha Ficha pelo botao close", async ({ page }) => {
    const fichaDrawer = page.locator("#fichaDrawer");
    await expect(fichaDrawer).toHaveClass(/is-hidden/);

    await page.locator("#btnFicha").click();
    await expect(fichaDrawer).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#closeFichaBtn")).toBeVisible();

    await page.locator("#closeFichaBtn").click();
    await expect(fichaDrawer).toHaveClass(/is-hidden/);
  });

  test("ficha aparece acima da tela principal", async ({ page }) => {
    await page.locator("#btnFicha").click();

    const zIndex = await page.locator("#fichaDrawer").evaluate((el) => {
      const raw = window.getComputedStyle(el).zIndex;
      return Number.parseInt(raw, 10) || 0;
    });
    expect(zIndex).toBeGreaterThanOrEqual(3);

    await expect(page.locator("#fichaDrawer .sheet-panel")).toBeVisible();
  });

  test("ficha mostra os campos reais do markdown", async ({ page }) => {
    await page.locator("#btnFicha").click();

    await expect(page.locator("#fichaDrawer")).toContainText("Aparência");
    await expect(page.locator("#fichaDrawer")).toContainText("Background");
    await expect(page.locator("#fichaDrawer")).toContainText(
      "Atributos (62 Pontos)",
    );
    await expect(page.locator("#fichaDrawer")).toContainText(
      "Humanidade e Cyberware",
    );
    await expect(page.locator("#fichaDrawer")).toContainText(
      "Drones / Gear / Armamento",
    );
    await expect(page.locator("#fichaDrawer")).toContainText(
      "Memórias Reprimidas e Gatilhos",
    );
  });

  test("journal persiste entrada apos recarregar", async ({ page }) => {
    const uniqueNote = `nota-e2e-${Date.now()}`;

    await page.locator("#btnJournal").click();
    await page.locator("#journalInput").fill(uniqueNote);
    await page.locator("#journalForm .journal-submit").click();
    await expect(page.locator("#journalList")).toContainText(uniqueNote);

    await page.reload();
    await page.locator("#btnJournal").click();
    await expect(page.locator("#journalList")).toContainText(uniqueNote);
  });

  test("journal exclui entrada com confirmacao", async ({ page }) => {
    const uniqueNote = `nota-delete-${Date.now()}`;

    await page.locator("#btnJournal").click();
    await page.locator("#journalInput").fill(uniqueNote);
    await page.locator("#journalForm .journal-submit").click();
    await expect(page.locator("#journalList")).toContainText(uniqueNote);

    page.once("dialog", (dialog) => dialog.accept());
    await page
      .locator("#journalList .journal-item", { hasText: uniqueNote })
      .locator(".journal-delete")
      .click();

    await expect(page.locator("#journalList")).not.toContainText(uniqueNote);
  });

  test("fala de npc exibe token clicavel para imagem", async ({ page }) => {
    await page.route("**/api/narracao", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "narracao",
          provider: "none",
          reply: "[NPC-F: Lira] Eu vi os rastros no perimetro.",
        }),
      });
    });

    await page.locator("#playerInput").fill("Observar arredores");
    await page.locator("#chatForm button[type='submit']").click();

    const tokenLink = page.locator(".npc-token-link").last();
    await expect(tokenLink).toBeVisible();
    await expect(page.locator(".npc-token").last()).toBeVisible();

    const [popup] = await Promise.all([
      page.waitForEvent("popup"),
      tokenLink.click(),
    ]);
    await expect(popup).toHaveURL(/\/api\/npc-image\?/);
    await popup.close();
  });

  test("mostra loading enquanto consulta a narracao", async ({ page }) => {
    await page.route("**/api/narracao", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 400));
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "narracao",
          provider: "none",
          reply: "Narracao pronta.",
        }),
      });
    });

    await page.locator("#playerInput").fill("Avançar pelo corredor");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator(".narration-card.loading")).toBeVisible();
    await expect(page.locator(".narration-card.loading")).toHaveCount(0);
    await expect(page.locator("#narrationFeed")).toContainText(
      "Narracao pronta.",
    );
  });

  test("transforma falha do provider em mensagem limpa", async ({ page }) => {
    await page.route("**/api/narracao", async (route) => {
      await route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({
          error:
            "Falha no provider grok: grok falhou: 402 Payment Required balance exhausted",
        }),
      });
    });

    await page.locator("#playerInput").fill("Testar erro do provider");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#narrationFeed")).toContainText(
      "Grok indisponivel no momento",
    );
    await expect(page.locator("#narrationFeed")).not.toContainText(
      "balance exhausted",
    );
  });
});
