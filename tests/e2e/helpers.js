// @ts-check

/**
 * @param {import('@playwright/test').Page} page
 * @param {string} groupButtonSelector
 * @param {import('@playwright/test').Locator} itemLocator
 */
async function openCascadeItem(page, groupButtonSelector, itemLocator) {
  await page.locator(groupButtonSelector).click();
  await page.waitForFunction(
    () =>
      document.body.classList.contains("menu-open") ||
      Boolean(document.querySelector(".side-actions .submenu:not(.is-hidden)")),
  );
  await itemLocator.waitFor({ state: "visible", timeout: 5000 });
  await itemLocator.scrollIntoViewIfNeeded();
  await itemLocator.click();
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {string} label
 */
async function selectChannel(page, label) {
  await openCascadeItem(
    page,
    "#btnGroupCanais",
    page.locator("#canaisSubmenu .submenu-item").filter({ hasText: label }),
  );
}

module.exports = { openCascadeItem, selectChannel };