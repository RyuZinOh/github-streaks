<template>
  <div class="home">
    <div class="documentation">
      <h1>GitHub Readme Stats Documentation</h1>
      <p>
        This documentation provides all the information you need to set up and use the GitHub Readme
        Stats application. The application is built on FastAPI and allows you to generate dynamic
        GitHub stats images to display on your profile readme.
      </p>

      <section id="sample-image">
        <h2>Sample Image</h2>
        <p>This is the generated image that will be reflected in your GitHub readme.</p>
        <img
          src="@/assets/response.png"
          alt="Sample GitHub Streaks Dashboard"
          class="sample-image"
        />
      </section>

      <section id="how-it-works">
        <h2>How It Works</h2>
        <p>
          The application tracks a GitHub user's contributions and generates a dynamic stats image.
          This image can be embedded in your GitHub readme markdown, reflecting your streaks and
          activity on the platform. It's designed for personal use and provides real-time data.
        </p>
      </section>

      <section id="installation">
        <h2>Installation</h2>
        <p>Follow these steps to install and configure the GitHub Readme Stats application:</p>
        <ol>
          <li>Clone the repository:</li>
          <pre><code>git clone https://github.com/RyuZinOh/github-streaks</code></pre>
          <li>Install dependencies:</li>
          <pre><code>pip install -r requirements.txt</code></pre>
          <li>Create a <code>.env</code> file and add your GitHub token:</li>
          <pre><code>GITHUB_TOKEN=your_personal_access_token</code></pre>
          <li>
            Generate a GitHub token
            <a href="https://github.com/settings/tokens" target="_blank" class="link">here</a>.
          </li>
          <li>Start the FastAPI server:</li>
          <pre><code>uvicorn main:app --reload</code></pre>
          <li>Access the app:</li>
          <pre><code>http://localhost:8000</code></pre>
        </ol>
      </section>

      <section id="hosting">
        <h2>How to Host</h2>
        <p>Use Cloudflare's tunneling service for public access:</p>
        <ol>
          <li>
            Install Cloudflared from
            <a
              href="https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/"
              target="_blank"
              class="link"
              >here</a
            >.
          </li>
          <li>Start the tunnel:</li>
          <pre><code>cloudflared tunnel --url http://localhost:8000</code></pre>
          <li>Your app will be accessible on a Cloudflare subdomain.</li>
          <li>Embed in your GitHub readme:</li>
          <pre><code>![readme](your_link_hosted_on_cloudflare)</code></pre>
        </ol>
        <p>
          <strong>Alternative:</strong> Use Render for hosting as it securely handles environment
          variables.
        </p>
      </section>

      <section id="custom-themes">
        <h2>Custom Themes</h2>
        <p>
          The application supports custom themes, allowing you to personalize the appearance of your
          GitHub stats image. Themes are contribution-based, meaning you can propose new themes, and
          they will be reviewed and merged if they meet the quality standards.
        </p>
        <h3>Using Predefined Themes</h3>
        <p>
          To use a predefined theme, append the <code>theme</code> query parameter to the API
          endpoint. For example:
        </p>
        <pre><code>GET /streak/ryuzinoh/image?theme=midnight</code></pre>
        <p>Available themes include:</p>
        <ul>
          <li><code>midnight</code> (default)</li>
          <li><code>sunset</code></li>
          <li><code>ocean</code></li>
          <li><code>forest</code></li>
          <li><code>many more....</code></li>
        </ul>
      </section>
    </div>
  </div>
</template>

<style scoped>
.home {
  font-family:Roboto ;
  display: flex;
  justify-content: center;
  padding: 40px 20px;
  background-color: #ffffff;
}

.documentation {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  width: 100%;
}

h1 {
  color: #2563eb;
  font-size: 2rem;
  margin-bottom: 20px;
}

h2 {
  color: #2563eb;
  font-size: 1.6rem;
  margin-top: 30px;
}

h3 {
  color: #2563eb;
  font-size: 1.4rem;
}

p {
  color: #333;
  line-height: 1.6;
}

ul,
ol {
  padding-left: 20px;
  color: #333;
}

pre,
code {
  background-color: #f1f5f9;
  border-radius: 6px;
  font-family: monospace;
  color: #1e40af;
}

.sample-image {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-top: 10px;
}

.link {
  color: #2563eb;
  text-decoration: none;
  font-weight: bold;
}

.link:hover {
  text-decoration: underline;
}
</style>
