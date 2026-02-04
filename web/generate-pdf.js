#!/usr/bin/env node
// Generate resume.pdf from resume.html using Puppeteer

const puppeteer = require('puppeteer');
const path = require('path');
const { pathToFileURL } = require('url');

async function generatePDF() {
  const noSandbox =
    process.env.PUPPETEER_NO_SANDBOX === '1' ||
    process.env.PUPPETEER_NO_SANDBOX === 'true' ||
    process.env.CI === 'true';

  const launchOptions = {
    headless: true
  };

  if (noSandbox) {
    launchOptions.args = ['--no-sandbox', '--disable-setuid-sandbox'];
  }

  let browser;
  let page;
  try {
    browser = await puppeteer.launch(launchOptions);
    page = await browser.newPage();

    // Load the resume.html file
    const resumePath = path.join(__dirname, 'resume.html');
    const resumeUrl = pathToFileURL(resumePath).toString();
    await page.goto(resumeUrl, { waitUntil: 'networkidle0' });

    // Generate PDF with print-optimized settings
    await page.pdf({
      path: path.join(__dirname, 'resume.pdf'),
      format: 'Letter',
      printBackground: true,
      margin: {
        top: '0.5in',
        right: '0.5in',
        bottom: '0.5in',
        left: '0.5in'
      }
    });
  } finally {
    if (page) {
      await page.close().catch(() => undefined);
    }
    if (browser) {
      await browser.close().catch(() => undefined);
    }
  }

  console.log('Generated resume.pdf');
}

generatePDF().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
