const { defineConfig, devices } = require("@playwright/test");
const fs = require("fs");
const path = require("path");

const e2eDataDir = path.join(__dirname, "tests", "tmp_e2e_data");
const e2eCampaignDir = path.join(e2eDataDir, "campaign");
const e2eHeatFixture = path.join(__dirname, "tests", "fixtures", "e2e_heat.md");
fs.mkdirSync(e2eCampaignDir, { recursive: true });
fs.copyFileSync(e2eHeatFixture, path.join(e2eCampaignDir, "heat.md"));

module.exports = defineConfig({
  testDir: "./tests/e2e",
  timeout: 30000,
  expect: {
    timeout: 5000,
  },
  fullyParallel: false,
  retries: 0,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:8787",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  webServer: {
    command: "python -m uvicorn api.main:app --host 127.0.0.1 --port 8787",
    url: "http://127.0.0.1:8787",
    reuseExistingServer: false,
    timeout: 120000,
    env: {
      NARRACAO_PROVIDER: "none",
      NARRACAO_SKIP_PROVIDER_PROMPT: "1",
      DATA_DIR: e2eDataDir,
      DB_PATH: path.join(e2eDataDir, "motor.db"),
      FAISS_DIR: path.join(e2eDataDir, "faiss"),
      JOURNAL_DIR: path.join(e2eDataDir, "journal"),
      CAMPANHA_ROOT: e2eCampaignDir,
      UPDATE_PROPOSALS_ENABLED: "true",
    },
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
});
