const puppeteer = require('puppeteer');
const fs = require('fs/promises'); // Import the 'fs' module for file operations

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Enable request interception
  await page.setRequestInterception(true);

  page.on('request', async (request) => {
    if (request.url().startsWith('https://apis-jiovoot.voot.com/playbackjv/v4/3816103') && request.method() === 'POST') {
      // Get the request headers
      const headers = request.headers();

      // Get the access-token header value (use the correct header name)
      const accessToken = headers['accesstoken'];

      console.log('Access Token:', accessToken);

      // Save the access token to a file
      await fs.writeFile('access_token.txt', accessToken);

      // Continue with the request
      request.continue();
    } else {
      // Continue with other requests
      request.continue();
    }
  });

  // Open the JioCinema page
  await page.goto('https://www.jiocinema.com/tv-shows/taali/1/teesri-ladai/3816103');

  // Wait for the network request to appear in the Network tab
  await page.waitForResponse((response) =>
    response.url().startsWith('https://apis-jiovoot.voot.com/playbackjv/v4/3816103') &&
    response.request().method() === 'POST'
  );

  // Optionally, you can perform other interactions on the page here

  // Close the browser when done
  await browser.close();
})();
