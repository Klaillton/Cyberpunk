const { test, expect } = require("@playwright/test");

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

    await page.locator("#btnNarrador").click();
    await expect(page.locator("#btnNarrador")).toHaveText(/Mestre \(ON\)/i);
    await expect(page.locator("#narratorFeed")).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#narrationFeed")).toHaveClass(/is-hidden/);

    await page.locator("#playerInput").fill("O Reyes esta confiavel?");
    await page.locator("#chatForm button[type='submit']").click();

    await expect(page.locator("#narratorFeed")).toContainText("Canon atual");
    await expect(page.locator("#narrationFeed")).not.toContainText("Off-record");
  });

  test("volta ao canal narracao principal", async ({ page }) => {
    await page.locator("#btnNarrador").click();
    await expect(page.locator("#btnNarrador")).toHaveText(/Mestre \(ON\)/i);

    await page.locator("#btnNarrador").click();
    await expect(page.locator("#btnNarrador")).toHaveText(/^Mestre$/);
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