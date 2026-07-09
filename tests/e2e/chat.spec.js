const { test, expect } = require("@playwright/test");
const { selectChannel } = require("./helpers");

test.describe("Chat e canais", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("alterna canal mestre e envia mensagem", async ({ page }) => {
    await page.route("**/api/mestre", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "mestre",
          provider: "none",
          reply: "Canon atual: Reyes parece cauteloso, mas leal ao pack.",
        }),
      });
    });

    await selectChannel(page, "Mestre off-game");
    await expect(page.locator("#chatModeLabel")).toContainText("Mestre off-game");
    await expect(page.locator("#mestreFeed")).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#narrationFeed")).toHaveClass(/is-hidden/);

    await page.locator("#playerInput").fill("O Reyes esta confiavel?");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#mestreFeed")).toContainText("Canon atual");
    await expect(page.locator("#narrationFeed")).not.toContainText("Off-record");
  });

  test("alterna canal sistema e envia mensagem", async ({ page }) => {
    await page.route("**/api/sistema", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "sistema",
          provider: "none",
          reply: "Ficha netrunner: fichas/netrunner - alex_specter_kane.md",
        }),
      });
    });

    await selectChannel(page, "Sistema (meta)");
    await expect(page.locator("#chatModeLabel")).toContainText("Sistema");
    await expect(page.locator("#sistemaFeed")).not.toHaveClass(/is-hidden/);

    await page.locator("#playerInput").fill("qual a ficha da netrunner?");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#sistemaFeed")).toContainText("alex_specter_kane");
  });

  test("narracao exibe meta de qualidade quando presente", async ({ page }) => {
    await page.route("**/api/narracao", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          channel: "narracao",
          provider: "ollama",
          model: "llama3.1:8b",
          reply: "Ryan observa o acampamento em silencio.",
          routing_decision: {
            provider: "ollama",
            model: "llama3.1:8b",
            tier: "standard",
            score: 3,
            policy: "local_only",
            escalated: false,
            reasons: ["heuristic:test"],
          },
          quality_passed: true,
          turn_attempts: 1,
        }),
      });
    });

    await page.locator("#playerInput").fill("Observo o pack.");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#narrationFeed")).toContainText("validacao: ok");
    await expect(page.locator("#narrationFeed")).toContainText("LLM: ollama");
  });

  test("volta ao canal narracao principal", async ({ page }) => {
    await selectChannel(page, "Mestre off-game");
    await expect(page.locator("#narrationFeed")).toHaveClass(/is-hidden/);

    await selectChannel(page, "Narracao principal");
    await expect(page.locator("#chatModeLabel")).toContainText("Narracao principal");
    await expect(page.locator("#narrationFeed")).not.toHaveClass(/is-hidden/);
  });

  test("character-profile API retorna ficha real", async ({ request }) => {
    const response = await request.get("/api/character-profile");
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.characterId).toBe("ryan_wireghost_voss");
    expect(data.sections?.length).toBeGreaterThan(0);
  });

  test("journal API aceita POST e GET", async ({ request }) => {
    const charId = "ryan_wireghost_voss";
    const note = `nota-api-e2e-${Date.now()}`;

    const post = await request.post(`/api/journal/${charId}`, {
      data: { timestamp: "07/07/2026, 12:00:00", text: note },
    });
    expect(post.status()).toBe(201);

    const get = await request.get(`/api/journal/${charId}`);
    expect(get.ok()).toBeTruthy();
    const body = await get.json();
    expect(body.entries.some((e) => e.text === note)).toBeTruthy();
  });
});