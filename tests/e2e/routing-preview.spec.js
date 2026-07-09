const { test, expect } = require("@playwright/test");

test.describe("Preview de roteamento", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("abre drawer e simula decisao sem gastar narracao", async ({ page }) => {
    await page.route("**/api/routing/policy", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          policy: "local_only",
          default_provider: "ollama",
          cloud_provider: "grok",
          cloud_fallback_enabled: false,
        }),
      });
    });

    await page.route("**/api/routing/preview", async (route) => {
      const body = route.request().postDataJSON();
      expect(body.message).toContain("acampamento");
      expect(body.channel).toBe("narracao");
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          decision: {
            provider: "ollama",
            model: "llama3.1:8b",
            tier: "standard",
            score: 3,
            policy: "local_only",
            requires_user_approval: false,
            reasons: ["heuristic:test"],
          },
          would_escalate_to_cloud: false,
          entities: {
            npc_ids: [],
            character_ids: ["ryan_wireghost_voss"],
            keywords: ["acampamento"],
            confidence: 0.8,
          },
          context_chars: 4200,
        }),
      });
    });

    await page.locator("#btnGroupSessao").click();
    await page.locator('[data-testid="sessao-roteamento"]').click();
    await expect(page.locator("#routingDrawer")).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#routingPolicyLine")).toContainText("local_only");
    await expect(page.locator("#routingPolicyLine")).toContainText("ollama");

    await page.locator("#routingPreviewInput").fill("Observo o acampamento em silencio.");
    await page.locator("#routingPreviewBtn").click();

    await expect(page.locator("#routingPreviewResult")).not.toHaveClass(/is-hidden/);
    await expect(page.locator("#routingPreviewResult")).toContainText("Provider");
    await expect(page.locator("#routingPreviewResult")).toContainText("ollama");
    await expect(page.locator("#routingPreviewResult")).toContainText("standard");
    await expect(page.locator("#routingPreviewResult")).toContainText("heuristic:test");
    await expect(page.locator("#routingPreviewResult")).toContainText("4200");
  });

  test("mapeia canal mestre para narrador na simulacao", async ({ page }) => {
    await page.route("**/api/routing/policy", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          policy: "local_only",
          default_provider: "ollama",
          cloud_provider: "grok",
          cloud_fallback_enabled: false,
        }),
      });
    });

    await page.route("**/api/routing/preview", async (route) => {
      const body = route.request().postDataJSON();
      expect(body.channel).toBe("narrador");
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          decision: {
            provider: "none",
            model: null,
            tier: "trivial",
            score: 1,
            policy: "local_only",
            requires_user_approval: false,
            reasons: ["channel:mestre"],
          },
          would_escalate_to_cloud: false,
          entities: {
            npc_ids: [],
            character_ids: [],
            keywords: [],
            confidence: 0,
          },
          context_chars: 900,
        }),
      });
    });

    await page.locator("#btnGroupCanais").click();
    await page.locator("#canaisSubmenu .submenu-item", { hasText: "Mestre off-game" }).click();
    await page.locator("#btnGroupSessao").click();
    await page.locator('[data-testid="sessao-roteamento"]').click();
    await page.locator("#routingPreviewInput").fill("O Reyes esta confiavel?");
    await page.locator("#routingPreviewBtn").click();

    await expect(page.locator("#routingPreviewResult")).toContainText("none");
  });
});