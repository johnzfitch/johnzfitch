#!/usr/bin/env node
// Generate resume.pdf from resume.html using Puppeteer

const puppeteer = require('puppeteer');
const path = require('path');

async function generatePDF() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Load the resume.html file
  const resumePath = path.join(__dirname, 'resume.html');
  await page.goto(`file://${resumePath}`, {
    waitUntil: 'networkidle0'
  });

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

  await browser.close();
  console.log('Generated resume.pdf');
}

generatePDF().catch(err => {
  console.error('Error generating PDF:', err);
  process.exit(1);
});
