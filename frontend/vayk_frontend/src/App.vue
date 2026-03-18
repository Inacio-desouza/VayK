<template>
  <RouterView />
</template>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100%;
}

body {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg, #0828a8 0%, #1c62ff 45%, #2aa6ff 100%);
}

input,
textarea,
button {
  font-family: 'Inter', sans-serif;
}

::placeholder {
  font-family: 'Inter', sans-serif;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}
</style>