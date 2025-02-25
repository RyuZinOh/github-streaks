<template>
  <div class="app-layout">
    <aside class="sidebar">
      <h1>My GitHub Stats</h1>
      <nav>
        <ul>
          <li><a href="#sample-image">Sample Image</a></li>
          <li><a href="#how-it-works">How It Works</a></li>
          <li><a href="#installation">Installation</a></li>
          <li><a href="#hosting">Hosting</a></li>
          <li><a href="#custom-themes">Custom Themes</a></li>
        </ul>
      </nav>
    </aside>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  font-family: Roboto;
  display: flex;
  height: 100vh;
  background-color: #ffffff;
}

.sidebar {
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.sidebar h1 {
  color: #2563eb;
  font-size: 1.8rem;
  margin-bottom: 30px;
}

.sidebar nav ul {
  list-style: none;
  padding: 0;
}

.sidebar nav ul li {
  margin: 15px 0;
}

.sidebar nav ul li a {
  color: #333;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
  transition: color 0.3s;
}

.sidebar nav ul li a:hover {
  color: #2563eb;
}

.content {
  margin-left: 250px;
  padding: 20px;
  background-color: #ffffff;
  width: calc(100% - 250px);
}

h1,
h2 {
  color: #2563eb;
  font-size: 2rem;
}

h3,
p,
ul,
ol {
  color: #333;
}

a {
  color: #2563eb;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
