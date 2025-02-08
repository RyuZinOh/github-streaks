<template>
  <div class="home">
    <div class="content">
      <!-- Main Content Section -->
      <div class="documentation">
        <h1>GitHub Readme Stats Documentation</h1>
        <p>
          This documentation provides all the information you need to set up and use the GitHub
          Readme Stats application. The application is built on FastAPI and allows you to generate
          dynamic GitHub stats images to display on your profile readme.
        </p>

        <section id="sample-image">
          <h2>Sample Image</h2>
          <p>This is the generated image that will be reflected in your GitHub readme.</p>
          <img src="@/assets/response.png" alt="Sample GitHub Streaks Dashboard" />
        </section>

        <section id="how-it-works">
          <h2>How It Works</h2>
          <p>
            The application tracks a GitHub user's contributions and generates a dynamic stats
            image. This image can be embedded in your GitHub readme markdown, reflecting your
            streaks and activity on the platform. It's designed for personal use and provides
            real-time data.
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
            <li>
              Create a <code>.env</code> file and add your GitHub token:
              <pre><code>GITHUB_TOKEN=your_personal_access_token</code></pre>
            </li>
            <li>
              Generate a GitHub token
              <a href="https://github.com/settings/tokens" target="_blank">here</a>.
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
                >here</a
              >.
            </li>
            <li>Start the tunnel:</li>
            <pre><code>cloudflared tunnel --url http://localhost:8000</code></pre>
            <li>Your app will be accessible on a Cloudflare subdomain.</li>
            <li>
              Embed in your GitHub readme:
              <pre><code>![readme](your_link_hosted_on_cloudflare)</code></pre>
            </li>
          </ol>
          <p>
            <strong>Alternative:</strong> Use Render for hosting as it securely handles environment
            variables.
          </p>
        </section>

        <!-- Navigation Links -->
        <nav>
          <ul>
            <li><a href="#sample-image">Sample Image</a></li>
            <li><a href="#how-it-works">How It Works</a></li>
            <li><a href="#installation">Installation</a></li>
            <li><a href="#hosting">Hosting</a></li>
          </ul>
        </nav>
      </div>

      <!-- GitHub Repository Section -->
      <div class="github-link">
        <h2>GitHub Repository</h2>
        <p>Check out the full source code and contribute to the project.</p>
        <a href="https://github.com/RyuZinOh/github-streaks" target="_blank" class="github-btn">
          View on GitHub
        </a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Home',
})
</script>

<style scoped>
.home {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.content {
  display: flex;
  justify-content: space-between;
  width: max-content;
  gap: 40px;
}

.documentation {
  max-width: 800px;
  font-family: Arial, sans-serif;
}

h1,
h2 {
  color: #42b983;
  font-weight: bold;
}

section {
  margin-bottom: 30px;
}

ol {
  list-style-type: decimal;
  padding-left: 20px;
}

pre,
code {
  background-color: #f4f4f4;
  padding: 5px;
  border-radius: 4px;
  font-family: monospace;
}

nav {
  margin-top: 40px;
}

nav ul {
  padding: 0;
}

nav ul li {
  margin: 10px 0;
}

nav a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}

nav a:hover {
  text-decoration: underline;
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 5px;
}

/* Expanded GitHub Link Section */
.github-link {
  flex: 1; /* Make it take up space */
  min-width: 300px; /* Prevent it from being too small */
  padding: 20px;
  background-color: #f4f4f4;
  text-align: center;
}

.github-link h2 {
  color: #333;
  margin-bottom: 15px;
}

.github-btn {
  display: block;
  padding: 12px 20px;
  background-color: #24292f;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  text-decoration: none;
  margin-top: 10px;
  transition: background 0.3s;
}

.github-btn:hover {
  background-color: #1b1f23;
}
</style>
