const { test, expect } = require("@playwright/test");

test.describe("Resumo de sessao", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("comando de resumo no canal narracao retorna estrutura", async ({ page }) => {
    await page.route("**/api/narracao", async (route) => {
      const body = route.request().postDataJSON();
      expect(Array.isArray(body.history)).toBeTruthy();
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "narracao",
          provider: "none",
          reply:
            "Resumo da Sessão — Teste (03/07/2026)\n\n## Eventos Principais\n- Ryan observou os recrutas.",
        }),
      });
    });

    await page.locator("#playerInput").fill("[Resumo da Sessão]");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#narrationFeed")).toContainText("Resumo da Sessão");
    await expect(page.locator("#narrationFeed")).toContainText("Eventos Principais");
  });
});