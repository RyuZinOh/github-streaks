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

        <!-- Sample Image Section -->
        <section id="sample-image">
          <h2>Sample Image</h2>
          <p>This is the generated image that will be reflected in your GitHub readme.</p>
          <img src="@/assets/response.png" alt="Sample GitHub Streaks Dashboard" />
        </section>

        <!-- How It Works Section -->
        <section id="how-it-works">
          <h2>How It Works</h2>
          <p>
            The application tracks the contributions of a single GitHub user and generates a dynamic
            stats image. This image can be embedded in your GitHub readme markdown, reflecting your
            streaks and activity on the platform. It's designed for personal use and provides
            real-time data from GitHub.
          </p>
        </section>

        <!-- Installation Section -->
        <section id="installation">
          <h2>Installation</h2>
          <p>Follow these steps to install and configure the GitHub Readme Stats application:</p>
          <ol>
            <li>Clone the repository to your local machine using the following command:</li>
            <pre><code>git clone https://github.com/RyuZinOh/github-streaks</code></pre>
            <li>Install the necessary dependencies by running:</li>
            <pre><code>pip install -r requirements.txt</code></pre>
            <li>
              Create a `.env` file in the root directory and add your GitHub personal access token:
              <pre><code>GITHUB_TOKEN=your_personal_access_token</code></pre>
            </li>
            <li>
              If you don't have a GitHub token, generate one by visiting
              <a href="https://github.com/settings/tokens" target="_blank"
                >GitHub's Personal Access Tokens page</a
              >.
            </li>
            <li>Start the FastAPI server locally by running:</li>
            <pre><code>uvicorn main:app --reload</code></pre>
            <li>Access the running app in your browser by navigating to:</li>
            <pre><code>http://localhost:8000</code></pre>
          </ol>
        </section>

        <!-- Hosting Section -->
        <section id="hosting">
          <h2>How to Host</h2>
          <p>
            To make the app publicly accessible, you can use Cloudflare's tunneling service to
            expose your local server:
          </p>
          <ol>
            <li>
              Install Cloudflared following the official guide from
              <a
                href="https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/"
                target="_blank"
                >Cloudflare</a
              >.
            </li>
            <li>Start the tunnel by running this command in your terminal:</li>
            <pre><code>cloudflared tunnel --url http://localhost:8000</code></pre>
            <li>Once the tunnel starts, your app will be accessible on a Cloudflare subdomain.</li>
            <li>
              Example: If you are using a subdomain like
              <code>https://dealer.safallama.com.np/streak/ryuzinoh/image</code>, you can embed this
              link in your GitHub markdown like so:
              <pre><code>![readme](your_link_hosted_on_cloudflare)</code></pre>
            </li>
          </ol>
        </section>

        <!-- Navigation Links -->
        <nav>
          <ul>
            <li><a href="#sample-image">Go to Sample Image</a></li>
            <li><a href="#how-it-works">How Does It Work?</a></li>
            <li><a href="#installation">Go to Installation</a></li>
            <li><a href="#hosting">Go to Hosting</a></li>
          </ul>
        </nav>
      </div>

      <!-- GitHub URL Section (Right side of the page) -->
      <div class="github-link">
        <h2>GitHub Repository</h2>
        <p>Visit the GitHub repository for more details and source code:</p>
        <a href="https://github.com/RyuZinOh/github-streaks" target="_blank" class="github-btn"
          >GitHub Repository</a
        >
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
/* Styling for the documentation */
.home {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.content {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.documentation {
  max-width: 800px;
  margin-right: 30px;
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

ul {
  list-style-type: none;
  padding: 0;
}

code,
pre {
  background-color: #f4f4f4;
  padding: 3px 6px;
  border-radius: 4px;
}

pre {
  padding: 10px;
  overflow-x: auto;
}

nav {
  margin-top: 40px;
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
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* GitHub link styling */
.github-link {
  max-width: 250px;
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.github-link h2 {
  color: #333;
}

.github-btn {
  display: inline-block;
  padding: 10px 15px;
  background-color: #24292f;
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  border-radius: 5px;
  text-align: center;
  width: 100%;
}

.github-btn:hover {
  background-color: #1b1f23;
}
</style>
