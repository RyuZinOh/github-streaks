<template>
  <div class="app-layout">
    <header>
      <h1>My GitHub Stats</h1>
    </header>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.content {
  display: flex;
  width: 100%;
  max-width: 1200px;
  justify-content: space-between;
}
</style>
